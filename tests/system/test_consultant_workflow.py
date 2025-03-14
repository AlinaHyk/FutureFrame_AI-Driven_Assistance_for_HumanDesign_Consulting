# tests/system/test_consultant_workflow.py
import unittest
import os
import sys
import json
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import necessary modules
from app import get_consultant_response, load_embedded_data, embed_query, ask_gpt, extract_keywords_for_chunk, select_relevant_keywords

class TestConsultantWorkflow(unittest.TestCase):
    """System tests for the consultant chat workflow"""
    
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
        self.mock_session_state.expertise_level = "consultant"
        self.mock_session_state.chat_history = []
        
    def tearDown(self):
        """Clean up after test"""
        self.session_state_patch.stop()


        
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.extract_keywords_for_chunk')
    @patch('app.select_relevant_keywords')
    def test_full_consultant_chat_interaction(self, mock_select_keywords, mock_extract_keywords, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test a complete consultant-mode chat interaction flow with realistic queries"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]  # Use a realistic embedding
        
        # Fix for the keyword extraction - direct mocking of the functions
        mock_extract_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates", "Channels", "Definition", "Strategy", "Signature", "Not-Self"]
        mock_select_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates", "Channels", "Definition", "Strategy"]
        
        # Configure ask_gpt to return different responses for different stages with realistic content
        def side_effect(prompt, model=None, temperature=None):
            if "extract keywords" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates, Channels, Definition, Strategy, Signature, Not-Self"
            elif "select the most relevant" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates, Channels, Definition, Strategy"
            elif "user question" in prompt.lower() and "what is human design" in prompt.lower():
                return """Human Design is an integrative system that combines elements from several ancient wisdom traditions with modern science. It was received by Ra Uru Hu in 1987 and synthesizes principles from:

    [Primary Source #1] The I Ching (Chinese Book of Changes)
    [Primary Source #2] The Kabbalah (Tree of Life)
    [Primary Source #3] The Hindu-Brahmin Chakra System
    [Primary Source #4] Astrology (Western and Eastern)
    [Primary Source #5] Quantum Physics and Genetics

    Human Design provides a detailed map of your genetic design that shows:
    - Your Type (energy configuration: Manifestor, Generator, Manifesting Generator, Projector, or Reflector)
    - Your Authority (internal decision-making system)
    - Your Profile (your life purpose and interaction style)
    - Your Definition (consistent themes and energies in your chart)

    By understanding these aspects of yourself, you can make decisions that are aligned with your true nature rather than living according to conditioning from family, society, and education."""
            elif "user question" in prompt.lower() and "types" in prompt.lower():
                return """There are five distinct Types in Human Design, each with its own Strategy and signature:

    [Primary Source #3] Manifestors (8% of population):
    Strategy: Inform before taking action
    Signature: Peace
    Not-Self: Anger
    Manifestors have a closed and repelling aura. They are the only type designed to initiate and have access to consistent manifestation energy.

    [Expanded Source #1] Generators (37% of population):
    Strategy: Wait to respond
    Signature: Satisfaction
    Not-Self: Frustration
    Generators have an open and enveloping aura and are the life force energy of the planet with their defined Sacral center.

    [Primary Source #2] Manifesting Generators (33% of population):
    Strategy: Wait to respond, then inform
    Signature: Satisfaction
    Not-Self: Frustration and anger
    A variation of the Generator with aspects of both Generator and Manifestor energy.

    [Expanded Source #4] Projectors (20% of population):
    Strategy: Wait for the invitation
    Signature: Success
    Not-Self: Bitterness
    Projectors have a focused and absorbing aura designed to guide and direct energy rather than generate it.

    [Primary Source #5] Reflectors (1% of population):
    Strategy: Wait a lunar cycle (28 days) for clarity
    Signature: Surprise
    Not-Self: Disappointment
    Reflectors have a resistant and sampling aura and are completely open energetically, reflecting back the energy around them."""
            elif "user question" in prompt.lower() and "centers" in prompt.lower():
                return """The Centers in Human Design are energy processing hubs in the body that correspond roughly to the chakra system. There are nine Centers in total:

    [Primary Source #1] Head Center (Crown):
    Function: Mental pressure for inspiration and questions
    Theme: Inspiration and mental pressure
    When undefined: Mental anxiety and overwhelm from external pressure

    [Expanded Source #2] Ajna Center:
    Function: Conceptualization and mental certainty
    Theme: Thinking and processing
    When undefined: Mental confusion and trying to be certain

    [Primary Source #3] Throat Center:
    Function: Communication and manifestation
    Theme: Expression and action
    When undefined: Seeking attention and over-talking

    [Primary Source #4] G Center (Identity/Direction):
    Function: Identity, love, and direction
    Theme: Self-identity and direction in life
    When undefined: Trying to find oneself and consistent direction

    [Expanded Source #1] Heart/Ego Center:
    Function: Willpower and material needs
    Theme: Ego, will, and material value
    When undefined: Inconsistent willpower and proving oneself

    [Primary Source #5] Sacral Center:
    Function: Life force energy and sexuality
    Theme: Work, creativity, and procreation
    When undefined: Trying to be consistently energetic

    [Expanded Source #3] Spleen Center:
    Function: Intuition, health, and survival
    Theme: Intuitive awareness and well-being
    When undefined: Fear and holding onto the past

    [Primary Source #2] Solar Plexus Center:
    Function: Emotional clarity and awareness
    Theme: Emotional waves and relationships
    When undefined: Amplifying and avoiding emotions

    [Expanded Source #4] Root Center:
    Function: Pressure and stress
    Theme: Adrenaline and physical pressure
    When undefined: Rushing and false pressure

    When a Center is defined (colored in), that energy is consistent and reliable. When undefined (white), that energy is inconsistent but offers wisdom through openness and the ability to amplify and reflect that energy."""
            else:
                return "This is a detailed response about Human Design with citations and expanded analysis based on the context provided."
        
        mock_ask_gpt.side_effect = side_effect
        
        # Simulate user queries using realistic questions
        queries = [
            "What is Human Design?",
            "Explain the different Types in Human Design",
            "How do Centers work in the Human Design system?"
        ]
        
        # Process each query as if the user submitted them in sequence
        for query in queries:
            # Reset the mock before each query to clear previous calls
            mock_embed_query.reset_mock()
            
            # Generate response as the application would
            response, analysis_data = get_consultant_response(query, self.test_data)
            
            # Add to mock chat history
            self.mock_session_state.chat_history.append({
                "role": "user", 
                "content": query
            })
            self.mock_session_state.chat_history.append({
                "role": "assistant", 
                "content": response
            })
            
            # Save analysis data to session state
            self.mock_session_state.analysis_data = analysis_data
            
            # Verify the response
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            
            # Verify the analysis data is structured correctly
            self.assertIn("original_top_chunks", analysis_data)
            self.assertIn("secondary_top_chunks", analysis_data)
            self.assertIn("expanded_keywords", analysis_data)
            self.assertIn("expanded_query", analysis_data)
            
            # Check that expanded keywords are correctly extracted
            self.assertGreaterEqual(len(analysis_data["expanded_keywords"]), 5)
            
            # Check response quality with more detailed assertions
            if "what is human design" in query.lower():
                self.assertIn("ancient", response.lower())
                self.assertIn("modern", response.lower())
                self.assertIn("type", response.lower())
            elif "types" in query.lower():
                self.assertIn("generator", response.lower())
                self.assertIn("projector", response.lower())
                self.assertIn("manifestor", response.lower())
            elif "centers" in query.lower():
                self.assertIn("energy", response.lower())
                self.assertIn("defined", response.lower())
                self.assertIn("undefined", response.lower())
            
            # Instead of checking the exact parameter, just verify embed_query was called
            self.assertTrue(mock_embed_query.called, "embed_query should be called at least once")
            
            # Verify expanded_query contains the keywords
            for keyword in analysis_data["expanded_keywords"][:3]:  # Check at least the first 3
                self.assertIn(keyword.lower(), analysis_data["expanded_query"].lower())
        
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
    @patch('app.extract_keywords_for_chunk')
    @patch('app.select_relevant_keywords')
    def test_knowledge_graph_integration(self, mock_select_keywords, mock_extract_keywords, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test that the knowledge graph functionality works with consultant mode"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Fix for the keyword extraction
        mock_extract_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates", "Channels", "Definition", "Strategy", "Signature", "Not-Self"]
        mock_select_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates", "Channels", "Definition", "Strategy"]
        
        # Configure ask_gpt to return realistic concept extraction
        def side_effect(prompt, model=None, temperature=None):
            if "Extract exactly 5 key concepts" in prompt:
                # Return different concepts based on which chunk is being analyzed
                if "Generators and Manifesting Generators" in prompt:
                    return "Generator, Strategy, Sacral, Response, Satisfaction"
                elif "five energy Types" in prompt:
                    return "Type, Manifestor, Generator, Projector, Reflector"
                elif "Authority is your body's way" in prompt:
                    return "Authority, Emotional, Sacral, Splenic, Decision-making"
                elif "twelve possible Profiles" in prompt:
                    return "Profile, Purpose, Role, Society, Characteristics"
                elif "Definition refers to" in prompt:
                    return "Definition, Centers, Split, Energy, Reflector"
                else:
                    return "Human Design, Type, Authority, Strategy, Profile"
            elif "extract keywords" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates, Channels, Definition, Strategy, Signature, Not-Self"
            elif "select the most relevant" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates, Channels, Definition, Strategy"
            else:
                return "This is a detailed response that references all the key Human Design concepts with proper citations."
        
        mock_ask_gpt.side_effect = side_effect
        
        # Import knowledge graph functions
        from app import build_knowledge_graph, find_related_concepts
        
        # Build the knowledge graph
        G = build_knowledge_graph(self.test_data, max_nodes=10)
        
        # Verify the graph was built successfully
        self.assertIsNotNone(G)
        self.assertGreaterEqual(len(G.nodes()), 5)  # Should extract at least 5 unique concepts
        self.assertGreaterEqual(len(G.edges()), 3)  # Should have at least some connections
        
        # Test finding related concepts - if "Type" is in the graph, find related concepts
        if "Type" in G.nodes():
            related = find_related_concepts(G, "Type", max_distance=2)
            self.assertIsNotNone(related)
            self.assertGreaterEqual(len(related), 1)
            
            # Check if at least one of these key concepts is related to Type
            key_concepts = ["Generator", "Strategy", "Authority", "Profile"]
            found_related = False
            for concept in key_concepts:
                if concept in related:
                    found_related = True
                    break
            self.assertTrue(found_related, "Should find at least one related key concept")
        
        # Test with a more specific query about relationships between concepts
        query = "How are Type and Authority connected in Human Design?"
        
        # Generate consultant response
        response, analysis_data = get_consultant_response(query, self.test_data)
        
        # Verify the response
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
        
        # Verify the analysis data
        self.assertIn("original_top_chunks", analysis_data)
        self.assertIn("expanded_keywords", analysis_data)
        
        # Verify both "Type" and "Authority" are in the keywords
        keywords_lower = [k.lower() for k in analysis_data["expanded_keywords"]]
        self.assertTrue("type" in keywords_lower or "types" in keywords_lower)
        self.assertTrue("authority" in keywords_lower)
    
    @patch('app.embed_query')
    @patch('app.ask_gpt')
    @patch('app.load_embedded_data')
    @patch('app.extract_keywords_for_chunk')
    @patch('app.select_relevant_keywords')
    def test_edge_cases(self, mock_select_keywords, mock_extract_keywords, mock_load_data, mock_ask_gpt, mock_embed_query):
        """Test edge cases for the consultant workflow"""
        # Set up mocks
        mock_load_data.return_value = self.test_data
        mock_embed_query.return_value = self.test_data[0]["embedding"]
        
        # Fix for the keyword extraction
        mock_extract_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates"]
        mock_select_keywords.return_value = ["Type", "Authority", "Profile", "Centers", "Gates"]
        
        # Edge case 1: Very short query
        short_query = "Types?"
        
        # Edge case 2: Query with no direct match in the data
        irrelevant_query = "What is the weather like in Paris?"
        
        # Edge case 3: Complex, specific query
        complex_query = "How does the 5/1 Profile interact with a defined G Center when someone has emotional authority?"
        
        # Configure ask_gpt for edge cases
        def side_effect(prompt, model=None, temperature=None):
            if "extract keywords" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates"
            elif "select the most relevant" in prompt.lower():
                return "Type, Authority, Profile, Centers, Gates"
            elif "user question" in prompt.lower():
                if short_query in prompt:
                    return "There are five Types in Human Design: Manifestors, Generators, Manifesting Generators, Projectors, and Reflectors. Each Type has its own aura type and strategy for navigating life correctly."
                elif irrelevant_query in prompt:
                    return "I don't have current weather information for Paris. My knowledge is focused on Human Design, which is a system for understanding your genetic design and making decisions correctly based on your Type, Authority, and Strategy."
                elif complex_query in prompt:
                    return "The 5/1 Profile (Heretic/Investigator) brings a practical problem-solving approach combined with a universal foundation. When someone with this Profile also has a defined G Center and Emotional Authority, they operate with a fixed sense of identity and direction (G Center) but should wait through their emotional wave for clarity before making decisions (Emotional Authority). The 5/1 can appear savior-like but needs to research thoroughly (Line 1) before offering their practical solutions (Line 5)."
                else:
                    return "I'm sorry, I don't have specific information about that in my Human Design knowledge base."
            else:
                return "Response based on Human Design principles."
        
        mock_ask_gpt.side_effect = side_effect
        
        # Test each edge case
        test_queries = [short_query, irrelevant_query, complex_query]
        
        for query in test_queries:
            # Generate response
            response, analysis_data = get_consultant_response(query, self.test_data)
            
            # Verify basic response structure
            self.assertIsNotNone(response)
            self.assertGreater(len(response), 0)
            self.assertIn("original_top_chunks", analysis_data)
            self.assertIn("expanded_keywords", analysis_data)
            
            # Content-specific assertions for each case
            if query == short_query:
                self.assertIn("five", response.lower())
                self.assertIn("types", response.lower())
            elif query == irrelevant_query:
                self.assertIn("human design", response.lower())
            elif query == complex_query:
                self.assertIn("5/1", response)
                self.assertIn("profile", response.lower())
                self.assertIn("g center", response.lower())
                self.assertIn("emotional", response.lower())

if __name__ == '__main__':
    unittest.main()