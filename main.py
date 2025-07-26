#!/usr/bin/env python3
"""
Master Budget Application
A professional desktop application for budget planning and financial analysis.
"""

from src.ui import MainWindow


def main():
    """Main entry point for the application."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main() 