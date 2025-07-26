from .utils import setup_logger
from .utils import DATA_DIR, ARCHIVE_DIR, ONEDRIVE_DIR, LOGFILE_DIR, RESULTS_DIR


# Instantiate logger

logger = setup_logger("expense_tracker", log_dir=LOGFILE_DIR)

#xpose global objects
__all__ = ['DATA_DIR', 'ARCHIVE_DIR', 'ONEDRIVE_DIR', 'LOGFILE_DIR', 'logger', 'RESULTS_DIR']