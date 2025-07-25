import os
import PySimpleGUI as sg
import pandas as pd
import numpy as np
from openpyxl import Workbook
import xlsxwriter

# ----------------------
# Language Dictionaries
# ----------------------
LANGUAGES = {
    'en': {
        'Inputs': 'Inputs',
        'Settings': 'Settings',
        'Results': 'Results',
        'Quarter': 'Quarter',
        'Sales Units': 'Sales Units',
        'Unit Price': 'Unit Price',
        'Sales-collection % current quarter': 'Sales-collection % current quarter',
        'Sales-collection % next quarter': 'Sales-collection % next quarter',
        'Purchases-payment % current quarter': 'Purchases-payment % current quarter',
        'Purchases-payment % next quarter': 'Purchases-payment % next quarter',
        'Ending-inventory % of next quarter': 'Ending-inventory % of next quarter',
        'External-financing ratio %': 'External-financing ratio %',
        'Working-capital turnover ratio': 'Working-capital turnover ratio',
        'Load CSV': 'Load CSV',
        'Generate Cash Budget': 'Generate Cash Budget',
        'Generate Income Statement': 'Generate Income Statement',
        'Generate Balance Sheet': 'Generate Balance Sheet',
        'Save All Reports': 'Save All Reports',
        'Language': 'Language',
        'English': 'English',
        'Arabic': 'Arabic',
        'Error': 'Error',
        'Invalid input': 'Invalid input',
        'File not found': 'File not found',
        'Success': 'Success',
        'Reports saved to outputs/': 'Reports saved to outputs/',
        'OK': 'OK',
        'Cancel': 'Cancel',
        'Browse': 'Browse',
        'Select CSV File': 'Select CSV File',
        'No data to export': 'No data to export',
        'Please generate all reports first.': 'Please generate all reports first.',
    },
    'ar': {
        'Inputs': 'المدخلات',
        'Settings': 'الإعدادات',
        'Results': 'النتائج',
        'Quarter': 'ربع السنة',
        'Sales Units': 'وحدات المبيعات',
        'Unit Price': 'سعر الوحدة',
        'Sales-collection % current quarter': 'تحصيل المبيعات % الربع الحالي',
        'Sales-collection % next quarter': 'تحصيل المبيعات % الربع القادم',
        'Purchases-payment % current quarter': 'دفع المشتريات % الربع الحالي',
        'Purchases-payment % next quarter': 'دفع المشتريات % الربع القادم',
        'Ending-inventory % of next quarter': 'مخزون نهاية الفترة % من الربع القادم',
        'External-financing ratio %': 'نسبة التمويل الخارجي %',
        'Working-capital turnover ratio': 'معدل دوران رأس المال العامل',
        'Load CSV': 'تحميل ملف CSV',
        'Generate Cash Budget': 'إنشاء ميزانية نقدية',
        'Generate Income Statement': 'إنشاء قائمة الدخل',
        'Generate Balance Sheet': 'إنشاء الميزانية العمومية',
        'Save All Reports': 'حفظ جميع التقارير',
        'Language': 'اللغة',
        'English': 'الإنجليزية',
        'Arabic': 'العربية',
        'Error': 'خطأ',
        'Invalid input': 'إدخال غير صالح',
        'File not found': 'الملف غير موجود',
        'Success': 'نجاح',
        'Reports saved to outputs/': 'تم حفظ التقارير في مجلد المخرجات',
        'OK': 'موافق',
        'Cancel': 'إلغاء',
        'Browse': 'تصفح',
        'Select CSV File': 'اختر ملف CSV',
        'No data to export': 'لا توجد بيانات للتصدير',
        'Please generate all reports first.': 'يرجى إنشاء جميع التقارير أولاً.',
    }
}

# ----------------------
# Default Policy Values
# ----------------------
DEFAULT_POLICIES = {
    'Sales-collection % current quarter': 0.7,
    'Sales-collection % next quarter': 0.3,
    'Purchases-payment % current quarter': 0.6,
    'Purchases-payment % next quarter': 0.4,
    'Ending-inventory % of next quarter': 0.2,
    'External-financing ratio %': 0.1,
    'Working-capital turnover ratio': 2.0,
}

# ----------------------
# Helper Functions
# ----------------------
def get_text(key, lang):
    """Return the translated text for the given key and language."""
    return LANGUAGES[lang].get(key, key)

def load_inputs(filepath):
    """Load input CSV file into a DataFrame."""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        return None

def compute_sales(inputs_df):
    """Compute sales revenue for each quarter."""
    df = inputs_df.copy()
    df['Sales Revenue'] = df['sales_units'] * df['unit_price']
    return df

