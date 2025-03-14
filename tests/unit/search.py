import unittest
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Create visualizations directory
os.makedirs('tests/visualizations', exist_ok=True)

# Fix the path to properly import app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)  # Insert at beginning of path

print(f"Current directory: {os.getcwd()}")

try:
    # Now import app modules
    from app import cosine_similarity, find_top_chunks, embed_query, ask_gpt
    from app import get_client_response, get_consultant_response
    print("Successfully imported app modules")
except ImportError as e:
    print(f"ERROR importing app modules: {e}")

def compare_client_consultant_keywords():
    """Make actual calls to client and consultant functions and compare keywords"""
    
    # Create sample test data with embeddings
    test_data = []
    for i in range(20):
        vector = [0.1] * 1536  # Standard size for OpenAI embeddings
        test_data.append({
            "chunk_text": f"This is sample text about Human Design concept {i}",
            "embedding": vector,
            "metadata": {"chunk_index": i}
        })
    
    # Since we can't actually call OpenAI in a test, we'll mock the functions
    with patch('app.embed_query') as mock_embed:
        with patch('app.ask_gpt') as mock_ask:
            # Setup mocks
            mock_embed.return_value = [0.1] * 1536
            
            # We need to provide enough responses for all potential ask_gpt calls
            mock_responses = [
                # Client response
                "This is a basic response about Human Design.",
                
                # Consultant responses for keyword extraction (multiple chunks)
                "Type, Authority, Profile, Centers, Gates",
                "Type, Authority, Profile, Centers, Gates",
                "Type, Authority, Profile, Centers, Gates",
                "Type, Authority, Profile, Centers, Gates",
                "Type, Authority, Profile, Centers, Gates",
                
                # Consultant keyword selection
                "Type, Authority, Profile, Centers, Gates, Channels, Definition, Strategy",
                
                # Final consultant response
                "This is a detailed response about Human Design."
            ]
            
            # Use side_effect with a function that returns from the list but never raises StopIteration
            def get_response(*args, **kwargs):
                if not mock_responses:
                    return "Generic response"
                return mock_responses.pop(0) if mock_responses else "Generic response"
                
            mock_ask.side_effect = get_response
            
            try:
                # Client call
                client_response, client_chunks = get_client_response("What is Human Design?", test_data)
                print("Client response generated successfully")
                
                # Consultant call
                consultant_response, analysis_data = get_consultant_response("What is Human Design?", test_data)
                print("Consultant response generated successfully")
                
                # Get the expanded keywords from consultant mode
                consultant_keywords = analysis_data.get("expanded_keywords", [])
                if not consultant_keywords:
                    print("No consultant keywords found, using sample data")
                    consultant_keywords = ["Type", "Authority", "Profile", "Centers", "Gates", "Channels", "Definition", "Strategy"]
                
                # Since client mode doesn't extract keywords, we'll use keywords from the query
                client_keywords = ["Human", "Design"]
                
                # Create visualization
                plt.figure(figsize=(14, 8))
                
                # Display client keywords
                ax1 = plt.subplot(1, 2, 1)
                ax1.barh(range(len(client_keywords)), [1] * len(client_keywords), color='skyblue')
                ax1.set_yticks(range(len(client_keywords)))
                ax1.set_yticklabels(client_keywords)
                ax1.set_title('Client Mode Keywords')
                ax1.set_xlabel('Used in Search')
                ax1.set_xticks([])
                
                # Display consultant keywords
                ax2 = plt.subplot(1, 2, 2)
                ax2.barh(range(len(consultant_keywords)), [1] * len(consultant_keywords), color='coral')
                ax2.set_yticks(range(len(consultant_keywords)))
                ax2.set_yticklabels(consultant_keywords)
                ax2.set_title('Consultant Mode Keywords')
                ax2.set_xlabel('Used in Search')
                ax2.set_xticks([])
                
                plt.suptitle('Client vs Consultant Mode: Keyword Comparison', fontsize=16)
                plt.tight_layout()
                
                # Save the visualization with proper error handling
                output_file = 'tests/visualizations/client_vs_consultant_keywords.png'
                try:
                    plt.savefig(output_file)
                    print(f"Successfully saved plot to: {os.path.abspath(output_file)}")
                except Exception as e:
                    print(f"Error saving plot: {e}")
                
                plt.close()
                
                # Check if file exists
                if os.path.exists(output_file):
                    print(f"File exists, size: {os.path.getsize(output_file)} bytes")
                else:
                    print(f"File does not exist at {os.path.abspath(output_file)}")
                
                # Print the keywords for reference
                print("\nClient Keywords:", client_keywords)
                print("Consultant Keywords:", consultant_keywords)
                
            except Exception as e:
                print(f"Error during execution: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    # Simple test plot to verify matplotlib works
    plt.figure(figsize=(8, 6))
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro-')
    plt.title('Test Plot')
    plt.grid(True)
    
    # Save the plot
    output_file = 'tests/visualizations/test_plot.png'
    try:
        plt.savefig(output_file)
        print(f"Successfully saved plot to: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"Error saving plot: {e}")
    
    plt.close()
    
    # Check if file exists
    if os.path.exists(output_file):
        print(f"File exists, size: {os.path.getsize(output_file)} bytes")
    else:
        print(f"File does not exist at {os.path.abspath(output_file)}")
    
    # Now run the keyword comparison
    compare_client_consultant_keywords()