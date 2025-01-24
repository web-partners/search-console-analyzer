from typing import Dict, List
import time
from datetime import datetime
from loguru import logger
from googleapiclient.errors import HttpError

class SearchConsoleCollector:
    def __init__(self, service, domain: str):
        self.service = service
        self.domain = domain
        
    def fetch_data(self, start_date: str, end_date: str, 
                   batch_size: int = 1000, max_retries: int = 3) -> List[Dict]:
        all_data = []
        start_row = 0
        
        while True:
            try:
                request = {
                    'startDate': start_date,
                    'endDate': end_date,
                    'dimensions': ['page', 'query'],
                    'rowLimit': batch_size,
                    'startRow': start_row,
                    'dataState': 'all'
                }
                
                response = self._execute_request(request, max_retries)
                if not response.get('rows'):
                    break
                    
                all_data.extend(response['rows'])
                start_row += batch_size
                
                if len(response['rows']) < batch_size:
                    break
                    
            except Exception as e:
                logger.error(f"Data fetch failed: {str(e)}")
                break
                
        return all_data
        
    def _execute_request(self, request: Dict, max_retries: int) -> Dict:
        for attempt in range(max_retries):
            try:
                return self.service.searchanalytics().query(
                    siteUrl=self.domain,
                    body=request
                ).execute()
            except HttpError as e:
                if e.resp.status == 429:  # Rate limit
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                raise
