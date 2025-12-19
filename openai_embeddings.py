from openai import OpenAI
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
import pandas as pd
import re
import os

# 1. Open and Clean a markdown file (previously converted from PDF)
# 2. Split the markdown document into chunks using Langchain
    # -> first split by Excercise
    # -> then apply a Recursive Character Split inside each excercise if needed.

key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

soccer_pdf_markdown_path = "soccer_tactics.md"
EMBEDDING_MODEL = "text-embedding-3-small"
SAVE_PATH = "soccer_training_embeddings.csv"
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

def generate_embeddings(chunks, batch_size=1000):
    rows = []

    for i in range(0, len(chunks), batch_size):
        print(f"Batch {i} to {i + batch_size - 1}")

        batch_docs = chunks[i:i + batch_size]
        batch_texts = [doc.page_content for doc in batch_docs]

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch_texts
        )

        for doc, emb in zip(batch_docs, response.data):
            rows.append({
                "text": doc.page_content,
                "exercise_number": doc.metadata["exercise_number"],
                "source": doc.metadata["source"],
                "embedding": emb.embedding
            })

    return pd.DataFrame(rows)


def clean_raw_text(text: str) -> str:
    import pdb; pdb.set_trace()

    text = re.sub(r'\n\d+\s*\n', '\n', text)
    # text = re.sub(
    #     r'_The Best of Soccer Journal.*',
    #     '',
    #     text,
    #     flags=re.DOTALL
    # )
    text = re.sub(r'\n\d+[A-Z]?\n', '', text)  # removes '1A', etc
   
    return text.strip()

def semantic_split(raw_text):

    blocks = re.split(
        r'(?=\nExercise\s+\d+|\n#\s+Chapter|\n##\s+)',
        raw_text
    )

    docs = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        exercise_match = re.search(r'Exercise\s+(\d+)', block)
        chapter_match = re.search(r'#\s*(Chapter\s+\d+)', block)

        if exercise_match:
            docs.append(
                Document(
                    page_content=block,
                    metadata={
                        "exercise_number": int(exercise_match.group(1)),
                        "type": "exercise",
                        "source": "soccer_tactics_clean.md"
                    }
                )
            )
        else:
            docs.append(
                Document(
                    page_content=block,
                    metadata={
                        "exercise_number": None,
                        "type": "reference",
                        "source": "soccer_tactics_clean.md"
                    }
                )
            )

    return docs

def header_split(semantic_chunk_split):
    header_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "chapter"),
        ("##", "section"),
        ]
    )

    processed_docs = []

    for doc in semantic_chunk_split:
        if doc.metadata["type"] == "exercise":
            processed_docs.append(doc)
        else:
            split_docs = header_splitter.split_text(doc.page_content)
            for sd in split_docs:
                sd.metadata.update(doc.metadata)
                processed_docs.append(sd)
    
    return processed_docs


# Recursive split inside each excercise:
def recursive_split(docs):
    
    splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=50,
    separators=["\n\n", "\n"]
    )

    chunks = []  

    for doc in docs:
        sub_chunks = splitter.split_text(doc.page_content)
        for text in sub_chunks:
            chunks.append(
                Document(
                    page_content=text,
                    metadata=doc.metadata.copy()
                )
            )

    return chunks

if __name__ == "__main__":

    loader = TextLoader(soccer_pdf_markdown_path, encoding="utf-8")
    docs = loader.load()
    raw_text = docs[0].page_content

    clean_text = clean_raw_text(raw_text)
    semantic_chunk_split = semantic_split(clean_text)
    split_by_header = header_split(semantic_chunk_split)
    chunks = recursive_split(split_by_header)

    import pdb; pdb.set_trace()

    embeddings = generate_embeddings(chunks)
    embeddings.to_csv(SAVE_PATH, index=False)
    import pdb; pdb.set_trace()

