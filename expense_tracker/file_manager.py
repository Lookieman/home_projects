
import shutil
from utils import DATA_DIR, ARCHIVE_DIR, GDRIVE_DIR, logger
from pathlib import Path

class ExpenseFileManager:

    def __init__(self):

        #set folder path
        self.archive_dir = ARCHIVE_DIR
        self.data_path = DATA_DIR
        self.gdrive_path = GDRIVE_DIR
        
                
        #initialize logging
        self.logger = logger

    def move_files_from_gdrive(self):
        """
        Find images in gdrive folder in gdrive folder and move it to 
        """

        #check if gdrive folder exists
        if self.gdrive_path.is_dir():
            #Get list of image files (*.png or *.jpg)
            image_files = list(self.gdrive_path.glob('*.jpg')) + list(self.gdrive_path.glob('*.png'))

        #for each file, move file to inbox_path
        for image in image_files:
            dest_path = self.data_path / image.name
            self.logger.info(f"moved {image.name} to {dest_path}")
            try:
                shutil.move(image, dest_path)
            except Exception as e:
                self.logger.error(f"failed to move {image.name}: {e}")

    def get_unprocessed_file(self)->list:
        """
        get all jpg and png files in the data_path. Returns list of all jpg/png files
        """
        unprocessed_file = list(self.data_path.glob('*.jpg')) + list(self.data_path.glob('*.png'))

        return unprocessed_file

