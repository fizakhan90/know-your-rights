from database import Database

class RightsSearch:
    def __init__(self):
        self.db = Database()
    
    def search_rights(self, region=None, category=None):
        query = """
        SELECT REGION, CATEGORY, RIGHT_TEXT, SOURCES 
        FROM WOMEN_RIGHTS 
        WHERE 1=1
        """
        params = []
        
        if region:
            query += " AND REGION = %s"
            params.append(region)
        if category:
            query += " AND CATEGORY = %s"
            params.append(category)
            
        results = self.db.execute_query(query, tuple(params) if params else None)
        return self._format_results(results)
    
    def _format_results(self, results):
        formatted = []
        for result in results:
            formatted.append({
                'region': result[0],
                'category': result[1],
                'right_text': result[2],
                'sources': result[3]
            })
        return formatted