def compute_collections(sales_df, policies):
    """Compute collections schedule for each quarter."""
    collect_current = float(policies['Sales-collection % current quarter'])
    collect_next = float(policies['Sales-collection % next quarter'])
    inflow = []
    sales_rev = sales_df['Sales Revenue'].values
    for i in range(len(sales_rev)):
        curr = sales_rev[i] * collect_current
        prev = sales_rev[i-1] * collect_next if i > 0 else 0
        inflow.append(curr + prev)
    return inflow

def compute_purchases(inputs_df, policies):
    """Compute purchases units and desired ending inventory for each quarter."""
    ending_inv_pct = float(policies['Ending-inventory % of next quarter'])
    sales_units = inputs_df['sales_units'].values
    purchases_units = []
    desired_ending_inv = []
    beginning_inventory = [0]
    for i in range(len(sales_units)):
        next_q = sales_units[i+1] if i+1 < len(sales_units) else sales_units[i]
        desired_end = next_q * ending_inv_pct
        desired_ending_inv.append(desired_end)
        if i == 0:
            begin_inv = 0
        else:
            begin_inv = desired_ending_inv[i-1]
        beginning_inventory.append(begin_inv)
        purchases = sales_units[i] + desired_end - begin_inv
        purchases_units.append(purchases)
    beginning_inventory = beginning_inventory[:-1]
    return purchases_units, desired_ending_inv, beginning_inventory

def compute_disbursements(purchases_units, policies):
    """Compute disbursements schedule for each quarter."""
    pay_current = float(policies['Purchases-payment % current quarter'])
    pay_next = float(policies['Purchases-payment % next quarter'])
    outflow = []
    for i in range(len(purchases_units)):
        curr = purchases_units[i] * pay_current
        prev = purchases_units[i-1] * pay_next if i > 0 else 0
        outflow.append(curr + prev)
    return outflow

def compute_cash_budget(inputs_df, inflow, outflow):
    """Compute cash budget for each quarter."""
    beginning_cash = 0
    cash = []
    for i in range(len(inflow)):
        if i == 0:
            begin = beginning_cash
        else:
            begin = cash[i-1]
        ending = begin + inflow[i] - outflow[i]
        cash.append(ending)
    return cash

def compute_income_statement(sales_df, purchases_units):
    """Compute income statement for the year."""
    total_revenue = sales_df['Sales Revenue'].sum()
    total_cogs = np.sum(purchases_units)
    gross_profit = total_revenue - total_cogs
    return pd.DataFrame({
        'Total Revenue': [total_revenue],
        'Total COGS': [total_cogs],
        'Gross Profit': [gross_profit]
    })

def compute_balance_sheet(cash_budget, desired_ending_inv, sales_df, policies):
    """Compute balance sheet at year end."""
    ending_cash = cash_budget[-1]
    inventory_value = desired_ending_inv[-1] * sales_df['unit_price'].iloc[-1]
    receivables = sales_df['Sales Revenue'].iloc[-1] * float(policies['Sales-collection % next quarter'])
    assets = ending_cash + inventory_value + receivables
    ext_finance_ratio = float(policies['External-financing ratio %'])
    wc_turnover = float(policies['Working-capital turnover ratio'])
    external_financing = assets * ext_finance_ratio
    working_capital = assets / wc_turnover if wc_turnover != 0 else 0
    liabilities_equity = external_financing + working_capital
    return pd.DataFrame({
        'Assets': [assets],
        'Ending Cash': [ending_cash],
        'Inventory Value': [inventory_value],
        'Receivables': [receivables],
        'Liabilities & Equity': [liabilities_equity],
        'External Financing': [external_financing],
        'Working Capital': [working_capital]
    })

def export_reports(cash_budget_df, income_statement_df, balance_sheet_df):
    """Export all reports to Excel files in outputs/ directory."""
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    cash_budget_df.to_excel('outputs/cash_budget.xlsx', index=False, engine='xlsxwriter')
    income_statement_df.to_excel('outputs/income_statement.xlsx', index=False, engine='xlsxwriter')
    balance_sheet_df.to_excel('outputs/balance_sheet.xlsx', index=False, engine='xlsxwriter')

