from mistralai import Mistral
from typing import List, Dict
from config import Config
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RightsLLM:
    MAX_HISTORY_LENGTH = 10
    
    def __init__(self):
        self.api_key = Config.MISTRAL_CONFIG['api_key']
        self.model = Config.MISTRAL_CONFIG['model']
        self.client = Mistral(api_key=self.api_key)
        self.conversation_history = []

    def generate_response(self, context: str, query: str, is_follow_up: bool = False, retries: int = 3) -> str:
        messages = [
            {"role": "system", "content": f"You are a women's rights assistant. Use this context to answer questions: {context}"}
        ]
        
        if is_follow_up:
            messages.extend(self.conversation_history)
        
        messages.append({"role": "user", "content": query})
        
        for attempt in range(retries):
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=messages,
                    timeout=10
                )
                self.conversation_history.append({"role": "user", "content": query})
                self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"Retry {attempt + 1}/{retries} failed: {str(e)}")
                time.sleep(2 ** attempt)
        
        return "Error: Unable to process your request. Please try again later."

    def clear_conversation(self):
        self.conversation_history = []
        logger.info("Conversation history cleared")




