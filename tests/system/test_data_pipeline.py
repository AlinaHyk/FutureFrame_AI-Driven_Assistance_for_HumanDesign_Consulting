# tests/system/test_data_pipeline.py
import unittest
import os
import sys
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import functions from data processing scripts
try:
    from Raw_data_extract import convert_pdf, convert_docx, convert_html
    from Embedings_gen import process_text_file, embed_text, build_embeddings
except ImportError:
    # Define mocks for the imports if the actual modules can't be imported
    def convert_pdf(*args): pass
    def convert_docx(*args): pass
    def convert_html(*args): pass
    def process_text_file(*args): pass
    def embed_text(*args): pass
    def build_embeddings(*args): pass

class TestDataPipeline(unittest.TestCase):
    """System tests for the data processing pipeline"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Sample text content for test files
        self.sample_content = """
        Human Design is a system of self-knowledge that helps you understand your unique genetic blueprint.
        It combines ancient wisdom traditions with modern science to provide a detailed map of your energetic makeup.
        By following your Strategy and Authority, you can make decisions that are aligned with your true nature.
        """
        
        # Create sample test files
        self.text_file = os.path.join(self.test_dir, "test_content.txt")
        with open(self.text_file, "w", encoding="utf-8") as f:
            f.write(self.sample_content)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary directory and all its contents
        shutil.rmtree(self.test_dir)
    
    @patch('pdfplumber.open')
    def test_pdf_conversion(self, mock_pdf_open):
        """Test PDF conversion process"""
        # Mock the PDF extraction
        mock_page = MagicMock()
        mock_page.extract_text.return_value = self.sample_content
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdf_open.return_value = mock_pdf
        
        # Test file paths
        pdf_file = os.path.join(self.test_dir, "test.pdf")
        out_file = os.path.join(self.test_dir, "test_output.txt")
        
        # Run the conversion
        convert_pdf(pdf_file, out_file)
        
        # Verify the PDF was processed
        mock_pdf_open.assert_called_once_with(pdf_file)
        mock_page.extract_text.assert_called_once()
        
        # Check if the output file exists and contains content
        self.assertTrue(os.path.exists(out_file))
        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertEqual(content, self.sample_content)
    
    @patch('docx.Document')
    def test_docx_conversion(self, mock_document):
        """Test DOCX conversion process"""
        # Mock the DOCX reading
        mock_doc = MagicMock()
        mock_paragraph1 = MagicMock()
        mock_paragraph1.text = "Human Design is a system of self-knowledge"
        mock_paragraph2 = MagicMock()
        mock_paragraph2.text = "that helps you understand your unique genetic blueprint."
        mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2]
        mock_document.return_value = mock_doc
        
        # Test file paths
        docx_file = os.path.join(self.test_dir, "test.docx")
        out_file = os.path.join(self.test_dir, "test_output.txt")
        
        # Run the conversion
        convert_docx(docx_file, out_file)
        
        # Verify the DOCX was processed
        mock_document.assert_called_once_with(docx_file)
        
        # Check if the output file exists and contains content
        self.assertTrue(os.path.exists(out_file))
        with open(out_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Human Design is a system", content)
            self.assertIn("unique genetic blueprint", content)
    
    @patch('bs4.BeautifulSoup')
    def test_html_conversion(self, mock_soup):
        """Test HTML conversion process"""
        # Mock the BeautifulSoup text extraction
        mock_soup_instance = MagicMock()
        mock_soup_instance.get_text.return_value = self.sample_content
        mock_soup.return_value = mock_soup_instance
        
        # Set up mock for open function
        html_content = "<html><body><p>Human Design content</p></body></html>"
        mock_file = mock_open(read_data=html_content)
        
        # Test file paths
        html_file = os.path.join(self.test_dir, "test.html")
        out_file = os.path.join(self.test_dir, "test_output.txt")
        
        # Run the conversion with mocked open
        with patch('builtins.open', mock_file):
            convert_html(html_file, out_file)
        
        # Verify BeautifulSoup was called
        mock_soup.assert_called_once()
        mock_soup_instance.get_text.assert_called_once()
        
        # We can't check the output file directly as we've mocked the open function
        # Instead, verify that open was called for writing the output
        mock_file.assert_called_with(out_file, "w", encoding="utf-8")
    
    @patch('nltk.tokenize.word_tokenize')
    def test_text_chunking(self, mock_tokenize):
        """Test text file processing and chunking"""
        # Mock the tokenization
        mock_tokenize.return_value = self.sample_content.split()
        
        # Process the text file
        chunks = process_text_file(self.text_file)
        
        # Verify we got chunked output
        self.assertIsInstance(chunks, list)
        self.assertTrue(len(chunks) > 0)
        
        # Check chunk structure
        for chunk in chunks:
            self.assertIn("chunk_text", chunk)
            self.assertIn("metadata", chunk)
            self.assertIn("chunk_index", chunk["metadata"])
            self.assertIn("first_sentence", chunk["metadata"])
    
    @patch('openai.Embedding.create')
    def test_text_embedding(self, mock_embedding):
        """Test the embedding generation process"""
        # Mock the OpenAI embedding response
        mock_response = {
            "data": [{"embedding": [0.1] * 1536}]
        }
        mock_embedding.return_value = mock_response
        
        # Generate an embedding
        text = "Human Design concept"
        result = embed_text(text)
        
        # Verify OpenAI API was called correctly
        mock_embedding.assert_called_once()
        call_args = mock_embedding.call_args[1]
        self.assertEqual(call_args["input"], text)
        self.assertEqual(call_args["model"], "text-embedding-ada-002")
        
        # Check result
        self.assertEqual(len(result), 1536)
        self.assertEqual(result[0], 0.1)
    
    @patch('Embedings_gen.embed_text')
    def test_build_embeddings(self, mock_embed_text):
        """Test the full embedding build process"""
        # Mock the embedding function
        mock_embed_text.return_value = [0.1] * 1536
        
        # Create test chunks
        chunks = [
            {
                "chunk_text": "Human Design concept 1",
                "metadata": {"chunk_index": 0, "first_sentence": "Human Design concept 1"}
            },
            {
                "chunk_text": "Human Design concept 2",
                "metadata": {"chunk_index": 1, "first_sentence": "Human Design concept 2"}
            }
        ]
        
        # Build embeddings
        result = build_embeddings(chunks)
        
        # Verify embedding function was called for each chunk
        self.assertEqual(mock_embed_text.call_count, 2)
        
        # Check result structure
        self.assertEqual(len(result), 2)
        for item in result:
            self.assertIn("chunk_text", item)
            self.assertIn("embedding", item)
            self.assertIn("metadata", item)
            self.assertEqual(len(item["embedding"]), 1536)
    
    @patch('openai.Embedding.create')
    @patch('json.dump')
    def test_end_to_end_pipeline(self, mock_json_dump, mock_embedding):
        """Test the entire data pipeline from text processing to embedding"""
        # Mock the OpenAI embedding response
        mock_response = {
            "data": [{"embedding": [0.1] * 1536}]
        }
        mock_embedding.return_value = mock_response
        
        # Process text file to get chunks
        chunks = process_text_file(self.text_file)
        self.assertTrue(len(chunks) > 0)
        
        # Build embeddings from chunks
        embedded_data = build_embeddings(chunks)
        self.assertEqual(len(embedded_data), len(chunks))
        
        # Ensure all components are present
        for item in embedded_data:
            self.assertIn("chunk_text", item)
            self.assertIn("embedding", item)
            self.assertIn("metadata", item)
        
        # Test saving to JSON
        output_file = os.path.join(self.test_dir, "embedded_data.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(embedded_data, f)
        
        # Verify the JSON file exists
        self.assertTrue(os.path.exists(output_file))
        
        # Load the JSON file to verify structure
        with open(output_file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        # Check the loaded data
        self.assertEqual(len(loaded_data), len(embedded_data))
        self.assertEqual(type(loaded_data), list)

if __name__ == '__main__':
    unittest.main()