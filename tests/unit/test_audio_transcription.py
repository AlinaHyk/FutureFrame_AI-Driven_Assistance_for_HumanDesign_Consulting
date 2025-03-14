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


if __name__ == '__main__':
    unittest.main()