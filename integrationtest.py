# tests/unit/test_embedding.py
import unittest
import json
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Embedings_gen import remove_punct_and_stops, chunk_tokens, first_sentence_of_chunk, embed_text

class TestEmbeddingFunctions(unittest.TestCase):
    """Unit tests for embedding generation functions"""
    
    def test_remove_punct_and_stops(self):
        """Test the removal of punctuation and stopwords"""
        input_tokens = ["This", "is", "a", "test", "sentence", ".", "It", "has", "some", "stopwords", "!"]
        expected_output = ["test", "sentence", "stopwords"]
        result = remove_punct_and_stops(input_tokens)
        self.assertEqual(result, expected_output)
    
    def test_chunk_tokens(self):
        """Test the chunking of tokens with overlap"""
        # Create a list of 1000 sample tokens
        sample_tokens = [f"token{i}" for i in range(1000)]
        
        # Test with default settings (chunk_size=700, overlap=50)
        chunks = chunk_tokens(sample_tokens)
        
        # Check we have the expected number of chunks
        expected_chunks = 2  # With 1000 tokens, chunk_size 700, overlap 50
        self.assertEqual(len(chunks), expected_chunks)
        
        # Check first chunk has correct size
        self.assertEqual(len(chunks[0]), 700)
        
        # Check second chunk starts at the right position (700-50 = 650)
        self.assertEqual(chunks[1][0], "token650")
    
    def test_first_sentence_of_chunk(self):
        """Test extracting the first "sentence" (based on token count)"""
        chunk = ["this", "is", "a", "test", "chunk", "with", "more", "than", "fifteen", "tokens", 
                "so", "we", "can", "verify", "it", "gets", "truncated", "correctly"]
                
        result = first_sentence_of_chunk(chunk)
        expected = "this is a test chunk with more than fifteen tokens so we can verify it"
        
        self.assertEqual(result, expected)
        
        # Test with fewer tokens than the limit
        short_chunk = ["short", "chunk"]
        short_result = first_sentence_of_chunk(short_chunk)
        self.assertEqual(short_result, "short chunk")
    
    @patch('openai.Embedding.create')
    def test_embed_text(self, mock_embed):
        """Test the embedding function with mocked OpenAI API"""
        # Mock the OpenAI embedding response
        mock_embedding = [0.1] * 1536  # 1536 is typical size for ada embeddings
        mock_embed.return_value = {
            "data": [{"embedding": mock_embedding}]
        }
        
        test_text = "This is a test text for embedding"
        result = embed_text(test_text)
        
        # Check that the API was called with correct params
        mock_embed.assert_called_once_with(
            input=test_text,
            model="text-embedding-ada-002"
        )
        
        # Check the result is as expected
        self.assertEqual(result, mock_embedding)
        self.assertEqual(len(result), 1536)


# tests/unit/test_text_extraction.py
import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Raw_data_extract import convert_doc, convert_docx, convert_pdf, convert_html

