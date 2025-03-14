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


if __name__ == '__main__':
    unittest.main()