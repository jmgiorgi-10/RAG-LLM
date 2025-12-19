# Overview
This repo aims to showcase the basic functionality of a RAG (resource augmented generation) application, utilizing a soccer training PDF markdown, to provide the User precise instructions on how to improve their technical and tactical awareness.
# Libraries
```pip3 install -r requirements.txt
# API Usage
This RAG demo used OpenAI's API, for which you must generate a key, and add it to an environmental variable, for safely loading it in the embedding script.
# Functionality
Clone the repo into your local system, run the libararies installation, and then generate OpenAI embedings with
```python3 openai_embeddings.py
Then, view the answer to your training queries by running:
```python3 rag.py
