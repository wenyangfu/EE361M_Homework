"""
Script will populate a dictionary containing all articles in S200.TiAbMe,
in addition to their citations that can be found on PubMed central.
"""

# Built-in python modules
import re
from itertools import islice
from itertools import zip_longest
# Third party modules
# from nltk.corpus import stopwords


# The format of citations.TiAbMe looks like this:
# PMID_of_article|c|num_citations
# -- list of citations for the above article --
# PMID_of_article_2|c|num_citations
# -- list of citations for the above article --

class TextPreprocessor(object):
    """ Loads multiple datasets and
    preprocesses them. """
    # Citations for each article. Key is the PMID of an article.
    # Value is a dict of the format {'cites:', 'title':, 'abstract': 'mesh:'}
    # Where cites is a list of articles that the current article cites,
    # title is the title of an article
    # abstract is the abstract of an article,
    # and mesh is the MeSH terms for an article.
    citations = {}
    # cached_stopwords = stopwords.words("English")
    # punctuation and numbers to be removed
    punctuation = re.compile(r'[-.?!,":;()|0-9]')

    def __init__(self, use_cfg=True, article_path='', citation_path=''):
        if use_cfg:
            with open('config/preprocessor.cfg') as cfg:
                self.citation_path = cfg.readline().strip(' \n')
                self.article_path = cfg.readline().strip(' \n')
            self._load_citations()
        else:
            self.citation_path = citation_path
            self.article_path = article_path
            self._load_citations()

    def _load_citations(self):
        """
        Load each article and its citations, and store them into a dict.
        The citations dict will use each article's PubMed ID as its key,
        and the values within this dict will be:
            'abstract' (str): the abstract of the paper.
            'cites' (list): pubmed IDs that an article cites.
            'mesh' (list): the mesh terms of a paper.
            'title': Title of the paper.
        """
        with open(self.citation_path, 'r') as f, \
                open(self.article_path, 'r') as f2:
            while True:
                article_info = f.readline().strip(' \n').split('|')
                # Read the citations for a given pmid, and store into dict.
                if self.is_original_article(article_info):
                    pmid = int(article_info[0])
                    # Group citations together.
                    # https://docs.python.org/3/library/itertools.html#itertools.islice
                    num_citations = int(article_info[2]) * 4
                    related_citations = list(islice(f, num_citations))
                    self._add_citations(pmid, related_citations)
                    # if pmid not in self.citations:
                    #     self.citations[pmid] = {
                    #         'cites': self.add_citations(related_citations)
                    #     }
                    # else:
                    #     self.citations[pmid]['cites'] = self.add_citations(
                    #         related_citations)
                elif article_info == [''] or article_info == []:
                    break
                else:
                    raise Exception('citations file was formatted '
                                    'incorrectly.\n'
                                    'Expected article metadata with citation'
                                    'count or newline character.')

            for article in self.grouper(f2, 3):  # Citations are grouped in 3
                self._add_article(article)

    @staticmethod
    def is_original_article(article_info):
        """ Checks if a line of text from a citations file
        is a valid citation metadata block. """
        if len(article_info) < 3:
            return False
        else:
            return article_info[1].lower() == 'c'

    @staticmethod
    def grouper(iterable, n, fillvalue=None):
        "Helper method to collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    def _add_citations(self, pmid, related_citations):
        """ Insert each citation metadata into the citations dictionary,
            and also add the  for a given article. """
        # Got some help from here:
        # https://stackoverflow.com/questions/6335839/python-how-to-read-n-number-of-lines-at-a-time#
        cites = []  # A given paper's citations.
        for citation in self.grouper(related_citations, 4):
            # PudMed ID of a citation
            cite_pmid = int(citation[0].strip(' \n').split('|')[0])
            cites.append(cite_pmid)
            _, title, abstract, mesh = map(
                lambda x: x.strip(' \n').split('|')[2:], citation)
            if cite_pmid not in self.citations:  # Insert a citation into the dict.
                self.citations[cite_pmid] = {
                    'title': title, 'abstract': abstract,
                    'mesh': mesh, 'cites': []
                }
            # Case where a top-level article is cited by another top-level
            # article.
            else:
                self.citations[cite_pmid]['title'] = title
                self.citations[cite_pmid]['abstract'] = abstract
                self.citations[cite_pmid]['mesh'] = mesh

        # Connect a paper to its citations.
        if pmid not in self.citations:
            self.citations[pmid] = {'cites': cites}
        else:
            self.citations[pmid]['cites'] = cites


    def _add_article(self, article):
        """ Insert article metadata into the citations dictionary. """
        pmid = int(article[0].strip(' \n').split('|')[0])
        title, abstract, mesh = map(
            lambda x: x.strip(' \n').split('|')[2:], article)
        self.citations[pmid]['title'] = title
        self.citations[pmid]['abstract'] = abstract
        self.citations[pmid]['mesh'] = mesh

    def test_output(self):
        first_key = list(self.citations.keys())[0]
        print(self.citations[first_key])

def main():
    proc = TextPreprocessor()
    proc.test_output()
        


if __name__ == '__main__':
    main()
