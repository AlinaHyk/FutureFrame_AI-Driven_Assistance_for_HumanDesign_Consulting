# Human Design AI Assistant

An AI-powered application providing Human Design insights through semantic search and large language models. This system processes documents, transcribes audio, generates embeddings, and delivers a professional chatbot interface with consultant and client functionality.

**Live Application:** [https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app](https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app)

## Overview

This repository contains a complete system for:

1. **Text extraction** from multiple document formats (`.doc`, `.docx`, `.pdf`, `.html`)
2. **Audio transcription** for `.mp3` files using OpenAI's Whisper
3. **Text embedding generation** via OpenAI Embeddings API
4. **Semantic search interface** using a Streamlit web application

The application offers different experience levels for clients seeking basic information and consultants requiring detailed analysis.

## Project Structure

```
.
├── .gitattributes               # Git LFS configuration
├── .gitignore                   # Git ignore configuration
├── Embedings_gen.py             # Embedding generation script
├── Procfile                     # Heroku deployment configuration
├── README.md                    # Project documentation
├── Raw_audio_data.py            # Audio transcription script
├── Raw_data_extract.py          # Document text extraction script
├── app.py                       # Main Streamlit application
├── embedded_data.json           # Generated embeddings data (Git LFS)
├── integrationtest.py           # Integration tests
├── requirements.txt             # Python dependencies
├── static/                      # Static assets directory
│   ├── manifest.json            # PWA manifest file
│   ├── pwa-installer.js         # PWA installation helper
│   └── service-worker.js        # Service worker for offline functionality
└── tests/                       # Test directory
    └── unit/                    # Unit tests
        ├── search.py            # Search functionality tests
        ├── test_audio_transcription.py  # Audio processing tests
        ├── test_embedding.py    # Embedding functionality tests
        ├── test_search.py       # Search algorithm tests
        └── test_text_extraction.py      # Document extraction tests
```

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Document processing dependencies:
  - For PDF: pdfplumber
  - For DOCX: python-docx
  - For DOC: textract (requires antiword on Linux or wps on Windows)
  - For HTML: BeautifulSoup4
- For audio transcription: OpenAI Whisper
- For PDF generation: wkhtmltopdf

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd human-design-ai-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

## Usage

### 1. Extracting Text from Documents

The `Raw_data_extract.py` script processes multiple document formats and extracts their text content.

Usage:
```bash
python Raw_data_extract.py
```

Configuration:
- Place documents in appropriate subdirectories within `Books_Cleand_type/` (Docx, HTML, PDF)
- Extracted text is saved to `Transcribed/` directory

Script behavior:
- Processes .doc, .docx, .pdf, and .html files
- Creates corresponding .txt files with extracted content
- Maintains source folder structure in output directory

### 2. Transcribing Audio

The `Raw_audio_data.py` script converts audio recordings to text.

Usage:
```bash
python Raw_audio_data.py
```

Configuration:
- Place .mp3 files in the `MP3 audio/` directory
- Transcriptions are saved to `Transcribed/Audio/` directory

Technical details:
- Uses OpenAI's Whisper model (base configuration by default)
- Creates text files with the same base name as the source audio

### 3. Generating Embeddings

The `Embedings_gen.py` script processes text files and creates semantic vector embeddings.

Usage:
```bash
python Embedings_gen.py
```

Functionality:
- Reads all text files from the `Transcribed_text_beta/` directory
- Processes text through tokenization and cleaning
- Splits text into semantic chunks with overlap
- Generates vector embeddings for each chunk using OpenAI's API
- Stores embeddings with metadata in `embedded_data.json`

Technical specifications:
- Default chunk size: 700 tokens
- Chunk overlap: 50 tokens
- Embedding model: `text-embedding-ada-002`
- Metadata includes file origin and position information

### 4. Running the Streamlit Application

The `app.py` script launches the web interface for querying the Human Design knowledge base.

Usage:
```bash
streamlit run app.py
```

Features:
- Chat interface with message history
- Client/Consultant expertise level selection
- Semantic search of embedded knowledge base
- Visualization of search results and keyword relevance
- Knowledge graph exploration of concept relationships
- API configuration options

Application architecture:
- Frontend built with Streamlit
- Semantic search using cosine similarity
- Enhanced prompting system for context-aware responses
- Optional data visualization with Plotly and PyVis
- Progressive Web App capabilities

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | API key for OpenAI services | Yes | None |
| `IS_CLOUD` | Flag for cloud deployment settings | No | False |
| `CACHE_DIR` | Custom cache directory path | No | `/tmp/streamlit_cache` |
| `GPT_MODEL` | Model for client queries | No | `gpt-4` |
| `CONSULTANT_MODEL` | Model for consultant responses | No | `gpt-4.5-preview` |

## Testing

The repository includes comprehensive tests for all major components:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test modules
python -m unittest tests.unit.test_embedding
python -m unittest tests.unit.test_search
```

Test coverage:
- Embedding generation functionality
- Document text extraction
- Audio transcription
- Semantic search algorithms
- Response generation for different user roles

## Deployment

### Streamlit Cloud

1. Push repository to GitHub
2. Connect to Streamlit Cloud
3. Configure environment variables
4. Deploy directly from repository

### Heroku

1. Ensure `Procfile` is configured correctly
2. Set environment variables in Heroku dashboard
3. Deploy using the Heroku CLI or GitHub integration

## Troubleshooting

### Common Issues

#### API Rate Limiting
- Error: `RateLimitError` from OpenAI
- Solution: Implement exponential backoff for retries or upgrade API tier

#### Embedding Generation Failures
- Problem: Empty or non-text files in source directories
- Solution: Verify file content and format before processing

#### Document Conversion Errors
- Issue: Missing dependencies for specific file formats
- Solution: Install format-specific libraries (`textract`, `pdfplumber`, etc.)

#### Memory Usage
- Problem: Large embedding files exceed memory limits
- Solution: Process in smaller batches or implement streaming

## Implementation Notes

### Semantic Search Architecture
- Document chunking with controlled overlap for context preservation
- Embedding vectors for semantic similarity measurement
- Two-stage retrieval for consultant mode with query expansion
- Source citation and relevance scoring

### Knowledge Graph Implementation
- Concept extraction from text chunks
- Relationship identification between concepts
- Graph visualization with node sizing based on centrality
- Interactive exploration of semantic connections

### Progressive Web App Features
- Service worker for offline capabilities
- Manifest configuration for installable application
- Custom icons and theming

## Acknowledgements

- OpenAI for embedding and LLM technologies
- Streamlit for application framework
- Open-source libraries: pdfplumber, textract, whisper, and others
