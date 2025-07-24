from datetime import date
import os
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
from expense_tracker import DATA_DIR, ARCHIVE_DIR, ONEDRIVE_DIR, logger
class ExcelManager:
    def __init__(self):
        #set folder path
        self.archive_dir = ARCHIVE_DIR
        self.data_path = DATA_DIR
        self.onedrive_path = ONEDRIVE_DIR
                
        #initialize logging
        self.logger = logger

    def create_monthly_workbook(self, month_year):
        # Create Excel file with weekly sheets
        # Add formulas and formatting
        # Create summary and review sheets
        pass

    def add_transaction (self, transaction_date):
        # Determine week number (19th-12th cycle)
        # Add to appropriate worksheet
        # Update totals and formulas
        pass

    def determine_week_num(self, date):
        # Calculate week based on custom cycle
        # Handle month boundaries
        # Return week number for sheet selection
        pass