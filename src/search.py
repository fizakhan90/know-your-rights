from typing import List, Dict, Optional
from database import Database
from llm import RightsLLM
import streamlit as st
import logging
from mistralai import Mistral
import os


logger = logging.getLogger(__name__)

class RightsSearch:
   def __init__(self):
       self.db = Database()
       self.llm = RightsLLM()
       self.mistral_client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))

   def generate_embedding(self, text: str) -> List[float]:
       """Generate embeddings using Mistral's embedding model"""
       try:
           
           response = self.mistral_client.embeddings.create(
               model="mistral-embed",
               inputs=[text]
           )
           return response.data[0].embedding
       except Exception as e:
           logger.error(f"Error generating embedding: {str(e)}")
           raise

   def semantic_search(self, query_text: str, limit: int = 5) -> List[Dict]:
       vector_query = f"""
       SELECT 
           r.REGION,
           r.CATEGORY,
           r.RIGHT_TEXT,
           r.SOURCES,
           VECTOR_COSINE_SIMILARITY(r.RIGHT_EMBEDDING, ARRAY_CONSTRUCT(%s)) as similarity
       FROM WOMEN_RIGHTS r
       WHERE RIGHT_TEXT IS NOT NULL
       AND RIGHT_EMBEDDING IS NOT NULL
       AND VECTOR_COSINE_SIMILARITY(r.RIGHT_EMBEDDING, ARRAY_CONSTRUCT(%s)) > 0.5
       ORDER BY similarity DESC
       LIMIT {limit}
       """
       
       try:
           
           query_embedding = self.generate_embedding(query_text)
           embedding_str = ','.join(map(str, query_embedding))
           
           results = self.db.execute_query(
               vector_query,
               [embedding_str, embedding_str]
           )
           
           return [{
               "region": r[0],
               "category": r[1],
               "right_text": r[2],
               "sources": r[3],
               "similarity": float(r[4])
           } for r in results]
       except Exception as e:
           logger.error(f"Search error: {str(e)}")
           return []

   @st.cache_data(ttl=3600)
   def enhanced_search(
       _self,
       region: Optional[str] = None,
       category: Optional[str] = None,
       search_text: Optional[str] = None,
       is_follow_up: bool = False
   ) -> Dict:
       try:
           if search_text:
               results = _self.semantic_search(search_text)
               if region or category:
                   results = [
                       r for r in results
                       if (not region or r['region'] == region) and
                          (not category or r['category'] == category)
                   ]
               
               if results:
                   context = "\n".join(f"{r['right_text']}" for r in results[:3])
                   rag_response = _self.llm.generate_response(
                       context, search_text, is_follow_up
                   )
                   return {'results': results, 'rag_response': rag_response}
               return {'results': [], 'rag_response': None}

           base_query = """
           SELECT DISTINCT
               r.REGION,
               r.CATEGORY,
               r.RIGHT_TEXT,
               r.SOURCES
           FROM WOMEN_RIGHTS r
           WHERE 1=1
           """
           params = []

           if region:
               base_query += " AND REGION = %s"
               params.append(region)
           if category:
               base_query += " AND CATEGORY = %s"
               params.append(category)

           results = _self.db.execute_query(base_query, params)
           return {
               'results': [{
                   "region": r[0],
                   "category": r[1],
                   "right_text": r[2],
                   "sources": r[3]
               } for r in results],
               'rag_response': None
           }
       except Exception as e:
           logger.error(f"Search error: {str(e)}")
           return {'results': [], 'rag_response': str(e)}