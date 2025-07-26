"""
Main application window and GUI components.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from typing import Optional, Dict, Any

from ..core import BudgetCalculator, DataManager, SettingsManager
from .language_manager import LanguageManager


class MainWindow:
    """Main application window."""
    
    def __init__(self):
        self.root = ttk.Window(themename="flatly")
        self.root.title("Master Budget Application")
        self.root.geometry("1200x800")
        
        # Initialize managers
        self.language_manager = LanguageManager()
        self.data_manager = DataManager()
        self.settings_manager = SettingsManager()
        self.budget_calculator = BudgetCalculator(self.settings_manager.get_all_settings())
        
        # Data storage
        self.data = None
        self.setting_vars = {}
        
        # UI elements for language updates
        self.ui_elements = {}
        self.setting_labels = {}
        self.inputs_setting_labels = {}  # Separate for inputs tab
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main user interface."""
        # Top bar with language selector
        self.create_top_bar()
        
        # Main notebook
        self.notebook = ttk.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        # Create tabs
        self.create_inputs_tab()
        self.create_settings_tab()
        self.create_results_tab()
    
    def create_top_bar(self):
        """Create the top bar with language selector."""
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=X, padx=10, pady=5)
        
        # Language label
        lang_label = ttk.Label(top_frame, text=self.language_manager.get_text("language"), 
                              font=("Segoe UI", 11))
        lang_label.pack(side=RIGHT, padx=(0,5))
        self.ui_elements['lang_label'] = lang_label
        
        # Language selector
        self.lang_var = tk.StringVar(value=self.language_manager.get_current_language())
        lang_combo = ttk.Combobox(top_frame, textvariable=self.lang_var, 
                                 values=self.language_manager.get_available_languages(), 
                                 width=10, state="readonly")
        lang_combo.pack(side=RIGHT)
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)
    
    def create_inputs_tab(self):
        """Create the inputs tab."""
        self.inputs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inputs_frame, text=self.language_manager.get_text("inputs"))
        
        # Left side - Data table
        left_frame = ttk.Frame(self.inputs_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0,10))
        
        # Budget data label
        budget_label = ttk.Label(left_frame, text=self.language_manager.get_text("budget_data"), 
                                font=("Segoe UI", 14, "bold"))
        budget_label.pack(anchor=W, pady=(0,10))
        self.ui_elements['budget_data_label'] = budget_label
        
        # Table
        columns = (self.language_manager.get_text("quarter"), 
                  self.language_manager.get_text("sales_units"), 
                  self.language_manager.get_text("unit_price"))
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=CENTER)
        
        self.tree.pack(fill=BOTH, expand=YES)
        self.ui_elements['tree'] = self.tree
        
        # Load CSV button
        load_button = ttk.Button(left_frame, text=self.language_manager.get_text("load_csv"), 
                                command=self.load_csv, bootstyle="primary")
        load_button.pack(pady=10)
        self.ui_elements['load_csv_button'] = load_button
        
        # Right side - Settings
        right_frame = ttk.Frame(self.inputs_frame)
        right_frame.pack(side=RIGHT, fill=Y, padx=(10,0))
        
        # Policy parameters label
        policy_label = ttk.Label(right_frame, text=self.language_manager.get_text("policy_parameters"), 
                                font=("Segoe UI", 14, "bold"))
        policy_label.pack(anchor=W, pady=(0,10))
        self.ui_elements['policy_parameters_label'] = policy_label
        
        # Settings inputs for inputs tab
        self.create_inputs_settings(right_frame)
    
    def create_inputs_settings(self, parent):
        """Create input fields for settings in the inputs tab."""
        settings_list = [
            ('sales_collection_current', self.language_manager.get_text("sales_collection_current")),
            ('sales_collection_next', self.language_manager.get_text("sales_collection_next")),
            ('purchases_payment_current', self.language_manager.get_text("purchases_payment_current")),
            ('purchases_payment_next', self.language_manager.get_text("purchases_payment_next")),
            ('ending_inventory_pct', self.language_manager.get_text("ending_inventory_pct")),
            ('external_financing_ratio', self.language_manager.get_text("external_financing_ratio")),
            ('working_capital_turnover', self.language_manager.get_text("working_capital_turnover")),
            ('beginning_cash', self.language_manager.get_text("beginning_cash"))
        ]
        
        for setting, label in settings_list:
            frame = ttk.Frame(parent)
            frame.pack(fill=X, pady=2)
            
            label_widget = ttk.Label(frame, text=f"{label}:", font=("Segoe UI", 10))
            label_widget.pack(anchor=W)
            self.inputs_setting_labels[setting] = label_widget
            
            # Create variable with default value
            default_value = self.settings_manager.get_setting(setting)
            var = tk.StringVar(value=f"{default_value:.2f}" if isinstance(default_value, float) else str(default_value))
            self.setting_vars[setting] = var
            ttk.Entry(frame, textvariable=var, width=15).pack(anchor=W, pady=(2,0))
    
    def create_settings_inputs(self, parent):
        """Create input fields for settings in the settings tab."""
        settings_list = [
            ('sales_collection_current', self.language_manager.get_text("sales_collection_current")),
            ('sales_collection_next', self.language_manager.get_text("sales_collection_next")),
            ('purchases_payment_current', self.language_manager.get_text("purchases_payment_current")),
            ('purchases_payment_next', self.language_manager.get_text("purchases_payment_next")),
            ('ending_inventory_pct', self.language_manager.get_text("ending_inventory_pct")),
            ('external_financing_ratio', self.language_manager.get_text("external_financing_ratio")),
            ('working_capital_turnover', self.language_manager.get_text("working_capital_turnover")),
            ('beginning_cash', self.language_manager.get_text("beginning_cash"))
        ]
        
        for setting, label in settings_list:
            frame = ttk.Frame(parent)
            frame.pack(fill=X, pady=2)
            
            label_widget = ttk.Label(frame, text=f"{label}:", font=("Segoe UI", 10))
            label_widget.pack(anchor=W)
            self.setting_labels[setting] = label_widget
            
            # Create variable with default value
            default_value = self.settings_manager.get_setting(setting)
            var = tk.StringVar(value=f"{default_value:.2f}" if isinstance(default_value, float) else str(default_value))
            self.setting_vars[setting] = var
            ttk.Entry(frame, textvariable=var, width=15).pack(anchor=W, pady=(2,0))
    
    def create_settings_tab(self):
        """Create the settings tab."""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.language_manager.get_text("settings"))
        
        # Application settings label
        settings_label = ttk.Label(self.settings_frame, text=self.language_manager.get_text("application_settings"), 
                                  font=("Segoe UI", 16, "bold"))
        settings_label.pack(anchor=W, pady=(0,20))
        self.ui_elements['application_settings_label'] = settings_label
        
        # Create settings inputs
        self.create_settings_inputs(self.settings_frame)
        
        # Save settings button
        save_button = ttk.Button(self.settings_frame, text=self.language_manager.get_text("save_settings"), 
                                command=self.save_settings, bootstyle="success")
        save_button.pack(pady=20)
        self.ui_elements['save_settings_button'] = save_button
    
    def create_results_tab(self):
        """Create the results tab."""
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text=self.language_manager.get_text("results"))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.results_frame)
        buttons_frame.pack(fill=X, pady=(0,20))
        
        # Generate buttons
        cash_button = ttk.Button(buttons_frame, text=self.language_manager.get_text("generate_cash"), 
                                command=self.generate_cash_budget, bootstyle="success")
        cash_button.pack(side=LEFT, padx=(0,10))
        self.ui_elements['generate_cash_button'] = cash_button
        
        income_button = ttk.Button(buttons_frame, text=self.language_manager.get_text("generate_income"), 
                                  command=self.generate_income_statement, bootstyle="info")
        income_button.pack(side=LEFT, padx=(0,10))
        self.ui_elements['generate_income_button'] = income_button
        
        balance_button = ttk.Button(buttons_frame, text=self.language_manager.get_text("generate_balance"), 
                                   command=self.generate_balance_sheet, bootstyle="warning")
        balance_button.pack(side=LEFT, padx=(0,10))
        self.ui_elements['generate_balance_button'] = balance_button
        
        save_reports_button = ttk.Button(buttons_frame, text=self.language_manager.get_text("save_reports"), 
                                        command=self.save_all_reports, bootstyle="danger")
        save_reports_button.pack(side=LEFT)
        self.ui_elements['save_reports_button'] = save_reports_button
        
        # Results display
        results_label = ttk.Label(self.results_frame, text=self.language_manager.get_text("results"), 
                                 font=("Segoe UI", 14, "bold"))
        results_label.pack(anchor=W, pady=(0,10))
        self.ui_elements['results_label'] = results_label
        
        # Text area for results
        self.results_text = tk.Text(self.results_frame, height=20, width=80, font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(self.results_frame, orient=VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def update_ui_language(self):
        """Update all UI elements with the current language."""
        # Update window title
        self.root.title(self.language_manager.get_text("title"))
        
        # Update notebook tabs
        self.notebook.tab(0, text=self.language_manager.get_text("inputs"))
        self.notebook.tab(1, text=self.language_manager.get_text("settings"))
        self.notebook.tab(2, text=self.language_manager.get_text("results"))
        
        # Update labels
        if 'lang_label' in self.ui_elements:
            self.ui_elements['lang_label'].config(text=self.language_manager.get_text("language"))
        
        if 'budget_data_label' in self.ui_elements:
            self.ui_elements['budget_data_label'].config(text=self.language_manager.get_text("budget_data"))
        
        if 'policy_parameters_label' in self.ui_elements:
            self.ui_elements['policy_parameters_label'].config(text=self.language_manager.get_text("policy_parameters"))
        
        if 'application_settings_label' in self.ui_elements:
            self.ui_elements['application_settings_label'].config(text=self.language_manager.get_text("application_settings"))
        
        if 'results_label' in self.ui_elements:
            self.ui_elements['results_label'].config(text=self.language_manager.get_text("results"))
        
        # Update buttons
        if 'load_csv_button' in self.ui_elements:
            self.ui_elements['load_csv_button'].config(text=self.language_manager.get_text("load_csv"))
        
        if 'save_settings_button' in self.ui_elements:
            self.ui_elements['save_settings_button'].config(text=self.language_manager.get_text("save_settings"))
        
        if 'generate_cash_button' in self.ui_elements:
            self.ui_elements['generate_cash_button'].config(text=self.language_manager.get_text("generate_cash"))
        
        if 'generate_income_button' in self.ui_elements:
            self.ui_elements['generate_income_button'].config(text=self.language_manager.get_text("generate_income"))
        
        if 'generate_balance_button' in self.ui_elements:
            self.ui_elements['generate_balance_button'].config(text=self.language_manager.get_text("generate_balance"))
        
        if 'save_reports_button' in self.ui_elements:
            self.ui_elements['save_reports_button'].config(text=self.language_manager.get_text("save_reports"))
        
        # Update tree columns
        if 'tree' in self.ui_elements:
            tree = self.ui_elements['tree']
            # Clear existing columns
            for col in tree['columns']:
                tree.heading(col, text="")
            
            # Set new columns
            new_columns = (self.language_manager.get_text("quarter"), 
                          self.language_manager.get_text("sales_units"), 
                          self.language_manager.get_text("unit_price"))
            tree['columns'] = new_columns
            
            for col in new_columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor=CENTER)
        
        # Update setting labels in inputs tab
        settings_list = [
            ('sales_collection_current', self.language_manager.get_text("sales_collection_current")),
            ('sales_collection_next', self.language_manager.get_text("sales_collection_next")),
            ('purchases_payment_current', self.language_manager.get_text("purchases_payment_current")),
            ('purchases_payment_next', self.language_manager.get_text("purchases_payment_next")),
            ('ending_inventory_pct', self.language_manager.get_text("ending_inventory_pct")),
            ('external_financing_ratio', self.language_manager.get_text("external_financing_ratio")),
            ('working_capital_turnover', self.language_manager.get_text("working_capital_turnover")),
            ('beginning_cash', self.language_manager.get_text("beginning_cash"))
        ]
        
        # Update inputs tab setting labels
        for setting, label in settings_list:
            if setting in self.inputs_setting_labels:
                self.inputs_setting_labels[setting].config(text=f"{label}:")
        
        # Update settings tab setting labels
        for setting, label in settings_list:
            if setting in self.setting_labels:
                self.setting_labels[setting].config(text=f"{label}:")
    
    def change_language(self, event=None):
        """Change the application language."""
        new_language = self.lang_var.get()
        if self.language_manager.set_language(new_language):
            self.update_ui_language()
    
    def load_csv(self):
        """Load CSV file."""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            success, df, error_msg = self.data_manager.load_csv(filename)
            
            if success:
                self.data = df
                
                # Update table
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                for _, row in df.iterrows():
                    self.tree.insert("", END, values=(row['quarter'], row['sales_units'], row['unit_price']))
                
                messagebox.showinfo(self.language_manager.get_text("success"), "CSV file loaded successfully!")
            else:
                messagebox.showerror(self.language_manager.get_text("error"), error_msg)
    
    def save_settings(self):
        """Save application settings."""
        try:
            new_settings = {}
            for setting, var in self.setting_vars.items():
                new_settings[setting] = float(var.get())
            
            if self.settings_manager.update_settings(new_settings):
                self.budget_calculator = BudgetCalculator(self.settings_manager.get_all_settings())
                messagebox.showinfo(self.language_manager.get_text("success"), 
                                 self.language_manager.get_text("settings_saved"))
            else:
                messagebox.showerror(self.language_manager.get_text("error"), 
                                  self.language_manager.get_text("invalid_settings"))
        except ValueError:
            messagebox.showerror(self.language_manager.get_text("error"), 
                              self.language_manager.get_text("invalid_settings"))
    
    def generate_cash_budget(self):
        """Generate cash budget."""
        if self.data is None:
            messagebox.showwarning("Warning", self.language_manager.get_text("no_data"))
            return
        
        try:
            # Calculate cash budget
            sales_data = self.budget_calculator.compute_sales_revenue(self.data)
            collections = self.budget_calculator.compute_collections(sales_data)
            purchases = self.budget_calculator.compute_purchases(sales_data)
            cash_budget = self.budget_calculator.compute_cash_budget(collections, purchases)
            
            # Display results
            self.results_text.delete(1.0, END)
            self.results_text.insert(END, "Cash Budget:\n\n")
            self.results_text.insert(END, cash_budget.to_string(index=False))
            
        except Exception as e:
            messagebox.showerror(self.language_manager.get_text("error"), f"Error generating cash budget: {str(e)}")
    
    def generate_income_statement(self):
        """Generate income statement."""
        if self.data is None:
            messagebox.showwarning("Warning", self.language_manager.get_text("no_data"))
            return
        
        try:
            # Calculate income statement
            sales_data = self.budget_calculator.compute_sales_revenue(self.data)
            income_stmt = self.budget_calculator.compute_income_statement(sales_data)
            
            # Display results
            self.results_text.delete(1.0, END)
            self.results_text.insert(END, "Income Statement:\n\n")
            self.results_text.insert(END, income_stmt.to_string(index=False))
            
        except Exception as e:
            messagebox.showerror(self.language_manager.get_text("error"), f"Error generating income statement: {str(e)}")
    
    def generate_balance_sheet(self):
        """Generate balance sheet."""
        if self.data is None:
            messagebox.showwarning("Warning", self.language_manager.get_text("no_data"))
            return
        
        try:
            # Calculate balance sheet
            sales_data = self.budget_calculator.compute_sales_revenue(self.data)
            collections = self.budget_calculator.compute_collections(sales_data)
            purchases = self.budget_calculator.compute_purchases(sales_data)
            cash_budget = self.budget_calculator.compute_cash_budget(collections, purchases)
            balance_sheet = self.budget_calculator.compute_balance_sheet(cash_budget, purchases, sales_data)
            
            # Display results
            self.results_text.delete(1.0, END)
            self.results_text.insert(END, "Balance Sheet:\n\n")
            self.results_text.insert(END, balance_sheet.to_string(index=False))
            
        except Exception as e:
            messagebox.showerror(self.language_manager.get_text("error"), f"Error generating balance sheet: {str(e)}")
    
    def save_all_reports(self):
        """Save all reports to Excel."""
        if self.data is None:
            messagebox.showwarning("Warning", self.language_manager.get_text("no_data"))
            return
        
        try:
            # Generate all reports
            sales_data = self.budget_calculator.compute_sales_revenue(self.data)
            collections = self.budget_calculator.compute_collections(sales_data)
            purchases = self.budget_calculator.compute_purchases(sales_data)
            cash_budget = self.budget_calculator.compute_cash_budget(collections, purchases)
            income_stmt = self.budget_calculator.compute_income_statement(sales_data)
            balance_sheet = self.budget_calculator.compute_balance_sheet(cash_budget, purchases, sales_data)
            
            # Prepare dataframes for export
            dataframes = {
                'Cash Budget': cash_budget,
                'Income Statement': income_stmt,
                'Balance Sheet': balance_sheet
            }
            
            # Export to Excel
            success, message = self.data_manager.export_to_excel(dataframes)
            
            if success:
                messagebox.showinfo(self.language_manager.get_text("success"), 
                                 self.language_manager.get_text("reports_saved"))
            else:
                messagebox.showerror(self.language_manager.get_text("error"), message)
                
        except Exception as e:
            messagebox.showerror(self.language_manager.get_text("error"), f"Error saving reports: {str(e)}")
    
    def run(self):
        """Start the application."""
        self.root.mainloop() 