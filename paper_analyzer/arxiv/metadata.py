import requests
from bs4 import BeautifulSoup
import pandas as pd


class Paper:
    def __init__(self, *args, **kwargs) -> None:
        self.paper_id = kwargs.get('paper_id')
        self.updated = kwargs.get('updated')
        self.published = kwargs.get('published')
        self.title = kwargs.get('title')
        self.authors = kwargs.get('authors')
        self.summary = kwargs.get('summary')
        self.comment = kwargs.get('comment')
        self.link = kwargs.get('link')
        self.pdf_link = kwargs.get('pdf_link')
        self.term = kwargs.get('term')
        self.metadata = self.to_dict()

    def __repr__(self) -> str:
        return f'Paper({self.paper_id})'

    def __str__(self) -> str:
        return (f"title: {self.title}\n"
                f"authors: {self.authors}\n"
                f"link: {self.link}\n"
                f"pdf_link: {self.pdf_link}\n"
                f"term: {self.term}\n")

    def to_dict(self) -> dict:
        return {
            'paper_id': self.paper_id,
            'updated': self.updated,
            'published': self.published,
            'title': self.title,
            'authors': self.authors,
            'summary': self.summary,
            'comment': self.comment,
            'link': self.link,
            'pdf_link': self.pdf_link,
            'term': self.term
        }

    def download_pdf(self, path="./data"):
        # if not os.path.exists(path):
        #     os.mkdir(path)
        pass


class Search:
    def __init__(self, query: str = None, id_list: list = None, start: int = 0,
                 max_results: int = 10, sort_by: str = "lastUpdatedDate", sort_order: str = 'descending') -> None:
        self.query = query
        self.id_list = id_list
        self.start = start
        self.max_results = max_results
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.url = self._url()  # query url
        self.response = self._check_response()  # response from query

    def __str__(self) -> str:
        return f"query at {self.query_date} for {self.query}/{self.id_list}"

    def _url(self) -> str:
        base_url = "http://export.arxiv.org/api/query?"
        if self.query:
            query = f"search_query={self.query}"
        elif self.id_list:
            query = f"id_list={','.join(self.id_list)}"
        else:
            raise ValueError("Must provide query or id_list")

        url = (f"{base_url}"
               f"{query}&start={self.start}"
               f"&max_results={self.max_results}"
               f"&sortBy={self.sort_by}"
               f"&sortOrder={self.sort_order}")
        return url

    def _check_response(self) -> None:
        url = self._url()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'xml')
        if soup.find("entry").find("title", recursive=False).text == "Error":
            print(url)
            raise ValueError("Invalid query or id_list")
        else:
            return soup

    def _parse_xml(self, xml) -> list:
        paper_id = xml.find('id').text
        updated = xml.find('updated').text
        published = xml.find('published').text
        title = xml.find('title').text
        authors = [author.find('name').text for author in xml.find_all('author')]
        summary = xml.find('summary').text
        comment = xml.find('arxiv:comment').text if xml.find(
            'arxiv:comment') else None
        link = xml.find("link", attrs={"rel": "alternate"})['href']
        pdf_link = xml.find("link", attrs={"title": "pdf"})['href']
        term = xml.find('arxiv:primary_category')['term']
        return Paper(paper_id=paper_id, updated=updated, published=published, title=title, authors=authors,
                     summary=summary, comment=comment, link=link, pdf_link=pdf_link, term=term)

    def results(self) -> list:
        soup = self.response
        entries = soup.find_all('entry')
        papers = []
        for entry in entries:
            paper = self._parse_xml(entry)
            papers.append(paper)
        return papers

    def to_dataframe(self) -> pd.DataFrame:
        papers = self.results()
        df = pd.DataFrame([paper.to_dict() for paper in papers])
        return df
