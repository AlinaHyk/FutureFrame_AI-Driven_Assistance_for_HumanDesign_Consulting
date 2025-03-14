# Human-Design AI Assistant

This repository provides a suite of scripts and a Streamlit app that together enable you to:

1. **Extract text** from a variety of document formats (`.doc`, `.docx`, `.pdf`, `.html`).  
2. **Transcribe audio** (`.mp3`) using [OpenAI’s Whisper](https://github.com/openai/whisper).  
3. **Generate text embeddings** with the [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings).  
4. **Serve a chatbot UI** via [Streamlit](https://streamlit.io/) to query the processed text data.

---

## Table of Contents

1. [Project Structure](#project-structure)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Usage](#usage)  
    - [1. Extracting Text from Documents](#1-extracting-text-from-documents)  
    - [2. Transcribing Audio](#2-transcribing-audio)  
    - [3. Generating Embeddings](#3-generating-embeddings)  
    - [4. Running the Streamlit App](#4-running-the-streamlit-app)  
5. [Environment Variables / API Key](#environment-variables--api-key)  
6. [Troubleshooting](#troubleshooting)  
7. [License](#license)  

---

## Project Structure

```bash
.
├── Raw_data_extract.py       # Extracts text from .doc, .docx, .pdf, .html
├── Raw_audio_data.py         # Transcribes .mp3 audio files using Whisper
├── Embedings_gen.py          # Generates text embeddings via OpenAI
├── Implimentation.py         # Streamlit app for querying embedded data (2 roles: Client & Consultant)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── ...
