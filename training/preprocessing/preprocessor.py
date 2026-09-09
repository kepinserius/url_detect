import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self, drop_cols=None):
        self.drop_cols = drop_cols or ['FILENAME', 'URL', 'Domain', 'TLD', 'Title']
    
    def prepare(self, df: pd.DataFrame):
        logger.info("Preparing features and labels")
        
        cols_to_drop = [col for col in self.drop_cols if col in df.columns]
        if 'label' not in df.columns:
            raise ValueError("Dataset must contain 'label' column")
        
        X = df.drop(columns=cols_to_drop + ['label'])
        y = df['label']
        
        logger.info(f"Features shape: {X.shape}, Labels shape: {y.shape}")
        logger.info(f"Feature columns: {X.columns.tolist()}")
        
        return X, y
