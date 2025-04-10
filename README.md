# Text Extract & Summarizer API

API for generating summaries and extracting data from various sources into consistent, structured JSON objects using FastAPI and Langchain.

## Features

- **Content Summarization**:
  - Generate summaries of PDF documents
  - Summarize text input directly
  - Summarize web content of provided URL

- **Multiple Content Sources**:
  - PDF uploads
  - Web content by URL
  - Raw text input

- **Information Extraction**:
  - Key points from text
  - Named entities (people, organizations, locations, etc.)
  - Custom extraction based on user instructions or questions

## Examples

Examples of requests and their responses covering the current features of this API are located in the [examples](./examples) folder. Content sources used for examples vary from websites like Wikipedia, ESPN, and SeekingAlpha, as well as PDF files of some books I have read.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/gt581/textextractsummarizer.git
   cd textextractsummarizer
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**:
   Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

## Configuration

Key settings can be adjusted in [`app.core.config.py`](./app/core/config.py)

## Planned Features & Improvements

- **Entities Mentions**: Improve entity extraction to not just include entity text specifically, but also the context around their inclusion.
- **Summary Cleaning**: Minor prompting / cleaning needed to remove unwanted line characters from summary responses.
- **Advanced Web Scraping**: Add additional methods for scraping websites (https connection with python http.client, Selenium, etc.)
- **Additional & Improved File Handling**: Explore using langchain document loaders and text splitters to support more document types in file uploads and improve quality (ex: CSV, JSON, HTML, etc. document loaders)
- **Other Goals**: Would like to develop / leverage this API into using an LLM to create personal daily emails, or "newsletters", that summarize content I am personally interested in on a daily basis and need to visit various websites or sources to consume (ex: The latest tech news, market and portfolio related news, earnings reports and call details, certain sports and sports leagues news and match results, alerts and answers to custom questions or analysis on given websites, etc.).