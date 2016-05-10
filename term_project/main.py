import sys
import argparse
import logging

from text_preprocessor import TextPreprocessor

from feature_extraction import features as mesh_features

def get_candidates(citations, pmid):
    # Find candidate terms (neighboring articles)
    candidate_terms = set()

    attributes = citations[pmid]
    
    for pmid, _ in attributes['neighbors']:
        if pmid in citations:
            candidate_terms |= set(citations[pmid]["mesh"])

    for pmid in attributes['cites']:
        if pmid in citations:
            candidate_terms |= set(citations[pmid]["mesh"])

    return candidate_terms

def engineer_features(citations, pmid):
    data = {}
    for candidate in candidates:
        data[candidate] = {
            name: func(citations, pmid, candidate)
            for name, func in mesh_features.items()
        }
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser('Ranker for MeSH terms')

    parser.add_argument('--citations-file', '-c', type=str, default='')
    parser.add_argument('--num-mesh-terms', '-k', type=int)
    parser.add_argument('-v', '--verbosity', action='count', default=0)
    args = parser.parse_args()
   
    if(args.verbosity == 0):
        level = logging.ERROR
    elif(args.verbosity == 1):
        level = logging.WARN
    elif(args.verbosity == 2):
        level = logging.INFO
    elif(args.verbosity >= 3):
        level = logging.DEBUG

    logging.basicConfig(
        format='[%(filename)s] %(levelname)s: %(message)s', 
        level=level,
    )


    logging.info('Loading dataset')
    if args.citations_file:
        logging.debug('Loading from '+args.citations_file)
        
        logging.error('Not implemented yet!')
        sys.exit(1) 

        citations = {}
    else:
        logging.debug('Loading from raw sources')
        citations = TextPreprocessor()


    for pmid in citations.articles:
        logging.debug('Ranking MeSH terms for %s' % pmid)
        candidates = get_candidates(citations, pmid)
        logging.debug('Building features for %d' % pmid)
        candidates = get_candidates(citations, pmid)
        features = engineer_features(citations, pmid) 
