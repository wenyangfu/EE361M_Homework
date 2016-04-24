import sys

from citation_grabber import write_citations

with open('citations.TiAbMe', 'a+') as citations_file:
    with open('paperdat/SMALL200/S200.pmids') as pubmed_ids_file:
        for pubmed_id in pubmed_ids_file:
            to_fetch = pubmed_id.strip()
            sys.stdout.write("%s\r" % to_fetch)
            sys.stdout.flush()
            write_citations(citations_file, to_fetch)
