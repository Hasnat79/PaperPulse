from transformers import pipeline
import asyncio
from typing import Dict, Any
# import torch
import replicate
class PaperSummarizer:
    # def __init__(self):
    #     """Initialize the summarizer with BART model"""
    #     # Use BART model fine-tuned on scientific papers
    #     model_name = "facebook/bart-large-cnn"
    #     # model_name = "google-t5/t5-small"
        
    #     # Set device to GPU if available
    #     self.device = 0 if torch.cuda.is_available() else -1
        
    #     # Initialize the summarization pipeline
    #     self.summarizer = pipeline(
    #         "summarization",
    #         model=model_name,
    #         device=self.device,
    #         max_length=200,  # Adjust for desired summary length
    #         min_length=50,
    #         do_sample=False,  # Use greedy decoding for more focused summaries
    #     )

    async def generate_summary(self, paper: Dict[str, Any]) -> str:
        """
        Generate a concise summary of a research paper using BART.
        
        Args:
            paper: Dictionary containing paper information with keys like
                  'title', 'abstract', 'authors', etc.
        
        Returns:
            str: A concise summary of the paper
        """
        # Prepare the input text
        input_text = f"Title: {paper.get('title', '')}\n\n"
        input_text += f"Abstract: {paper.get('abstract', '')}"

        try:
            # Run summarization in a separate thread to keep async operation
            summary = await asyncio.to_thread(
                self._generate_summary_sync,
                input_text
            )
            return summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Summary generation failed. Please try again later."

    def _generate_summary_sync(self, text: str) -> str:
        """
        Synchronous method to generate summary.
        Splits long texts if needed and combines summaries.
        """
        # BART has a token limit, so we'll split long texts
        max_chunk_length = 1024
        
        if len(text) > max_chunk_length:
            # Split into chunks and summarize each
            chunks = self._split_text(text, max_chunk_length)
            summaries = []
            
            for chunk in chunks:
                summary = self.summarizer(chunk, max_length=200, min_length=50)[0]['summary_text']
                summaries.append(summary)
            
            # Combine and summarize again if needed
            final_summary = " ".join(summaries)
            if len(final_summary) > max_chunk_length:
                final_summary = self.summarizer(final_summary, max_length=200, min_length=50)[0]['summary_text']
            
            return final_summary
        else:
            return self.summarizer(text, max_length=200, min_length=50)[0]['summary_text']

    def _split_text(self, text: str, max_length: int) -> list:
        """Split text into chunks of maximum length while preserving sentence boundaries."""
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length <= max_length:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks

async def process_papers_with_summaries(papers: list, summarizer: PaperSummarizer) -> list:
    """
    Process a list of papers and add AI-generated summaries to each one.
    
    Args:
        papers: List of paper dictionaries
        summarizer: Initialized PaperSummarizer instance
    
    Returns:
        list: Papers with added 'summary' field
    """
    summarized_papers = []
    
    # Process papers concurrently in batches to manage memory
    batch_size = 4  # Adjust based on available memory
    for i in range(0, len(papers), batch_size):
        batch = papers[i:i + batch_size]
        tasks = [summarizer.generate_summary(paper) for paper in batch]
        summaries = await asyncio.gather(*tasks)
        
        for paper, summary in zip(batch, summaries):
            paper['summary'] = summary
            summarized_papers.append(paper)
    
    return summarized_papers
async def replicate_summarizer(papers: list):
    summarized_papers = []

    for i in range(0, len(papers)):
        input_text = f"""
    Instruction: given a research paper abstract, generate a five line bullet point summary of the paper. Keep each points within 10 words and concise. This will be used to generate annotated bibliography.
    
    Abstract:{papers[i]['abstract']}
    Expected output: 
    Motivation: 
    Method: 
    Results: 
    Impact: 
    """
        input = {
        "top_p": 0.95,
        "prompt": input_text,
        "max_tokens": 512,
        "temperature": 0.7,
        "presence_penalty": 0,
        "length_penalty":1,
        "max_new_tokens": 512
    }

        output = replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input=input
        )
        summary = "".join(output)
        summary = summary.replace("•", "<li>").replace("\n", "</li>\n")
        summary = f"<ul>\n{summary}\n</ul>"
        summary = summary.replace("**", "<b>").replace("**", "</b>")
        papers[i]['summary'] = summary
        summarized_papers.append(papers[i])
    # print("".join(output))
    return summarized_papers


