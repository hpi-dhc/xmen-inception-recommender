# Cross-lingual Medical Entity Linking Recommenders for INCEpTION

Simple integration of pre-configured [xMEN](https://github.com/hpi-dhc/xmen) pipelines as recommenders for (biomedical) entity linking in [INCEpTION](https://inception-project.github.io/example-projects/xmen/).

![External Recommender](assets/recommender.png)

## German SNOMED CT Quickstart (with Docker)

- Download pre-computed xMEN index for SNOMED CT and extract contents into `xmen_index`:
    - [HPI Nextcloud Link](https://nextcloud.hpi.de/s/LQM7s5oWGnoHRJ6) (password: name of this repository)

- `docker run -m=12g -p 5000:5000 -v "$(pwd)"/xmen_index/index:/index/ ghcr.io/hpi-dhc/xmen-inception-recommender:main`

## Create xMEN KB and Index from Scratch

- Adapt `snomed_german.yaml` as needed
- Create KB and indices (takes about 1 hour with a GPU)
    - `git clone https://github.com/hpi-dhc/xmen`
    - `xmen dict snomed_german.yaml --code xmen/examples/dicts/umls_source.py`
    - `xmen index snomed_german.yaml --all --overwrite`

## Running the Recommender without Docker

### Install dependencies

- `pip install -r requirements.txt` (see [here](https://github.com/hpi-dhc/xmen/issues/37) for known issues during installation of `xmen`)

### Run the recommender

- Start the Ariadne Server (on `http://localhost:5000/xmen_snomed`):
    - `python run_snomed_german_recommender.py ./xmen_index/index`
