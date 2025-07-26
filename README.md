# Master Budget Application

A professional, enterprise-grade desktop application for comprehensive budget planning and financial analysis. Built with modern Python technologies and a clean, modular architecture.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green.svg)
![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-Styling-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data-orange.svg)

## 🚀 Features

### 📊 **Professional Interface**
- Modern, responsive GUI with ttkbootstrap styling
- Intuitive three-tab interface (Inputs, Settings, Results)
- Real-time data validation and error handling
- Professional color scheme and typography

### 📈 **Comprehensive Financial Analysis**
- **Cash Budget Generation**: Complete cash flow analysis
- **Income Statement**: Revenue and cost analysis
- **Balance Sheet**: Asset and liability calculations
- **Advanced Calculations**: Collections, purchases, inventory management

### 🌐 **Multilingual Support**
- English and Arabic language support
- Dynamic language switching
- Localized error messages and interface elements

### 📁 **Data Management**
- CSV import with validation
- Excel export with multiple worksheets
- Sample data included
- Robust error handling

### ⚙️ **Configurable Settings**
- Policy parameter customization
- Settings persistence
- Validation and error checking
- Default value management

## 🏗️ Architecture

### **Modular Design**
```
MasterBudget/
├── src/
│   ├── core/                    # Business Logic Layer
│   │   ├── budget_calculator.py # Financial calculations
│   │   ├── data_manager.py      # Data I/O operations
│   │   └── settings_manager.py  # Configuration management
│   ├── ui/                      # Presentation Layer
│   │   ├── main_window.py       # GUI components
│   │   └── language_manager.py  # Internationalization
│   └── __init__.py
├── data/
│   └── sample_data.csv          # Sample budget data
├── outputs/                     # Generated reports
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                   # Documentation
```

### **Core Components**

#### **Business Logic (`src/core/`)**
- **`BudgetCalculator`**: Handles all financial calculations
- **`DataManager`**: CSV import/export and validation
- **`SettingsManager`**: Application configuration

#### **User Interface (`src/ui/`)**
- **`MainWindow`**: Main application window
- **`LanguageManager`**: Multilingual support system

