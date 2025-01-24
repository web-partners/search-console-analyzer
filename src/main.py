from datetime import datetime
from typing import Optional, List
import argparse
from loguru import logger
import os
from auth import SearchConsoleAuth
from data_collector import SearchConsoleCollector
from data_processor import DataProcessor
from excel_generator import ExcelGenerator
import re

def process_single_domain(domain: str, start_date: str, end_date: str, 
                         auth: SearchConsoleAuth, output_file: Optional[str] = None,
                         min_impressions: Optional[int] = None, 
                         max_position: Optional[float] = None) -> bool:
    try:
        # Collect data
        collector = SearchConsoleCollector(auth.service, domain)
        raw_data = collector.fetch_data(start_date, end_date)
        
        # Process data with filters
        df = DataProcessor.process_data(raw_data, min_impressions, max_position)
        
        # Generate Excel file
        if output_file is None:
            cleaned_domain = re.sub(r'^https?://', '', domain).rstrip('/').replace('/', '-').replace(':', '-')
            output_file = f"output/search_console_data_{cleaned_domain}_{start_date}_{end_date}.xlsx"
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        excel_gen = ExcelGenerator(df, output_file)
        excel_gen.generate()
        
        logger.info(f"Successfully processed domain: {domain}")
        logger.info(f"Output file: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to process domain {domain}: {str(e)}")
        return False

def main(domain: str, start_date: str, end_date: str, 
         credentials_path: str, output_file: Optional[str] = None,
         min_impressions: Optional[int] = None, max_position: Optional[float] = None):
    
    # Setup logging
    log_file = "logs/search_console_{time}.log"
    logger.add(log_file)
    
    try:
        # Initialize authentication
        auth = SearchConsoleAuth(credentials_path)
        if not auth.authenticate():
            raise Exception("Authentication failed")
        
        if domain.lower() == "all":
            # Get all authorized domains
            domains = auth.get_allowed_domains()
            if not domains:
                raise Exception("No authorized domains found")
            
            logger.info(f"Found {len(domains)} authorized domains")
            
            # Process each domain
            successful = 0
            failed = 0
            
            for current_domain in domains:
                logger.info(f"Processing domain: {current_domain}")
                
                # For multiple domains, we'll create individual files
                domain_output = None
                if output_file:
                    # If output file is specified, add domain name to it
                    base, ext = os.path.splitext(output_file)
                    domain_output = f"{base}_{current_domain.replace('://', '_').replace('/', '_')}{ext}"
                
                if process_single_domain(current_domain, start_date, end_date, 
                                      auth, domain_output, min_impressions, max_position):
                    successful += 1
                else:
                    failed += 1
            
            # Final summary
            logger.info(f"Export completed: {successful} successful, {failed} failed")
            if failed > 0:
                logger.warning("Some domains failed to process. Check the logs for details.")
            
        else:
            # Single domain processing
            if not auth.verify_domain_access(domain):
                allowed_domains = auth.get_allowed_domains()
                raise Exception(f"No access to domain: {domain}. Allowed domains: {', '.join(allowed_domains)}")
            
            if not process_single_domain(domain, start_date, end_date, 
                                      auth, output_file, min_impressions, max_position):
                raise Exception(f"Failed to process domain: {domain}")
        
        return log_file
        
    except Exception as e:
        logger.error(f"Process failed: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Domain to analyze (e.g., https://example.com) or 'all' for all authorized domains")
    parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("credentials_path", help="Path to service account credentials")
    parser.add_argument("--output", help="Output filename (optional)")
    parser.add_argument("--min-impressions", type=int, help="Minimum number of impressions to include")
    parser.add_argument("--max-position", type=float, help="Maximum position to include (e.g., 10.0 for first page)")
    
    args = parser.parse_args()
    main(args.domain, args.start_date, args.end_date, 
         args.credentials_path, args.output,
         args.min_impressions, args.max_position)