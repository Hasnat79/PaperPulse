import arxiv
from datetime import datetime, timedelta

class ArxivScraper:
    def __init__(self):
        # self.categories = categories
        self.categories = ['cs.AI', 'cs.CV', 'cs.CL']
        
    async def fetch_papers(self):
        """Fetch papers from arXiv"""
        papers = []
        
        for category in self.categories:
            search = arxiv.Search(
                query=f"cat:{category}",
                max_results=5,  # Limit for testing
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in search.results():
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'pdf_url': result.pdf_url,
                    'published': result.published.strftime("%Y-%m-%d"),
                    'category': category
                })
    
        return papers
    async def fetch_papers_by_keyword(self, keyword):
        """Fetch papers from arXiv by keyword"""
        search = arxiv.Search(
            query=keyword,
            max_results=5,  # Limit for testing
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'pdf_url': result.pdf_url,
                'published': result.published.strftime("%Y-%m-%d"),
                'category': result.primary_category
            })
        # print(f"Found {len(papers)} papers for keyword '{keyword}'")
        return papers
