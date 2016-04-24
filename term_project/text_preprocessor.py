# Built-in python modules
from itertools import islice
from itertools import zip_longest
# Third party modules
import nltk

# Citations for each article. Key is the PMID of an article.
# Value is a dict of the format {'cites:', 'title':, 'abstract': 'mesh:'}
# Where cites is a list of articles that the current article cites,
# title is the title of an article
# abstract is the abstract of an article,
# and mesh is the MeSH terms for an article.
citations = {}


# The format of citations.TiAbMe looks like this:
# PMID_of_article|c|num_citations
# -- list of citations for the above article --
# PMID_of_article_2|c|num_citations
# -- list of citations for the above article --


def is_original_article(article_info):
    """ Checks if a line of text from citations.TiAbMe
    is a valid citation. """
    if len(article_info) < 3:
        return False
    else:
        return article_info[1].lower() == 'c'


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def process_citations(related_citations):
    """ Return a list of citation IDs given a list of citations.
    Also insert each citation into the citations dictionary. """
    global citations
    # Got some help from here:
    # https://stackoverflow.com/questions/6335839/python-how-to-read-n-number-of-lines-at-a-time#
    cites = []  # Sources that a research paper cites.
    # Group data for each citation together.
    # https://docs.python.org/3/library/itertools.html#itertools.islice
    for citation in grouper(related_citations, 4):
        # PudMed ID of a research paper
        pmid = int(citation[0].strip(' \n').split('|')[0])
        cites.append(pmid)
        _, title, abstract, mesh = map(
            lambda x: x.strip(' \n').split('|')[2:], citation)
        if pmid not in citations:  # Insert a citation into the dict.
            citations[pmid] = {
                'title': title, 'abstract': abstract, 'mesh': mesh, 'cites': []
            }
        # Case where a top-level article is cited by another top-level article.
        else:
            citations[pmid]['title'] = title
            citations[pmid]['abstract'] = abstract
            citations[pmid]['mesh'] = mesh
    return cites


def main():
    global citations
    with open('ourdat/citations_small200.TiAbMe', 'r') as f, \
            open('paperdat/SMALL200/S200.TiAbMe') as f2:
        while True:
            article_info = f.readline().strip(' \n').split('|')
            # Read the citations for a given pmid, and store into dict.
            if is_original_article(article_info):
                pmid = int(article_info[0])
                num_citations = int(article_info[2]) * 4
                related_citations = list(islice(f, num_citations))
                if pmid not in citations:
                    citations[pmid] = {
                        'cites': process_citations(related_citations)
                    }
                else:
                    citations[pmid]['cites'] = process_citations(
                        related_citations)
            elif article_info == [''] or article_info == []:
                break
            else:
                raise Exception('citations file was formatted incorrectly.\n'
                                'Expected article metadata with citation count'
                                ' or newline character.')
        for citation in grouper(f2, 3):  # Citations are grouped in 3
            pmid = int(citation[0].strip(' \n').split('|')[0])
            title, abstract, mesh = map(
                lambda x: x.strip(' \n').split('|')[2:], citation)
            citations[pmid]['title'] = title
            citations[pmid]['abstract'] = abstract
            citations[pmid]['mesh'] = mesh
    print(citations[12386918])
if __name__ == '__main__':
    main()
