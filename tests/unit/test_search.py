# tests/unit/test_search.py
import unittest
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Add this near the top of your script, before any tests run
import os
# Create visualizations directory
os.makedirs('tests/visualizations', exist_ok=True)

# Fix the path to properly import app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)  # Insert at beginning of path

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

try:
    # Now import app modules
    from app import cosine_similarity, find_top_chunks, embed_query, ask_gpt
    from app import get_client_response, get_consultant_response
    print("Successfully imported app modules")
except ImportError as e:
    print(f"ERROR importing app modules: {e}")

# Add the parent directory to the path (adjust this based on your folder structure)
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)
print(f"Added to path: {parent_dir}")

# Now try to import
from app import get_client_response, get_consultant_response, embed_query, ask_gpt

# Adds parent directory to path to import application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import relevant functions from app.py
from app import cosine_similarity, find_top_chunks, embed_query, ask_gpt
from app import get_client_response, get_consultant_response

os.makedirs('tests/visualizations_search', exist_ok=True)

class TestSearchBasic(unittest.TestCase):
    """Basic tests for the search functionality"""
    
    def test_cosine_similarity(self):
        """Test the cosine similarity calculation"""
        # Test with orthogonal vectors (should be 0)
        vec_a = [1, 0, 0, 0]
        vec_b = [0, 1, 0, 0]
        self.assertEqual(cosine_similarity(vec_a, vec_b), 0)
        
        # Test with identical vectors (should be 1)
        vec_c = [0.5, 0.5, 0.5, 0.5]
        self.assertEqual(cosine_similarity(vec_c, vec_c), 1)
        
        # Test with known similarity
        vec_d = [1, 1, 0, 0]
        vec_e = [1, 0, 0, 0]
        self.assertAlmostEqual(cosine_similarity(vec_d, vec_e), 1/np.sqrt(2))

        self._visualize_similarity_cases()
    
    def _visualize_similarity_cases(self):
        """Create visualization of similarity cases"""
        # Define sample vectors
        vectors = [
            ([1, 0, 0, 0], [1, 0, 0, 0], "Identical"),
            ([1, 0, 0, 0], [0, 1, 0, 0], "Orthogonal"),
            ([1, 0, 0, 0], [0.7, 0.7, 0, 0], "Partial similarity"),
            ([1, 0, 0, 0], [-1, 0, 0, 0], "Opposite"),
            ([0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], "Identical normalized"),
        ]
        
        # Calculate similarities
        similarities = [cosine_similarity(v1, v2) for v1, v2, _ in vectors]
        labels = [label for _, _, label in vectors]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(labels, similarities, color='skyblue')
        plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        plt.ylim(-1.1, 1.1)
        plt.ylabel('Cosine Similarity')
        plt.title('Cosine Similarity Between Different Vector Pairs')
        
        # Save visualization
        plt.savefig('tests/visualizations/cosine_similarity_cases.png')
        plt.close()
    
    @patch('app.embed_query')
    def test_find_top_chunks_basic(self, mock_embed_query):
        """Test finding top chunks based on query relevance (basic case)"""
        # Mock the embedding function
        mock_embed_query.return_value = [1, 0, 0, 0]
        
        # Create test embedded data
        test_data = [
            {"chunk_text": "This is about topic A", "embedding": [1, 0, 0, 0]},
            {"chunk_text": "This is about topic B", "embedding": [0, 1, 0, 0]},
            {"chunk_text": "This is about topic C", "embedding": [0, 0, 1, 0]},
        ]
        
        # Find top chunks for a query
        results = find_top_chunks("Test query", test_data, top_k=2)
        
        # Verify 2 results returned
        self.assertEqual(len(results), 2)
        
        # Check that results are ordered by similarity (highest first)
        self.assertEqual(results[0][1]["chunk_text"], "This is about topic A")
        self.assertEqual(results[1][1]["chunk_text"], "This is about topic B")
        
        # Visualize the results
        self._visualize_basic_search_results(results)
    
    def _visualize_basic_search_results(self, results):
        """Create visualization of basic search results"""
        # Extract data
        texts = [result[1]["chunk_text"] for result in results]
        scores = [result[0] for result in results]
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        plt.bar(texts, scores, color='lightgreen')
        plt.ylabel('Similarity Score')
        plt.title('Basic Search Results - Top Chunks by Similarity')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save visualization
        plt.savefig('tests/visualizations/basic_search_results.png')
        plt.close()


