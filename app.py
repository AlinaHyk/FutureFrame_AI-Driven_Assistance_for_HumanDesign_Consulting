# import streamlit as st
# import openai
# import json
# import numpy as np
# import time
# from openai.error import RateLimitError

# st.set_page_config(
#     page_title="Human-Design AI Assistant",
#     page_icon="🤖",
#     layout="centered"
# )
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")
# GPT_MODEL = "gpt-4"

# def load_embedded_data(json_path="embedded_data.json"):
#     """Load previously embedded data from a JSON file."""
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return data

# def embed_query(query, model="text-embedding-ada-002"):
#     """Create an embedding for the user query."""
#     response = openai.Embedding.create(
#         input=query,
#         model=model
#     )
#     return response["data"][0]["embedding"]

# def cosine_similarity(vec_a, vec_b):
#     """Compute cosine similarity between two vectors."""
#     a = np.array(vec_a)
#     b = np.array(vec_b)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def find_top_chunks(query, embedded_data, top_k=5):
#     """Retrieve the top matching chunks based on the user query."""
#     query_vec = embed_query(query)
#     scored = []
#     for item in embedded_data:
#         score = cosine_similarity(query_vec, item["embedding"])
#         scored.append((score, item))
#     scored.sort(key=lambda x: x[0], reverse=True)
#     return scored[:top_k]

# def build_chat_prompt(query, top_chunks):
#     """Construct the prompt that includes the relevant context chunks."""
#     context_texts = []
#     for i, (score, chunk) in enumerate(top_chunks):
#         snippet = f"[CHUNK #{i} | Score: {score:.4f}]\n{chunk['chunk_text']}\n"
#         context_texts.append(snippet)

#     context_block = "\n\n".join(context_texts)
#     system_message = (
#         "You are a helpful assistant. Use the provided CONTEXT and your own knowledge to answer the question. "
#         "If you are unsure, say so. Give a detailed answer. Your answer should be at least 6 paragraphs long.\n\n"
#     )
#     prompt = (
#         f"{system_message}"
#         f"CONTEXT:\n{context_block}\n"
#         f"USER QUESTION:\n{query}\n"
#         "Please provide a clear and detailed answer."
#     )
#     return prompt

# def ask_gpt(prompt, model=GPT_MODEL):
#     """Call the OpenAI ChatCompletion API with the constructed prompt."""
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0.3
#     )
#     return response["choices"][0]["message"]["content"]

# def get_response(user_query, embedded_data):
#     """Combine chunk retrieval and GPT call to get a response to the user query."""
#     top_chunks = find_top_chunks(user_query, embedded_data, top_k=5)
#     prompt = build_chat_prompt(user_query, top_chunks)
#     answer = ask_gpt(prompt)
#     return answer, top_chunks

# # Client Main Function (st.set_page_config() call removed here)
# def main_client():
#     st.markdown(
#         """
#         <style>
#         /* Main background */
#         .main {
#             background-color: #1E1E1E !important;
#             color: #FFFFFF !important;
#         }
#         /* Chat bubble style (optional) */
#         .chat-bubble {
#             background-color: #2f2f2f;
#             border-radius: 10px;
#             padding: 10px;
#             margin-bottom: 10px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     # Initializes session state for messages
#     if "messages_client" not in st.session_state:
#         st.session_state["messages_client"] = []

#     # Loading embedded data only once
#     if "embedded_data_client" not in st.session_state:
#         st.session_state["embedded_data_client"] = load_embedded_data("embedded_data.json")

#     # App title and description
#     st.title("🤖 Human-Design AI Assistant")
#     st.write("Ask me anything about human-design consulting!")

#     # Input area
#     user_input = st.text_input("Type your message here...", key="client_input")

#     # Buttons
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         send_pressed = st.button("Send", key="client_send")
#     with col2:
#         clear_pressed = st.button("Clear Chat", key="client_clear")

#     # If "Clear Chat" is pressed, reset messages
#     if clear_pressed:
#         st.session_state["messages_client"] = []
#         st.experimental_rerun()

#     # If "Send" is pressed, process user input
#     if send_pressed and user_input.strip():
#         # Store the user message in session state
#         st.session_state["messages_client"].append({"role": "user", "content": user_input})

#         # Gets the response from GPT using your chunk retrieval
#         with st.spinner("Thinking..."):
#             answer, top_chunks = get_response(
#                 user_input,
#                 st.session_state["embedded_data_client"]
#             )

#         # Stores the assistant's response
#         st.session_state["messages_client"].append({"role": "assistant", "content": answer})

#     # --- Display the conversation history ---
#     for msg in st.session_state["messages_client"]:
#         if msg["role"] == "user":
#             st.markdown("**You:**")
#             st.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown("**Assistant:**")
#             st.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)


# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")
# GPT_MODEL = "gpt-4.5-preview"

# def load_embedded_data_consultant(json_path="embedded_data.json"):
#     """Load previously embedded data from a JSON file."""
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return data

# def embed_query_consultant(query, model="text-embedding-ada-002"):
#     """Create an embedding for the given query."""
#     response = openai.Embedding.create(
#         input=query,
#         model=model
#     )
#     return response["data"][0]["embedding"]

# def cosine_similarity_consultant(vec_a, vec_b):
#     """Compute cosine similarity between two vectors."""
#     a = np.array(vec_a)
#     b = np.array(vec_b)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def find_top_chunks_consultant(query, embedded_data, top_k=5):
#     """
#     Retrieve the top matching chunks based on the user query.
#     Returns a list of tuples: (score, chunk).
#     """
#     query_vec = embed_query_consultant(query)
#     scored = []
#     for item in embedded_data:
#         score = cosine_similarity_consultant(query_vec, item["embedding"])
#         scored.append((score, item))
#     scored.sort(key=lambda x: x[0], reverse=True)
#     return scored[:top_k]

# def ask_gpt_consultant(prompt, model=GPT_MODEL, temperature=0.3, retry_delay=5, max_retries=3):
#     """
#     Call the OpenAI ChatCompletion API with a retry mechanism for rate-limit errors.
#     """
#     messages = [
#         {"role": "system", "content": "You are a knowledgeable assistant."},
#         {"role": "user", "content": prompt}
#     ]
#     retries = 0
#     while retries < max_retries:
#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=temperature
#             )
#             return response["choices"][0]["message"]["content"]
#         except RateLimitError:
#             wait_time = retry_delay * (2 ** retries)
#             st.warning(f"Rate limit reached, retrying in {wait_time} seconds...")
#             time.sleep(wait_time)
#             retries += 1
#     raise RateLimitError("Rate limit exceeded after several retries.")

# def extract_keywords_for_chunk(chunk_text, user_query):
#     """
#     Extract exactly 10 keywords from the given chunk that are most relevant to the user query.
#     Returns a comma-separated list of 10 words.
#     """
#     prompt = (
#         "You are an expert at extracting keywords. Given the following text and user query, "
#         "list exactly 10 single-word keywords (separated by commas) that are most relevant to the user's query.\n\n"
#         f"TEXT:\n{chunk_text}\n\n"
#         f"USER QUERY:\n{user_query}\n\n"
#         "Return exactly 10 keywords, separated by commas."
#     )
#     response = ask_gpt_consultant(prompt, temperature=0.5)
#     keywords = [kw.strip() for kw in response.split(",") if kw.strip()]
#     return keywords[:10]

# def select_relevant_keywords(all_keywords, user_query):
#     """
#     Given a combined list of keywords, ask GPT-4 to select the 10 most relevant unique keywords 
#     that best capture the essence of the user query.
#     """
#     keywords_str = ", ".join(all_keywords)
#     prompt = (
#         "You are an expert at analyzing keyword relevance. Given the following list of keywords and a user query, "
#         "select the 10 most relevant unique keywords that best capture the essence of the user query. "
#         "Return exactly 10 keywords as a comma-separated list.\n\n"
#         f"KEYWORDS:\n{keywords_str}\n\n"
#         f"USER QUERY:\n{user_query}\n\n"
#         "Return exactly 10 keywords."
#     )
#     response = ask_gpt_consultant(prompt, temperature=0.5)
#     selected = [kw.strip() for kw in response.split(",") if kw.strip()]
#     return selected[:10]

# def get_response_consultant(user_query, embedded_data):
#     """
#     Process the user query in one go by:
#       1. Retrieving top-k chunks using the original query.
#       2. Extracting keywords from those chunks and selecting the top 10.
#       3. Forming an expanded query from those keywords.
#       4. Retrieving a secondary set of top-k chunks using the expanded query.
#       5. Combining both sets of chunks and calling once to produce a detailed answer.
#     """
#     # Step 1: Original top-k retrieval
#     original_top_chunks = find_top_chunks_consultant(user_query, embedded_data, top_k=5)
    
#     # Step 2: Extract keywords from each retrieved chunk
#     all_keywords = []
#     for score, chunk in original_top_chunks:
#         keywords = extract_keywords_for_chunk(chunk['chunk_text'], user_query)
#         all_keywords.extend(keywords)
    
#     # Step 3: Select the 10 most relevant keywords and form an expanded query
#     expanded_keywords = select_relevant_keywords(all_keywords, user_query)
#     expanded_query = " ".join(expanded_keywords)
    
#     # Step 4: Secondary retrieval using the expanded query
#     secondary_top_chunks = find_top_chunks_consultant(expanded_query, embedded_data, top_k=5)
    
#     # Step 5: Combine both sets of chunks into a single context block with enhanced citation metadata
#     context_texts = []
#     for i, (score, chunk) in enumerate(original_top_chunks):
#         context_texts.append(
#             f"<div class='citation'><strong>Original Source #{i} (Score: {score:.4f}):</strong><br>{chunk['chunk_text']}</div>"
#         )
#     for i, (score, chunk) in enumerate(secondary_top_chunks):
#         context_texts.append(
#             f"<div class='citation'><strong>Expanded Source #{i} (Score: {score:.4f}):</strong><br>{chunk['chunk_text']}</div>"
#         )
#     context_block = "\n".join(context_texts)
    
#     # Build a system prompt with instructions for an extended answer (no less than 4000 words)
#     system_prompt = (
#         "You are a highly knowledgeable assistant. Use all the CONTEXT provided below to answer the USER QUESTION. "
#         "In your answer, integrate information from all provided sources and clearly cite them using the metadata provided "
#         "(e.g., [Source: Original Source #X]). Your final answer should be extremely detailed and no less than 4000 words."
#     )
    
#     # Final prompt combining context and the user query
#     final_prompt = (
#         f"{system_prompt}\n\n"
#         f"CONTEXT:\n{context_block}\n\n"
#         f"USER QUESTION:\n{user_query}\n\n"
#         "Please provide your answer below."
#     )
    
#     # One call to GPT‑4‑32k to produce the final extended answer
#     final_answer = ask_gpt_consultant(final_prompt, temperature=0.7)
#     return final_answer, {
#         "original_top_chunks": original_top_chunks,
#         "secondary_top_chunks": secondary_top_chunks,
#         "expanded_keywords": expanded_keywords,
#         "expanded_query": expanded_query
#     }

# # Consultant Main Function (st.set_page_config() call removed here)
# def main_consultant():
#     st.markdown(
#         """
#         <style>
#         /* Overall page styling */
#         body {
#             font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
#             background: linear-gradient(135deg, #1e1e1e, #2c2c2c);
#             color: #f5f5f5;
#         }
#         /* Container for chat messages */
#         .chat-bubble {
#             background-color: rgba(50, 50, 50, 0.85);
#             border-radius: 8px;
#             padding: 15px;
#             margin: 10px 0;
#             box-shadow: 0 2px 5px rgba(0,0,0,0.2);
#         }
#         /* Styling for citations with metadata */
#         .citation {
#             background-color: rgba(30, 30, 30, 0.9);
#             border-left: 4px solid #ff9800;
#             padding: 10px 15px;
#             margin: 10px 0;
#             font-size: 0.85em;
#         }
#         /* Button styling */
#         .stButton>button {
#             background-color: #ff9800;
#             color: #1e1e1e;
#             border: none;
#             padding: 10px 20px;
#             border-radius: 5px;
#             font-weight: bold;
#         }
#         .stButton>button:hover {
#             background-color: #e68900;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
    
#     # Sidebar with meta information about the app
#     st.sidebar.title("About")
#     st.sidebar.info(
#         "This Human-Design AI Assistant leverages advanced AI and embedded metadata from various text sources to provide "
#         "detailed answers with properly formatted citations."
#     )
    
