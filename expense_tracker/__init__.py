from .utils import setup_logger
from .utils import DATA_DIR, ARCHIVE_DIR, GDRIVE_DIR, LOGFILE_DIR, RESULTS_DIR

# Instantiate logger
logger = setup_logger(LOGFILE_DIR, "expense_tracker.log")

#xpose global objects
__all__ = ['DATA_DIR', 'ARCHIVE_DIR', 'GDRIVE_DIR', 'LOGFILE_DIR', 'logger', 'RESULTS_DIR']