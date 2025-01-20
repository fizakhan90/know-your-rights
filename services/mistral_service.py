from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import List, Dict
from app.config import MISTRAL_API_KEY

class MistralService:
    def __init__(self):
        self.client = MistralClient(api_key=MISTRAL_API_KEY)
    
    def get_therapeutic_context(self, mood: str, activity: str, songs: List[Dict]) -> str:
        """Generate therapeutic context for the playlist"""
        songs_list = "\n".join([
            f"- {song['title']} by {song['artist']}"
            for song in songs
        ])
        
        prompt = f"""As a music therapy expert, explain how this playlist can help someone who is feeling {mood} while {activity}.

Playlist:
{songs_list}

Please explain:
1. The therapeutic benefits of these songs
2. How the musical elements support emotional regulation
3. Tips for mindful listening
4. Expected emotional benefits

Keep the explanation concise, supportive, and accessible."""
        
        messages = [
            ChatMessage(role="user", content=prompt)
        ]
        
        try:
            response = self.client.chat(
                model="mistral-tiny",
                messages=messages
            )
            return response.messages[0].content
        except Exception as e:
            print(f"Error getting Mistral response: {e}")
            return "Unable to generate therapeutic context at the moment."
    
    def get_mindfulness_prompt(self, song: Dict, mood: str) -> str:
        """Generate a mindfulness prompt for a specific song"""
        prompt = f"""Create a brief mindfulness prompt for listening to "{song['title']}" by {song['artist']} 
        when feeling {mood}. Focus on emotional awareness and therapeutic benefit."""
        
        messages = [
            ChatMessage(role="user", content=prompt)
        ]
        
        try:
            response = self.client.chat(
                model="mistral-tiny",
                messages=messages
            )
            return response.messages[0].content
        except Exception as e:
            print(f"Error getting mindfulness prompt: {e}")
            return "Focus on your breathing as you listen to this song."