import paper_analyzer as pa

search = pa.Search(query="all:electron", start=0, max_results=10)

for paper in search.results():
    print(paper)
    print("")