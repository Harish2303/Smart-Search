# -*- coding: utf-8 -*-
"""Smart Search.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-9Afs5ZH_NZ-VImNcYe0q-Rg1CjXcoU8
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of Analytics Vidhya Free Courses
url = "https://www.udemy.com/"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Parse course data
courses = []
for course in soup.find_all("div", class_="course-card"):  # Adjust the selector based on actual HTML
    title = course.find("h2").text.strip()  # Adjust selector
    description = course.find("p", class_="course-description").text.strip()  # Adjust selector
    link = course.find("a")["href"]
    courses.append({"title": title, "description": description, "link": link})

# Save data to a CSV
df = pd.DataFrame(courses)
df.to_csv("courses.csv", index=False)
print("Courses data saved to courses.csv")

pip install langchain llama-index pinecone-client gradio

!pip install -U langchain-community

import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone instance
pc = Pinecone(api_key = "pcsk_58zJHT_3nGMfD5V4eqVYYViJjwx77TKpiJbooD9LmBuvvnxSksSXiM1QWcGDSZHscDLUaN")

# Create Pinecone index if not already created
index_name = "course-search"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Adjust the dimension based on your embedding model
        metric='cosine',  # Using cosine similarity for vector search
        spec=ServerlessSpec(
            cloud='aws',  # Adjust cloud provider if necessary
            region='us-east-1'  # Specify region
        )
    )

# Connect to the index
index = pc.Index(index_name)

import pandas as pd

try:
    df = pd.read_csv("courses.csv")
    print(df.head())  # Check the first few rows to confirm data
except pd.errors.EmptyDataError:
    print("The file is empty or cannot be read.")
except Exception as e:
    print(f"An error occurred: {e}")

import gradio as gr

def search_courses(query):
    query_vector = embeddings.embed_text(query)
    results = index.query(query_vector, top_k=5, include_metadata=True)
    return [
        f"**{match['metadata']['title']}**\n{match['metadata']['link']}" for match in results["matches"]
    ]

# Gradio interface
interface = gr.Interface(
    fn=search_courses,
    inputs="text",
    outputs="text",
    title="Smart Course Search",
    description="Enter a keyword or phrase to search Analytics Vidhya's free courses."
)

interface.launch()











pip install transformers pinecone-client gradio pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import pinecone
import gradio as gr

import requests
from bs4 import BeautifulSoup
import pandas as pd
import openai
import pinecone
import gradio as gr
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI and Pinecone API keys
openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your OpenAI API key
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))  # Pinecone API key from .env

# Function to get embeddings using OpenAI
def get_embeddings(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

# URL of Analytics Vidhya Courses
url = "https://courses.analyticsvidhya.com/collections/courses"

# Fetch the webpage
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Debug: Check raw HTML for course structure
print(soup.prettify())  # Print formatted HTML for debugging

# Parse course data
courses = []
# Check the actual structure of the courses and update accordingly
for course in soup.find_all("div", class_="product-card"):  # Adjust the selector based on actual HTML
    title = course.find("p", class_="title").text.strip()  # Adjust selector
    description = course.find("p", class_="description").text.strip()  # Adjust selector
    link = course.find("a")["href"]
    courses.append({"title": title, "description": description, "link": link})

# Debug: Check if courses list is populated
if not courses:
    print("No courses found. Please check the scraping logic or the website.")
else:
    print(f"Found {len(courses)} courses.")

# Save data to a CSV
df = pd.DataFrame(courses)

# Check if DataFrame is not empty
if df.empty:
    print("DataFrame is empty. No courses scraped.")
else:
    print(df.head())  # Preview first few rows

df.to_csv("courses.csv", index=False)
print("Courses data saved to courses.csv")

# Create Pinecone index (if not already created)
index_name = "course-search"

# Change region to 'us-east1' for free plan compatibility
if index_name not in pinecone_client.list_indexes():
    pinecone_client.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud='aws', region='us-east-1')  # Updated to us-east1
    )

index = pinecone_client.Index(index_name)

# Indexing course data into Pinecone
for idx, course in enumerate(courses):
    embedding = get_embeddings(course["description"])
    index.upsert(
        vectors=[(f"course-{idx}", embedding, {"title": course["title"], "description": course["description"], "link": course["link"]})]
    )

# Function to search courses using embeddings
def search_courses(query):
    try:
        query_vector = get_embeddings(query)  # Use OpenAI embeddings
        results = index.query(query_vector, top_k=5, include_metadata=True)

        return [
            f"**{match['metadata']['title']}**\n{match['metadata']['link']}" for match in results["matches"]
        ]
    except Exception as e:
        return str(e)

# Gradio interface
interface = gr.Interface(
    fn=search_courses,
    inputs="text",
    outputs="text",
    title="Smart Course Search",
    description="Enter a keyword or phrase to search Analytics Vidhya's free courses."
)

# Ensure Gradio runs with `share=True` for public URL in Colab
interface.launch(share=True)

"""### FOR .ENV of API KEYS"""

