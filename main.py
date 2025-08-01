from engine.agent import root_agent
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from google.adk.runners import Runner
from google.adk.events import Event
from google import genai
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse

import uvicorn, uuid, datetime, asyncio, json
from google.genai import types
from contextlib import asynccontextmanager
import asyncio
from utils import (
    extract_attachment_ids_and_sanitize_response,
    download_image_from_gcs,
    extract_thinking_process,
    format_user_request_to_adk_content_and_store_artifacts,
)
from schema import ImageData, AgentRequest, AgentResponse
import logger
from google.adk.artifacts import InMemoryArtifactService, GcsArtifactService
from settings import get_settings
import vertexai
from vertexai import agent_engines

# Create an agent engine instance
# agent_engine = agent_engines.create()

# print(f"Agent Engine:  {agent_engine.name.split("/")[-1]}")


SETTINGS = get_settings()
APP_NAME = (
    "projects/917357044046/locations/us-central1/reasoningEngines/7529270909056581632"
)
# "1822084281271320576"  # f"{ agent_engine.name.split("/")[-1] }"

artifact_service = artifact_service = InMemoryArtifactService()
# GcsArtifactService(bucket_name=SETTINGS.storage_bucket_name)


client = genai.Client(vertexai=True)._api_client
string_response = client.request(
    http_method="POST",
    path=f"reasoningEngines",
    request_dict={
        "displayName": "Express-Mode-Agent-Engine",
        "description": "Test Agent Engine demo",
    },
).body
response = json.loads(string_response)
print(response)

APP_NAME = "/".join(response["name"].split("/")[:6])
print(f"APP_NAME:  {APP_NAME}")

APP_ID = "7529270909056581632"  # APP_NAME.split("/")[-1]
print(f"APP_ID:  {APP_ID}")


session_service = VertexAiSessionService(agent_engine_id=APP_ID)
memory_service = VertexAiMemoryBankService(agent_engine_id=APP_ID)


USER_ID = str(uuid.uuid4())
SESSION = None


async def initialize_session():
    SESSION = await session_service.create_session(app_name=APP_ID, user_id=USER_ID)
    SESSION_ID = SESSION.id
    print(f"Session:  {SESSION}")
    await memory_service.add_session_to_memory(session=SESSION)
    return SESSION, SESSION_ID


SESSION, SESSION_ID = asyncio.run(initialize_session())


# Create FastAPI app
app = FastAPI(title="Marketrix API")

runner = Runner(
    agent=root_agent,  # The agent we want to run
    app_name=APP_ID,  # Associates runs with our app
    session_service=session_service,  # Uses vertex session service
    memory_service=memory_service,
    artifact_service=artifact_service,  # Uses vertex memory service
)

print(f"Runner created for agent '{runner.agent.name}'.")


@app.post("/agent", response_model=AgentResponse)
async def agent(request: AgentRequest = Body()) -> AgentResponse:
    base64_attachments = []

    def get_long_running_function_call(event: Event) -> types.FunctionCall:
        # Get the long running function call from the event
        if (
            not event.long_running_tool_ids
            or not event.content
            or not event.content.parts
        ):
            return
        for part in event.content.parts:
            if (
                part
                and part.function_call
                and event.long_running_tool_ids
                and part.function_call.id in event.long_running_tool_ids
            ):
                return part.function_call

    def get_function_response(
        event: Event, function_call_id: str
    ) -> types.FunctionResponse:
        # Get the function response for the fuction call with specified id.
        if not event.content or not event.content.parts:
            return
        for part in event.content.parts:
            if (
                part
                and part.function_response
                and part.function_response.id == function_call_id
            ):
                return part.function_response

    content = await asyncio.to_thread(
        format_user_request_to_adk_content_and_store_artifacts,
        request=request,
        app_name=APP_NAME,
        artifact_service=artifact_service,
    )

    print("\nRunning agent...")
    events_async = runner.run_async(
        session_id=SESSION_ID, user_id=USER_ID, new_message=content
    )

    long_running_function_call, long_running_function_response, ticket_id = (
        None,
        None,
        None,
    )

    final_response_text = "Agent did not produce a final response."  # Default
    base64_attachments = []
    sanitized_text = final_response_text
    thinking_process = ""
    attachment_ids = []
    async for event in events_async:
        # Use helper to check for the specific auth request event
        if not long_running_function_call:
            long_running_function_call = get_long_running_function_call(event)
        else:
            long_running_function_response = get_function_response(
                event, long_running_function_call.id
            )
            # if long_running_function_response:
            # ticket_id = long_running_function_response.response["ticket-id"]
        if event.content and event.content.parts:
            if text := "".join(part.text or "" for part in event.content.parts):
                final_response_text = f"[{event.author}]: {text}"

        if long_running_function_response:
            # query the status of the correpsonding ticket via tciket_id
            # send back an intermediate / final response
            updated_response = long_running_function_response.model_copy(deep=True)
            updated_response.response = {"status": "approved"}
            async for event in runner.run_async(
                session_id=SESSION_ID,
                user_id=USER_ID,
                new_message=types.Content(
                    parts=[types.Part(function_response=updated_response)], role="user"
                ),
            ):
                if event.content and event.content.parts:
                    if text := "".join(part.text or "" for part in event.content.parts):
                        final_response_text = f"[{event.author}]: {text}"

    sanitized_text, attachment_ids = extract_attachment_ids_and_sanitize_response(
        final_response_text
    )
    sanitized_text, thinking_process = extract_thinking_process(sanitized_text)

    # Download images from GCS and replace hash IDs with base64 data
    for image_hash_id in attachment_ids:
        # Download image data and get MIME type
        result = await asyncio.to_thread(
            download_image_from_gcs,
            artifact_service=artifact_service,
            image_hash=image_hash_id,
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,  # get_or_create_session(APP_NAME, USER_ID),
        )
        if result:
            base64_data, mime_type = result
            base64_attachments.append(
                ImageData(serialized_image=base64_data, mime_type=mime_type)
            )

    logger.info(
        "Processed response with attachments",
        sanitized_response=sanitized_text,
        thinking_process=thinking_process,
        attachment_ids=attachment_ids,
    )

    logger.info(
        "Received final response from agent",
        raw_final_response=final_response_text,
    )

    return AgentResponse(
        response=sanitized_text,
        thinking_process=thinking_process,
        attachments=base64_attachments,
    )


# Only run the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
