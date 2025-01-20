import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SNOWFLAKE_CONFIG = {
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'database': 'KNOW_YOUR_RIGHTS',
        'schema': 'RIGHTS_DATA'
    }
    
    MISTRAL_CONFIG = {
        'api_key': os.getenv('MISTRAL_API_KEY'),
        'model': 'mistral-large-latest'
    }