
def unigram_overlap(article_title, term):
    ''' Returns the number of unigrams that overlap between the
    title of an article and a MeSH term.
    
    Assumes article_title and term are strings. '''
    words = term.split()
    overlap = 0
    
    for word in words:
        if word in article_title:
            overlap += 1

    return overlap


def bigram_overlap(article_title, article_abstract, term):
    ''' Returns the number of bigrams that overlap between the
    title and abstract of an article and a MeSH term.
    
    Assumes article_title, article_abstract, and term are all strings. '''
    words = term.split()
    bigrams = zip(words, words[1:])
    overlap = 0

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

    Assumes articles is the main dict, article_neighbors are a tuple of (pmid, score),
    and term is a string. '''
    count = 0
    total_score = 0.0

    for neighbor, score in article_neighbors:
        if "terms" not in articles[neighbor]:
            continue

        if term in articles[neighbor]["terms"]:
            count += 1
            total_score += float(score)

    return count, total_score


def preprocess_terms(terms):
    terms = [item.split("!")[0] for item in terms]
    terms = [term.split("*")[0] for term in terms]
    terms = [term.replace(",", "") for term in terms]

    return terms


def add_articles_from_file(f, articles):
    ''' Reads file f and adds all articles to the articles dict. '''
    for line in f:
        items = line.split('|')

        # Remove newlines
        while '\n' in items:
            items.remove('\n')

        pmid = items[0]
        typ = items[1]

        if pmid not in articles:
            articles[pmid] = dict()

        if typ == 't':
            articles[pmid]["title"] = items[2]
        elif typ == 'a':
            articles[pmid]["abstract"] = items[2]
        elif typ == 'm':
            articles[pmid]["terms"] = preprocess_terms(items[2:])
        else:
            print("Unknown type of information")


def initalize_articles():
    ''' Creates a dict of articles.
    The dict includes the SMALL200 articles and all of the neighbors. '''
    articles = dict()

    # Original articles (to predict)
    with open("paperdat/SMALL200/S200.TiAbMe", 'r') as f:
        add_articles_from_file(f, articles)

    # Neighboring articles
    with open("paperdat/SMALL200/S200_50neighbors.TiAbMe", 'r') as f:
        add_articles_from_file(f, articles)

    return articles


def add_neighbors_to_articles(articles):
    ''' Adds a list of neighboring PMIDs to each of the original articles
    in the articles dict. '''
    with open("paperdat/SMALL200/S200_50neighbors.score", 'r') as f:
        for line in f:
            pmid, neighbor, score = line.split()
            
            if "neighbors" not in articles[pmid]:
                articles[pmid]["neighbors"] = []

            articles[pmid]["neighbors"].append((neighbor, score))


if __name__ == '__main__':
    articles = initalize_articles()
    add_neighbors_to_articles(articles)

    for article, attributes in articles.items():
        # Skip neighboring articles
        if "neighbors" not in attributes:    
            continue

        # Find candidate terms (neighboring articles)
        candidate_terms = []
        for pmid, _ in attributes["neighbors"]:
            if "terms" in articles[pmid]:
                candidate_terms.extend(articles[pmid]["terms"])

        # We don't want duplicate terms
        candidate_terms = set(candidate_terms)

        # Make features
        # Just printing them for now
        print("Article: {}".format(article))
        for term in candidate_terms:
            features = dict()
            features['unigram'] = unigram_overlap(attributes["title"], term)
            features['bigram'] = bigram_overlap(attributes["title"], attributes["abstract"], term)
            neighbor_freq, neighbor_score = neighboring_features(articles, attributes["neighbors"], term)

            features['neighbor_frequency'] = neighbor_freq
            features['neighbor_score'] = neighbor_score

            print("Candidate Term: {}, Features: {}".format(term, features))
        print("\n")


