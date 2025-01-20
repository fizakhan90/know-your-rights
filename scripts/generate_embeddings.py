import os
import sys
from mistralai import Mistral
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from database import Database

import json

class EmbeddingGenerator:
    def __init__(self):
        self.db = Database()
        self.mistral_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))

    def generate_and_store_embeddings(self):
        query = "SELECT ID, RIGHT_TEXT FROM WOMEN_RIGHTS WHERE RIGHT_EMBEDDING IS NULL"
        raw_results = self.db.execute_query(query)

        for row in raw_results:
            record_id = row[0]
            right_text = row[1]


            embedding_response = self.mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=[right_text]
            )
            embedding = embedding_response.data[0].embedding
            self.store_embedding(record_id, embedding)

    def store_embedding(self, record_id, embedding):
        embedding_str = json.dumps(embedding)

        update_query = """
        UPDATE WOMEN_RIGHTS 
        SET RIGHT_EMBEDDING = %s 
        WHERE ID = %s
        """
        params = (embedding_str, record_id)
        self.db.execute_query(update_query, params)





if __name__ == "__main__":
    generator = EmbeddingGenerator()
    generator.generate_and_store_embeddings()


