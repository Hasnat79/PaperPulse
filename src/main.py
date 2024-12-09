import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root)

import asyncio

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from utils.config import settings
# from anthropic import Anthropic
from src.scrapers.arxiv_scraper import ArxivScraper
from src.processors.summary_generator import replicate_summarizer
# Add the previous directory to the system path

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(root, "src", "web", "static")), name="static")
templates = Jinja2Templates(directory=root+"/src/web/templates")

# Initialize Anthropic client
# anthropic = Anthropic(api_key = settings.ANTHROPIC_API_KEY)
# categories = ['cs.AI', 'cs.CV', 'cs.CL']  # AI, Computer Vision, Computational Linguistics
arxiv_scrapper = ArxivScraper()

@app.get("/")
async def home(request: Request):
    # papers = await arxiv_scrapper.fetch_papers()
    # print(papers)
    # # Generate summaries for each paper
    # for paper in papers:
    #     paper['ai_summary'] = await generate_summary(paper)
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
@app.get("/search/{query}")
async def search(query: str):
    # Gather results from all sources concurrently
    arxiv_results = await arxiv_scrapper.fetch_papers_by_keyword(query)
    print(len(arxiv_results))
    # Generate summaries for the papers
    summarized_results = await replicate_summarizer(arxiv_results)
    return {
        "arxiv": summarized_results
    }
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
