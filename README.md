# Cross-lingual Medical Entity Linking Recommenders for INCEpTION

Simple integration of pre-configured [xMEN](https://github.com/hpi-dhc/xmen) pipelines as recommenders for (biomedical) entity linking in [INCePTION](https://github.com/inception-project/inception).

## German SNOMED CT Linking

![External Recommender](assets/recommender.png)

- Prepare xMEN KB and index:
    - `git clone https://github.com/hpi-dhc/xmen`
    - `xmen dict snomed_german.yaml --code xmen/examples/dicts/umls_source.py`
    - `xmen index snomed_german.yaml --all --overwrite`
- **OR**: download pre-computed index and put contents into `xmen_index`:
    - 

- Prepare xMEN KB and index as described here: https://github.com/hpi-dhc/xmen/blob/main/examples/03_SNOMED_Linking_German.ipynb
- Start the Ariadne Server (on `http://localhost:5000/xmen_snomed`):
    - `python run_snomed_german_recommender.py ./xmen_index`