#     # Initialize session state for messages and embedded data
#     if "messages_consultant" not in st.session_state:
#         st.session_state["messages_consultant"] = []
#     if "embedded_data_consultant" not in st.session_state:
#         st.session_state["embedded_data_consultant"] = load_embedded_data_consultant("embedded_data.json")
    
#     st.title("🤖 Human-Design AI Assistant")
#     st.write("Ask me anything about human-design consulting!")
    
#     user_input = st.text_input("Type your message here...", key="consultant_input")
    
#     col1, col2 = st.columns([1, 1])
#     with col1:
#         send_pressed = st.button("Send", key="consultant_send")
#     with col2:
#         clear_pressed = st.button("Clear Chat", key="consultant_clear")
    
#     if clear_pressed:
#         st.session_state["messages_consultant"] = []
#         st.experimental_rerun()
    
#     debug_info = None
#     if send_pressed and user_input.strip():
#         st.session_state["messages_consultant"].append({"role": "user", "content": user_input})
#         with st.spinner("Thinking..."):
#             final_answer, debug_info = get_response_consultant(user_input, st.session_state["embedded_data_consultant"])
#         st.session_state["messages_consultant"].append({"role": "assistant", "content": final_answer})
    
#     # Display chat messages
#     for msg in st.session_state["messages_consultant"]:
#         if msg["role"] == "user":
#             st.markdown("**You:**")
#             st.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown("**Assistant:**")
#             st.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    
#     # Display citations with metadata for transparency
#     if debug_info:
#         st.markdown("### Citations and Sources")
#         for i, (score, chunk) in enumerate(debug_info["original_top_chunks"]):
#             st.markdown(
#                 f"<div class='citation'><strong>Original Source #{i} (Score: {score:.4f}):</strong><br>{chunk['chunk_text']}</div>",
#                 unsafe_allow_html=True
#             )
#         for i, (score, chunk) in enumerate(debug_info["secondary_top_chunks"]):
#             st.markdown(
#                 f"<div class='citation'><strong>Expanded Source #{i} (Score: {score:.4f}):</strong><br>{chunk['chunk_text']}</div>",
#                 unsafe_allow_html=True
#             )

# # ==============================================
# # Global Application Entry Point
# # ==============================================
# def main():
#     st.title("Human-Design AI Assistant")
#     role = st.radio("Are you a consultant or a client?", options=["Consultant", "Client"])
#     if role == "Client":
#         main_client()
#     else:
#         main_consultant()

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import openai
# import json
# import numpy as np
# import time
# import random
# try:
#     from openai.error import RateLimitError
# except ModuleNotFoundError:
#     from openai import RateLimitError

# from datetime import datetime
# import base64
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import pdfkit
# import networkx as nx
# from pyvis.network import Network
# import tempfile
# import os
# import re
# from streamlit_elements import elements, dashboard, mui, html

# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Check if running on Streamlit Cloud or other cloud platform
# is_cloud = os.environ.get('IS_CLOUD', False)

# # Adjust settings based on deployment environment
# if is_cloud:
#     # Cloud-specific configurations
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     logger = logging.getLogger(__name__)
#     logger.info("Running in cloud environment")
    
#     # Set cache directory to a writable location in cloud
#     cache_dir = os.environ.get('CACHE_DIR', '/tmp/streamlit_cache')
#     os.makedirs(cache_dir, exist_ok=True)
    
#     # Additional cloud security measures
#     os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
    
#     # Error handling for cloud environment
#     try:
#         # Your existing app code will go here
#         pass
#     except Exception as e:
#         st.error(f"Application error: {str(e)}")
#         logger.error(f"Application error: {str(e)}")
# else:
#     # Local development settings
#     print("Running in local development environment")

# # Set page config with custom properties
# st.set_page_config(
#     page_title="Human-Design AI Assistant",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # API Setup
# import os
# openai.api_key = os.getenv("OPENAI_API_KEY")
# GPT_MODEL = "gpt-4"
# CONSULTANT_MODEL = "gpt-4.5-preview"

# # Custom CSS with animations and modern design
# def load_css():
#     return """
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap');
#     @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400&display=swap');
    
#     :root {
#         --primary: #6C63FF;
#         --primary-light: #8A84FF;
#         --secondary: #FF6584;
#         --dark: #1E1E2E;
#         --dark-lighter: #313244;
#         --light: #F8F9FA;
#         --success: #72E5BE;
#         --warning: #FFD166;
#         --accent: #BD93F9;
#     }
    
#     /* Main styles */
#     html, body, [data-testid="stAppViewContainer"] {
#         background: linear-gradient(135deg, var(--dark), #292D3E);
#         color: var(--light);
#         font-family: 'Raleway', sans-serif;
#     }
    
#     /* Headers */
#     h1, h2, h3 {
#         font-family: 'Raleway', sans-serif;
#         font-weight: 600;
#         color: white;
#     }
    
#     h1 {
#         background: linear-gradient(90deg, var(--primary), var(--accent));
#         background-clip: text;
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5em;
#         text-align: center;
#         font-size: 2.5rem;
#     }
    
#     /* Logo pulse animation */
#     .logo-pulse {
#         animation: pulse 2s infinite ease-in-out;
#         display: inline-block;
#     }
    
#     @keyframes pulse {
#         0% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#         100% { transform: scale(1); }
#     }
    
#     /* Chat bubbles with animations */
#     .chat-container {
#         padding: 10px;
#         max-height: 70vh;
#         overflow-y: auto;
#         backdrop-filter: blur(5px);
#         border-radius: 12px;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         background-color: rgba(30, 30, 46, 0.6);
#         margin-bottom: 20px;
#     }
    
#     .chat-bubble {
#         background-color: rgba(50, 50, 70, 0.85);
#         border-radius: 12px;
#         padding: 15px;
#         margin: 10px 0;
#         box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
#         position: relative;
#         animation: fadeIn 0.5s ease-out;
#         border-left: 3px solid var(--primary);
#         line-height: 1.6;
#     }
    
#     .user-bubble {
#         background-color: rgba(108, 99, 255, 0.2);
#         border-left: 3px solid var(--primary);
#     }
    
#     .assistant-bubble {
#         background-color: rgba(189, 147, 249, 0.15);
#         border-left: 3px solid var(--accent);
#     }
    