# ----------------------
# GUI Construction
# ----------------------
def build_gui():
    lang = 'en'
    sg.theme('LightBlue')
    
    def refresh_texts(lang):
        return [
            get_text('Quarter', lang),
            get_text('Sales Units', lang),
            get_text('Unit Price', lang)
        ]
    
    # Initial Data
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    table_data = [[q, '', ''] for q in quarters]
    policy_fields = list(DEFAULT_POLICIES.keys())
    policy_values = list(DEFAULT_POLICIES.values())
    
    # Layouts
    def make_inputs_tab(lang):
        return [
            [sg.Table(
                values=table_data,
                headings=refresh_texts(lang),
                key='-INPUT-TABLE-',
                auto_size_columns=False,
                col_widths=[8, 12, 10],
                justification='center',
                num_rows=4,
                enable_events=True,
                alternating_row_color='lightyellow',
                row_height=25,
                expand_x=True,
                expand_y=False
            )],
            [sg.Text(get_text('Sales-collection % current quarter', lang)), sg.Input(str(policy_values[0]), key='-SCURR-', size=(8,1))],
            [sg.Text(get_text('Sales-collection % next quarter', lang)), sg.Input(str(policy_values[1]), key='-SNEXT-', size=(8,1))],
            [sg.Text(get_text('Purchases-payment % current quarter', lang)), sg.Input(str(policy_values[2]), key='-PCURR-', size=(8,1))],
            [sg.Text(get_text('Purchases-payment % next quarter', lang)), sg.Input(str(policy_values[3]), key='-PNEXT-', size=(8,1))],
            [sg.Text(get_text('Ending-inventory % of next quarter', lang)), sg.Input(str(policy_values[4]), key='-EINV-', size=(8,1))],
            [sg.Text(get_text('External-financing ratio %', lang)), sg.Input(str(policy_values[5]), key='-EXTF-', size=(8,1))],
            [sg.Text(get_text('Working-capital turnover ratio', lang)), sg.Input(str(policy_values[6]), key='-WCT-', size=(8,1))],
            [sg.Button(get_text('Load CSV', lang), key='-LOAD-CSV-'), sg.FileBrowse(get_text('Browse', lang), file_types=(('CSV Files', '*.csv'),), key='-BROWSE-', target='-LOAD-CSV-')],
        ]
    def make_settings_tab(lang):
        return [
            [sg.Text(get_text(f, lang)), sg.Input(str(DEFAULT_POLICIES[f]), key=f'-SET-{f}-', size=(10,1))] for f in policy_fields
        ]
    def make_results_tab(lang):
        return [
            [sg.Button(get_text('Generate Cash Budget', lang), key='-GEN-CASH-'),
             sg.Button(get_text('Generate Income Statement', lang), key='-GEN-INC-'),
             sg.Button(get_text('Generate Balance Sheet', lang), key='-GEN-BAL-')],
            [sg.Button(get_text('Save All Reports', lang), key='-SAVE-ALL-')],
            [sg.Text('', key='-RESULT-TITLE-', size=(40,1))],
            [sg.Table(values=[[]], headings=[], key='-RESULT-TABLE-',
                      auto_size_columns=True, justification='center',
                      num_rows=10, expand_x=True, expand_y=True, enable_events=False)]
        ]
    # Language menu
    lang_menu = [[get_text('Language', lang), [get_text('English', lang), get_text('Arabic', lang)]]]
    layout = [
        [sg.Menu(lang_menu, key='-LANG-MENU-')],
        [sg.TabGroup([
            [sg.Tab(get_text('Inputs', lang), make_inputs_tab(lang), key='-TAB-INPUTS-'),
             sg.Tab(get_text('Settings', lang), make_settings_tab(lang), key='-TAB-SETTINGS-'),
             sg.Tab(get_text('Results', lang), make_results_tab(lang), key='-TAB-RESULTS-')]
        ], key='-TABGROUP-', expand_x=True, expand_y=True)]
    ]
    window = sg.Window('Master Budget GUI', layout, finalize=True, resizable=True)

    # State
    inputs_df = pd.DataFrame({
        'quarter': quarters,
        'sales_units': [0]*4,
        'unit_price': [0]*4
    })
    policies = DEFAULT_POLICIES.copy()
    cash_budget_df = None
    income_statement_df = None
    balance_sheet_df = None

    def update_table_from_df(df):
        vals = df[['quarter', 'sales_units', 'unit_price']].values.tolist()
        window['-INPUT-TABLE-'].update(values=vals)

    def update_df_from_table(values):
        try:
            for i, row in enumerate(values):
                inputs_df.at[i, 'sales_units'] = float(row[1]) if row[1] != '' else 0
                inputs_df.at[i, 'unit_price'] = float(row[2]) if row[2] != '' else 0
        except Exception:
            pass

    def update_policy_from_inputs():
        try:
            policies['Sales-collection % current quarter'] = float(window['-SCURR-'].get())
            policies['Sales-collection % next quarter'] = float(window['-SNEXT-'].get())
            policies['Purchases-payment % current quarter'] = float(window['-PCURR-'].get())
            policies['Purchases-payment % next quarter'] = float(window['-PNEXT-'].get())
            policies['Ending-inventory % of next quarter'] = float(window['-EINV-'].get())
            policies['External-financing ratio %'] = float(window['-EXTF-'].get())
            policies['Working-capital turnover ratio'] = float(window['-WCT-'].get())
        except Exception:
            sg.popup(get_text('Invalid input', lang), title=get_text('Error', lang))

    def update_policy_from_settings():
        try:
            for f in policy_fields:
                val = float(window[f'-SET-{f}-'].get())
                policies[f] = val
        except Exception:
            sg.popup(get_text('Invalid input', lang), title=get_text('Error', lang))

    def show_result_table(df, title):
        if df is not None:
            window['-RESULT-TITLE-'].update(title)
            window['-RESULT-TABLE-'].update(values=df.values.tolist(), headings=list(df.columns))
        else:
            window['-RESULT-TITLE-'].update('')
            window['-RESULT-TABLE-'].update(values=[[]], headings=[])

    # Main Event Loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        # Language switching
        if event in (get_text('English', lang), get_text('Arabic', lang)):
            lang = 'en' if event == get_text('English', lang) else 'ar'
            window.close()
            build_gui()
            return
        # Load CSV
        if event == '-LOAD-CSV-':
            filename = values['-BROWSE-']
            if filename and os.path.exists(filename):
                df = load_inputs(filename)
                if df is not None and set(['quarter','sales_units','unit_price']).issubset(df.columns):
                    df = df.head(4)
                    df['sales_units'] = df['sales_units'].astype(float)
                    df['unit_price'] = df['unit_price'].astype(float)
                    inputs_df.update(df)
                    update_table_from_df(inputs_df)
                else:
                    sg.popup(get_text('Invalid input', lang), title=get_text('Error', lang))
            else:
                sg.popup(get_text('File not found', lang), title=get_text('Error', lang))
        # Table edit
        if event == '-INPUT-TABLE-':
            update_df_from_table(values['-INPUT-TABLE-'])
        # Settings override
        if event.startswith('-SET-'):
            update_policy_from_settings()
        # Generate Cash Budget
        if event == '-GEN-CASH-':
            update_df_from_table(window['-INPUT-TABLE-'].get())
            update_policy_from_inputs()
            sales_df = compute_sales(inputs_df)
            inflow = compute_collections(sales_df, policies)
            purchases_units, desired_ending_inv, beginning_inventory = compute_purchases(inputs_df, policies)
            outflow = compute_disbursements(purchases_units, policies)
            cash_budget = compute_cash_budget(inputs_df, inflow, outflow)
            cash_budget_df = pd.DataFrame({
                'Quarter': quarters,
                'Sales Revenue': sales_df['Sales Revenue'],
                'Collections': inflow,
                'Purchases Units': purchases_units,
                'Disbursements': outflow,
                'Ending Cash': cash_budget
            })
            show_result_table(cash_budget_df, get_text('Generate Cash Budget', lang))
        # Generate Income Statement
        if event == '-GEN-INC-':
            if cash_budget_df is None:
                sg.popup(get_text('Invalid input', lang), title=get_text('Error', lang))
                continue
            sales_df = compute_sales(inputs_df)
            purchases_units, _, _ = compute_purchases(inputs_df, policies)
            income_statement_df = compute_income_statement(sales_df, purchases_units)
            show_result_table(income_statement_df, get_text('Generate Income Statement', lang))
        # Generate Balance Sheet
        if event == '-GEN-BAL-':
            if cash_budget_df is None:
                sg.popup(get_text('Invalid input', lang), title=get_text('Error', lang))
                continue
            sales_df = compute_sales(inputs_df)
            purchases_units, desired_ending_inv, _ = compute_purchases(inputs_df, policies)
            balance_sheet_df = compute_balance_sheet(
                cash_budget_df['Ending Cash'].values,
                desired_ending_inv,
                sales_df,
                policies
            )
            show_result_table(balance_sheet_df, get_text('Generate Balance Sheet', lang))
        # Save All Reports
        if event == '-SAVE-ALL-':
            if cash_budget_df is not None and income_statement_df is not None and balance_sheet_df is not None:
                export_reports(cash_budget_df, income_statement_df, balance_sheet_df)
                sg.popup(get_text('Reports saved to outputs/', lang), title=get_text('Success', lang))
            else:
                sg.popup(get_text('Please generate all reports first.', lang), title=get_text('No data to export', lang))
    window.close()

if __name__ == "__main__":
    build_gui()