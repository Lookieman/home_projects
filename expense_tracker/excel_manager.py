from datetime import date
import os
import pandas as pd
from openpyxl import Workbook
from pathlib import Path
from utils import RESULTS_DIR, logger
class ExcelManager:
    def __init__(self):
        #set folder path to save excel
        self.results_path = RESULTS_DIR        
        #initialize logging
        self.logger = logger

    def create_monthly_workbook(self, month_year: list):
        """ Create workbook and tabs if file does not exist
        excel name convention is Exepense_<mon>_<yy>.xlsx.
        month_year will already concatenate the month and year
        Workbook covers week from 14th of the month prior to 13th of the
        current month, e.g. Expense_Jul_25.xlsx should contain receipts from
        Jun 14 to Jul 13
        """

        expense_mth = month_year[0]
        expense_year = month_year[1]

        #get excel filename
        excel_filename = f"Expense_{expense_mth}_{expense_year}.xlsx"
        excel_filepath = Path(RESULTS_DIR / excel_filename)
        
        #get week number
        start_date = date(expense_year, expense_mth, "14")
        end_date = date(expense_year, int(expense_mth) + 1, 14)

        formatted_start_date = start_date.strtime("%d%m%y")
        formatted_end_date = end_date.strtime("%d%m%y")

        start_week = self.determine_week_num(formatted_start_date)
        end_week = self.determine_week_num(formatted_end_date)

        # check if excel file exists already 
        if excel_filepath.exists():
            self.logger.info(f"file {excel_filename} already exists")
            return None
        else:       
            # if not Create Excel file with weekly sheets
            wb = Workbook()

            for week_num in (start_week, end_week):
                sheet_name = f"week_{week_num}"
                wb.create_sheet(title = sheet_name)
            # Add formulas and formatting
            # Create summary and review sheets
            pass

    def add_transaction (self,  transaction_details: dict):
        # Determine week number (19th-12th cycle)
        week_no = self.determine_week_num(transaction_details['date'])
        # Add to appropriate worksheet
        # Update totals and formulas
        pass

    def determine_week_num(self, date_to_check: date):
        """ Calculate week based on date using ISO calendar"""
        #Get iso_calendar representation (year, week no, weekday)
        iso_calendar = date_to_check.isocalendar()

        #get week number
        week_number =iso_calendar[1]
        
        return week_number