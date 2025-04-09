# Text Extract & Summarizer API

API for summarizing content from multiple sources and extracting specific information from text.

## Features

- **Content Summarization**:
  - Generate summaries of PDF documents
  - Summarize text input directly
  - Summarize web content of provided URL

- **Multiple Content Sources**:
  - PDF uploads
  - Web content by URL
  - Raw text input

## Planned Features

- **Information Extraction**:
  - Key points from text
  - Named entities (people, organizations, locations, etc.)
  - Custom extraction based on user instructions

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