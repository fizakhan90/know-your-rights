from snowflake.connector import connect, errors
from typing import List, Tuple, Optional, Union, Dict
import streamlit as st
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        """Establish connection to Snowflake"""
        try:
            conn = connect(**Config.SNOWFLAKE_CONFIG)
            cur = conn.cursor()
            cur.execute("USE DATABASE KNOW_YOUR_RIGHTS")
            cur.execute("USE SCHEMA RIGHTS_DATA")
            cur.close()
            logger.info("Successfully connected to Snowflake")
            return conn
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            raise

    def reconnect(self):
        """Reconnect if connection is lost"""
        logger.info("Attempting to reconnect to Snowflake")
        self.close()
        self.conn = self.connect()

    def close(self):
        """Close the database connection"""
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                logger.info("Database connection closed")
            except Exception as e:
                logger.error(f"Error closing connection: {str(e)}")

    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[List, Tuple, Dict]] = None
    ) -> List[Tuple]:
        """
        Execute a query with parameters and return results
        
        Args:
            query: SQL query string
            params: Query parameters as list, tuple, or dict
        
        Returns:
            List of result tuples
        """
        if params is None:
            params = []
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            cur = None
            try:
                if not self.conn:
                    self.reconnect()
                
                cur = self.conn.cursor()
                
                
                logger.debug(f"Executing query: {query}")
                logger.debug(f"Query parameters: {params}")
                
                
                if isinstance(params, dict):
                    cur.execute(query, params)
                else:
                    cur.execute(query, params if params else None)
                
                results = cur.fetchall()
                return results
                
            except errors.ProgrammingError as e:
                logger.error(f"Programming error in query: {str(e)}")
                raise
                
            except (errors.OperationalError, errors.DatabaseError) as e:
                retry_count += 1
                logger.warning(f"Database error (attempt {retry_count}/{max_retries}): {str(e)}")
                self.reconnect()
                if retry_count == max_retries:
                    logger.error("Max retries reached, raising error")
                    raise
                
            except Exception as e:
                logger.error(f"Unexpected error executing query: {str(e)}")
                raise
                
            finally:
                if cur is not None:
                    try:
                        cur.close()
                    except:
                        pass

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()