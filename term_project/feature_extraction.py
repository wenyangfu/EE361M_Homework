import numpy as np

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel

from text_preprocessor import TextPreprocessor

def unigram_overlap(citations, pmid, mesh_term):
    ''' Returns the number of unigrams that overlap between the
    title of an article and a MeSH term.

    Assumes article_title and term are strings. '''
    
    words = mesh_term.split()
    overlap = 0

    article_title = citations[pmid]['title']

    for word in words:
        if word in article_title:
            overlap += 1

    return overlap

def bigram_overlap(citations, pmid, mesh_term):
    ''' Returns the number of bigrams that overlap between the
    title and abstract of an article and a MeSH term.

    Assumes article_title, article_abstract, and term are all strings. '''

    words = mesh_term.split()
    bigrams = zip(words, words[1:])
    overlap = 0

    article_title = citations[pmid]['title']
    article_abstract = citations[pmid]['abstract']

    for bigram in bigrams:
        gram = bigram[0] + " " + bigram[1]

        if gram in article_title:
            overlap += 1

        if gram in article_abstract:
            overlap += 1

    return overlap

def neighboring_features(articles, article_neighbors, term):
    ''' Returns two features. The first is the count of how many times
    the given MeSH term appears as a term in the article_neighbors. The
    second is the total neighborosity score of each article_neighbors that
    the term appears in.

    Assumes articles is the main dict, article_neighbors are
    a tuple of (pmid, score), and term is a string. '''
    count = 0
    total_score = 0.0

    for neighbor, score in article_neighbors:
        if neighbor not in articles:
            continue

        if term in articles[neighbor]["mesh"]:
            count += 1
            total_score += float(score)

    return count, total_score


def citation_count(articles, article_citations, term):
    ''' Count the number of citations for each article. '''
    count = 0

    for citation in article_citations:
        if term in articles[citation]['mesh']:
            count += 1

    return count


def get_tf_idf_model(citations=None):
    if citations is None:
        citations = TextPreprocessor()
        citations.preprocess()

    documents = [
        citation['title'] + ' \n' + citation['abstract']
        for citation in list(citations.values())
    ]
    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2))
    bigrams = bigram_vectorizer.fit_transform(documents)

    tfidf = TfidfTransformer().fit_transform(bigrams)

    return citations, bigram_vectorizer, tfidf


def get_most_similar_documents(tfidf_matrix, vectorizer, query):
    query_tfidf = TfidfTransformer().fit_transform(
        vectorizer.transform([query])
    )
    document_similarities = linear_kernel(query_tfidf, tfidf_matrix).flatten()
    return document_similarities.argsort()[::-1]


if __name__ == '__main__':
    citations = TextPreprocessor()
    citations.preprocess()

    # c, v, t = get_tf_idf_model(citations)
    # r = get_most_similar_documents(t, v, 'williams syndrome')
    # import ipdb; ipdb.set_trace()
    
    # from pprint import pprint
    # for index in r[:10]:
    #     pprint(c[index]['title'])

    print(len(citations))
    input("Hit enter to continue...")

    count = 0
    skipped_count = 0
    for article, attributes in citations.items():
        # Skip neighboring articles
        if len(attributes['neighbors']) == 0:
            skipped_count += 1
            continue

        # Find candidate terms (neighboring articles)
        candidate_terms = []
        for pmid, _ in attributes["neighbors"]:
            if pmid in citations:
                candidate_terms.extend(citations[pmid]["mesh"])
        for pmid in attributes['cites']:
            if pmid in citations:
                candidate_terms.extend(citations[pmid]['mesh'])

        # We don't want duplicate terms
        candidate_terms = set(candidate_terms)

        # Make features
        # Just printing them for now
        print("Article: {}".format(article))
        count += 1
        for term in candidate_terms:
            features = dict()
            features['unigram'] = unigram_overlap(citations, article, term)
            features['bigram'] = bigram_overlap(citations, article, term)
            features['citation_frequency'] = citation_count(
                citations, attributes['cites'], term)

            neighbor_freq, neighbor_score = neighboring_features(
                citations, attributes["neighbors"], term)
            features['neighbor_frequency'] = neighbor_freq
            features['neighbor_score'] = neighbor_score

            print("Candidate Term: {}, Features: {}".format(term, features))
        print("\n")

    print('Count: {}'.format(count))
    print('Skipped Count: {}'.format(skipped_count))
