---
title: Marketrix
app_file: public.py
sdk: gradio
sdk_version: 5.38.2
---
# Marketrix marketing Agent

A comprehensive marketing agent leveraging [QLoo](https://www.qloo.com/)

## local Installation

* Create virtual python environment by running `python -m venv marketrix_env`
* Activate virtual environment by running `marketrix_env\Scripts\activate`
* Install python packages by running `pip install -r requirements.txt` from the Marketrix folder.

## Using ADK Web Interface

* From the marketrix folder run `adk web` it bootstraps a web interface for interacting with the agent, accessible through `http://localhost:8000`, the select engine as the agent.

## Running Separate Frontend and Backend Servers

    * For backend run `python main.py` and for frontend run `python public.py`.
