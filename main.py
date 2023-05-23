# VoiceForm will ask questions to users in a human voice and record their answers.

# Pseudo Code
# Create database
# Create schema
# Fetch schema from database
# Generate prompt based on schema and a prompt variable
# Send prompt to OpenAI API
# Show OpenAI generated questions to user
# Collect user responses and save to database
# Update conversation thread (or dialog) with user responses
# Repeat until all questions are answered
# Extract all responses in a structured format and save to database


# Imports
import os
import openai
import json
import sqlite3
import datetime
import time
import random
import string
import re
import sys
import argparse
import logging
import requests


# Constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"
OPENAI_API_MAX_TOKENS = 150
OPENAI_API_TEMPERATURE = 0.9
OPENAI_API_TOP_P = 1
OPENAI_API_FREQUENCY_PENALTY = 0.5
OPENAI_API_PRESENCE_PENALTY = 0.5

# Database
DATABASE_NAME = "voiceform.db"
DATABASE_SCHEMA = "schema.json"