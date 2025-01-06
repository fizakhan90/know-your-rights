import os
from mistralai import Mistral
import dotenv


dotenv.load_dotenv()

class RightsLLM:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)
    
    def generate_response(self, context, query):
        prompt = f"""
        Based on the following women's rights information:
        {context}
        
        Answer the following question:
        {query}
        
        Provide a clear and concise response using only the information given.
        Include relevant citations when possible.
        """
        
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return f"Error: Unable to generate response due to: {str(e)}"
    
    def __str__(self):
        return f"RightsLLM(model={self.model})"


