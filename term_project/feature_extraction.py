
# Unigram/bigram feature extraction
def unigram_overlap(article_title, term):
    words = term.split()
    overlap = 0
    
    for word in words:
        if word in article_title:
            overlap += 1

    return overlap


def bigram_overlap(article_title, article_abstract, term):
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

# Reading in articles from file
def add_articles_from_file(f, articles):
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
            articles[pmid]["terms"] = items[2:]
        else:
            print("Unknown type of information")


def initalize_articles():
    articles = dict()

    # Original articles
    with open("paperdat/SMALL200/S200.TiAbMe", 'r') as f:
        add_articles_from_file(f, articles)

    with open("paperdat/SMALL200/S200_50neighbors.TiAbMe", 'r') as f:
        add_articles_from_file(f, articles)

    return articles

def add_neighbors_to_articles(articles):
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

        candidate_terms = []

        for pmid, _ in attributes["neighbors"]:
            if "terms" in articles[pmid]:
                candidate_terms.extend(articles[pmid]["terms"])

        #print(candidate_terms)
        print("Article: {}".format(article))
        for term in candidate_terms:
            features = dict()
            features['unigram'] = unigram_overlap(attributes["title"], term)
            features['bigram'] = bigram_overlap(attributes["title"], attributes["abstract"], term)

            print("Candidate Term: {}, Features: {}".format(term, features))
        print("\n")


