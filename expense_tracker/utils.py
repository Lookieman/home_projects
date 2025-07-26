import logging

from typing import Optional
from pathlib import Path

#set folder path
ARCHIVE_DIR = Path('C:/home_projects/expense_tracker/data/archive')
DATA_DIR = Path('C:/home_projects/expense_tracker/data/inbox')
ONEDRIVE_DIR = Path('E:/OneDrive/expense_inbox')
LOGFILE_DIR = Path('C:/home_projects/expense_tracker/log/')


def setup_logger(self, log_dir: Path, log_file: Optional[str] = "expense_tracker.log", log_level: int = logging.INFO) -> logging.Logger:

    logger = logging.getLogger("expense_tracker")

    # Configure the logger only if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(log_level)
        full_logname = log_dir / log_file
        
        # Create handlers
        file_handler = logging.FileHandler(full_logname)
        console_handler = logging.StreamHandler()
        
        # Create formatter and add it to handlers
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger