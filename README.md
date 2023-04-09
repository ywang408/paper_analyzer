# paper_analyzer

Final project of BIA667/660, which is textual analysis on academic papers.

## Scrape data

To query the metadata of papers in an area, run the following command:

```python
import paper_analyzer as pa

# chagne "all:electron" to your query
search = pa.Search(query="all:electron", start=0, max_results=10)

for paper in search.results():
    print(paper)
    print("")
```

It can be converted to a pandas dataframe:

```python
import paper_analyzer as pa

search = pa.Search(query="all:electron", start=0, max_results=10)
    
df = search.to_dataframe()
print(df.head())
```
