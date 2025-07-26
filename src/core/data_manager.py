"""
Data management for CSV import/export and validation.
"""

import pandas as pd
import os
from datetime import datetime
from typing import Optional, Tuple, List


class DataManager:
    """Handles data import, export, and validation."""
    
    def __init__(self):
        self.required_columns = ['quarter', 'sales_units', 'unit_price']
    
    def load_csv(self, filename: str) -> Tuple[bool, Optional[pd.DataFrame], str]:
        """
        Load and validate CSV data.
        
        Returns:
            Tuple of (success, dataframe, error_message)
        """
        try:
            df = pd.read_csv(filename)
            
            # Check required columns
            if not all(col in df.columns for col in self.required_columns):
                return False, None, f"CSV must contain columns: {', '.join(self.required_columns)}"
            
            # Validate data types and values
            for _, row in df.iterrows():
                if not (isinstance(row['sales_units'], (int, float)) and 
                       isinstance(row['unit_price'], (int, float)) and
                       row['sales_units'] > 0 and row['unit_price'] > 0):
                    return False, None, "Sales units and unit price must be positive numbers"
            
            return True, df, ""
            
        except Exception as e:
            return False, None, f"Error loading CSV: {str(e)}"
    
    def export_to_excel(self, dataframes: dict, output_dir: str = "outputs") -> Tuple[bool, str]:
        """
        Export multiple dataframes to Excel files.
        
        Args:
            dataframes: Dict of {sheet_name: dataframe}
            output_dir: Directory to save files
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/budget_reports_{timestamp}.xlsx"
            
            with pd.ExcelWriter(filename) as writer:
                for sheet_name, df in dataframes.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return True, f"Reports saved to {filename}"
            
        except Exception as e:
            return False, f"Error saving reports: {str(e)}"
    
    def validate_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate dataframe structure and content."""
        if df is None or df.empty:
            return False, "No data available"
        
        # Check for required columns
        missing_cols = [col for col in self.required_columns if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns: {', '.join(missing_cols)}"
        
        # Check for valid data types
        for col in ['sales_units', 'unit_price']:
            if not pd.api.types.is_numeric_dtype(df[col]):
                return False, f"Column '{col}' must contain numeric values"
        
        # Check for positive values
        if (df['sales_units'] <= 0).any() or (df['unit_price'] <= 0).any():
            return False, "Sales units and unit price must be positive numbers"
        
        return True, "Data validation passed"
    
    def get_sample_data(self) -> pd.DataFrame:
        """Return sample data for testing."""
        return pd.DataFrame({
            'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
            'sales_units': [10000, 12000, 15000, 13000],
            'unit_price': [20, 20, 20, 20]
        }) 