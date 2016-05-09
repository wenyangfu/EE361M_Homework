"""
Script will populate a dictionary containing all articles in S200.TiAbMe,
in addition to their citations that can be found on PubMed central.
"""

# Built-in python modules
import re
from itertools import islice
from itertools import zip_longest
from collections import UserDict
# Third party modules
""" README: You must install the NLTK Corpus before this script can be run!!!
You can find instructions here: http://www.nltk.org/data.html """
from nltk.corpus import stopwords


# The format of citations.TiAbMe looks like this:
# PMID_of_article|c|num_citations
# -- list of citations for the above article --
# PMID_of_article_2|c|num_citations
# -- list of citations for the above article --

class TextPreprocessor(UserDict):
    """ Loads articles from the training/test set with their citations and
    preprocesses them. """
    # Citations for each article. Key is the PMID of an article.
    # Value is a dict of the format {'cites:', 'title':, 'abstract': 'mesh:'}
    # Where cites is a list of articles that the current article cites,
    # title is the title of an article
    # abstract is the abstract of an article,
    # and mesh is the MeSH terms for an article.
    citations = {}

    data = citations

    cached_stopwords = stopwords.words("English")
    # punctuation and numbers to be removed
    punctuation = re.compile(r'[-.?!,":;()|0-9]')

    def __init__(self, use_cfg=True, article_path='', citation_path='', neighbor_path=''):
        if use_cfg:
            with open('config/preprocessor.cfg') as cfg:
                self.citation_path = cfg.readline().strip(' \n')
                self.article_path = cfg.readline().strip(' \n')
                self.neighbor_path = cfg.readline().strip(' \n')
            self._load_citations()
        else:
            self.citation_path = citation_path
            self.article_path = article_path
            self.neighbor_path = neighbor_path
            self._load_citations()

    def _load_citations(self):
        """
        Load each article and its citations, and store them into a dict.
        We assume that article_path points to a file in the form:
            -- title --
            -- abstract --
            -- mesh terms --
        The citations dict will use each article's PubMed ID as its key,
        and the values within this dict will be:
            'abstract' (str): the abstract of the paper.
            'cites' (list): pubmed IDs that an article cites.
            'mesh' (list): the mesh terms of a paper.
            'title': Title of the paper.
        """
        with open(self.citation_path, 'r') as f, \
                open(self.article_path, 'r') as f2, \
                open(self.neighbor_path, 'r') as f3:
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
                elif article_info == [''] or article_info == []:
                    break
                else:
                    raise Exception('citations file was formatted '
                                    'incorrectly.\n'
                                    'Expected article metadata with citation'
                                    'count or newline character.')

            # Add the original article information
            for article in self.grouper(f2, 3):  # Citations are grouped in 3
                self._add_article(article)

            self._add_neighbor_articles(f3)

    def preprocess(self):
        """ Apply all steps of the preprocessing pipeline. """
        self.regularize()
        self.tokenize()

    def tokenize(self):
        """ Separate all phrases in each article's abstract
        and title into lists of words, with the stopwords removed. """
        self.citations = {
            k: {'cites': v['cites'],
                'title': self._tokenize(v['title']),
                'abstract': self._tokenize(v['abstract']),
                'mesh': v['mesh']
                } for k, v in self.citations.items()
        }

    @classmethod
    def _tokenize(cls, text):
        """ Remove all stopwords from a text and tokenize it.
        Returns a list of words (str). """
        # Got help from:
        # https://stackoverflow.com/questions/19560498/faster-way-to-remove-stop-words-in-python
        return [word for word in text.split()
                if word not in cls.cached_stopwords]

    def regularize(self):
        """ Remove all punctuation and digits from abstracts and titles
        of every article/citation. """
        for pmid in self.citations:
            title = self.citations[pmid]['title']
            self.citations[pmid]['title'] = self._regularize(title)
            abstract = self.citations[pmid]['abstract']
            self.citations[pmid]['abstract'] = self._regularize(abstract)
            # TODO: Not sure how to handle MeSH terms for regularization

    @classmethod
    def _regularize(cls, text):
        """ Remove all punctuation and digits from a text. """
        # Got help from here:
        # https://stackoverflow.com/questions/5512765/removing-punctuation-numbers-from-text-problem
        # print(text)
        return cls.punctuation.sub("", text)

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
            # The order we saved our data is slightly inconsistent
            # with S200.TiAbMe
            # We did "orig_id", abstract, title, mesh
            # while S200 did title, abstract, mesh
            # The change in code reflects that.

            _, abstract, title, mesh = [data.strip(' \n').split('|')[2:]
                                        for data in citation]
            mesh_terms = { 
                m.partition('!')[0].lower().strip().rstrip('*') 
                for m in mesh 
            } - { '' } # Remove empty term

            # Note: The 2: slicing makes title, abstract, and mesh list objects
            # Had I only indexed into 2, then they would've all been str objs.
            # I casted them to strings so they're easier to preprocess later.
            title, abstract = ''.join(title), ''.join(abstract)

            if cite_pmid not in self.citations:  # Add a new citation.
                self.citations[cite_pmid] = {
                    'title': title, 'abstract': abstract,
                    'mesh': list(mesh_terms), 'cites': []
                }
            else:  # top-level paper is cited by another top-level paper
                self.citations[cite_pmid]['title'] = title
                self.citations[cite_pmid]['abstract'] = abstract
                self.citations[cite_pmid]['mesh'] = list(mesh_terms)

        # Connect a top-level paper to its citations.
        if pmid not in self.citations:
            self.citations[pmid] = {'cites': cites}
        else:
            self.citations[pmid]['cites'] = cites

    def _add_article(self, article):
        """ Insert article metadata into the citations dictionary. """
        pmid = int(article[0].strip(' \n').split('|')[0])
        # Note: The 2: slicing makes title, abstract, and mesh list objects
        # Had I only indexed into 2, then they would've all been str objs.
        title, abstract, mesh = [data.strip(' \n').split('|')[2:]
                                 for data in article]


        mesh_terms = { 
            m.partition('!')[0].lower().strip().rstrip('*') 
            for m in mesh 
        } - { '' } # Remove empty term

        self.citations[pmid]['title'] = ''.join(title)
        self.citations[pmid]['abstract'] = ''.join(abstract)
        self.citations[pmid]['mesh'] = list(mesh_terms)

    def _add_neighbor_articles(self, f):
        """ Insert neighbor article metadata into citations dictionary. """
        # Since not all of the neighboring documents have a title, abstract,
        # and terms, we have to go line by line and add information as we find it.
        for line in f:
            items = line.strip(' \n').split('|')
            pmid = items[0]
            typ = items[1]

            # Add a new entry if it doesn't exist yet.
            if pmid not in self.citations:
                self.citations[pmid] = {
                    'title': '', 'abstract': '',
                    'mesh': [], 'cites': []
                }

            if typ == 't':
                self.citations[pmid]['title'] = items[2]
            elif typ == 'a':
                self.citations[pmid]['abstract'] = items[2]
            elif typ == 'm':
                mesh = items[2:]
                mesh_terms = { 
                    m.partition('!')[0].lower().strip().rstrip('*') 
                    for m in mesh 
                } - { '' } # Remove empty term

                self.citations[pmid]['mesh'] = list(mesh_terms)
            else:
                raise Exception('Unknown article information found when parsing neighbors.')

    def test_output(self):
        first_key = list(self.citations.keys())[32]
        print(self.citations[first_key])


def main():
    proc = TextPreprocessor()
    proc.test_output()
    proc.preprocess()
    proc.test_output()

if __name__ == '__main__':
    main()
