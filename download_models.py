from xmen.linkers.model_wrapper import Model_Wrapper
from xmen.linkers import SapBERTLinker
from transformers import logging as tf_logging
import logging

logging.basicConfig(level=logging.INFO)
tf_logging.set_verbosity_info()

def download_models():
    """ Downloads the Hugging Face models required for the project. """
    Model_Wrapper().load_model(SapBERTLinker.CROSS_LINGUAL, use_cuda=False)

if __name__ == '__main__':

    download_models()