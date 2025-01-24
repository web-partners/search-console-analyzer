from google.oauth2 import service_account
from googleapiclient.discovery import build
from loguru import logger
from typing import Optional
import json

class SearchConsoleAuth:
    SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
    
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.credentials: Optional[service_account.Credentials] = None
        self.service = None
        
    def authenticate(self) -> bool:
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, 
                scopes=self.SCOPES
            )
            self.service = build(
                'searchconsole', 
                'v1', 
                credentials=self.credentials
            )
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
            
    def verify_domain_access(self, domain: str) -> bool:
        try:
            sites = self.service.sites().list().execute()
            return any(site['siteUrl'].strip('/') == domain.strip('/') 
                      for site in sites.get('siteEntry', []))
        except Exception as e:
            logger.error(f"Domain verification failed: {str(e)}")
            return False

    def get_allowed_domains(self) -> list:
        """
        Retrieve the list of domains the authenticated user has access to.
        Returns:
            list: A list of domain URLs (e.g., ['https://example.com', 'https://another.com'])
        """
        try:
            if not self.service:
                raise Exception("Service is not initialized. Authenticate first.")
            
            sites = self.service.sites().list().execute()
            allowed_domains = [
                site['siteUrl'] for site in sites.get('siteEntry', [])
            ]
            return allowed_domains
        except Exception as e:
            logger.error(f"Failed to retrieve allowed domains: {str(e)}")
            return []

