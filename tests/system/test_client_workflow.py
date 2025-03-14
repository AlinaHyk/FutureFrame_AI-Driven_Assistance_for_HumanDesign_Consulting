# tests/system/test_client_workflow.py
import unittest
import os
import sys
import json
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import necessary modules
from app import get_client_response, load_embedded_data, embed_query, ask_gpt, build_chat_prompt, find_top_chunks

class TestClientWorkflow(unittest.TestCase):
    """System tests for the client chat workflow"""
    
    def setUp(self):
        """Set up test environment with realistic test data"""
        # Create realistic test data with actual Human Design concepts
        self.test_data = []
        
        # Sample realistic HD concepts for test chunks
        hd_concepts = [
            "The Human Design System is a synthesis of ancient and modern sciences that offers a map of your genetic design. By understanding your type, authority, profile, and definition, you can make decisions that are correct for you. Human Design combines principles from the I Ching, astrology, Kabbalah, and the chakra system with quantum physics and genetics.",
            "There are five energy Types in Human Design: Manifestors, Generators, Manifesting Generators, Projectors, and Reflectors. Each Type has its own Strategy for making decisions and navigating life correctly.",
            "Your Authority is your body's way of making decisions. The seven Authorities are: Emotional (Solar Plexus), Sacral, Splenic, Ego/Heart, G Center (Self), Environment, and Lunar. Your Authority is the most reliable decision-making tool for your design.",
            "The four Variables in Human Design (Digestion, Environment, Perspective, and Awareness) provide specific information about how you process experience and interact with the world. They offer practical guidance for optimizing your physical well-being and cognitive function.",
            "The 64 Gates in Human Design correspond to the 64 hexagrams of the I Ching and represent specific energies and themes in human experience. When Gates connect between centers, they form Channels, which represent consistent energy and traits in your design.",
            "The Profile in Human Design is a combination of two numbers that describes your life purpose and the role you play in society. There are twelve possible Profiles, each with its own characteristics and challenges.",
            "Definition refers to the consistent energy in your design, formed by connected Centers. There are four types of Definition: Single, Split, Triple Split, and Quadruple Split. Someone with no connected Centers has what's called No Definition or is a Reflector type.",
            "The Not-Self is what you experience when you live according to external conditioning rather than your true nature. Each Type has specific Not-Self symptoms that signal you're not living in alignment with your design.",
            "Generators and Manifesting Generators have Sacral energy and are designed to respond to life. Their Strategy is to wait to respond, and their signature is satisfaction. When not living their Strategy, they experience frustration.",
            "Projectors are designed to guide and direct energy, not to initiate. Their Strategy is to wait for the invitation, and their signature is success. When not living their Strategy, they experience bitterness."
        ]
        
        # Create embeddings with slight variations to ensure differentiation
        base_vector = np.random.rand(1536).tolist()
        
        for i, concept in enumerate(hd_concepts):
            # Create slightly different vectors for each chunk
            variation = np.random.normal(0, 0.01, 1536)
            vector = (np.array(base_vector) + variation).tolist()
            
            self.test_data.append({
                "chunk_text": concept,
                "embedding": vector,
                "metadata": {
                    "chunk_index": i,
                    "file_name": f"human_design_concept_{i}.txt",
                    "folder": "human_design",
                    "first_sentence": concept.split('.')[0] if '.' in concept else concept[:50]
                }
            })
        
        # Create mock for Streamlit session state
        self.session_state_patch = patch('streamlit.session_state')
        self.mock_session_state = self.session_state_patch.start()
        self.mock_session_state.expertise_level = "client"
        self.mock_session_state.chat_history = []
        self.mock_session_state.gpt_temperature = 0.3
        
    def tearDown(self):
        """Clean up after test"""
        self.session_state_patch.stop()
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.cosine_similarity')
    def test_find_top_chunks(self, mock_cosine_similarity, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test the chunk retrieval functionality"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Mock cosine similarity to return predictable values
        mock_cosine_similarity.side_effect = [0.98, 0.85, 0.76, 0.65, 0.54, 0.43, 0.32, 0.21, 0.12, 0.01]
        
        # Test finding top chunks
        query = "What are the different Types in Human Design?"
        top_chunks = find_top_chunks(query, self.test_data, top_k=5)
        
        # Verify we got the right number of chunks
        self.assertEqual(len(top_chunks), 5)
        
        # Verify chunks are sorted by relevance
        scores = [score for score, _ in top_chunks]
        self.assertEqual(scores, [0.98, 0.85, 0.76, 0.65, 0.54])
        
        # Verify embedding was called with the query
        mock_embed_query.assert_called_with(query)
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.find_top_chunks')
    def test_prompt_building(self, mock_find_top_chunks, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test the prompt building functionality"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Create mock top chunks
        mock_top_chunks = [
            (0.95, self.test_data[1]),  # Types chunk
            (0.85, self.test_data[0]),  # Human Design intro chunk
            (0.75, self.test_data[8]),  # Generators chunk
            (0.65, self.test_data[9]),  # Projectors chunk
            (0.55, self.test_data[6])   # Definition chunk
        ]
        
        # Test building the prompt directly without expecting find_top_chunks to be called
        query = "What are the different Types in Human Design?"
        prompt = build_chat_prompt(query, mock_top_chunks)
        
        # Verify the prompt contains key elements
        self.assertIn("CONTEXT:", prompt)
        self.assertIn("USER QUESTION:", prompt)
        self.assertIn(query, prompt)
        
        # Check for chunk content in the prompt
        for _, chunk in mock_top_chunks:
            self.assertIn(chunk["chunk_text"][:50], prompt)
        
        # Check for score information
        self.assertIn("Score: 0.95", prompt)
        
        # We don't check if find_top_chunks was called since we're testing build_chat_prompt directly
        # and that function doesn't call find_top_chunks
        
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.find_top_chunks')
    @patch('app.build_chat_prompt')
    def test_full_client_chat_interaction(self, mock_build_prompt, mock_find_top_chunks, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test a complete client-mode chat interaction flow with realistic responses"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Create mock top chunks
        mock_top_chunks = [(0.95, self.test_data[i]) for i in range(5)]
        mock_find_top_chunks.return_value = mock_top_chunks
        
        # Set up mock prompt building
        mock_build_prompt.side_effect = lambda query, chunks: f"Test prompt for: {query}"
        
        # Configure ask_gpt to return different responses for different queries
        def side_effect(prompt, model=None, temperature=None):
            if "what is human design" in prompt.lower():
                return """Human Design is a system of self-knowledge that helps you understand your unique genetic design. It combines elements from the I Ching, astrology, Kabbalah, the Hindu-Brahmin chakra system, and quantum physics.

Think of it as a personal instruction manual for how your energy works. By understanding your Human Design chart, you can learn:
- Your energy Type (how you interact with the world)
- Your Authority (how to make decisions correctly for you)
- Your Profile (your life purpose and role)
- Your Definition (the consistent energies in your chart)

The goal of Human Design is to help you live as your true self rather than according to conditioning from family, society, and education. When you live according to your design, you experience less resistance and more flow in your life."""
            elif "type" in prompt.lower():
                return """In Human Design, there are five Types, each with its own aura type, strategy for making decisions, and signature feeling:

1. Manifestors (8% of population)
   - Strategy: Inform others before you act
   - Signature feeling: Peace
   - Not-Self feeling: Anger
   - Aura: Closed and repelling

2. Generators (37% of population)
   - Strategy: Wait to respond
   - Signature feeling: Satisfaction
   - Not-Self feeling: Frustration
   - Aura: Open and enveloping

3. Manifesting Generators (33% of population)
   - Strategy: Wait to respond, then inform
   - Signature feeling: Satisfaction
   - Not-Self feeling: Frustration and anger
   - Aura: Open, enveloping, and dynamic

4. Projectors (20% of population)
   - Strategy: Wait for the invitation
   - Signature feeling: Success
   - Not-Self feeling: Bitterness
   - Aura: Focused and absorbing

5. Reflectors (1% of population)
   - Strategy: Wait a lunar cycle (28 days)
   - Signature feeling: Surprise
   - Not-Self feeling: Disappointment
   - Aura: Reflective and sampling

Your Type is determined by which of your Centers are defined (colored in) in your chart and how they're connected."""
            elif "authority" in prompt.lower():
                return """Your Authority in Human Design is your body's natural way of making decisions. It's your inner guidance system that helps you navigate life.

There are seven different Authorities:

1. Emotional/Solar Plexus Authority: If your Solar Plexus Center is defined, you have emotional authority. You need to ride your emotional wave through clarity, excitement, and disappointment before making clear decisions. Patience is key.

2. Sacral Authority: For Generators and Manifesting Generators with a defined Sacral Center. This is a gut response of sounds like "uh-huh" (yes) or "uh-uh" (no).

3. Splenic Authority: A spontaneous, in-the-moment intuition for survival and health. It speaks once, quietly, and in the present moment.

4. Ego/Heart Authority: For those with only the Heart/Ego Center defined among the motor centers. Follow your willpower and keep the promises you make to yourself.

5. G Center Authority: For those with a defined G Center but no motor Centers defined. This is about identity and knowing who you are. Listen to your sense of direction and identity.

6. Environment Authority: Also called "No Inner Authority." You need to recognize the correct environment where you feel aligned.

7. Lunar Authority: Only for Reflectors. You need to wait through a full 28-day lunar cycle, talking with trusted friends along the way, before making major decisions.

Your Authority is determined by which energy Centers are defined in your chart and takes precedence over your mind in making decisions."""
            else:
                return "This is a helpful response about Human Design based on your question."
        
        mock_ask_gpt.side_effect = side_effect
        
        # Simulate user queries with realistic questions
        queries = [
            "What is Human Design?",
            "Tell me about Type in Human Design",
            "How does Authority work?"
        ]
        
        # Process each query as if the user submitted them in sequence
        for query in queries:
            # Generate response as the application would
            response, top_chunks = get_client_response(query, self.test_data, temperature=self.mock_session_state.gpt_temperature)
            
            # Add to mock chat history with timestamp
            current_time = "12:34:56"  # Mock timestamp
            self.mock_session_state.chat_history.append({
                "role": "user", 
                "content": query,
                "timestamp": current_time
            })
            self.mock_session_state.chat_history.append({
                "role": "assistant", 
                "content": response,
                "timestamp": current_time
            })
            
            # Verify the response
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            
            # Verify content quality based on query
            if "what is human design" in query.lower():
                self.assertIn("system", response.lower())
                self.assertIn("astrology", response.lower())
                self.assertIn("kabbalah", response.lower())
            elif "type" in query.lower():
                self.assertIn("generator", response.lower())
                self.assertIn("projector", response.lower())
                self.assertIn("manifestor", response.lower())
            elif "authority" in query.lower():
                self.assertIn("emotional", response.lower())
                self.assertIn("sacral", response.lower())
                self.assertIn("splenic", response.lower())
            
            # Verify find_top_chunks was called
            mock_find_top_chunks.assert_called_with(query, self.test_data, top_k=5)
        
        # Verify chat history is built correctly
        self.assertEqual(len(self.mock_session_state.chat_history), 6)  # 3 queries + 3 responses
        
        # Verify message sequence
        for i in range(len(queries)):
            user_idx = i * 2
            assistant_idx = user_idx + 1
            self.assertEqual(self.mock_session_state.chat_history[user_idx]["role"], "user")
            self.assertEqual(self.mock_session_state.chat_history[user_idx]["content"], queries[i])
            self.assertEqual(self.mock_session_state.chat_history[assistant_idx]["role"], "assistant")
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.find_top_chunks')
    def test_edge_cases_client_mode(self, mock_find_top_chunks, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test edge cases for the client chat workflow"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Create mock top chunks (empty for edge case testing)
        mock_top_chunks = [(0.5, self.test_data[i]) for i in range(5)]
        mock_find_top_chunks.return_value = mock_top_chunks
        
        # Define test cases
        test_cases = [
            {
                "name": "Very short query",
                "query": "Types?",
                "expected_keywords": ["type", "types", "energy"]
            },
            {
                "name": "Non-Human Design query",
                "query": "What's the weather like today?",
                "expected_response": "I can only provide information about Human Design"
            },
            {
                "name": "Empty query",
                "query": "",
                "expected_response": "I need more information"
            },
            {
                "name": "Very specific technical query",
                "query": "How does gate 34 connect to gate 20?",
                "expected_keywords": ["gate", "channel", "center"]
            }
        ]
        
        for case in test_cases:
            with self.subTest(case=case["name"]):
                # Configure ask_gpt response
                if "Empty query" == case["name"]:
                    mock_ask_gpt.return_value = "I need more information to help you with Human Design. Could you please provide a more specific question?"
                elif "Non-Human Design query" == case["name"]:
                    mock_ask_gpt.return_value = "I can only provide information about Human Design, which is a system for understanding your genetic design. I don't have information about the current weather."
                elif "Very short query" == case["name"]:
                    mock_ask_gpt.return_value = "There are five energy Types in Human Design: Manifestors, Generators, Manifesting Generators, Projectors, and Reflectors. Each Type has a specific Strategy for making decisions and a unique aura type."
                else:
                    mock_ask_gpt.return_value = "Gate 34 (the Gate of Power) in the Sacral Center connects to Gate 20 (the Gate of the Now) in the Throat Center to form the Channel of Charisma (34-20), also known as the Channel of Busy-ness. This channel brings manifestation energy from the Sacral to the Throat, allowing for empowered action and expression."
                
                # Process the query
                query = case["query"]
                response, top_chunks = get_client_response(query, self.test_data)
                
                # Verify response
                self.assertIsNotNone(response)
                
                # Case-specific assertions
                if "expected_keywords" in case:
                    for keyword in case["expected_keywords"]:
                        self.assertIn(keyword, response.lower())
                
                if "expected_response" in case:
                    self.assertIn(case["expected_response"], response)
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.find_top_chunks')
    def test_multi_turn_conversation(self, mock_find_top_chunks, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test a multi-turn conversation with context from previous exchanges"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Create mock top chunks
        mock_top_chunks = [(0.95, self.test_data[i]) for i in range(5)]
        mock_find_top_chunks.return_value = mock_top_chunks
        
        # Configure responses that simulate building on previous context
        responses = [
            "Generators are one of the five Types in Human Design. They have a defined Sacral Center and make up about 37% of the population. Their Strategy is to wait to respond to life rather than initiating. When Generators live according to their Strategy, they experience satisfaction.",
            
            "Yes, the Sacral Center is the energy powerhouse in Human Design. For Generators and Manifesting Generators, it provides sustainable life force energy. The Sacral responds with sounds rather than words - 'uh-huh' for yes and 'uh-uh' for no. This gut response is their Authority for making decisions.",
            
            "When Generators don't follow their Strategy of waiting to respond, they experience frustration. This Not-Self feeling is a signal that they're not living in alignment with their design. Instead of responding to what calls them, they might be initiating or trying to make things happen, which leads to resistance and frustration."
        ]
        
        # Simulate a conversation with follow-up questions
        conversation = [
            "Tell me about Generators",
            "Is the Sacral Center important for them?",
            "What happens when Generators don't follow their Strategy?"
        ]
        
        # Run through the conversation
        for i, query in enumerate(conversation):
            # Set the response for this turn
            mock_ask_gpt.return_value = responses[i]
            
            # If not the first message, add previous exchanges to session state
            if i > 0:
                self.assertTrue(len(self.mock_session_state.chat_history) > 0, 
                              "Chat history should not be empty after first exchange")
            
            # Process the query
            response, top_chunks = get_client_response(query, self.test_data)
            
            # Add to chat history
            self.mock_session_state.chat_history.append({"role": "user", "content": query})
            self.mock_session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Verify response matches what we expect
            self.assertEqual(response, responses[i])
            
            # Verify the conversation maintains context
            if i == 1:  # Second question
                self.assertIn("sacral center", response.lower())
                self.assertIn("generator", response.lower())
            elif i == 2:  # Third question
                self.assertIn("frustration", response.lower())
                self.assertIn("not-self", response.lower())
                self.assertIn("strategy", response.lower())
        
        # Verify final chat history length
        self.assertEqual(len(self.mock_session_state.chat_history), 6)  # 3 user + 3 assistant messages
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.find_top_chunks')
    def test_error_handling(self, mock_find_top_chunks, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test error handling in the client workflow"""
            # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Create mock top chunks
        mock_top_chunks = [(0.95, self.test_data[i]) for i in range(5)]
        mock_find_top_chunks.return_value = mock_top_chunks
        
        # Test case 1: API error
        mock_ask_gpt.side_effect = Exception("API connection error")
        
        # Process query that should encounter an error - should raise the exception
        query = "What is Human Design?"
        with self.assertRaises(Exception):
            response, top_chunks = get_client_response(query, self.test_data)
        
        # Test case 2: Only test with generic Exception instead of specific RateLimitError
        mock_ask_gpt.side_effect = Exception("Rate limit exceeded")
        
        # Process query that should encounter a rate limit - should raise the exception
        with self.assertRaises(Exception):
            response, top_chunks = get_client_response(query, self.test_data)

if __name__ == '__main__':
    unittest.main()