import pandas as pd
from typing import Dict
from loguru import logger

class ExcelGenerator:
    def __init__(self, df: pd.DataFrame, filename: str):
        self.df = df
        self.filename = filename
        
    def generate(self):
        try:
            with pd.ExcelWriter(self.filename, engine='openpyxl') as writer:
                # Main data sheet
                self.df.to_excel(writer, sheet_name='Data', index=False)
                self._format_data_sheet(writer)
                
                # Summary dashboard
                self._create_summary(writer)
                
            logger.info(f"Excel file generated: {self.filename}")
            
        except Exception as e:
            logger.error(f"Excel generation failed: {str(e)}")
            raise
            
    def _format_data_sheet(self, writer):
        worksheet = writer.sheets['Data']
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            worksheet.column_dimensions[column[0].column_letter].width = max_length + 2
            
    def _create_summary(self, writer):
        total_impressions = self.df['impressions'].sum()
        total_clicks = self.df['clicks'].sum()
        
        summary = {
            'Total Clicks': total_clicks,
            'Total Impressions': total_impressions,
            'Average Position': self.df['position'].mean(),
            'Average CTR': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        }
        
        pd.DataFrame([summary]).to_excel(writer, sheet_name='Summary', index=False)