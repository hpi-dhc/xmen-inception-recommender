from pathlib import Path
from cassis import Cas
import argparse

from ariadne.server import Server
from ariadne.classifier import Classifier
from ariadne.contrib.inception_util import create_span_prediction

from xmen.linkers import default_ensemble
from xmen.linkers import EntityLinker

import warnings
from sklearn.exceptions import InconsistentVersionWarning

from utils import handle_dates

class xMENSNOMEDLinker(Classifier):
    def __init__(self, linker: EntityLinker, top_k = 3):
        self.linker = linker
        self.top_k = top_k        
        super().__init__()
        
    def predict(self, cas: Cas, layer: str, feature: str, project_id: str, document_id: str, user_id: str):
        # For every annotated SNOMED span, predict the SNOMED code        
        annos = [anno for anno in cas.select(layer) if not anno[feature]]
        if not annos:
            return
        preds_ = self.linker.predict_no_context([anno.get_covered_text() for anno in annos])
        preds = handle_dates(preds_)
        # TODO: support re-ranking (see GraSCCo_Evaluation.ipynb)

        for anno, pred in zip(annos, preds):
            for concept in pred['normalized'][0:self.top_k]:                
                sctid = concept['db_id']
                score = concept['score']
                prediction = create_span_prediction(cas, layer, feature, anno.begin, anno.end, f"http://snomed.info/id/{sctid}", score=score)
                cas.add(prediction)     

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('index_base_path', type=Path)
    parser.add_argument('--gpu', action=argparse.BooleanOptionalAction)
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--num_recs', type=int, default=3)
    
    args = parser.parse_args()
    
    # Suppress InconsistentVersionWarning from TF-IDF vectorizer
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
    print("Loading xMEN SNOMED Linker...")
    linker = default_ensemble(args.index_base_path, cuda=args.gpu)

    print("Starting Ariadne server...")
    server = Server()
    server.add_classifier("xmen_snomed", xMENSNOMEDLinker(linker, top_k=args.num_recs))

    server.start(port=args.port)

if __name__ == '__main__':
    run()
