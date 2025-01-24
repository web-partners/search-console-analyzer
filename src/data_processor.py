import pandas as pd
import json
from typing import Dict, List, Optional
from loguru import logger

class DataProcessor:
    @staticmethod
    def process_data(raw_data: List[Dict], min_impressions: Optional[int] = None, max_position: Optional[float] = None) -> pd.DataFrame:
        try:
            # Sauvegarder raw_data dans un fichier JSON pour examen
            with open("logs/raw_data.json", "w", encoding="utf-8") as f:
                json.dump(raw_data, f, indent=4, ensure_ascii=False)
            logger.info("Raw data saved to raw_data.json for inspection.")
            
            df = pd.DataFrame(raw_data)
            
            # Check if 'keys' exists in the data
            if 'keys' not in df.columns:
                logger.error("Invalid data format: 'keys' field is missing")
                raise ValueError("Invalid data format: 'keys' field is missing")
            
            # Extract dimensions
            df['url'] = df['keys'].apply(lambda x: x[0])
            df['query'] = df['keys'].apply(lambda x: x[1])
            
            # Clean and format
            df = df.drop('keys', axis=1)
            df['position'] = df['position'].round(2)
            
            # Apply filters
            if min_impressions is not None:
                logger.info(f"Filtering results with minimum {min_impressions} impressions")
                df = df[df['impressions'] >= min_impressions]
                
            if max_position is not None:
                logger.info(f"Filtering results with maximum position {max_position}")
                df = df[df['position'] <= max_position]
            
            # Remove duplicates and sort
            df = df.drop_duplicates()
            df = df.sort_values('impressions', ascending=False)
            
            # Calculate metrics
            df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(2)
            
            logger.info(f"Processed {len(df)} rows after filtering")
            return df
            
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}")
            raise