class TestTextExtraction(unittest.TestCase):
    """Unit tests for text extraction functions"""
    
    @patch('textract.process')
    def test_convert_doc(self, mock_textract):
        """Test .doc file conversion"""
        # Set up mock return value for textract
        mock_textract.return_value = b"This is sample doc content."
        
        # Create temporary files for input/output
        with tempfile.NamedTemporaryFile(suffix='.doc') as in_file, \
             tempfile.NamedTemporaryFile(suffix='.txt') as out_file:
            
            # Call the function
            convert_doc(in_file.name, out_file.name)
            
            # Check that textract was called with the right path
            mock_textract.assert_called_once_with(in_file.name)
            
            # Read the output file to verify content
            with open(out_file.name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertEqual(content, "This is sample doc content.")
    
    @patch('docx.Document')
    def test_convert_docx(self, mock_document):
        """Test .docx file conversion"""
        # Set up mock for docx.Document
        mock_doc = MagicMock()
        mock_document.return_value = mock_doc
        
        # Create mock paragraphs
        para1, para2 = MagicMock(), MagicMock()
        para1.text = "First paragraph."
        para2.text = "Second paragraph."
        mock_doc.paragraphs = [para1, para2]
        
        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(suffix='.docx') as in_file, \
             tempfile.NamedTemporaryFile(suffix='.txt') as out_file:
            
            # Call the function
            convert_docx(in_file.name, out_file.name)
            
            # Check that Document was called with right params
            mock_document.assert_called_once_with(in_file.name)
            
            # Read output and verify
            with open(out_file.name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertEqual(content, "First paragraph.\nSecond paragraph.")
    
    @patch('pdfplumber.open')
    def test_convert_pdf(self, mock_pdf_open):
        """Test PDF file conversion"""
        # Set up mocks for pdfplumber
        mock_pdf = MagicMock()
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf
        
        # Create mock pages
        page1, page2 = MagicMock(), MagicMock()
        page1.extract_text.return_value = "Page 1 content."
        page2.extract_text.return_value = "Page 2 content."
        mock_pdf.pages = [page1, page2]
        
        # Test with temp files
        with tempfile.NamedTemporaryFile(suffix='.pdf') as in_file, \
             tempfile.NamedTemporaryFile(suffix='.txt') as out_file:
            
            # Call function
            convert_pdf(in_file.name, out_file.name)
            
            # Verify PDF was opened correctly
            mock_pdf_open.assert_called_once_with(in_file.name)
            
            # Check output
            with open(out_file.name, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertEqual(content, "Page 1 content.\nPage 2 content.")
    
    @patch('builtins.open', new_callable=mock_open, read_data="<html><body><p>Test content.</p></body></html>")
    @patch('bs4.BeautifulSoup')
    def test_convert_html(self, mock_soup, mock_file):
        """Test HTML file conversion"""
        # Set up BeautifulSoup mock
        mock_soup_instance = MagicMock()
        mock_soup.return_value = mock_soup_instance
        mock_soup_instance.get_text.return_value = "Test content."
        
        # Test with temp output file
        with tempfile.NamedTemporaryFile(suffix='.txt') as out_file:
            # Call function
            convert_html("test.html", out_file.name)
            
            # Verify BeautifulSoup was called correctly
            mock_soup.assert_called_once()
            mock_soup_instance.get_text.assert_called_once_with(separator="\n")


# tests/unit/test_audio_transcription.py
import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Raw_audio_data import main

class TestAudioTranscription(unittest.TestCase):
    """Unit tests for audio transcription functionality"""
    
    @patch('os.path.isdir')
    @patch('os.makedirs')
    @patch('os.listdir')
    @patch('whisper.load_model')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_transcription_workflow(self, mock_open, mock_load_model, mock_listdir, mock_makedirs, mock_isdir):
        """Test the complete transcription workflow"""
        # Configure mocks
        mock_isdir.return_value = True
        mock_listdir.return_value = ['sample1.mp3', 'sample2.mp3', 'not_an_audio.txt']
        
        # Mock the whisper model
        mock_model = MagicMock()
        mock_load_model.return_value = mock_model
        
        # Configure transcription results
        mock_model.transcribe.side_effect = [
            {"text": "This is the transcription of sample 1."},
            {"text": "This is the transcription of sample 2."}
        ]
        
        # Call the main function
        main()
        
        # Verify the model was loaded
        mock_load_model.assert_called_once_with("base")
        
        # Verify transcribe was called for each MP3 file
        self.assertEqual(mock_model.transcribe.call_count, 2)
        
        # Verify directory creation
        mock_makedirs.assert_called_once_with(os.path.join("Transcribed", "Audio"), exist_ok=True)
        
        # Verify file writing operations
        write_calls = mock_open().write.call_args_list
        self.assertEqual(len(write_calls), 2)
        
        # Check content of write operations
        self.assertEqual(write_calls[0][0][0], "This is the transcription of sample 1.")
        self.assertEqual(write_calls[1][0][0], "This is the transcription of sample 2.")


# tests/unit/test_search.py
import unittest
import os
import sys
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import relevant functions from app.py
from app import cosine_similarity, find_top_chunks, embed_query

class TestSearchFunctions(unittest.TestCase):
    """Unit tests for semantic search functionality"""
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation"""
        # Test with known vectors and similarity
        vec_a = [1, 0, 0, 0]
        vec_b = [0, 1, 0, 0]
        vec_c = [1, 1, 0, 0]
        
        # Orthogonal vectors should have zero similarity
        self.assertEqual(cosine_similarity(vec_a, vec_b), 0)
        
        # Vector with itself should have similarity 1
        self.assertEqual(cosine_similarity(vec_a, vec_a), 1)
        
        # Check a specific case with known value
        self.assertAlmostEqual(cosine_similarity(vec_a, vec_c), 1/np.sqrt(2))
    
    @patch('app.embed_query')
    def test_find_top_chunks(self, mock_embed_query):
        """Test finding top chunks based on query relevance"""
        # Mock the embedding function
        mock_embed_query.return_value = [1, 0, 0, 0]
        
        # Create test embedded data
        test_data = [
            {"chunk_text": "This is about topic A", "embedding": [1, 0, 0, 0]},
            {"chunk_text": "This is about topic B", "embedding": [0, 1, 0, 0]},
            {"chunk_text": "This is about both A and B", "embedding": [0.7, 0.7, 0, 0]},
            {"chunk_text": "This is about something else", "embedding": [0, 0, 1, 0]},
            {"chunk_text": "This is a mix of topics", "embedding": [0.5, 0.5, 0.5, 0.5]}
        ]
        
        # Find top 3 chunks for a query
        results = find_top_chunks("Test query", test_data, top_k=3)
        
        # Verify 3 results returned
        self.assertEqual(len(results), 3)
        
        # Check that results are ordered by similarity (highest first)
        self.assertEqual(results[0][1]["chunk_text"], "This is about topic A")  # Most similar
        self.assertEqual(results[1][1]["chunk_text"], "This is about both A and B")  # Second most similar
        
        # Verify scores are in descending order
        self.assertGreaterEqual(results[0][0], results[1][0])
        self.assertGreaterEqual(results[1][0], results[2][0])
    
    @patch('openai.Embedding.create')
    def test_embed_query(self, mock_embed):
        """Test the query embedding function"""
        # Mock OpenAI API response
        mock_embedding = [0.1] * 1536
        mock_embed.return_value = {
            "data": [{"embedding": mock_embedding}]
        }
        
        # Call the function
        result = embed_query("What is Human Design?")
        
        # Verify the API was called correctly
        mock_embed.assert_called_once_with(
            input="What is Human Design?",
            model="text-embedding-ada-002"
        )
        
        # Check result matches the mock
        self.assertEqual(result, mock_embedding)
        
# Add the test_helpers.py file in the tests directory

# tests/test_helpers.py
import os
import json
import tempfile
import numpy as np

def create_sample_embeddings(count=10, vector_size=1536):
    """Create sample embeddings for testing"""
    embeddings = []
    for i in range(count):
        vector = list(np.random.random(vector_size))
        embeddings.append({
            "chunk_text": f"This is test chunk {i} about Human Design topic {i % 3 + 1}.",
            "embedding": vector,
            "metadata": {
                "chunk_index": i,
                "first_sentence": f"This is test chunk {i}",
                "file_name": f"test_file_{i % 5}.txt",
                "folder": "test_folder"
            }
        })
    return embeddings

def create_temp_embeddings_file(embeddings=None):
    """Create a temporary JSON file with embeddings for tests"""
    if embeddings is None:
        embeddings = create_sample_embeddings()
        
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as temp_file:
        json.dump(embeddings, temp_file)
        temp_path = temp_file.name
    
    return temp_path