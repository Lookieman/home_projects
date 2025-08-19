from pipeline import Path
from typing import Dict, List, Optional, Any
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
        

    def setup_components(self)->bool:
        
        setup_complete = None
        #Setup ModelManage
        if self.model_manager is None:
            self.model_manager = ModelManager
        
        #Setup RAG system
        rag_check =  self.model_manager.get_rag_system()

        if rag_check is None:
                result = self.model_manager.setup_rag_system(papers_dir=self.env['papers_dir'])

        #Load ground truth data
        ground_truth_check = self.load_ground_truth_data()

        #Validate all components ready
        if result:
                logger.info (f"RAG system succesfully initialized")
                self.rag_system = self.model_manager.get_rag_system()
        else: 
                logger.error(f"Error setting up rag system, Please check log for further info on error")
        return setup_complete
    
        if ground_truth_check:
            logger.info (f"ground truth succesfully loaded")
             

    def load_ground_truth_data(self) -> bool:
         """
         Load QA pairs and retrieve summary from JSON from reference_dir
         """
        #Retrieve QA pairs from reference_dir
        #Retrieve summary from reference_dir
        pass
    
    def select_models_for_eval(self, model_key: List[str]) -> bool:
        pass

    def run_rag_eval(self)->Dict[str, Any]:
        pass

    def run_eval_metric(self, rag_results: Dict[str, Any])-> Dict[str, Any]:
         pass
    def save_all_results(self, rag_results: Dict, eval_results: Dict, timestamp: str)->bool:
        pass

    def run_full_pipeline(self)-> Dict[str, Any]:
         pass
