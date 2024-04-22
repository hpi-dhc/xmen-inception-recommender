from pathlib import Path
from cassis import Cas
import argparse

from ariadne.server import Server
from ariadne.classifier import Classifier
from ariadne.contrib.inception_util import create_span_prediction

from xmen.linkers import default_ensemble
from xmen.linkers import EntityLinker

class xMENSNOMEDLinker(Classifier):
    def __init__(self, linker: EntityLinker, top_k = 10):
        self.last_cas = None
        self.linker = linker
        self.top_k = top_k        
        super().__init__()
        
    def predict(self, cas: Cas, layer: str, feature: str, project_id: str, document_id: str, user_id: str):
        self.last_cas = cas
        # For every annotated SNOMED span, predict the SNOMED code
        
        annos = cas.select(layer)
        preds = self.linker.predict_no_context([anno.get_covered_text() for anno in annos])

        for anno, pred in zip(annos, preds):
            for concept in pred['normalized'][0:self.top_k]:
                sctid = concept['db_id']
                prediction = create_span_prediction(cas, layer, feature, anno.begin, anno.end, f"http://snomed.info/id/{sctid}", score=concept['score'])
                cas.add(prediction)     

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('index_base_path', type=Path)
    parser.add_argument('--gpu', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    index_base_path = args.index_base_path
    linker = default_ensemble(index_base_path, cuda=args.gpu)
  
    recommender = xMENSNOMEDLinker(linker)

    server = Server()
    server.add_classifier("xmen_snomed", recommender)

    server.start()

if __name__ == '__main__':
    run()