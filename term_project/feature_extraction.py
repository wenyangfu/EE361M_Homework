

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
        print(gram)

        if gram in article_title:
            overlap += 1

        if gram in article_abstract:
            overlap += 1

    return overlap


def initalize_articles():
    articles = dict()

    with open("paperdat/SMALL200/S200.TiAbMe", 'r') as f:
        for line in f:
            items = line.split('|')
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

    return articles

def add_neighbors_to_articles(articles):
    with open("paperdat/SMALL200/S200_50neighbors.score", 'r') as f:
        for line in f:
            pmid, neighbor, score = line.split()
            
            if "neighbors" not in articles[pmid]:
                articles[pmid]["neighbors"] = []

            articles[pmid]["neighbors"].append(neighbor)

def terms_for_article(pmid):
    # Get the terms from the neighbors


    # Get the terms from the citations
    return None

if __name__ == '__main__':
    articles = initalize_articles()
    add_neighbors_to_articles(articles)

    print(articles)