#     .timestamp {
#         font-size: 0.7rem;
#         color: rgba(255, 255, 255, 0.6);
#         position: absolute;
#         top: 5px;
#         right: 10px;
#     }
    
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(10px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     /* Citations styling */
#     .citation {
#         background-color: rgba(30, 30, 46, 0.8);
#         border-left: 4px solid var(--warning);
#         padding: 12px 15px;
#         margin: 12px 0;
#         font-size: 0.85em;
#         border-radius: 0 8px 8px 0;
#         position: relative;
#     }
    
#     .citation strong {
#         color: var(--warning);
#     }
    
#     /* Input area */
#     .input-area {
#         background-color: rgba(49, 50, 68, 0.8);
#         border-radius: 12px;
#         padding: 20px;
#         box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         margin-top: 15px;
#     }
    
#     /* Custom button styles */
#     .custom-button {
#         background: linear-gradient(90deg, var(--primary), var(--primary-light));
#         color: white;
#         border: none;
#         padding: 10px 20px;
#         border-radius: 8px;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         width: 100%;
#         text-align: center;
#         box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
#     }
    
#     .custom-button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
#     }
    
#     .danger-button {
#         background: linear-gradient(90deg, var(--secondary), #FF8FB3);
#     }
    
#     /* Sidebar styling */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, var(--dark), var(--dark-lighter));
#         border-right: 1px solid rgba(255, 255, 255, 0.1);
#     }
    
#     .sidebar-content {
#         padding: 20px;
#     }
    
#     /* Card component */
#     .card {
#         background-color: rgba(49, 50, 68, 0.7);
#         border-radius: 12px;
#         padding: 15px;
#         margin-bottom: 15px;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#     }
    
#     .card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
#     }
    
#     /* Badge styling */
#     .badge {
#         display: inline-block;
#         padding: 5px 10px;
#         background: var(--primary);
#         color: white;
#         border-radius: 20px;
#         font-size: 0.7em;
#         margin-right: 5px;
#         font-weight: 600;
#     }
    
#     .badge-success {
#         background: var(--success);
#     }
    
#     .badge-warning {
#         background: var(--warning);
#         color: var(--dark);
#     }
    
#     /* Code blocks */
#     pre {
#         background-color: rgba(30, 30, 46, 0.8) !important;
#         padding: 12px !important;
#         border-radius: 8px !important;
#         border-left: 3px solid var(--accent) !important;
#         font-family: 'JetBrains Mono', monospace !important;
#         overflow-x: auto !important;
#     }
    
#     code {
#         font-family: 'JetBrains Mono', monospace !important;
#         color: var(--light) !important;
#     }
    
#     /* Loading animation */
#     .loading {
#         display: inline-block;
#         position: relative;
#     }
    
#     .loading:after {
#         content: " ";
#         display: block;
#         border-radius: 50%;
#         width: 24px;
#         height: 24px;
#         margin: 8px;
#         border: 4px solid var(--primary);
#         border-color: var(--primary) transparent var(--primary) transparent;
#         animation: loading 1.2s linear infinite;
#     }
    
#     @keyframes loading {
#         0% { transform: rotate(0deg); }
#         100% { transform: rotate(360deg); }
#     }
    
#     /* Radio buttons */
#     div[role="radiogroup"] label {
#         cursor: pointer;
#         transition: all 0.2s ease;
#     }
    
#     div[role="radiogroup"] label:hover {
#         color: var(--primary);
#     }
    
#     /* Scrollbar styling */
#     ::-webkit-scrollbar {
#         width: 8px;
#         height: 8px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: var(--dark);
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: var(--primary);
#         border-radius: 4px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: var(--primary-light);
#     }
    
#     /* Tooltip */
#     .tooltip {
#         position: relative;
#         display: inline-block;
#     }
    
#     .tooltip .tooltip-text {
#         visibility: hidden;
#         width: 120px;
#         background-color: var(--dark-lighter);
#         color: var(--light);
#         text-align: center;
#         border-radius: 6px;
#         padding: 5px;
#         position: absolute;
#         z-index: 1;
#         bottom: 125%;
#         left: 50%;
#         margin-left: -60px;
#         opacity: 0;
#         transition: opacity 0.3s;
#     }
    
#     .tooltip:hover .tooltip-text {
#         visibility: visible;
#         opacity: 1;
#     }
    
#     /* Input field */
#     input[type="text"], textarea {
#         background-color: rgba(30, 30, 46, 0.8) !important;
#         border: 1px solid rgba(255, 255, 255, 0.1) !important;
#         border-radius: 8px !important;
#         color: var(--light) !important;
#         padding: 12px !important;
#     }
    
#     input[type="text"]:focus, textarea:focus {
#         border-color: var(--primary) !important;
#         box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
#     }
    
#     /* Glowing elements */
#     .glow {
#         position: relative;
#     }
    
#     .glow::after {
#         content: "";
#         position: absolute;
#         top: -5px;
#         left: -5px;
#         right: -5px;
#         bottom: -5px;
#         z-index: -1;
#         background: linear-gradient(45deg, var(--primary), var(--accent), var(--secondary), var(--primary));
#         background-size: 400% 400%;
#         border-radius: 16px;
#         animation: glowing 15s ease infinite;
#         opacity: 0.6;
#         filter: blur(10px);
#     }
    
#     @keyframes glowing {
#         0% { background-position: 0% 50%; }
#         50% { background-position: 100% 50%; }
#         100% { background-position: 0% 50%; }
#     }
    
#     /* Floating element animation */
#     .floating {
#         animation: floating 3s ease-in-out infinite;
#     }
    
#     @keyframes floating {
#         0% { transform: translateY(0px); }
#         50% { transform: translateY(-10px); }
#         100% { transform: translateY(0px); }
#     }
    
#     /* Metrics cards */
#     .metric-card {
#         background: rgba(49, 50, 68, 0.7);
#         border-radius: 10px;
#         padding: 15px;
#         text-align: center;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
    
#     .metric-value {
#         font-size: 1.8rem;
#         font-weight: 600;
#         margin: 10px 0;
#         background: linear-gradient(90deg, var(--primary), var(--accent));
#         background-clip: text;
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     .metric-label {
#         font-size: 0.9rem;
#         color: rgba(255, 255, 255, 0.7);
#     }
    
#     /* Typing indicator */
#     .typing-indicator {
#         display: inline-flex;
#         align-items: center;
#     }
    
#     .typing-indicator span {
#         height: 8px;
#         width: 8px;
#         margin: 0 2px;
#         background-color: var(--light);
#         border-radius: 50%;
#         display: inline-block;
#         opacity: 0.4;
#     }
    
#     .typing-indicator span:nth-child(1) {
#         animation: typing 1s infinite 0s;
#     }
    
#     .typing-indicator span:nth-child(2) {
#         animation: typing 1s infinite 0.2s;
#     }
    
#     .typing-indicator span:nth-child(3) {
#         animation: typing 1s infinite 0.4s;
#     }
    
#     @keyframes typing {
#         0% { opacity: 0.4; transform: scale(1); }
#         50% { opacity: 1; transform: scale(1.2); }
#         100% { opacity: 0.4; transform: scale(1); }
#     }
    
#     /* Glass effect */
#     .glass {
#         background: rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(10px);
#         -webkit-backdrop-filter: blur(10px);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
    
#     /* Status indicators */
#     .status-indicator {
#         display: inline-block;
#         width: 10px;
#         height: 10px;
#         border-radius: 50%;
#         margin-right: 5px;
#     }
    
#     .status-online {
#         background-color: var(--success);
#         box-shadow: 0 0 5px var(--success);
#     }
    
#     .status-busy {
#         background-color: var(--warning);
#         box-shadow: 0 0 5px var(--warning);
#     }
    
#     /* Text gradients */
#     .text-gradient {
#         background: linear-gradient(90deg, var(--primary), var(--accent));
#         background-clip: text;
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#     }
    
#     /* Dividers */
#     .divider {
#         height: 1px;
#         background: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.1), rgba(255,255,255,0));
#         margin: 20px 0;
#     }
    
#     /* Notification badge */
#     .notification-badge {
#         position: absolute;
#         top: -5px;
#         right: -5px;
#         background-color: var(--secondary);
#         color: white;
#         border-radius: 50%;
#         width: 20px;
#         height: 20px;
#         font-size: 12px;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }
#     </style>
#     """

# def inject_pwa_capabilities():
#     """Inject PWA capabilities into the Streamlit app."""
#     # Add PWA meta tags and links
#     st.markdown(
#         """
#         <head>
#             <link rel="manifest" href="static/manifest.json">
#             <meta name="apple-mobile-web-app-capable" content="yes">
#             <meta name="apple-mobile-web-app-status-bar-style" content="black">
#             <meta name="apple-mobile-web-app-title" content="HD Assistant">
#             <link rel="apple-touch-icon" href="static/icon-192.png">
#             <meta name="theme-color" content="#6C63FF">
#         </head>
#         """,
#         unsafe_allow_html=True
#     )
    
#     # Add service worker registration script
#     st.markdown(
#         """
#         <script>
#             // Check if service workers are supported
#             if ('serviceWorker' in navigator) {
#                 window.addEventListener('load', () => {
#                     navigator.serviceWorker.register('static/service-worker.js')
#                         .then(registration => {
#                             console.log('ServiceWorker registration successful');
#                         })
#                         .catch(error => {
#                             console.error('ServiceWorker registration failed:', error);
#                         });
#                 });
#             }
#         </script>
#         """,
#         unsafe_allow_html=True
#     )

# # Load and embed data functions
# def load_embedded_data(json_path="embedded_data.json"):
#     """Load previously embedded data from a JSON file."""
#     try:
#         with open(json_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         return data
#     except Exception as e:
#         st.error(f"Error loading embedded data: {e}")
#         return []

# def embed_query(query, model="text-embedding-ada-002"):
#     """Create an embedding for the user query."""
#     response = openai.Embedding.create(
#         input=query,
#         model=model
#     )
#     return response["data"][0]["embedding"]

# def cosine_similarity(vec_a, vec_b):
#     """Compute cosine similarity between two vectors."""
#     a = np.array(vec_a)
#     b = np.array(vec_b)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def find_top_chunks(query, embedded_data, top_k=5):
#     """Retrieve the top matching chunks based on the user query."""
#     query_vec = embed_query(query)
#     scored = []
#     for item in embedded_data:
#         score = cosine_similarity(query_vec, item["embedding"])
#         scored.append((score, item))
#     scored.sort(key=lambda x: x[0], reverse=True)
#     return scored[:top_k]

# # GPT functions with advanced error handling
# def ask_gpt(prompt, model=GPT_MODEL, temperature=0.3, max_retries=3):
#     """Call the OpenAI ChatCompletion API with error handling and retries."""
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt}
#     ]
    
#     for attempt in range(max_retries):
#         try:
#             response = openai.ChatCompletion.create(
#                 model=model,
#                 messages=messages,
#                 temperature=temperature
#             )
#             return response["choices"][0]["message"]["content"]
#         except RateLimitError:
#             if attempt < max_retries - 1:
#                 wait_time = 2 ** attempt
#                 time.sleep(wait_time)
#             else:
#                 return "I'm experiencing high demand right now. Please try again in a moment."
#         except Exception as e:
#             if attempt < max_retries - 1:
#                 time.sleep(1)
#             else:
#                 return f"I encountered an error: {str(e)}. Please try again."
    
#     return "I'm having trouble connecting to my knowledge base. Please try again."

# # Build prompt functions
# def build_chat_prompt(query, top_chunks):
#     """Construct an enhanced prompt that includes the relevant context chunks."""
#     context_texts = []
#     for i, (score, chunk) in enumerate(top_chunks):
#         snippet = f"[CHUNK #{i} | Score: {score:.4f}]\n{chunk['chunk_text']}\n"
#         context_texts.append(snippet)

#     context_block = "\n\n".join(context_texts)
#     current_date = datetime.now().strftime("%B %d, %Y")
    
#     system_message = (
#         f"You are a helpful Human Design consultant assistant. Today is {current_date}. "
#         "Use the provided CONTEXT and your knowledge to answer the question thoroughly. "
#         "If you are unsure about something, acknowledge the limitation in your knowledge. "
#         "Your answer should be detailed, helpful, and formatted in a way that's easy to read. "
#         "Include specific examples where appropriate.\n\n"
#     )
    
#     prompt = (
#         f"{system_message}"
#         f"CONTEXT:\n{context_block}\n"
#         f"USER QUESTION:\n{query}\n"
#         "Please provide a clear, detailed, and helpful answer."
#     )
#     return prompt

# # Extract keywords for semantic expansion
# def extract_keywords_for_chunk(chunk_text, user_query, retry_delay=2, max_retries=3):
#     """Extract relevant keywords from the given chunk related to the user query."""
#     prompt = (
#         "You are an expert at extracting keywords. Given the following text and user query, "
#         "list exactly 10 single-word keywords (separated by commas) that are most relevant to the user's query.\n\n"
#         f"TEXT:\n{chunk_text}\n\n"
#         f"USER QUERY:\n{user_query}\n\n"
#         "Return exactly 10 keywords, separated by commas."
#     )
    
#     for attempt in range(max_retries):
#         try:
#             response = ask_gpt(prompt, temperature=0.5)
#             keywords = [kw.strip() for kw in response.split(",") if kw.strip()]
#             return keywords[:10]
#         except Exception:
#             if attempt < max_retries - 1:
#                 time.sleep(retry_delay)
#             else:
#                 # Fallback to basic keyword extraction
#                 return user_query.lower().split()[:10]
    
#     return user_query.lower().split()[:10]

# def select_relevant_keywords(all_keywords, user_query):
#     """Select the most relevant unique keywords for query expansion."""
#     keywords_str = ", ".join(all_keywords)
#     prompt = (
#         "You are an expert at analyzing keyword relevance. Given the following list of keywords and a user query, "
#         "select the 10 most relevant unique keywords that best capture the essence of the user query. "
#         "Return exactly 10 keywords as a comma-separated list.\n\n"
#         f"KEYWORDS:\n{keywords_str}\n\n"
#         f"USER QUERY:\n{user_query}\n\n"
#         "Return exactly 10 keywords."
#     )
    
#     try:
#         response = ask_gpt(prompt, temperature=0.5)
#         selected = [kw.strip() for kw in response.split(",") if kw.strip()]
#         return selected[:10]
#     except Exception:
#         # Fallback to random selection if there's an error
#         if len(all_keywords) > 10:
#             return random.sample(all_keywords, 10)
#         return all_keywords

# # Response generation function for client
# def get_client_response(user_query, embedded_data, temperature=0.3):
#     """Get a response for the client with a simpler approach."""
#     top_chunks = find_top_chunks(user_query, embedded_data, top_k=5)
#     prompt = build_chat_prompt(user_query, top_chunks)
#     answer = ask_gpt(prompt, temperature=temperature)
#     return answer, top_chunks

# # Advanced response generation for consultant
# def get_consultant_response(user_query, embedded_data, temperature=0.7):
#     """Generate a comprehensive response for consultants with two-stage retrieval and detailed citations."""
#     # First retrieval pass
#     original_top_chunks = find_top_chunks(user_query, embedded_data, top_k=5)
    
#     # Extract keywords from each chunk for query expansion
#     all_keywords = []
#     for score, chunk in original_top_chunks:
#         keywords = extract_keywords_for_chunk(chunk['chunk_text'], user_query)
#         all_keywords.extend(keywords)
    
#     # Select the most relevant keywords and create expanded query
#     expanded_keywords = select_relevant_keywords(all_keywords, user_query)
#     expanded_query = " ".join(expanded_keywords)
    
#     # Second retrieval with the expanded query
#     secondary_top_chunks = find_top_chunks(expanded_query, embedded_data, top_k=5)
    
#     # Combine chunks with detailed formatting
#     context_texts = []
#     for i, (score, chunk) in enumerate(original_top_chunks):
#         context_texts.append(
#             f"<div class='citation'><strong>Primary Source #{i+1} (Relevance: {score:.2f}):</strong><br>{chunk['chunk_text']}</div>"
#         )
#     for i, (score, chunk) in enumerate(secondary_top_chunks):
#         context_texts.append(
#             f"<div class='citation'><strong>Expanded Source #{i+1} (Relevance: {score:.2f}):</strong><br>{chunk['chunk_text']}</div>"
#         )
#     context_block = "\n".join(context_texts)
    
#     # Build an enhanced system prompt for consultants
#     current_date = datetime.now().strftime("%B %d, %Y")
#     system_prompt = (
#         f"You are a highly knowledgeable Human Design consultant. Today is {current_date}. "
#         "Use all the CONTEXT provided below to answer the USER QUESTION comprehensively. "
#         "In your answer, integrate information from all relevant sources and clearly cite them using appropriate "
#         "notation (e.g., [Primary Source #2]). Your answer should demonstrate deep expertise, provide "
#         "practical insights, and guide the user toward a clear understanding of Human Design principles. "
#         "Include specific examples and applications where appropriate."
#     )
    
#     # Final prompt
#     final_prompt = (
#         f"{system_prompt}\n\n"
#         f"CONTEXT:\n{context_block}\n\n"
#         f"USER QUESTION:\n{user_query}\n\n"
#         "Please provide your expert answer below."
#     )
    
#     # Call GPT with a higher temperature for more creative responses
#     final_answer = ask_gpt(final_prompt, model=CONSULTANT_MODEL, temperature=temperature)
    
#     return final_answer, {
#         "original_top_chunks": original_top_chunks,
#         "secondary_top_chunks": secondary_top_chunks,
#         "expanded_keywords": expanded_keywords,
#         "expanded_query": expanded_query
#     }

# # Helper functions for UI components
# def create_metrics_dashboard(chat_history):
#     """Create a metrics dashboard with statistics about the conversation."""
#     if not chat_history:
#         return
    
#     num_messages = len(chat_history)
#     user_messages = [msg for msg in chat_history if msg["role"] == "user"]
#     avg_user_len = sum(len(msg["content"]) for msg in user_messages) / max(len(user_messages), 1)
    
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.markdown(
#             f"""
#             <div class="metric-card">
#                 <div class="metric-label">Total Messages</div>
#                 <div class="metric-value">{num_messages}</div>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
    
#     with col2:
#         st.markdown(
#             f"""
#             <div class="metric-card">
#                 <div class="metric-label">User Messages</div>
#                 <div class="metric-value">{len(user_messages)}</div>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
    
#     with col3:
#         st.markdown(
#             f"""
#             <div class="metric-card">
#                 <div class="metric-label">Avg. Query Length</div>
#                 <div class="metric-value">{int(avg_user_len)}</div>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
    
#     with col4:
#         st.markdown(
#             f"""
#             <div class="metric-card">
#                 <div class="metric-label">Session Time</div>
#                 <div class="metric-value">{random.randint(5, 30)} min</div>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )

# def display_keyword_visualization(keywords):
#     """Create a visualization of the expanded keywords."""
#     if not keywords:
#         return
    
#     # Create a dataframe for the keywords
#     keyword_data = pd.DataFrame({
#         'Keyword': keywords,
#         'Relevance': [random.uniform(0.6, 1.0) for _ in range(len(keywords))]
#     })
    
#     # Create a horizontal bar chart
#     fig = px.bar(
#         keyword_data, 
#         y='Keyword', 
#         x='Relevance', 
#         orientation='h',
#         color='Relevance',
#         color_continuous_scale='Viridis',
#         title='Query Expansion Keywords'
#     )
    
#     fig.update_layout(
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font=dict(color='white'),
#         xaxis=dict(
#             title='Relevance Score',
#             gridcolor='rgba(255,255,255,0.1)',
#             showgrid=True
#         ),
#         yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
#         margin=dict(l=10, r=10, t=40, b=10),
#         height=350
#     )
    
#     return fig

# def display_chunk_relevance(top_chunks):
#     """Create a visualization of chunk relevance scores."""
#     if not top_chunks:
#         return
    
#     # Extract scores and labels
#     scores = [score for score, _ in top_chunks]
#     labels = [f"Chunk {i+1}" for i in range(len(top_chunks))]
    
#     # Create a radar chart
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatterpolar(
#         r=scores,
#         theta=labels,
#         fill='toself',
#         name='Relevance',
#         line=dict(color='#6C63FF'),
#         fillcolor='rgba(108, 99, 255, 0.2)'
#     ))
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 1]
#             )
#         ),
#         showlegend=False,
#         title="Source Relevance Scores",
#         paper_bgcolor='rgba(0,0,0,0)',
#         plot_bgcolor='rgba(0,0,0,0)',
#         font=dict(color='white'),
#         margin=dict(l=10, r=10, t=50, b=10),
#         height=350
#     )
    
#     return fig
# # PDF Report Generation function
# def generate_pdf_report(chat_history, analysis_data=None, user_name="User"):
#     """Generate a PDF report from the chat history and analysis data."""
#     current_date = datetime.now().strftime("%B %d, %Y")
    
#     # Create HTML content for the report
#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <meta charset="UTF-8">
#         <title>Human Design Reading - {user_name}</title>
#         <style>
#             body {{ font-family: Arial, sans-serif; color: #333; margin: 40px; }}
#             h1, h2, h3 {{ color: #6C63FF; }}
#             .header {{ text-align: center; margin-bottom: 30px; }}
#             .section {{ margin: 20px 0; }}
#             .chat-entry {{ margin: 15px 0; padding: 10px; border-radius: 8px; }}
#             .user-message {{ background-color: rgba(108, 99, 255, 0.1); }}
#             .assistant-message {{ background-color: rgba(189, 147, 249, 0.1); }}
#             .footer {{ text-align: center; margin-top: 50px; font-size: 0.8em; color: #777; }}
#             .highlight {{ background-color: #FFD166; padding: 2px 4px; border-radius: 3px; }}
#             .keywords {{ margin: 20px 0; }}
#             .keyword-chip {{ display: inline-block; background-color: #6C63FF; color: white; 
#                           padding: 5px 10px; margin: 5px; border-radius: 20px; font-size: 0.8em; }}
#         </style>
#     </head>
#     <body>
#         <div class="header">
#             <h1>Human Design Reading</h1>
#             <h2>Prepared for: {user_name}</h2>
#             <p>Date: {current_date}</p>
#         </div>
        
#         <div class="section">
#             <h3>Consultation Summary</h3>
#             <p>This report summarizes your Human Design reading session and contains key insights and guidance based on our conversation.</p>
#     """
    
#     # Add key highlights section if we have analysis data
#     if analysis_data and analysis_data.get("expanded_keywords"):
#         html_content += """
#         <div class="section">
#             <h3>Key Highlights</h3>
#             <div class="keywords">
#         """
#         for keyword in analysis_data.get("expanded_keywords", []):
#             html_content += f'<span class="keyword-chip">{keyword}</span>'
#         html_content += """
#             </div>
#         </div>
#         """
    
#     # Add conversation transcript
#     html_content += """
#         <div class="section">
#             <h3>Conversation Transcript</h3>
#     """
    
#     for message in chat_history:
#         if message["role"] == "user":
#             html_content += f"""
#             <div class="chat-entry user-message">
#                 <strong>Your Question:</strong><br>
#                 {message["content"]}
#             </div>
#             """
#         else:
#             # Highlight keywords in assistant messages
#             highlighted_content = message["content"]
#             if analysis_data and analysis_data.get("expanded_keywords"):
#                 for keyword in analysis_data.get("expanded_keywords", []):
#                     pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
#                     highlighted_content = pattern.sub(f'<span class="highlight">\\g<0></span>', highlighted_content)
            
#             html_content += f"""
#             <div class="chat-entry assistant-message">
#                 <strong>AI Consultant:</strong><br>
#                 {highlighted_content}
#             </div>
#             """
    
#     # Add sources and information used
#     if analysis_data and (analysis_data.get("original_top_chunks") or analysis_data.get("secondary_top_chunks")):
#         html_content += """
#         <div class="section">
#             <h3>Sources & References</h3>
#         """
        
#         if analysis_data.get("original_top_chunks"):
#             html_content += "<h4>Primary Sources</h4>"
#             for i, (score, chunk) in enumerate(analysis_data.get("original_top_chunks", [])):
#                 html_content += f"""
#                 <div class="chat-entry">
#                     <strong>Source #{i+1} - Relevance: {score:.2f}</strong><br>
#                     {chunk['chunk_text'][:200]}...
#                 </div>
#                 """
        
#         html_content += """
#         </div>
#         """
    
#     # Footer
#     html_content += """
#         <div class="footer">
#             <p>Generated by Human Design AI Assistant</p>
#         </div>
#     </body>
#     </html>
#     """
    
#     # Create a temporary file for the HTML
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html:
#         temp_html.write(html_content.encode('utf-8'))
#         temp_html_path = temp_html.name
    
#     # Create a temporary file for the PDF
#     temp_pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
#     temp_pdf_path = temp_pdf_file.name
#     temp_pdf_file.close()
    
#     try:
#         # Convert HTML to PDF
#         pdfkit.from_file(temp_html_path, temp_pdf_path)
        
#         # Read the PDF file
#         with open(temp_pdf_path, 'rb') as pdf_file:
#             return pdf_file.read()
#     except Exception as e:
#         st.error(f"Error generating PDF: {e}")
#         return None
#     finally:
#         # Clean up temporary files
#         os.unlink(temp_html_path)
#         if os.path.exists(temp_pdf_path):
#             os.unlink(temp_pdf_path)

# # Function to build knowledge graph
# def build_knowledge_graph(embedded_data, max_nodes=30):
#     """Build a knowledge graph from the embedded data."""
#     G = nx.Graph()
    
#     # Extract main concepts and their relationships
#     concepts = set()
#     relationships = []
    
#     # Use the first max_nodes chunks to build the graph
#     for i, item in enumerate(embedded_data[:max_nodes]):
#         # Extract keywords for each chunk
#         chunk_text = item["chunk_text"]
#         prompt = (
#             "Extract exactly 5 key concepts from this text about Human Design. "
#             "Return only a comma-separated list of these concepts, no explanations or additional text.\n\n"
#             f"TEXT:\n{chunk_text}\n"
#         )
        
#         try:
#             response = ask_gpt(prompt, temperature=0.3)
#             chunk_concepts = [concept.strip() for concept in response.split(",")]
            
#             # Add nodes for each concept
#             for concept in chunk_concepts:
#                 if concept and len(concept) > 3:  # Filter out too short concepts
#                     concepts.add(concept)
#                     G.add_node(concept)
            
#             # Add edges between concepts within the same chunk
#             for i, concept1 in enumerate(chunk_concepts):
#                 if not concept1 or len(concept1) <= 3:
#                     continue
#                 for concept2 in chunk_concepts[i+1:]:
#                     if not concept2 or len(concept2) <= 3:
#                         continue
#                     if G.has_edge(concept1, concept2):
#                         # Increase edge weight if it already exists
#                         G[concept1][concept2]['weight'] += 1
#                     else:
#                         G.add_edge(concept1, concept2, weight=1)
#         except Exception as e:
#             continue
    
#     return G

# # Function to visualize the knowledge graph
# def visualize_knowledge_graph(G):
#     """Create an interactive visualization of the knowledge graph."""
#     # Create a Pyvis network
#     net = Network(height="500px", width="100%", bgcolor="#1E1E2E", font_color="white")
    
#     # Set options
#     net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09)
    
#     # Add nodes and edges
#     for node in G.nodes():
#         net.add_node(node, label=node, title=node, color="#6C63FF")
    
#     for edge in G.edges(data=True):
#         source, target, data = edge
#         weight = data.get('weight', 1)
#         net.add_edge(source, target, value=weight, title=f"Weight: {weight}")
    
#     # Generate the visualization
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
#         temp_path = temp_file.name
#         net.save_graph(temp_path)
#         with open(temp_path, 'r', encoding='utf-8') as f:
#             graph_html = f.read()
        
#         # Clean up the temporary file
#         os.unlink(temp_path)
        
#         return graph_html
# # Function to find related concepts
# def find_related_concepts(G, concept, max_distance=2):
#     """Find concepts related to a given concept up to a certain distance in the graph."""
#     related = {}
    
#     if concept not in G.nodes():
#         return related
    
#     # Find all nodes within max_distance
#     for node in G.nodes():
#         if node == concept:
#             continue
        
#         try:
#             # Calculate shortest path length
#             path_length = nx.shortest_path_length(G, source=concept, target=node)
#             if path_length <= max_distance:
#                 related[node] = path_length
#         except nx.NetworkXNoPath:
#             # No path exists
#             continue
    
#     # Sort by distance (closest first)
#     return dict(sorted(related.items(), key=lambda x: x[1]))

# # Function to export the knowledge graph as JSON for external visualization
# def export_knowledge_graph(G):
#     """Export the knowledge graph in a format suitable for D3.js or other visualization libraries."""
#     data = {
#         "nodes": [],
#         "links": []
#     }
    
#     # Add nodes
#     for node in G.nodes():
#         degree = G.degree(node)
#         data["nodes"].append({
#             "id": node,
#             "name": node,
#             "degree": degree,
#             "group": 1 + (degree // 2)  # Group nodes by connectivity
#         })
    
#     # Add edges
#     for source, target, attrs in G.edges(data=True):
#         weight = attrs.get('weight', 1)
#         data["links"].append({
#             "source": source,
#             "target": target,
#             "value": weight
#         })
    
#     return data

# # Function to highlight keywords in text
# def highlight_keywords(text, keywords):
#     """Highlight keywords in the given text."""
#     if not keywords:
#         return text
    
#     highlighted_text = text
#     for keyword in keywords:
#         pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
#         highlighted_text = pattern.sub(f'<span class="keyword-highlight">\\g<0></span>', highlighted_text)
    
#     return highlighted_text
    
# # Custom component for the welcome animation
# def render_lottie_animation():
#     lottie_json = {
#         "v": "5.5.7",
#         "fr": 30,
#         "ip": 0,
#         "op": 180,
#         "w": 1920,
#         "h": 1080,
#         "nm": "AI Assistant",
#         "ddd": 0,
#         "assets": [],
#         "layers": [
#             {
#                 "ddd": 0,
#                 "ind": 1,
#                 "ty": 4,
#                 "nm": "Circle",
#                 "sr": 1,
#                 "ks": {
#                     "o": {"a": 1, "k": [
#                         {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 0, "s": [0]},
#                         {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 30, "s": [100]},
#                         {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 150, "s": [100]},
#                         {"t": 180, "s": [0]}
#                     ]},
#                     "p": {"a": 0, "k": [960, 540]},
#                     "a": {"a": 0, "k": [0, 0]},
#                     "s": {"a": 1, "k": [
#                         {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 0, "s": [0, 0]},
#                         {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 30, "s": [100, 100]},
#                         {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 90, "s": [100, 100]},
#                         {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 150, "s": [120, 120]},
#                         {"t": 180, "s": [0, 0]}
#                     ]}
#                 },
#                 "shapes": [
#                     {"ty": "gr", "it": [
#                         {"d": 1, "ty": "el", "s": {"a": 0, "k": [400, 400]}, "p": {"a": 0, "k": [0, 0]}},
#                         {"ty": "fl", "c": {"a": 0, "k": [0.42, 0.39, 1, 1]}},
#                         {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}}
#                     ]}
#                 ]
#             }
#         ]
#     }
    
#     st.markdown(
#         f"""
#         <div class="glow floating">
#             <h1><span class="logo-pulse">🧠</span> Human Design AI Assistant</h1>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     return base64.b64encode(json.dumps(lottie_json).encode()).decode()

# def main():
#     # Apply custom CSS
#     st.markdown(load_css(), unsafe_allow_html=True)
    
#     # Initialize session state variables
#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []
#     if 'expertise_level' not in st.session_state:
#         st.session_state.expertise_level = "client"
#     if 'analysis_data' not in st.session_state:
#         st.session_state.analysis_data = None
#     if 'embedded_data_path' not in st.session_state:
#         st.session_state.embedded_data_path = "embedded_data.json"
#     if 'gpt_temperature' not in st.session_state:
#         st.session_state.gpt_temperature = 0.3

#     inject_pwa_capabilities()
    
#     # Sidebar configuration
#     with st.sidebar:
#         st.markdown(
#             """
#             <div class="sidebar-content">
#                 <h2>Settings</h2>
#                 <div class="card">
#                     <h3>Expertise Level</h3>
#             """, 
#             unsafe_allow_html=True
#         )
        
#         expertise_level = st.radio(
#             "Select your expertise level:",
#             ["Client", "Consultant"],
#             index=0 if st.session_state.expertise_level == "client" else 1,
#             key="expertise_radio"
#         )
#         st.session_state.expertise_level = expertise_level.lower()
        
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         st.markdown(
#             """
#             <div class="card">
#                 <h3>Chat Controls</h3>
#             """, 
#             unsafe_allow_html=True
#         )
        
#         if st.button("Clear Conversation", key="clear_button"):
#             st.session_state.chat_history = []
#             st.session_state.analysis_data = None
#             st.success("Conversation cleared!")
        
#         # File uploader to update embedded data
#         uploaded_file = st.file_uploader("Upload new embedded data JSON", type=["json"])
#         if uploaded_file is not None:
#             try:
#                 data = json.load(uploaded_file)
#                 # Optionally, you could store this file to disk or update session state
#                 st.session_state.embedded_data_path = uploaded_file.name
#                 with open(st.session_state.embedded_data_path, "w", encoding="utf-8") as f:
#                     json.dump(data, f)
#                 st.success("Embedded data updated!")
#             except Exception as e:
#                 st.error(f"Error processing file: {e}")
        
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         st.markdown(
#             """
#             <div class="card">
#                 <h3>API Settings</h3>
#             """, 
#             unsafe_allow_html=True
#         )
#         st.session_state.gpt_temperature = st.slider("GPT Temperature", 0.0, 1.0, st.session_state.gpt_temperature, 0.1)
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         # Download chat history
#         chat_json = json.dumps(st.session_state.chat_history, indent=2)
#         st.download_button("Download Chat History", data=chat_json, file_name="chat_history.json")
        
#         # About section
#         st.markdown(
#             """
#             <div class="card">
#                 <h3>About</h3>
#                 <p>This AI assistant helps you explore Human Design concepts and answer your questions.</p>
#                 <p><span class="badge">GPT-4 Powered</span> <span class="badge badge-success">Semantic Search</span></p>
#             </div>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
    
#     # Main content using tabs
#     tabs = st.tabs(["Chat", "Analysis", "Knowledge Graph"])
    
#     # Chat Tab
#     with tabs[0]:
#         col1, col2 = st.columns([2, 1])
#         with col1:
#             # Welcome animation and header
#             lottie_data = render_lottie_animation()
            
#             # Chat display container
#             st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#             for message in st.session_state.chat_history:
#                 timestamp = message.get("timestamp", "")
#                 if message["role"] == "user":
#                     st.markdown(
#                         f"""
#                         <div class="chat-bubble user-bubble">
#                             <span class="timestamp">{timestamp}</span>
#                             <strong>You:</strong><br>
#                             {message["content"]}
#                         </div>
#                         """, 
#                         unsafe_allow_html=True
#                     )
#                 else:
#                     st.markdown(
#                         f"""
#                         <div class="chat-bubble assistant-bubble">
#                             <span class="timestamp">{timestamp}</span>
#                             <strong>AI Assistant:</strong><br>
#                             {message["content"]}
#                         </div>
#                         """, 
#                         unsafe_allow_html=True
#                     )
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             # Input area
#             st.markdown('<div class="input-area">', unsafe_allow_html=True)
#             user_query = st.text_area("What would you like to know about Human Design?", key="user_input", height=100)
#             submit_button = st.button("Submit", key="submit")
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             # Process user query
#             if submit_button and user_query:
#                 # Add timestamp to user message
#                 current_time = datetime.now().strftime("%H:%M:%S")
#                 st.session_state.chat_history.append({"role": "user", "content": user_query, "timestamp": current_time})
                
#                 # Display loading indicator
#                 with st.spinner("Thinking..."):
#                     try:
#                         # Load embedded data (from file or default)
#                         embedded_data = load_embedded_data(st.session_state.embedded_data_path)
                        
#                         # Get response based on expertise level
#                         if st.session_state.expertise_level == "client":
#                             response, top_chunks = get_client_response(user_query, embedded_data, temperature=st.session_state.gpt_temperature)
#                             st.session_state.analysis_data = {
#                                 "top_chunks": top_chunks,
#                                 "expanded_keywords": None
#                             }
#                         else:
#                             response, analysis_data = get_consultant_response(user_query, embedded_data, temperature=st.session_state.gpt_temperature)
#                             st.session_state.analysis_data = analysis_data
                        
#                         # Add assistant response with timestamp
#                         st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now().strftime("%H:%M:%S")})
                        
#                         try:
#                             st.experimental_rerun()
#                         except AttributeError:
#                             # If st.experimental_rerun is not available, do nothing
#                                 pass
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")
        
#         with col2:
#             st.markdown("<h3>Conversation Metrics</h3>", unsafe_allow_html=True)
#             create_metrics_dashboard(st.session_state.chat_history)
    
#     # Analysis Tab (visible for consultant mode)
#     with tabs[1]:
#         if st.session_state.expertise_level == "consultant" and st.session_state.analysis_data:
#             st.markdown(
#                 """
#                 <div class="glass" style="padding: 15px; border-radius: 12px; margin-bottom: 20px;">
#                     <h2>Analysis Dashboard</h2>
#                 """, 
#                 unsafe_allow_html=True
#             )
            
#             # Metrics dashboard
#             create_metrics_dashboard(st.session_state.chat_history)
            
#             # Display expanded keywords visualization if available
#             if st.session_state.analysis_data.get("expanded_keywords"):
#                 keywords_fig = display_keyword_visualization(
#                     st.session_state.analysis_data["expanded_keywords"]
#                 )
#                 if keywords_fig:
#                     st.plotly_chart(keywords_fig, use_container_width=True)
            
#             # Display chunk relevance visualization if available
#             if st.session_state.analysis_data.get("original_top_chunks"):
#                 relevance_fig = display_chunk_relevance(
#                     st.session_state.analysis_data["original_top_chunks"]
#                 )
#                 if relevance_fig:
#                     st.plotly_chart(relevance_fig, use_container_width=True)
            
#             # Expandable raw analysis data view
#             with st.expander("Show Raw Analysis Data"):
#                 st.json(st.session_state.analysis_data)
            
#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.info("Switch to consultant mode or wait for analysis data to be generated.")



#     with tabs[2]:
#         st.markdown(
#         """
#         <div class="glass" style="padding: 15px; border-radius: 12px; margin-bottom: 20px;">
#             <h2>Knowledge Graph Explorer</h2>
#             <p>Explore how Human Design concepts are interconnected. Select concepts to see their relationships and discover new connections.</p>
#         </div>
#         """, 
#         unsafe_allow_html=True
#     )
    
#     # Load embedded data
#     embedded_data = load_embedded_data(st.session_state.embedded_data_path)
    
#     # Add session state for knowledge graph if not already there
#     if 'knowledge_graph' not in st.session_state:
#         st.session_state.knowledge_graph = None
    
#     # Add a button to generate the knowledge graph
#     generate_graph = st.button("Generate Knowledge Graph", key="generate_graph")
    
#     # Generate the graph when the button is clicked
#     if generate_graph or st.session_state.knowledge_graph is not None:
#         if st.session_state.knowledge_graph is None:
#             with st.spinner("Building knowledge graph... This may take a moment."):
#                 G = build_knowledge_graph(embedded_data)
#                 st.session_state.knowledge_graph = G
#                 st.success("Knowledge graph built successfully!")
#         else:
#             G = st.session_state.knowledge_graph
        
#         # Layout with two columns
#         col1, col2 = st.columns([1, 3])
        
#         with col1:
#             st.markdown("<h3>Explore Concepts</h3>", unsafe_allow_html=True)
            
#             # Get all concepts (nodes) from the graph
#             all_concepts = sorted(list(G.nodes()))
            
#             # Search box for finding concepts
#             search_term = st.text_input("Search concepts", "")
#             if search_term:
#                 filtered_concepts = [c for c in all_concepts if search_term.lower() in c.lower()]
#                 st.write(f"Found {len(filtered_concepts)} matching concepts")
#             else:
#                 filtered_concepts = all_concepts
            
#             # Concept selection
#             selected_concept = st.selectbox(
#                 "Select a concept to explore", 
#                 options=filtered_concepts if filtered_concepts else ["No matching concepts"]
#             )
            
#             if selected_concept in G.nodes():
#                 # Show related concepts
#                 st.markdown("<h4>Related Concepts</h4>", unsafe_allow_html=True)
#                 related = find_related_concepts(G, selected_concept)
                
#                 for concept, distance in list(related.items())[:10]:  # Show top 10 related concepts
#                     relationship_strength = G[selected_concept][concept]['weight'] if G.has_edge(selected_concept, concept) else "Indirect"
#                     st.markdown(
#                         f"""
#                         <div class="card" style="padding: 8px; margin-bottom: 8px;">
#                             <strong>{concept}</strong><br>
#                             <small>Distance: {distance}, Strength: {relationship_strength}</small>
#                         </div>
#                         """, 
#                         unsafe_allow_html=True
#                     )
                
#                 # Show concept statistics
#                 st.markdown("<h4>Concept Statistics</h4>", unsafe_allow_html=True)
#                 degree = G.degree(selected_concept)
#                 st.markdown(
#                     f"""
#                     <div class="metric-card">
#                         <div class="metric-label">Connections</div>
#                         <div class="metric-value">{degree}</div>
#                     </div>
#                     """, 
#                     unsafe_allow_html=True
#                 )
                
#                 # Add button to reset/rebuild the graph
#                 if st.button("Rebuild Knowledge Graph", key="rebuild_graph"):
#                     st.session_state.knowledge_graph = None
#                     st.experimental_rerun()
                
#         with col2:
#             st.markdown("<h3>Knowledge Graph Visualization</h3>", unsafe_allow_html=True)
            
#             # Controls for the visualization
#             viz_options = st.expander("Visualization Guide")
#             with viz_options:
#                 st.markdown(
#                     """
#                     - **Node Size**: Larger nodes have more connections
#                     - **Colors**:
#                         - **Red**: Highly connected concepts (central to Human Design)
#                         - **Purple**: Moderately connected concepts
#                         - **Blue**: Less connected concepts (specific topics)
#                     - **Interactive controls**:
#                         - Click and drag nodes to rearrange
#                         - Scroll to zoom in/out
#                         - Click on nodes to focus
#                     """, unsafe_allow_html=True
#                 )
            
#             # Generate the graph visualization
#             try:
#                 graph_html = visualize_knowledge_graph(G)
                
#                 # Display the graph
#                 st.components.v1.html(graph_html, height=600)
                
#                 # Option to download the graph data
#                 graph_data = export_knowledge_graph(G)
#                 download_json = json.dumps(graph_data)
#                 st.download_button(
#                     "Download Graph Data", 
#                     data=download_json,
#                     file_name="human_design_knowledge_graph.json",
#                     mime="application/json"
#                 )
#             except Exception as e:
#                 st.error(f"Error rendering knowledge graph: {str(e)}")
#     else:
#         # Show a placeholder and instructions when the graph hasn't been generated yet
#         st.info("Click the 'Generate Knowledge Graph' button to build and visualize relationships between Human Design concepts.")
        
#         # Add a sample image or description
#         st.markdown(
#             """
#             <div class="card">
#                 <h3>What is a Knowledge Graph?</h3>
#                 <p>A knowledge graph shows how different concepts in Human Design relate to each other. The graph visualization will help you:</p>
#                 <ul>
#                     <li>Discover connections between concepts you might not have known</li>
#                     <li>See which concepts are central to Human Design</li>
#                     <li>Navigate through related topics visually</li>
#                     <li>Understand the overall structure of Human Design knowledge</li>
#                 </ul>
#                 <p>Building the graph may take a moment as it analyzes relationships across all the content.</p>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

# # Run the application
# if __name__ == "__main__":
#     main()



import streamlit as st
import openai
import json
import numpy as np
import time
import random
try:
    from openai.error import RateLimitError
except ModuleNotFoundError:
    from openai import RateLimitError

from datetime import datetime
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pdfkit
import networkx as nx
from pyvis.network import Network
import tempfile
import os
import re
from streamlit_elements import elements, dashboard, mui, html

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if running on Streamlit Cloud or other cloud platform
is_cloud = os.environ.get('IS_CLOUD', False)

# Adjust settings based on deployment environment
if is_cloud:
    # Cloud-specific configurations
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Running in cloud environment")
    
    # Set cache directory to a writable location in cloud
    cache_dir = os.environ.get('CACHE_DIR', '/tmp/streamlit_cache')
    os.makedirs(cache_dir, exist_ok=True)
    
    # Additional cloud security measures
    os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
    
    # Error handling for cloud environment
    try:
        # Your existing app code will go here
        pass
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}")
else:
    # Local development settings
    print("Running in local development environment")

# Set page config with custom properties
st.set_page_config(
    page_title="Human-Design AI Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Setup
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-4"
CONSULTANT_MODEL = "gpt-4.5-preview"

# Custom CSS with animations and modern design
def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400&display=swap');
    
    :root {
        --primary: #6C63FF;
        --primary-light: #8A84FF;
        --secondary: #FF6584;
        --dark: #1E1E2E;
        --dark-lighter: #313244;
        --light: #F8F9FA;
        --success: #72E5BE;
        --warning: #FFD166;
        --accent: #BD93F9;
    }
    
    /* Main styles */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, var(--dark), #292D3E);
        color: var(--light);
        font-family: 'Raleway', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Raleway', sans-serif;
        font-weight: 600;
        color: white;
    }
    
    h1 {
        background: linear-gradient(90deg, var(--primary), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
        text-align: center;
        font-size: 2.5rem;
    }
    
    /* Logo pulse animation */
    .logo-pulse {
        animation: pulse 2s infinite ease-in-out;
        display: inline-block;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Chat bubbles with animations */
    .chat-container {
        padding: 10px;
        max-height: 70vh;
        overflow-y: auto;
        backdrop-filter: blur(5px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background-color: rgba(30, 30, 46, 0.6);
        margin-bottom: 20px;
    }
    
    .chat-bubble {
        background-color: rgba(50, 50, 70, 0.85);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        position: relative;
        animation: fadeIn 0.5s ease-out;
        border-left: 3px solid var(--primary);
        line-height: 1.6;
    }
    
    .user-bubble {
        background-color: rgba(108, 99, 255, 0.2);
        border-left: 3px solid var(--primary);
    }
    
    .assistant-bubble {
        background-color: rgba(189, 147, 249, 0.15);
        border-left: 3px solid var(--accent);
    }
    
    .timestamp {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.6);
        position: absolute;
        top: 5px;
        right: 10px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Citations styling */
    .citation {
        background-color: rgba(30, 30, 46, 0.8);
        border-left: 4px solid var(--warning);
        padding: 12px 15px;
        margin: 12px 0;
        font-size: 0.85em;
        border-radius: 0 8px 8px 0;
        position: relative;
    }
    
    .citation strong {
        color: var(--warning);
    }
    
    /* Input area */
    .input-area {
        background-color: rgba(49, 50, 68, 0.8);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 15px;
    }
    
    /* Custom button styles */
    .custom-button {
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25);
    }
    
    .danger-button {
        background: linear-gradient(90deg, var(--secondary), #FF8FB3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark), var(--dark-lighter));
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .sidebar-content {
        padding: 20px;
    }
    
    /* Card component */
    .card {
        background-color: rgba(49, 50, 68, 0.7);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        background: var(--primary);
        color: white;
        border-radius: 20px;
        font-size: 0.7em;
        margin-right: 5px;
        font-weight: 600;
    }
    
    .badge-success {
        background: var(--success);
    }
    
    .badge-warning {
        background: var(--warning);
        color: var(--dark);
    }
    
    /* Code blocks */
    pre {
        background-color: rgba(30, 30, 46, 0.8) !important;
        padding: 12px !important;
        border-radius: 8px !important;
        border-left: 3px solid var(--accent) !important;
        font-family: 'JetBrains Mono', monospace !important;
        overflow-x: auto !important;
    }
    
    code {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--light) !important;
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        position: relative;
    }
    
    .loading:after {
        content: " ";
        display: block;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        margin: 8px;
        border: 4px solid var(--primary);
        border-color: var(--primary) transparent var(--primary) transparent;
        animation: loading 1.2s linear infinite;
    }
    
    @keyframes loading {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Radio buttons */
    div[role="radiogroup"] label {
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    div[role="radiogroup"] label:hover {
        color: var(--primary);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-light);
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltip-text {
        visibility: hidden;
        width: 120px;
        background-color: var(--dark-lighter);
        color: var(--light);
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    
    /* Input field */
    input[type="text"], textarea {
        background-color: rgba(30, 30, 46, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: var(--light) !important;
        padding: 12px !important;
    }
    
    input[type="text"]:focus, textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.2) !important;
    }
    
    /* Glowing elements */
    .glow {
        position: relative;
    }
    
    .glow::after {
        content: "";
        position: absolute;
        top: -5px;
        left: -5px;
        right: -5px;
        bottom: -5px;
        z-index: -1;
        background: linear-gradient(45deg, var(--primary), var(--accent), var(--secondary), var(--primary));
        background-size: 400% 400%;
        border-radius: 16px;
        animation: glowing 15s ease infinite;
        opacity: 0.6;
        filter: blur(10px);
    }
    
    @keyframes glowing {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating element animation */
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* Metrics cards */
    .metric-card {
        background: rgba(49, 50, 68, 0.7);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 10px 0;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        margin: 0 2px;
        background-color: var(--light);
        border-radius: 50%;
        display: inline-block;
        opacity: 0.4;
    }
    
    .typing-indicator span:nth-child(1) {
        animation: typing 1s infinite 0s;
    }
    
    .typing-indicator span:nth-child(2) {
        animation: typing 1s infinite 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation: typing 1s infinite 0.4s;
    }
    
    @keyframes typing {
        0% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.4; transform: scale(1); }
    }
    
    /* Glass effect */
    .glass {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 5px;
    }
    
    .status-online {
        background-color: var(--success);
        box-shadow: 0 0 5px var(--success);
    }
    
    .status-busy {
        background-color: var(--warning);
        box-shadow: 0 0 5px var(--warning);
    }
    
    /* Text gradients */
    .text-gradient {
        background: linear-gradient(90deg, var(--primary), var(--accent));
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Dividers */
    .divider {
        height: 1px;
        background: linear-gradient(to right, rgba(255,255,255,0), rgba(255,255,255,0.1), rgba(255,255,255,0));
        margin: 20px 0;
    }
    
    /* Notification badge */
    .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background-color: var(--secondary);
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """

def inject_pwa_capabilities():
    """Inject PWA capabilities into the Streamlit app."""
    # Add PWA meta tags and links
    st.markdown(
        """
        <head>
            <link rel="manifest" href="static/manifest.json">
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="black">
            <meta name="apple-mobile-web-app-title" content="HD Assistant">
            <link rel="apple-touch-icon" href="static/icon-192.png">
            <meta name="theme-color" content="#6C63FF">
        </head>
        """,
        unsafe_allow_html=True
    )
    
    # Add service worker registration script
    st.markdown(
        """
        <script>
            // Check if service workers are supported
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', () => {
                    navigator.serviceWorker.register('static/service-worker.js')
                        .then(registration => {
                            console.log('ServiceWorker registration successful');
                        })
                        .catch(error => {
                            console.error('ServiceWorker registration failed:', error);
                        });
                });
            }
        </script>
        """,
        unsafe_allow_html=True
    )

# Load and embed data functions
def load_embedded_data(json_path="embedded_data.json"):
    """Load previously embedded data from a JSON file."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading embedded data: {e}")
        return []

def embed_query(query, model="text-embedding-ada-002"):
    """Create an embedding for the user query."""
    response = openai.Embedding.create(
        input=query,
        model=model
    )
    return response["data"][0]["embedding"]

def cosine_similarity(vec_a, vec_b):
    """Compute cosine similarity between two vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_top_chunks(query, embedded_data, top_k=5):
    """Retrieve the top matching chunks based on the user query."""
    query_vec = embed_query(query)
    scored = []
    for item in embedded_data:
        score = cosine_similarity(query_vec, item["embedding"])
        scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]

# GPT functions with advanced error handling
def ask_gpt(prompt, model=GPT_MODEL, temperature=0.3, max_retries=3):
    """Call the OpenAI ChatCompletion API with error handling and retries."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response["choices"][0]["message"]["content"]
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                return "I'm experiencing high demand right now. Please try again in a moment."
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return f"I encountered an error: {str(e)}. Please try again."
    
    return "I'm having trouble connecting to my knowledge base. Please try again."

# Build prompt functions
def build_chat_prompt(query, top_chunks):
    """Construct an enhanced prompt that includes the relevant context chunks."""
    context_texts = []
    for i, (score, chunk) in enumerate(top_chunks):
        snippet = f"[CHUNK #{i} | Score: {score:.4f}]\n{chunk['chunk_text']}\n"
        context_texts.append(snippet)

    context_block = "\n\n".join(context_texts)
    current_date = datetime.now().strftime("%B %d, %Y")
    
    system_message = (
        f"You are a helpful Human Design consultant assistant. Today is {current_date}. "
        "Use the provided CONTEXT and your knowledge to answer the question thoroughly. "
        "If you are unsure about something, acknowledge the limitation in your knowledge. "
        "Your answer should be detailed, helpful, and formatted in a way that's easy to read. "
        "Include specific examples where appropriate.\n\n"
    )
    
    prompt = (
        f"{system_message}"
        f"CONTEXT:\n{context_block}\n"
        f"USER QUESTION:\n{query}\n"
        "Please provide a clear, detailed, and helpful answer."
    )
    return prompt

# Extract keywords for semantic expansion
def extract_keywords_for_chunk(chunk_text, user_query, retry_delay=2, max_retries=3):
    """Extract relevant keywords from the given chunk related to the user query."""
    prompt = (
        "You are an expert at extracting keywords. Given the following text and user query, "
        "list exactly 10 single-word keywords (separated by commas) that are most relevant to the user's query.\n\n"
        f"TEXT:\n{chunk_text}\n\n"
        f"USER QUERY:\n{user_query}\n\n"
        "Return exactly 10 keywords, separated by commas."
    )
    
    for attempt in range(max_retries):
        try:
            response = ask_gpt(prompt, temperature=0.5)
            keywords = [kw.strip() for kw in response.split(",") if kw.strip()]
            return keywords[:10]
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                # Fallback to basic keyword extraction
                return user_query.lower().split()[:10]
    
    return user_query.lower().split()[:10]

def select_relevant_keywords(all_keywords, user_query):
    """Select the most relevant unique keywords for query expansion."""
    keywords_str = ", ".join(all_keywords)
    prompt = (
        "You are an expert at analyzing keyword relevance. Given the following list of keywords and a user query, "
        "select the 10 most relevant unique keywords that best capture the essence of the user query. "
        "Return exactly 10 keywords as a comma-separated list.\n\n"
        f"KEYWORDS:\n{keywords_str}\n\n"
        f"USER QUERY:\n{user_query}\n\n"
        "Return exactly 10 keywords."
    )
    
    try:
        response = ask_gpt(prompt, temperature=0.5)
        selected = [kw.strip() for kw in response.split(",") if kw.strip()]
        return selected[:10]
    except Exception:
        # Fallback to random selection if there's an error
        if len(all_keywords) > 10:
            return random.sample(all_keywords, 10)
        return all_keywords

# Response generation function for client
def get_client_response(user_query, embedded_data, temperature=0.3):
    """Get a response for the client with a simpler approach."""
    top_chunks = find_top_chunks(user_query, embedded_data, top_k=5)
    prompt = build_chat_prompt(user_query, top_chunks)
    answer = ask_gpt(prompt, temperature=temperature)
    return answer, top_chunks

# Advanced response generation for consultant
def get_consultant_response(user_query, embedded_data, temperature=0.7):
    """Generate a comprehensive response for consultants with two-stage retrieval and detailed citations."""
    # First retrieval pass
    original_top_chunks = find_top_chunks(user_query, embedded_data, top_k=5)
    
    # Extract keywords from each chunk for query expansion
    all_keywords = []
    for score, chunk in original_top_chunks:
        keywords = extract_keywords_for_chunk(chunk['chunk_text'], user_query)
        all_keywords.extend(keywords)
    
    # Select the most relevant keywords and create expanded query
    expanded_keywords = select_relevant_keywords(all_keywords, user_query)
    expanded_query = " ".join(expanded_keywords)
    
    # Second retrieval with the expanded query
    secondary_top_chunks = find_top_chunks(expanded_query, embedded_data, top_k=5)
    
    # Combine chunks with detailed formatting
    context_texts = []
    for i, (score, chunk) in enumerate(original_top_chunks):
        context_texts.append(
            f"<div class='citation'><strong>Primary Source #{i+1} (Relevance: {score:.2f}):</strong><br>{chunk['chunk_text']}</div>"
        )
    for i, (score, chunk) in enumerate(secondary_top_chunks):
        context_texts.append(
            f"<div class='citation'><strong>Expanded Source #{i+1} (Relevance: {score:.2f}):</strong><br>{chunk['chunk_text']}</div>"
        )
    context_block = "\n".join(context_texts)
    
    # Build an enhanced system prompt for consultants
    current_date = datetime.now().strftime("%B %d, %Y")
    system_prompt = (
        f"You are a highly knowledgeable Human Design consultant. Today is {current_date}. "
        "Use all the CONTEXT provided below to answer the USER QUESTION comprehensively. "
        "In your answer, integrate information from all relevant sources and clearly cite them using appropriate "
        "notation (e.g., [Primary Source #2]). Your answer should demonstrate deep expertise, provide "
        "practical insights, and guide the user toward a clear understanding of Human Design principles. "
        "Include specific examples and applications where appropriate."
    )
    
    # Final prompt
    final_prompt = (
        f"{system_prompt}\n\n"
        f"CONTEXT:\n{context_block}\n\n"
        f"USER QUESTION:\n{user_query}\n\n"
        "Please provide your expert answer below."
    )
    
    # Call GPT with a higher temperature for more creative responses
    final_answer = ask_gpt(final_prompt, model=CONSULTANT_MODEL, temperature=temperature)
    
    return final_answer, {
        "original_top_chunks": original_top_chunks,
        "secondary_top_chunks": secondary_top_chunks,
        "expanded_keywords": expanded_keywords,
        "expanded_query": expanded_query
    }

# Helper functions for UI components
def create_metrics_dashboard(chat_history):
    """Create a metrics dashboard with statistics about the conversation."""
    if not chat_history:
        return
    
    num_messages = len(chat_history)
    user_messages = [msg for msg in chat_history if msg["role"] == "user"]
    avg_user_len = sum(len(msg["content"]) for msg in user_messages) / max(len(user_messages), 1)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Messages</div>
                <div class="metric-value">{num_messages}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">User Messages</div>
                <div class="metric-value">{len(user_messages)}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Avg. Query Length</div>
                <div class="metric-value">{int(avg_user_len)}</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Session Time</div>
                <div class="metric-value">{random.randint(5, 30)} min</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

def display_keyword_visualization(keywords):
    """Create a visualization of the expanded keywords."""
    if not keywords:
        return
    
    # Create a dataframe for the keywords
    keyword_data = pd.DataFrame({
        'Keyword': keywords,
        'Relevance': [random.uniform(0.6, 1.0) for _ in range(len(keywords))]
    })
    
    # Create a horizontal bar chart
    fig = px.bar(
        keyword_data, 
        y='Keyword', 
        x='Relevance', 
        orientation='h',
        color='Relevance',
        color_continuous_scale='Viridis',
        title='Query Expansion Keywords'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            title='Relevance Score',
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        ),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350
    )
    
    return fig

def display_chunk_relevance(top_chunks):
    """Create a visualization of chunk relevance scores."""
    if not top_chunks:
        return
    
    # Extract scores and labels
    scores = [score for score, _ in top_chunks]
    labels = [f"Chunk {i+1}" for i in range(len(top_chunks))]
    
    # Create a radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=labels,
        fill='toself',
        name='Relevance',
        line=dict(color='#6C63FF'),
        fillcolor='rgba(108, 99, 255, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        title="Source Relevance Scores",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=10, r=10, t=50, b=10),
        height=350
    )
    
    return fig
# PDF Report Generation function
def generate_pdf_report(chat_history, analysis_data=None, user_name="User"):
    """Generate a PDF report from the chat history and analysis data."""
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Create HTML content for the report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Human Design Reading - {user_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 40px; }}
            h1, h2, h3 {{ color: #6C63FF; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .section {{ margin: 20px 0; }}
            .chat-entry {{ margin: 15px 0; padding: 10px; border-radius: 8px; }}
            .user-message {{ background-color: rgba(108, 99, 255, 0.1); }}
            .assistant-message {{ background-color: rgba(189, 147, 249, 0.1); }}
            .footer {{ text-align: center; margin-top: 50px; font-size: 0.8em; color: #777; }}
            .highlight {{ background-color: #FFD166; padding: 2px 4px; border-radius: 3px; }}
            .keywords {{ margin: 20px 0; }}
            .keyword-chip {{ display: inline-block; background-color: #6C63FF; color: white; 
                          padding: 5px 10px; margin: 5px; border-radius: 20px; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Human Design Reading</h1>
            <h2>Prepared for: {user_name}</h2>
            <p>Date: {current_date}</p>
        </div>
        
        <div class="section">
            <h3>Consultation Summary</h3>
            <p>This report summarizes your Human Design reading session and contains key insights and guidance based on our conversation.</p>
    """
    
    # Add key highlights section if we have analysis data
    if analysis_data and analysis_data.get("expanded_keywords"):
        html_content += """
        <div class="section">
            <h3>Key Highlights</h3>
            <div class="keywords">
        """
        for keyword in analysis_data.get("expanded_keywords", []):
            html_content += f'<span class="keyword-chip">{keyword}</span>'
        html_content += """
            </div>
        </div>
        """
    
    # Add conversation transcript
    html_content += """
        <div class="section">
            <h3>Conversation Transcript</h3>
    """
    
    for message in chat_history:
        if message["role"] == "user":
            html_content += f"""
            <div class="chat-entry user-message">
                <strong>Your Question:</strong><br>
                {message["content"]}
            </div>
            """
        else:
            # Highlight keywords in assistant messages
            highlighted_content = message["content"]
            if analysis_data and analysis_data.get("expanded_keywords"):
                for keyword in analysis_data.get("expanded_keywords", []):
                    pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                    highlighted_content = pattern.sub(f'<span class="highlight">\\g<0></span>', highlighted_content)
            
            html_content += f"""
            <div class="chat-entry assistant-message">
                <strong>AI Consultant:</strong><br>
                {highlighted_content}
            </div>
            """
    
    # Add sources and information used
    if analysis_data and (analysis_data.get("original_top_chunks") or analysis_data.get("secondary_top_chunks")):
        html_content += """
        <div class="section">
            <h3>Sources & References</h3>
        """
        
        if analysis_data.get("original_top_chunks"):
            html_content += "<h4>Primary Sources</h4>"
            for i, (score, chunk) in enumerate(analysis_data.get("original_top_chunks", [])):
                html_content += f"""
                <div class="chat-entry">
                    <strong>Source #{i+1} - Relevance: {score:.2f}</strong><br>
                    {chunk['chunk_text'][:200]}...
                </div>
                """
        
        html_content += """
        </div>
        """
    
    # Footer
    html_content += """
        <div class="footer">
            <p>Generated by Human Design AI Assistant</p>
        </div>
    </body>
    </html>
    """
    
    # Create a temporary file for the HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_html:
        temp_html.write(html_content.encode('utf-8'))
        temp_html_path = temp_html.name
    
    # Create a temporary file for the PDF
    temp_pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_pdf_path = temp_pdf_file.name
    temp_pdf_file.close()
    
    try:
        # Convert HTML to PDF
        pdfkit.from_file(temp_html_path, temp_pdf_path)
        
        # Read the PDF file
        with open(temp_pdf_path, 'rb') as pdf_file:
            return pdf_file.read()
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None
    finally:
        # Clean up temporary files
        os.unlink(temp_html_path)
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)

# Function to build knowledge graph
def build_knowledge_graph(embedded_data, max_nodes=30):
    """Build a knowledge graph from the embedded data."""
    G = nx.Graph()
    
    # Extract main concepts and their relationships
    concepts = set()
    relationships = []
    
    # Use the first max_nodes chunks to build the graph
    for i, item in enumerate(embedded_data[:max_nodes]):
        # Extract keywords for each chunk
        chunk_text = item["chunk_text"]
        prompt = (
            "Extract exactly 5 key concepts from this text about Human Design. "
            "Return only a comma-separated list of these concepts, no explanations or additional text.\n\n"
            f"TEXT:\n{chunk_text}\n"
        )
        
        try:
            response = ask_gpt(prompt, temperature=0.3)
            chunk_concepts = [concept.strip() for concept in response.split(",")]
            
            # Add nodes for each concept
            for concept in chunk_concepts:
                if concept and len(concept) > 3:  # Filter out too short concepts
                    concepts.add(concept)
                    G.add_node(concept)
            
            # Add edges between concepts within the same chunk
            for i, concept1 in enumerate(chunk_concepts):
                if not concept1 or len(concept1) <= 3:
                    continue
                for concept2 in chunk_concepts[i+1:]:
                    if not concept2 or len(concept2) <= 3:
                        continue
                    if G.has_edge(concept1, concept2):
                        # Increase edge weight if it already exists
                        G[concept1][concept2]['weight'] += 1
                    else:
                        G.add_edge(concept1, concept2, weight=1)
        except Exception as e:
            continue
    
    return G

# Function to visualize the knowledge graph
def visualize_knowledge_graph(G):
    """Create an interactive visualization of the knowledge graph."""
    # Create a Pyvis network
    net = Network(height="500px", width="100%", bgcolor="#1E1E2E", font_color="white")
    
    # Set options
    net.barnes_hut(gravity=-80000, central_gravity=0.3, spring_length=250, spring_strength=0.001, damping=0.09)
    
    # Add nodes and edges
    for node in G.nodes():
        net.add_node(node, label=node, title=node, color="#6C63FF")
    
    for edge in G.edges(data=True):
        source, target, data = edge
        weight = data.get('weight', 1)
        net.add_edge(source, target, value=weight, title=f"Weight: {weight}")
    
    # Generate the visualization
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as temp_file:
        temp_path = temp_file.name
        net.save_graph(temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            graph_html = f.read()
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        return graph_html
# Function to find related concepts
def find_related_concepts(G, concept, max_distance=2):
    """Find concepts related to a given concept up to a certain distance in the graph."""
    related = {}
    
    if concept not in G.nodes():
        return related
    
    # Find all nodes within max_distance
    for node in G.nodes():
        if node == concept:
            continue
        
        try:
            # Calculate shortest path length
            path_length = nx.shortest_path_length(G, source=concept, target=node)
            if path_length <= max_distance:
                related[node] = path_length
        except nx.NetworkXNoPath:
            # No path exists
            continue
    
    # Sort by distance (closest first)
    return dict(sorted(related.items(), key=lambda x: x[1]))

# Function to export the knowledge graph as JSON for external visualization
def export_knowledge_graph(G):
    """Export the knowledge graph in a format suitable for D3.js or other visualization libraries."""
    data = {
        "nodes": [],
        "links": []
    }
    
    # Add nodes
    for node in G.nodes():
        degree = G.degree(node)
        data["nodes"].append({
            "id": node,
            "name": node,
            "degree": degree,
            "group": 1 + (degree // 2)  # Group nodes by connectivity
        })
    
    # Add edges
    for source, target, attrs in G.edges(data=True):
        weight = attrs.get('weight', 1)
        data["links"].append({
            "source": source,
            "target": target,
            "value": weight
        })
    
    return data

# Function to highlight keywords in text
def highlight_keywords(text, keywords):
    """Highlight keywords in the given text."""
    if not keywords:
        return text
    
    highlighted_text = text
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        highlighted_text = pattern.sub(f'<span class="keyword-highlight">\\g<0></span>', highlighted_text)
    
    return highlighted_text
    
# Custom component for the welcome animation
def render_lottie_animation():
    lottie_json = {
        "v": "5.5.7",
        "fr": 30,
        "ip": 0,
        "op": 180,
        "w": 1920,
        "h": 1080,
        "nm": "AI Assistant",
        "ddd": 0,
        "assets": [],
        "layers": [
            {
                "ddd": 0,
                "ind": 1,
                "ty": 4,
                "nm": "Circle",
                "sr": 1,
                "ks": {
                    "o": {"a": 1, "k": [
                        {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 0, "s": [0]},
                        {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 30, "s": [100]},
                        {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 150, "s": [100]},
                        {"t": 180, "s": [0]}
                    ]},
                    "p": {"a": 0, "k": [960, 540]},
                    "a": {"a": 0, "k": [0, 0]},
                    "s": {"a": 1, "k": [
                        {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 0, "s": [0, 0]},
                        {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 30, "s": [100, 100]},
                        {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 90, "s": [100, 100]},
                        {"i": {"x": [0.667, 0.667], "y": [1, 1]}, "o": {"x": [0.333, 0.333], "y": [0, 0]}, "t": 150, "s": [120, 120]},
                        {"t": 180, "s": [0, 0]}
                    ]}
                },
                "shapes": [
                    {"ty": "gr", "it": [
                        {"d": 1, "ty": "el", "s": {"a": 0, "k": [400, 400]}, "p": {"a": 0, "k": [0, 0]}},
                        {"ty": "fl", "c": {"a": 0, "k": [0.42, 0.39, 1, 1]}},
                        {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}}
                    ]}
                ]
            }
        ]
    }
    
    st.markdown(
        f"""
        <div class="glow floating">
            <h1><span class="logo-pulse">🧠</span> Human Design AI Assistant</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    return base64.b64encode(json.dumps(lottie_json).encode()).decode()

def main():
    # Apply custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Initialize session state variables
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'expertise_level' not in st.session_state:
        st.session_state.expertise_level = "client"
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None
    if 'embedded_data_path' not in st.session_state:
        st.session_state.embedded_data_path = "embedded_data.json"
    if 'gpt_temperature' not in st.session_state:
        st.session_state.gpt_temperature = 0.3

    inject_pwa_capabilities()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-content">
                <h2>Settings</h2>
                <div class="card">
                    <h3>Expertise Level</h3>
            """, 
            unsafe_allow_html=True
        )
        
        expertise_level = st.radio(
            "Select your expertise level:",
            ["Client", "Consultant"],
            index=0 if st.session_state.expertise_level == "client" else 1,
            key="expertise_radio"
        )
        st.session_state.expertise_level = expertise_level.lower()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="card">
                <h3>Chat Controls</h3>
            """, 
            unsafe_allow_html=True
        )
        
        if st.button("Clear Conversation", key="clear_button"):
            st.session_state.chat_history = []
            st.session_state.analysis_data = None
            st.success("Conversation cleared!")
        
        # File uploader to update embedded data
        uploaded_file = st.file_uploader("Upload new embedded data JSON", type=["json"])
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                # Optionally, you could store this file to disk or update session state
                st.session_state.embedded_data_path = uploaded_file.name
                with open(st.session_state.embedded_data_path, "w", encoding="utf-8") as f:
                    json.dump(data, f)
                st.success("Embedded data updated!")
            except Exception as e:
                st.error(f"Error processing file: {e}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="card">
                <h3>API Settings</h3>
            """, 
            unsafe_allow_html=True
        )
        st.session_state.gpt_temperature = st.slider("GPT Temperature", 0.0, 1.0, st.session_state.gpt_temperature, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download chat history
        chat_json = json.dumps(st.session_state.chat_history, indent=2)
        st.download_button("Download Chat History", data=chat_json, file_name="chat_history.json")
        
        # About section
        st.markdown(
            """
            <div class="card">
                <h3>About</h3>
                <p>This AI assistant helps you explore Human Design concepts and answer your questions.</p>
                <p><span class="badge">GPT-4 Powered</span> <span class="badge badge-success">Semantic Search</span></p>
            </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Main content using tabs
    tabs = st.tabs(["Chat", "Analysis", "Knowledge Graph"])
    
    # Chat Tab
    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        with col1:
            # Welcome animation and header
            lottie_data = render_lottie_animation()
            
            # Chat display container
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                timestamp = message.get("timestamp", "")
                if message["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-bubble user-bubble">
                            <span class="timestamp">{timestamp}</span>
                            <strong>You:</strong><br>
                            {message["content"]}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-bubble assistant-bubble">
                            <span class="timestamp">{timestamp}</span>
                            <strong>AI Assistant:</strong><br>
                            {message["content"]}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Input area
            st.markdown('<div class="input-area">', unsafe_allow_html=True)
            user_query = st.text_area("What would you like to know about Human Design?", key="user_input", height=100)
            submit_button = st.button("Submit", key="submit")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Process user query
            if submit_button and user_query:
                # Add timestamp to user message
                current_time = datetime.now().strftime("%H:%M:%S")
                st.session_state.chat_history.append({"role": "user", "content": user_query, "timestamp": current_time})
                
                # Display loading indicator
                with st.spinner("Thinking..."):
                    try:
                        # Load embedded data (from file or default)
                        embedded_data = load_embedded_data(st.session_state.embedded_data_path)
                        
                        # Get response based on expertise level
                        if st.session_state.expertise_level == "client":
                            response, top_chunks = get_client_response(user_query, embedded_data, temperature=st.session_state.gpt_temperature)
                            st.session_state.analysis_data = {
                                "top_chunks": top_chunks,
                                "expanded_keywords": None
                            }
                        else:
                            response, analysis_data = get_consultant_response(user_query, embedded_data, temperature=st.session_state.gpt_temperature)
                            st.session_state.analysis_data = analysis_data
                        
                        # Add assistant response with timestamp
                        st.session_state.chat_history.append({"role": "assistant", "content": response, "timestamp": datetime.now().strftime("%H:%M:%S")})
                        
                        try:
                            st.experimental_rerun()
                        except AttributeError:
                            # If st.experimental_rerun is not available, do nothing
                                pass
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown("<h3>Conversation Metrics</h3>", unsafe_allow_html=True)
            create_metrics_dashboard(st.session_state.chat_history)
    
    # Analysis Tab (visible for consultant mode)
    with tabs[1]:
        if st.session_state.expertise_level == "consultant" and st.session_state.analysis_data:
            st.markdown(
                """
                <div class="glass" style="padding: 15px; border-radius: 12px; margin-bottom: 20px;">
                    <h2>Analysis Dashboard</h2>
                """, 
                unsafe_allow_html=True
            )
            
            # Metrics dashboard
            create_metrics_dashboard(st.session_state.chat_history)
            
            # Display expanded keywords visualization if available
            if st.session_state.analysis_data.get("expanded_keywords"):
                keywords_fig = display_keyword_visualization(
                    st.session_state.analysis_data["expanded_keywords"]
                )
                if keywords_fig:
                    st.plotly_chart(keywords_fig, use_container_width=True)
            
            # Display chunk relevance visualization if available
            if st.session_state.analysis_data.get("original_top_chunks"):
                relevance_fig = display_chunk_relevance(
                    st.session_state.analysis_data["original_top_chunks"]
                )
                if relevance_fig:
                    st.plotly_chart(relevance_fig, use_container_width=True)
            
            # Expandable raw analysis data view
            with st.expander("Show Raw Analysis Data"):
                st.json(st.session_state.analysis_data)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Switch to consultant mode or wait for analysis data to be generated.")



    with tabs[2]:
        st.markdown(
        """
        <div class="glass" style="padding: 15px; border-radius: 12px; margin-bottom: 20px;">
            <h2>Knowledge Graph Explorer</h2>
            <p>Explore how Human Design concepts are interconnected. Select concepts to see their relationships and discover new connections.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Load embedded data
    embedded_data = load_embedded_data(st.session_state.embedded_data_path)
    
    # Add session state for knowledge graph if not already there
    if 'knowledge_graph' not in st.session_state:
        st.session_state.knowledge_graph = None
    
    # Add a button to generate the knowledge graph
    generate_graph = st.button("Generate Knowledge Graph", key="generate_graph")
    
    # Generate the graph when the button is clicked
    if generate_graph or st.session_state.knowledge_graph is not None:
        if st.session_state.knowledge_graph is None:
            with st.spinner("Building knowledge graph... This may take a moment."):
                G = build_knowledge_graph(embedded_data)
                st.session_state.knowledge_graph = G
                st.success("Knowledge graph built successfully!")
        else:
            G = st.session_state.knowledge_graph
        
        # Layout with two columns
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("<h3>Explore Concepts</h3>", unsafe_allow_html=True)
            
            # Get all concepts (nodes) from the graph
            all_concepts = sorted(list(G.nodes()))
            
            # Search box for finding concepts
            search_term = st.text_input("Search concepts", "")
            if search_term:
                filtered_concepts = [c for c in all_concepts if search_term.lower() in c.lower()]
                st.write(f"Found {len(filtered_concepts)} matching concepts")
            else:
                filtered_concepts = all_concepts
            
            # Concept selection
            selected_concept = st.selectbox(
                "Select a concept to explore", 
                options=filtered_concepts if filtered_concepts else ["No matching concepts"]
            )
            
            if selected_concept in G.nodes():
                # Show related concepts
                st.markdown("<h4>Related Concepts</h4>", unsafe_allow_html=True)
                related = find_related_concepts(G, selected_concept)
                
                for concept, distance in list(related.items())[:10]:  # Show top 10 related concepts
                    relationship_strength = G[selected_concept][concept]['weight'] if G.has_edge(selected_concept, concept) else "Indirect"
                    st.markdown(
                        f"""
                        <div class="card" style="padding: 8px; margin-bottom: 8px;">
                            <strong>{concept}</strong><br>
                            <small>Distance: {distance}, Strength: {relationship_strength}</small>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Show concept statistics
                st.markdown("<h4>Concept Statistics</h4>", unsafe_allow_html=True)
                degree = G.degree(selected_concept)
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Connections</div>
                        <div class="metric-value">{degree}</div>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Add button to reset/rebuild the graph
                if st.button("Rebuild Knowledge Graph", key="rebuild_graph"):
                    st.session_state.knowledge_graph = None
                    st.experimental_rerun()
                
        with col2:
            st.markdown("<h3>Knowledge Graph Visualization</h3>", unsafe_allow_html=True)
            
            # Controls for the visualization
            viz_options = st.expander("Visualization Guide")
            with viz_options:
                st.markdown(
                    """
                    - **Node Size**: Larger nodes have more connections
                    - **Colors**:
                        - **Red**: Highly connected concepts (central to Human Design)
                        - **Purple**: Moderately connected concepts
                        - **Blue**: Less connected concepts (specific topics)
                    - **Interactive controls**:
                        - Click and drag nodes to rearrange
                        - Scroll to zoom in/out
                        - Click on nodes to focus
                    """, unsafe_allow_html=True
                )
            
            # Generate the graph visualization
            try:
                graph_html = visualize_knowledge_graph(G)
                
                # Display the graph
                st.components.v1.html(graph_html, height=600)
                
                # Option to download the graph data
                graph_data = export_knowledge_graph(G)
                download_json = json.dumps(graph_data)
                st.download_button(
                    "Download Graph Data", 
                    data=download_json,
                    file_name="human_design_knowledge_graph.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Error rendering knowledge graph: {str(e)}")
    else:
        # Show a placeholder and instructions when the graph hasn't been generated yet
        st.info("Click the 'Generate Knowledge Graph' button to build and visualize relationships between Human Design concepts.")
        
        # Add a sample image or description
        st.markdown(
            """
            <div class="card">
                <h3>What is a Knowledge Graph?</h3>
                <p>A knowledge graph shows how different concepts in Human Design relate to each other. The graph visualization will help you:</p>
                <ul>
                    <li>Discover connections between concepts you might not have known</li>
                    <li>See which concepts are central to Human Design</li>
                    <li>Navigate through related topics visually</li>
                    <li>Understand the overall structure of Human Design knowledge</li>
                </ul>
                <p>Building the graph may take a moment as it analyzes relationships across all the content.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Run the application
if __name__ == "__main__":
    main()