## 🛠️ Installation

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Quick Start**
```bash
# Clone or download the project
cd MasterBudget

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### **Development Setup**
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

## 📋 Usage Guide

### **1. Getting Started**
1. Launch the application: `python main.py`
2. The application opens with three main tabs
3. Switch languages using the dropdown in the top-right corner

### **2. Inputs Tab**
- **Load Data**: Click "📂 Load CSV" to import your budget data
- **View Data**: Data appears in a professional table format
- **Adjust Parameters**: Modify policy parameters on the right panel

### **3. Settings Tab**
- **Configure Settings**: Adjust all application parameters
- **Save Settings**: Click "Save Settings" to persist changes
- **Validation**: Invalid inputs are automatically detected

### **4. Results Tab**
- **Generate Reports**: Use the colored buttons to create reports
  - 💵 **Cash Budget**: Cash flow analysis
  - 📈 **Income Statement**: Revenue and profit analysis
  - 📑 **Balance Sheet**: Asset and liability overview
- **Export Reports**: Click "💾 Save All Reports" to export to Excel

## 📊 Data Format

### **CSV Input Format**
Your CSV file must contain these columns:
```csv
quarter,sales_units,unit_price
Q1,10000,20
Q2,12000,20
Q3,15000,20
Q4,13000,20
```

### **Required Fields**
- **`quarter`**: Quarter identifier (Q1, Q2, Q3, Q4)
- **`sales_units`**: Number of units sold (positive number)
- **`unit_price`**: Price per unit (positive number)

### **Sample Data**
A sample CSV file is included in `data/sample_data.csv` for testing.

## 🔧 Configuration

### **Policy Parameters**
The application uses these configurable parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| Sales Collection % (Current) | Current quarter collection rate | 60% |
| Sales Collection % (Next) | Next quarter collection rate | 40% |
| Purchases Payment % (Current) | Current quarter payment rate | 50% |
| Purchases Payment % (Next) | Next quarter payment rate | 50% |
| Ending Inventory % | Inventory as % of next quarter sales | 20% |
| External Financing Ratio | External financing as % of assets | 30% |
| Working Capital Turnover | Working capital efficiency ratio | 2.0 |
| Beginning Cash | Starting cash balance | $100,000 |

## 📈 Calculations

### **Cash Budget**
- **Sales Revenue**: `sales_units × unit_price`
- **Collections**: Current + previous quarter collections
- **Purchases**: Units needed + ending inventory - beginning inventory
- **Cash Flow**: Beginning cash + collections - disbursements

### **Income Statement**
- **Revenue**: Total sales revenue
- **Cost of Goods Sold**: 60% of selling price
- **Gross Profit**: Revenue - COGS

### **Balance Sheet**
- **Assets**: Cash + Inventory + Receivables
- **Liabilities**: External financing
- **Equity**: Assets - Liabilities

## 🌐 Language Support

### **Available Languages**
- **English**: Default language
- **Arabic**: Full Arabic translation with RTL support

### **Language Switching**
- Use the language dropdown in the top-right corner
- Interface updates dynamically
- Error messages are localized

## 📁 Output Files

### **Excel Reports**
Reports are saved to the `outputs/` folder with timestamps:
```
outputs/
├── budget_reports_20241201_143022.xlsx
├── budget_reports_20241201_150145.xlsx
└── ...
```

### **Report Contents**
Each Excel file contains multiple worksheets:
- **Cash Budget**: Cash flow analysis
- **Income Statement**: Revenue and profit analysis
- **Balance Sheet**: Asset and liability overview

## 🛠️ Development

### **Project Structure**
```
src/
├── core/                    # Business logic
│   ├── budget_calculator.py # Financial calculations
│   ├── data_manager.py      # Data operations
│   └── settings_manager.py  # Configuration
├── ui/                      # User interface
│   ├── main_window.py       # Main window
│   └── language_manager.py  # Languages
└── __init__.py
```

### **Adding Features**
1. **Business Logic**: Add to `src/core/`
2. **UI Components**: Add to `src/ui/`
3. **New Languages**: Update `LanguageManager`
4. **Calculations**: Extend `BudgetCalculator`

### **Testing**
```bash
# Run basic functionality test
python -c "from src.core import BudgetCalculator; print('Core modules working')"

# Test data loading
python -c "from src.core import DataManager; dm = DataManager(); print('Data manager ready')"
```

## 📦 Dependencies

### **Core Dependencies**
- **ttkbootstrap**: Modern Tkinter styling
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **openpyxl**: Excel file export

### **Version Requirements**
```
pandas==2.3.1
numpy==2.3.2
openpyxl==3.1.5
ttkbootstrap==1.10.1
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

#### **CSV Loading Issues**
- Verify CSV format matches the required structure
- Check that all values are positive numbers
- Ensure file encoding is UTF-8

#### **GUI Display Issues**
- Update ttkbootstrap: `pip install --upgrade ttkbootstrap`
- Check Python version (3.8+ required)

### **Error Messages**
- **"No data available"**: Load CSV data first
- **"Invalid settings"**: Check parameter values (0-1 for percentages)
- **"CSV format error"**: Verify column names and data types

## 🤝 Contributing

### **Development Guidelines**
1. Follow the modular architecture
2. Add type hints to all functions
3. Include comprehensive docstrings
4. Test new features thoroughly
5. Update documentation

### **Code Style**
- Use PEP 8 formatting
- Include type annotations
- Write descriptive variable names
- Add error handling

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

### **Getting Help**
1. Check the troubleshooting section above
2. Verify your data format matches the requirements
3. Ensure all dependencies are installed
4. Test with the provided sample data

### **Feature Requests**
- Suggest new features through issues
- Provide detailed use cases
- Include sample data if relevant

---

**Built with ❤️ using Python, Tkinter, and ttkbootstrap**