import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate(df: pd.DataFrame, required_cols: list = None) -> dict:
        report = {
            "total_rows": int(len(df)),
            "duplicates": int(df.duplicated().sum()),
            "missing_values": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
            "label_distribution": {str(k): int(v) for k, v in df['label'].value_counts().to_dict().items()} if 'label' in df.columns else None,
            "issues": []
        }
        
        if df.duplicated().sum() > 0:
            report["issues"].append(f"Found {df.duplicated().sum()} duplicate rows")
            logger.warning(f"Found {df.duplicated().sum()} duplicate rows")
        
        if df.isnull().any().any():
            null_cols = df.columns[df.isnull().any()].tolist()
            report["issues"].append(f"Missing values in columns: {null_cols}")
            logger.warning(f"Missing values in columns: {null_cols}")
        
        if required_cols:
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                report["issues"].append(f"Missing required columns: {missing_cols}")
                logger.error(f"Missing required columns: {missing_cols}")
        
        if 'label' in df.columns:
            invalid_labels = df[~df['label'].isin([0, 1])]
            if len(invalid_labels) > 0:
                report["issues"].append(f"Found {len(invalid_labels)} rows with invalid labels")
                logger.error(f"Found {len(invalid_labels)} rows with invalid labels")
        
        report["is_valid"] = len(report["issues"]) == 0
        return report
