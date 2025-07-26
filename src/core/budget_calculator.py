"""
Budget calculation engine for financial analysis.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any


class BudgetCalculator:
    """Handles all budget-related calculations."""
    
    def __init__(self, settings: Dict[str, float]):
        self.settings = settings
    
    def compute_sales_revenue(self, data: pd.DataFrame) -> pd.DataFrame:
        """Compute sales revenue for each quarter."""
        if data is None or data.empty:
            return pd.DataFrame()
        
        sales_data = data.copy()
        sales_data['sales_revenue'] = sales_data['sales_units'] * sales_data['unit_price']
        return sales_data
    
    def compute_collections(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """Compute cash collections schedule."""
        if sales_data is None or sales_data.empty:
            return pd.DataFrame()
        
        collections = sales_data.copy()
        collections['collections'] = 0.0
        
        for i, row in collections.iterrows():
            current_revenue = row['sales_revenue']
            
            # Current quarter collections
            collections.loc[i, 'collections'] += (current_revenue * 
                                               self.settings['sales_collection_current'])
            
            # Previous quarter collections (if not first quarter)
            if i > 0:
                prev_revenue = collections.loc[i-1, 'sales_revenue']
                collections.loc[i, 'collections'] += (prev_revenue * 
                                                   self.settings['sales_collection_next'])
        
        return collections
    
    def compute_purchases(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """Compute purchases and inventory."""
        if sales_data is None or sales_data.empty:
            return pd.DataFrame()
        
        purchases = sales_data.copy()
        purchases['desired_ending_inventory'] = 0.0
        purchases['beginning_inventory'] = 0.0
        purchases['purchases_units'] = 0.0
        purchases['purchases_cost'] = 0.0
        
        # Assume cost per unit is 60% of selling price
        cost_per_unit = purchases['unit_price'] * 0.6
        
        for i, row in purchases.iterrows():
            # Desired ending inventory (20% of next quarter's sales)
            if i < len(purchases) - 1:
                next_q_sales = purchases.loc[i+1, 'sales_units']
                purchases.loc[i, 'desired_ending_inventory'] = (next_q_sales * 
                                                             self.settings['ending_inventory_pct'])
            
            # Beginning inventory (ending inventory from previous quarter)
            if i > 0:
                purchases.loc[i, 'beginning_inventory'] = purchases.loc[i-1, 'desired_ending_inventory']
            
            # Purchases = Sales + Desired Ending Inventory - Beginning Inventory
            purchases.loc[i, 'purchases_units'] = (row['sales_units'] + 
                                                 purchases.loc[i, 'desired_ending_inventory'] - 
                                                 purchases.loc[i, 'beginning_inventory'])
            
            # Purchases cost
            purchases.loc[i, 'purchases_cost'] = (purchases.loc[i, 'purchases_units'] * 
                                                cost_per_unit.iloc[i])
        
        return purchases
    
    def compute_cash_budget(self, collections: pd.DataFrame, purchases: pd.DataFrame) -> pd.DataFrame:
        """Compute cash budget."""
        if collections is None or collections.empty or purchases is None or purchases.empty:
            return pd.DataFrame()
        
        cash_budget = collections.copy()
        cash_budget['disbursements'] = 0.0
        cash_budget['beginning_cash'] = self.settings['beginning_cash']
        cash_budget['ending_cash'] = 0.0
        
        for i, row in cash_budget.iterrows():
            current_purchases = purchases.loc[i, 'purchases_cost']
            
            # Current quarter disbursements
            cash_budget.loc[i, 'disbursements'] += (current_purchases * 
                                                  self.settings['purchases_payment_current'])
            
            # Previous quarter disbursements (if not first quarter)
            if i > 0:
                prev_purchases = purchases.loc[i-1, 'purchases_cost']
                cash_budget.loc[i, 'disbursements'] += (prev_purchases * 
                                                      self.settings['purchases_payment_next'])
            
            # Cash flow
            if i == 0:
                cash_budget.loc[i, 'ending_cash'] = (self.settings['beginning_cash'] + 
                                                   row['collections'] - 
                                                   cash_budget.loc[i, 'disbursements'])
            else:
                cash_budget.loc[i, 'ending_cash'] = (cash_budget.loc[i-1, 'ending_cash'] + 
                                                   row['collections'] - 
                                                   cash_budget.loc[i, 'disbursements'])
        
        return cash_budget
    
    def compute_income_statement(self, sales_data: pd.DataFrame) -> pd.DataFrame:
        """Compute income statement."""
        if sales_data is None or sales_data.empty:
            return pd.DataFrame()
        
        income_stmt = pd.DataFrame()
        income_stmt['quarter'] = sales_data['quarter']
        income_stmt['total_revenue'] = sales_data['sales_units'] * sales_data['unit_price']
        
        # Cost of goods sold
        cost_per_unit = sales_data['unit_price'] * 0.6
        income_stmt['total_cogs'] = sales_data['sales_units'] * cost_per_unit
        
        # Gross profit
        income_stmt['gross_profit'] = income_stmt['total_revenue'] - income_stmt['total_cogs']
        
        return income_stmt
    
    def compute_balance_sheet(self, cash_budget: pd.DataFrame, purchases: pd.DataFrame, 
                            sales_data: pd.DataFrame) -> pd.DataFrame:
        """Compute balance sheet."""
        if (cash_budget is None or cash_budget.empty or 
            purchases is None or purchases.empty or 
            sales_data is None or sales_data.empty):
            return pd.DataFrame()
        
        balance_sheet = pd.DataFrame()
        balance_sheet['quarter'] = sales_data['quarter']
        
        # Assets
        balance_sheet['cash'] = cash_budget['ending_cash']
        
        # Inventory value
        inventory_value = purchases['desired_ending_inventory'] * (sales_data['unit_price'] * 0.6)
        balance_sheet['inventory'] = inventory_value
        
        # Receivables (uncollected sales)
        receivables = []
        for i, row in sales_data.iterrows():
            if i == 0:
                receivables.append(row['sales_revenue'] * (1 - self.settings['sales_collection_current']))
            else:
                prev_uncollected = receivables[i-1]
                current_uncollected = row['sales_revenue'] * (1 - self.settings['sales_collection_current'])
                receivables.append(prev_uncollected + current_uncollected - 
                                sales_data.loc[i-1, 'sales_revenue'] * self.settings['sales_collection_next'])
        
        balance_sheet['receivables'] = receivables
        
        # Total assets
        balance_sheet['total_assets'] = (balance_sheet['cash'] + 
                                       balance_sheet['inventory'] + 
                                       balance_sheet['receivables'])
        
        # Liabilities & Equity
        # External financing based on ratio
        external_financing = balance_sheet['total_assets'] * self.settings['external_financing_ratio']
        balance_sheet['external_financing'] = external_financing
        
        # Equity (plug figure)
        balance_sheet['equity'] = balance_sheet['total_assets'] - balance_sheet['external_financing']
        
        balance_sheet['liabilities_equity'] = (balance_sheet['external_financing'] + 
                                             balance_sheet['equity'])
        
        return balance_sheet 