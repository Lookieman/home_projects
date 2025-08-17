from pipeline import Path
from typing import Dict, list, Optional
from datetime import datetime

from .rag_system import RAGSystem
from .model_manager import ModelManager
from .utils import logger, init_env
#from.evaluator import CombinedEvaluator

class RAGPipeline:
    def __init__(self):

        #initialize component
        self.env = init_env()
        self.rag_system = None
        self.model_manager = None
        #self.evaluator = None
        self.ground_truth = {}
        self.results = {}
        self.config = {}
        self.models_to_eval = {}
        

    def setup_rag_system(self):
        
        if self.model_manager is None:
            self.model_manager = ModelManager
        
        rag_check =  self.model_manager.get_rag_system()

        if rag_check is None:
                result = self.model_manager.setup_rag_system(papers_dir=self.env['papers_dir'])

        if result:
                logger.info (f"RAG system succesfully initialized")
                self.rag_system = self.model_manager.get_rag_system()     
        else: 
                logger.error(f"Error setting up rag system, Please check log for further info on error")

    def evaluate_model(self, model_key: str) -> Dict:
        pass

    def run_full_evaluation(self, model_keys: List[str])->Dict:
        pass

    def save_results(self, output_dir: Path):
        pass