class TestSearchIntermediate(unittest.TestCase):
    """Intermediate tests for the search functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create varied test data with 10 items
        self.test_data = []
        for i in range(10):
            # Create various embedding patterns
            if i < 3:
                # First 3 items are similar to query [1,0,0,0]
                embedding = [0.9 - (i * 0.2), 0.1 + (i * 0.1), 0, 0]
            elif i < 6:
                # Next 3 are somewhat similar
                embedding = [0.5 - (i * 0.1), 0.5 + (i * 0.1), 0, 0]
            else:
                # Last 4 are not similar
                embedding = [0.1, 0.1, 0.8 - ((i-6) * 0.1), (i-6) * 0.2]
            
            self.test_data.append({
                "chunk_text": f"This is test chunk {i+1}",
                "embedding": embedding,
                "metadata": {"chunk_index": i}
            })
    
    @patch('app.embed_query')
    def test_find_top_chunks_varied(self, mock_embed_query):
        """Test finding top chunks with more varied data"""
        # Mock query embedding
        mock_embed_query.return_value = [1, 0, 0, 0]
        
        # Get top 5 chunks
        results = find_top_chunks("Test query", self.test_data, top_k=5)
        
        # Verify correct number of results
        self.assertEqual(len(results), 5)
        
        # First result should be most similar to [1,0,0,0]
        self.assertEqual(results[0][1]["metadata"]["chunk_index"], 0)
        
        # Scores should be in descending order
        for i in range(1, len(results)):
            self.assertGreaterEqual(results[i-1][0], results[i][0])
        
        # Visualize results
        self._visualize_intermediate_search_results(results)
    
    def _visualize_intermediate_search_results(self, results):
        """Create visualization of intermediate search results"""
        # Extract data
        chunk_indices = [result[1]["metadata"]["chunk_index"] + 1 for result in results]
        scores = [result[0] for result in results]
        
        # Prepare data for visualization
        sorted_data = sorted(zip(chunk_indices, scores), key=lambda x: x[1], reverse=True)
        chunk_indices = [f"Chunk {idx}" for idx, _ in sorted_data]
        scores = [score for _, score in sorted_data]
        
        # Create horizontal bar chart
        plt.figure(figsize=(10, 6))
        plt.barh(chunk_indices, scores, color='coral')
        plt.xlabel('Similarity Score')
        plt.title('Intermediate Search Results - Top Chunks by Similarity')
        plt.tight_layout()
        
        # Save visualization
        plt.savefig('tests/visualizations/intermediate_search_results.png')
        plt.close()
    
    @patch('app.embed_query')
    def test_find_top_chunks_threshold(self, mock_embed_query):
        """Test finding chunks above certain similarity threshold"""
        # Mock query embedding
        mock_embed_query.return_value = [1, 0, 0, 0]
        
        # Get all top chunks
        all_results = find_top_chunks("Test query", self.test_data, top_k=10)
        
        # Filter results above threshold (0.7)
        threshold = 0.7
        above_threshold = [r for r in all_results if r[0] >= threshold]
        
        # Visualize threshold-based filtering
        self._visualize_threshold_filtering(all_results, threshold)
        
        # Test assertions
        self.assertGreaterEqual(len(above_threshold), 1)  # At least one result should be above threshold
        for result in above_threshold:
            self.assertGreaterEqual(result[0], threshold)
    
    def _visualize_threshold_filtering(self, results, threshold):
        """Create visualization of threshold-based filtering"""
        # Extract data
        chunk_indices = [result[1]["metadata"]["chunk_index"] + 1 for result in results]
        scores = [result[0] for result in results]
        
        # Create colors based on threshold
        colors = ['green' if score >= threshold else 'lightgray' for score in scores]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(1, len(chunk_indices) + 1), scores, color=colors)
        plt.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold ({threshold})')
        
        # Count chunks above threshold
        above_count = sum(1 for score in scores if score >= threshold)
        
        plt.xlabel('Chunk Index')
        plt.ylabel('Similarity Score')
        plt.title(f'Threshold Filtering - {above_count} Chunks Above Threshold')
        plt.legend()
        plt.xticks(range(1, len(chunk_indices) + 1), [f"Chunk {idx}" for idx in chunk_indices])
        plt.tight_layout()
        
        # Save visualization
        plt.savefig('tests/visualizations/threshold_filtering.png')
        plt.close()


class TestSearchAdvanced(unittest.TestCase):
    """Advanced tests for the search functionality"""
    
    def setUp(self):
        """Set up test data"""
        # Create a synthetic document collection with topic clusters
        np.random.seed(42)  # For reproducibility
        
        topics = {
            "Human Design": [0.9, 0.1, 0.0, 0.0, 0.0],
            "Type": [0.3, 0.8, 0.1, 0.0, 0.0],
            "Authority": [0.2, 0.2, 0.9, 0.0, 0.0],
            "Profile": [0.1, 0.1, 0.1, 0.9, 0.0],
            "Centers": [0.1, 0.1, 0.1, 0.1, 0.9]
        }
        
        self.test_data = []
        chunk_index = 0
        
        for topic, base_vector in topics.items():
            # Generate 5 documents for each topic with some variance
            for i in range(5):
                # Create a variation of the base vector with some noise
                noise = np.random.uniform(-0.1, 0.1, len(base_vector))
                vector = np.clip(np.array(base_vector) + noise, 0, 1).tolist()
                
                # Normalize to ensure it's a unit vector
                magnitude = np.sqrt(sum(v**2 for v in vector))
                normalized_vector = [v/magnitude for v in vector]
                
                self.test_data.append({
                    "chunk_text": f"This document is about {topic} - variation {i+1}",
                    "embedding": normalized_vector,
                    "metadata": {
                        "chunk_index": chunk_index,
                        "topic": topic
                    }
                })
                chunk_index += 1
    
    @patch('app.embed_query')
    def test_topic_based_search(self, mock_embed_query):
        """Test search across different topics"""
        # Test queries for different topics
        queries = {
            "Human Design": [0.9, 0.1, 0.0, 0.0, 0.0],
            "Type": [0.3, 0.8, 0.1, 0.0, 0.0],
            "Authority": [0.2, 0.2, 0.9, 0.0, 0.0]
        }
        
        all_results = {}
        
        for topic, query_vector in queries.items():
            # Set the mock to return this query vector
            mock_embed_query.return_value = query_vector
            
            # Get top results
            results = find_top_chunks(f"Tell me about {topic}", self.test_data, top_k=5)
            all_results[topic] = results
            
            # Verify the top result is from the expected topic
            top_result_topic = results[0][1]["metadata"]["topic"]
            self.assertEqual(top_result_topic, topic)
        
        # Visualize topic-based search results
        self._visualize_topic_based_search(all_results)
    
    def _visualize_topic_based_search(self, all_results):
        """Create visualization of topic-based search results"""
        plt.figure(figsize=(15, 10))
        
        # Set up the plot
        topics = list(all_results.keys())
        num_topics = len(topics)
        num_results = len(all_results[topics[0]])
        
        # Create position arrays
        ind = np.arange(num_results)
        width = 0.25
        
        # Plot bars for each topic query
        for i, topic in enumerate(topics):
            results = all_results[topic]
            scores = [result[0] for result in results]
            result_topics = [result[1]["metadata"]["topic"] for result in results]
            
            # Create colors based on whether result topic matches query topic
            colors = ['green' if rt == topic else 'lightgray' for rt in result_topics]
            
            # Offset the bars
            offset = (i - num_topics/2 + 0.5) * width
            plt.bar(ind + offset, scores, width, label=f'Query: {topic}', color=colors, alpha=0.7)
        
        # Add labels and legend
        plt.ylabel('Similarity Score')
        plt.title('Topic-Based Search Results')
        plt.xticks(ind, [f'Result {i+1}' for i in range(num_results)])
        plt.legend()
        plt.tight_layout()
        
        # Save visualization
        plt.savefig('tests/visualizations/topic_based_search.png')
        plt.close()
    

if __name__ == '__main__':
    unittest.main()