import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCleaner:
    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"Starting data cleaning. Initial rows: {len(df)}")
        
        initial_rows = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
        
        df = df.dropna(subset=['label'])
        logger.info(f"Rows after dropping null labels: {len(df)}")
        
        df = df[df['label'].isin([0, 1])]
        logger.info(f"Rows after filtering valid labels: {len(df)}")
        
        for col in df.select_dtypes(include=['object']).columns:
            if col not in ['FILENAME', 'URL', 'Domain', 'TLD', 'Title']:
                df[col] = df[col].fillna(0)
        
        for col in df.select_dtypes(include=['number']).columns:
            df[col] = df[col].fillna(df[col].median())
        
        logger.info(f"Data cleaning complete. Final rows: {len(df)}")
        return df
