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
            
            # Check that open was called for reading the HTML file
            mock_file.assert_any_call("test.html", "r", encoding="utf-8", errors="replace")
            
            # Check that open was called for writing the output
            mock_file.assert_any_call(out_file.name, "w", encoding="utf-8")
  
            mock_file().write.assert_called_with("Test content.")


if __name__ == '__main__':
    unittest.main()