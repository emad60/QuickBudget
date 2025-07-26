"""
Language management for multilingual support.
"""

from typing import Dict, Any


class LanguageManager:
    """Manages application languages and translations."""
    
    def __init__(self):
        self.current_language = "English"
        self.languages = {
            "English": {
                "title": "Master Budget Application",
                "inputs": "📝 Inputs",
                "settings": "⚙️ Settings", 
                "results": "📊 Results",
                "load_csv": "📂 Load CSV",
                "generate_cash": "💵 Generate Cash Budget",
                "generate_income": "📈 Generate Income Statement",
                "generate_balance": "📑 Generate Balance Sheet",
                "save_reports": "💾 Save All Reports",
                "language": "Language:",
                "quarter": "Quarter",
                "sales_units": "Sales Units",
                "unit_price": "Unit Price",
                "sales_collection_current": "Sales Collection % (Current Quarter)",
                "sales_collection_next": "Sales Collection % (Next Quarter)",
                "purchases_payment_current": "Purchases Payment % (Current Quarter)",
                "purchases_payment_next": "Purchases Payment % (Next Quarter)",
                "ending_inventory_pct": "Ending Inventory % of Next Quarter",
                "external_financing_ratio": "External Financing Ratio %",
                "working_capital_turnover": "Working Capital Turnover Ratio",
                "beginning_cash": "Beginning Cash",
                "success": "Success",
                "error": "Error",
                "reports_saved": "All reports saved successfully",
                "no_data": "No data available",
                "save_settings": "Save Settings",
                "settings_saved": "Settings saved successfully",
                "invalid_settings": "Please enter valid numbers for all settings",
                "budget_data": "Budget Data",
                "policy_parameters": "Policy Parameters",
                "application_settings": "Application Settings",
                "results": "Results"
            },
            "Arabic": {
                "title": "تطبيق الميزانية الرئيسية",
                "inputs": "📝 المدخلات",
                "settings": "⚙️ الإعدادات",
                "results": "📊 النتائج",
                "load_csv": "📂 تحميل CSV",
                "generate_cash": "💵 إنشاء ميزانية النقدية",
                "generate_income": "📈 إنشاء بيان الدخل",
                "generate_balance": "📑 إنشاء الميزانية العمومية",
                "save_reports": "💾 حفظ جميع التقارير",
                "language": "اللغة:",
                "quarter": "الربع",
                "sales_units": "وحدات المبيعات",
                "unit_price": "سعر الوحدة",
                "sales_collection_current": "نسبة تحصيل المبيعات % (الربع الحالي)",
                "sales_collection_next": "نسبة تحصيل المبيعات % (الربع التالي)",
                "purchases_payment_current": "نسبة دفع المشتريات % (الربع الحالي)",
                "purchases_payment_next": "نسبة دفع المشتريات % (الربع التالي)",
                "ending_inventory_pct": "نسبة المخزون النهائي من الربع التالي %",
                "external_financing_ratio": "نسبة التمويل الخارجي %",
                "working_capital_turnover": "نسبة دوران رأس المال العامل",
                "beginning_cash": "النقدية الافتتاحية",
                "success": "نجح",
                "error": "خطأ",
                "reports_saved": "تم حفظ جميع التقارير بنجاح",
                "no_data": "لا توجد بيانات متاحة",
                "save_settings": "حفظ الإعدادات",
                "settings_saved": "تم حفظ الإعدادات بنجاح",
                "invalid_settings": "يرجى إدخال أرقام صحيحة لجميع الإعدادات",
                "budget_data": "بيانات الميزانية",
                "policy_parameters": "معاملات السياسة",
                "application_settings": "إعدادات التطبيق",
                "results": "النتائج"
            }
        }
    
    def get_text(self, key: str) -> str:
        """Get translated text for the current language."""
        return self.languages.get(self.current_language, {}).get(key, key)
    
    def set_language(self, language: str) -> bool:
        """Set the current language."""
        if language in self.languages:
            self.current_language = language
            return True
        return False
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.languages.keys())
    
    def get_current_language(self) -> str:
        """Get the current language."""
        return self.current_language
    
    def get_all_texts(self) -> Dict[str, str]:
        """Get all texts for the current language."""
        return self.languages.get(self.current_language, {}).copy()
    
    def add_language(self, language_code: str, translations: Dict[str, str]) -> bool:
        """Add a new language to the system."""
        try:
            self.languages[language_code] = translations
            return True
        except Exception:
            return False
    
    def get_language_info(self) -> Dict[str, Any]:
        """Get information about available languages."""
        return {
            'current_language': self.current_language,
            'available_languages': self.get_available_languages(),
            'total_languages': len(self.languages),
            'total_translations': len(self.languages.get(self.current_language, {}))
        } 