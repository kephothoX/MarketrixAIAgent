---
title: Marketrix
app_file: public.py
sdk: gradio
sdk_version: 5.38.2
adk_version: 1.7.0
server: main.py
agent: engine/agent.py
---
# Marketrix Market Insights Agent

A comprehensive marketing agent leveraging [QLoo](https://www.qloo.com/)

## Local Installation

* Create virtual python environment by running `python -m venv marketrix_env`
* Activate virtual environment by running `marketrix_env\Scripts\activate`
* Install python packages by running `pip install -r requirements.txt` from the Marketrix folder.

## Using ADK Web Interface

* From the marketrix folder run `adk web` it bootstraps a web interface for interacting with the agent, accessible through `http://localhost:8000`, the select engine as the agent.

## Running Separate Frontend and Backend Servers

* For backend run `python main.py` and for frontend run `python public.py`.
* This will bootstrap a gradio app with a backed, go to `http://localhost:8080/`  for agent interface. backend  is running on `http://localhost:8000`
