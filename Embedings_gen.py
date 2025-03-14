import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
import openai
import numpy as np
import json


CHUNK_SIZE = 700
CHUNK_OVERLAP = 50
FIRST_SENTENCE_TOKEN_COUNT = 15

# Set your OpenAI API key here
import os
openai.api_key = os.getenv("OPENAI_API_KEY")


def remove_punct_and_stops(tokens):
    """
    Remove punctuation tokens and NLTK stopwords.
    """
    stop_words = set(stopwords.words("english"))
    cleaned = []
    for t in tokens:
        t_low = t.lower()
        # Skip if it's punctuation or a stopword
        if t_low in stop_words:
            continue
        if all(ch in punctuation for ch in t_low):
            continue
        cleaned.append(t_low)
    return cleaned

def chunk_tokens(tokens, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split the tokens into overlapping chunks.
    """
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        if not chunk:
            break
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def first_sentence_of_chunk(tokens):
    """
    Approximate "first sentence" by taking the first N tokens 
    """
    count = min(FIRST_SENTENCE_TOKEN_COUNT, len(tokens))
    return " ".join(tokens[:count])

def process_text_file(file_path):
    """
    1) Read the text
    2) Tokenize
    3) Remove punctuation & stopwords
    4) Chunk into ~500 tokens with 50 overlap
    5) For each chunk, capture the first sentence
    Returns a list of dicts, each with 'chunk_text' and 'metadata'.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    raw_text = re.sub(r"\s+", " ", raw_text).strip()

    # Tokenize
    tokens = word_tokenize(raw_text)

    # Remove punctuation + stopwords
    cleaned_tokens = remove_punct_and_stops(tokens)

    # Chunk
    chunked = chunk_tokens(cleaned_tokens, CHUNK_SIZE, CHUNK_OVERLAP)

    results = []
    for i, c_tokens in enumerate(chunked):
        chunk_str = " ".join(c_tokens)
        # First sentence is the first N tokens joined
        f_sentence = first_sentence_of_chunk(c_tokens)

        results.append({
            "chunk_text": chunk_str,
            "metadata": {
                "chunk_index": i,
                "first_sentence": f_sentence
            }
        })
    return results

def embed_text(text, model="text-embedding-ada-002"):
    """
    Calls OpenAI's Embedding.create with the new 1.0+ interface.
    Returns a list of floats (the embedding vector).
    """
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    vector = response["data"][0]["embedding"]
    return vector

def build_embeddings(chunks):
    """
    Takes a list of chunk dicts like:
    {
      "chunk_text": "...",
      "metadata": { ... }
    }
    and appends an "embedding" field with the vector from openai.
    Returns a new list of dicts with "embedding" included.
    """
    embedded_data = []
    for i, chunk_dict in enumerate(chunks):
        text = chunk_dict["chunk_text"]
        vector = embed_text(text)
        # Merge into a new dict
        new_item = {
            "chunk_text": text,
            "embedding": vector,
            "metadata": chunk_dict["metadata"]
        }
        embedded_data.append(new_item)

        if i % 100 == 0 and i > 0:
            print(f"Embedded {i} chunks so far...")

    return embedded_data

def main():
    # We'll walk through file that incudes raw data (for now jsut testign)
    root_folder = "Transcribed_text_beta"

    all_chunks = []

    # Counters for debug
    file_count = 0
    files_processed = {} 

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                # Print each file as we process it
                print(f"Processing file: {file_path}")

                # Chunking logic
                chunk_dicts = process_text_file(file_path)
                chunk_count = len(chunk_dicts)
                files_processed[file_path] = chunk_count
                file_count += 1

                rel_folder = os.path.relpath(root, root_folder)

                # Add file/folder metadata
                for cd in chunk_dicts:
                    cd["metadata"]["file_name"] = file
                    cd["metadata"]["folder"] = rel_folder

                all_chunks.extend(chunk_dicts)

    print("\n==============================================")
    print(f"Processed {file_count} text files in total.")
    print(f"Total chunks across all files: {len(all_chunks)}")

    print("\nPer-file chunk counts:")
    for fpath, ccount in files_processed.items():
        print(f"  {fpath} => {ccount} chunks")

    # Added counters to show how many chunks and embeddings will be generated.
    print(f"\nCounter: Total number of chunks: {len(all_chunks)}")
    print(f"Counter: Total number of embeddings to be generated: {len(all_chunks)}")

    if not all_chunks:
        print("No chunks found. Exiting.")
        return

    print("\nEmbedding all chunks (this may take a while)...")
    embedded_data = build_embeddings(all_chunks)

    print(f"\nDone: Embedded {len(embedded_data)} chunks total.")
    print("\nSample embedded chunk:")
    print({
        "chunk_text": embedded_data[0]["chunk_text"],
        "metadata": embedded_data[0]["metadata"],
        "embedding_preview": str(embedded_data[0]["embedding"][:10]) + "..."
    })

    # SAVE TO JSON
    with open("embedded_data.json", "w", encoding="utf-8") as f:
      json.dump(embedded_data, f, ensure_ascii=False, indent=2)


    print("Saved embedded data to 'embedded_data.json'.")


if __name__ == "__main__":
    nltk.download("punkt", quiet=True)
    nltk.download("stopwords", quiet=True)
    main()
