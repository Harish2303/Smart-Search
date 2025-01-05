Smart Search Tool for Analytics Vidhya Free Courses

Table of Contents

Introduction

Features

Installation

Usage

Project Workflow

Deployment

Future Improvements

License

Introduction

The Smart Search Tool is designed to help users efficiently find relevant free courses on the Analytics Vidhya platform. By leveraging advanced natural language processing (NLP) techniques, this tool ensures high search relevance and enhances user experience.

Features

Web Scraping: Gather course data directly from the Analytics Vidhya platform (or similar sites).

Data Preprocessing: Normalize, clean, and prepare data for better indexing.

Semantic Search: Use embeddings from models like Sentence Transformers to find courses based on meaning, not just keywords.

User Interface: Simple and interactive search interface using Gradio.

Efficient Storage: Use a vector database like Pinecone for fast and accurate searches.

Installation

Prerequisites

Python 3.8+

Required Python packages:

beautifulsoup4

pandas

sentence-transformers

faiss

gradio

pinecone-client

Steps

Clone the repository:

git clone https://github.com/your-username/smart-search-tool.git
cd smart-search-tool

Install dependencies:

pip install -r requirements.txt

Create a Pinecone account and obtain an API key.

Usage

Data Collection

Run the script to scrape course data:

python data_scraper.py

This will save the course data in courses.csv.

Data Preprocessing

Preprocess the data to remove duplicates and normalize text:

python preprocess_data.py

Embedding Generation

Generate embeddings for the course descriptions:

python generate_embeddings.py

Running the Search Tool

Launch the search interface:

python app.py

The interface will open in your browser or provide a URL.

Project Workflow

1. Data Collection

Course data is gathered using web scraping or API calls. Each course includes information like title, description, curriculum, instructor, and duration.

2. Data Preprocessing

Data is cleaned and normalized to improve search accuracy. Special characters are removed, and text is converted to lowercase.

3. Embedding Model Selection

The project uses Sentence Transformers for semantic embeddings to capture the contextual meaning of course descriptions.

4. Search System Implementation

Embedding Generation: Course descriptions are converted into vector embeddings.

Vector Database: Embeddings are stored in Pinecone for fast similarity searches.

Search Algorithm: Retrieves the most relevant courses based on user queries.

5. Deployment

The tool is deployed on Huggingface Spaces using Gradio for a user-friendly interface.

Deployment

Steps to Deploy on Huggingface Spaces

Create a Huggingface account.

Set up a new Space and select Gradio as the framework.

Upload the project files, including:

app.py

requirements.txt

courses.csv

Launch the Space and test the interface.

Future Improvements

Integrate additional course platforms.

Add support for advanced filters (e.g., duration, difficulty level).

Enhance the embedding model with domain-specific fine-tuning.

Provide multilingual support.

