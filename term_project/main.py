import sys
import argparse
import logging

import numpy as np

from text_preprocessor import TextPreprocessor

from feature_extraction import features as mesh_features
from feature_extraction import get_target
from listnet import ListNet


def get_candidates(citations, pmid):
    # Find candidate mesh terms (neighboring articles)
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
    candidates = get_candidates(citations, pmid)
    data = [
        np.asarray([func(citations, pmid, candidate)
                    for func in mesh_features])
        for candidate in candidates
    ]
    return data


def generate_targets(citations, pmid):
    candidates = get_candidates(citations, pmid)
    targets = np.asarray([get_target(citations, pmid, candidate)
                          for candidate in candidates])
    return targets

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
        logging.debug('Loading from ' + args.citations_file)

        logging.error('Not implemented yet!')
        sys.exit(1)

        citations = {}
    else:
        logging.debug('Loading from raw sources')
        citations = TextPreprocessor()

    metadata = {
        'input_size': len(citations.articles),
        'scores': [1]
    }
    logging.debug(
        'Number of training examples: {}'.format(metadata['input_size']))

    ranker = ListNet(n_stages=1, hidden_size=6)
    ranker.initialize_learner(metadata)
    logging.info('Train ListNet')

    ''' Train ListNet:
    candidates - is a list of feature vectors (ndarray)
    targets - is a list of relevance scores - whether or not
    the candidate MeSH term is a correct choice (0 or 1)
    query - is the pmid of the current article.
    '''
    for pmid in citations.articles:
        logging.debug('Ranking MeSH terms for %s' % pmid)
        candidates = get_candidates(citations, pmid)
        logging.debug('Building features for %d' % pmid)
        features = engineer_features(citations, pmid)
        targets = generate_targets(citations, pmid)
        training_example = [features, targets, pmid]
        logging.debug(
            'Number of MeSH terms associated with current article!?: {}'.format(len(features)))
        
        # ranker.update_learner(training_example)
        # logging.debug('Features for current article: {}'.format(features))
