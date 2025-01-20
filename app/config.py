import os
from dotenv import load_dotenv


load_dotenv()


MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = "music_therapy"
SNOWFLAKE_SCHEMA = "app"


MOOD_OPTIONS = [
    "Anxious",
    "Stressed",
    "Sad",
    "Calm",
    "Happy",
    "Energetic"
]

ACTIVITY_OPTIONS = [
    "Working",
    "Relaxing",
    "Exercising",
    "Meditating",
    "Studying"
]

THERAPEUTIC_GOALS = [
    "Stress Reduction",
    "Mood Improvement",
    "Focus Enhancement",
    "Anxiety Relief",
    "Energy Boost"
]