# Install the required libraries
!pip install python-dotenv
!pip install pinecone-client

# Write the content to an .env file
env_content = """
PINECONE_API_KEY=pcsk_58zJHT_3nGMfD5V4eqVYYViJjwx77TKpiJbooD9LmBuvvnxSksSXiM1QWcGDSZHscDLUaN
OPENAI_API_KEY=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
"""

# Save the content to the .env file
with open('.env', 'w') as f:
    f.write(env_content)

# Now, load the environment variables using python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # Load the .env file

# Access the environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Import pinecone and openai
import pinecone
import openai

# Create a Pinecone instance
from pinecone import Pinecone

# Initialize Pinecone with your API key
pc = Pinecone(api_key=pinecone_api_key)

# Initialize OpenAI with your API key
openai.api_key = openai_api_key

# Check the values
print(f"Pinecone API Key: {pinecone_api_key}")
print(f"OpenAI API Key: {openai_api_key}")









"""### LAST ATTEMPT"""

!pip install langchain faiss-cpu faker openai streamlit

import random
from faker import Faker
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import streamlit as st
import faiss

import pandas as pd
import numpy as np
import random
import faiss
from faker import Faker
from sentence_transformers import SentenceTransformer
import streamlit as st

# Initialize Faker instance to simulate data
fake = Faker()

# Simulate Dataset for Free Courses
def generate_mock_data(num_courses=10):
    courses = []
    for _ in range(num_courses):
        course = {
            "title": fake.bs(),
            "description": fake.paragraph(),
            "curriculum": fake.text(),
            "tags": random.choice(["Machine Learning", "Data Science", "Deep Learning", "AI", "Python"]),
        }
        courses.append(course)
    return courses

# Generate a list of mock courses
courses = generate_mock_data()

# Convert the courses list to a pandas DataFrame
df = pd.DataFrame(courses)

# Display data for verification
st.write("Courses Data:", df)

# Embedding model setup (using Hugging Face's SentenceTransformer)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained transformer model for sentence embeddings

# Create embeddings for course descriptions (This will take time but will avoid rate limits)
embeddings = embedding_model.encode(df['description'].tolist())

# Create a FAISS index for efficient search
index = faiss.IndexFlatL2(len(embeddings[0]))  # L2 distance for similarity
index.add(np.array(embeddings).astype("float32"))

# Function for querying the database
def search_courses(query):
    query_embedding = embedding_model.encode([query])
    # Search using FAISS
    distances, indices = index.search(np.array(query_embedding).astype("float32"), k=5)
    results = []
    for idx in indices[0]:
        result = df.iloc[idx]
        results.append({
            "title": result['title'],
            "description": result['description'],
            "curriculum": result['curriculum'],
            "tags": result['tags']
        })
    return results

# Streamlit UI
st.title("Smart Course Search")

# User input for search
query = st.text_input("Search for free courses (e.g., Machine Learning, Data Science)")

if query:
    results = search_courses(query)
    if results:
        st.write("Top 5 Relevant Courses:")
        for result in results:
            st.write(f"### {result['title']}")
            st.write(f"**Description:** {result['description']}")
            st.write(f"**Tags:** {result['tags']}")
            st.write(f"**Curriculum:** {result['curriculum']}")
            st.write("---")
    else:
        st.write("No relevant courses found!")

streamlit run "Smart Search.py"

