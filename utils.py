import dateparser

GENERIC_DATE_CONCEPT = {'db_name': 'SNOMED CT', 'db_id': '258695005', 'score' : 1.0, 'predicted_by' : ['rule-based']}

def to_map_fn(fn):
    def map_fn(doc):
        entities = fn(doc['entities'])
        return { 'entities' : entities }
    return map_fn
        
def handle_dates(entities):
    for e in entities:
        if dateparser.parse(e['text'][0]):
            e['normalized'].insert(0, GENERIC_DATE_CONCEPT)
    return entities