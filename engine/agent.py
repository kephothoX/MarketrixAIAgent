import warnings, logging


from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import LongRunningFunctionTool


# from subagents.marketrix_insights_agent import marketrix_insights_agent
from engine.agent_tools.marketrix_entities_agent_tools.tools import (
    entitiesFilterTypes,
    getEntitiesByName,
    getEntitiesByID,
    getEntitiesID,
)

from engine.agent_tools.marketrix_trending_data_agent_tools.tools import getTrendingData
from engine.agent_tools.marketrix_analysis_agent_tools.tools import marketAnalysis

from engine.agent_tools.marketrix_geo_location_agent_tools.tools import (
    brandInsights,
    destinationInsights,
    placeInsights,
    movieInsights,
    bookInsights,
    personInsights,
)
from engine.agent_tools.marketrix_heatmaps_agent_tools.tools import (
    getEntitiesID,
    getAgeDemographicsHeatmaps,
    getEntitiesInterestsHeatmaps,
    getGenderDemographicsHeatmaps,
    getInterestsTagsHeatmaps,
    getBiasTrendsHeatmaps,
    getBrandsHeatmapsData,
    drawHeatMapImage,
)

MODEL = "gemini-2.0-flash"

# Ignore all warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)


root_agent = LlmAgent(
    name="Marketrix_Agent",
    model=MODEL,
    description="""You are marketrix  agent use agent within your reach as tools to provide a comprehensive, detailed, easily understandable and accurate marketing, product development and research strategies to help the user reach target audience quickly and effectively.""",
    instruction="""
    Delegate and use tools within your reach to answer user query, and avoid reaching conclusion until you have exhausted all previously provided information and used other agents to complete users request.

    Avoid responding to user if you are still finding suitable tool to execute user task, if you must respond, inform the user you are looking for a tool that can help you to complete users request.

    If you dont fully understand users request, ask a user for more information after exhausting all previously provided information.   
    
    For tags, parameters, signals, filters and entities, use the qloo_documentation_agent to come up with relevant tags, parameters, signals, filters and entities based on user query, then use them with other tools to complete users request.
    """,
    tools=[
        LongRunningFunctionTool(func=getEntitiesByName),
        LongRunningFunctionTool(func=getEntitiesByID),
        LongRunningFunctionTool(func=getTrendingData),
        LongRunningFunctionTool(func=entitiesFilterTypes),
        LongRunningFunctionTool(func=brandInsights),
        LongRunningFunctionTool(func=marketAnalysis),
        LongRunningFunctionTool(func=destinationInsights),
        LongRunningFunctionTool(func=placeInsights),
        LongRunningFunctionTool(func=movieInsights),
        LongRunningFunctionTool(func=bookInsights),
        LongRunningFunctionTool(func=personInsights),
        LongRunningFunctionTool(func=getEntitiesID),
        LongRunningFunctionTool(func=getAgeDemographicsHeatmaps),
        LongRunningFunctionTool(func=getEntitiesInterestsHeatmaps),
        LongRunningFunctionTool(func=getGenderDemographicsHeatmaps),
        LongRunningFunctionTool(func=getInterestsTagsHeatmaps),
        LongRunningFunctionTool(func=getBiasTrendsHeatmaps),
        LongRunningFunctionTool(func=getBrandsHeatmapsData),
        LongRunningFunctionTool(func=drawHeatMapImage),
    ],
)
