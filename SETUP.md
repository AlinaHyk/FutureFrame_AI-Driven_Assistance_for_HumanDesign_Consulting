# Human Design AI Assistant - Administrator Deployment Guide

## Table of Contents
- [System Architecture Overview](#system-architecture-overview)
- [Prerequisites](#prerequisites)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Dependencies](#software-dependencies)
- [Installation and Setup from Repository](#installation-and-setup-from-repository)
  - [Cloning the Repository](#cloning-the-repository)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Configuring API Keys](#configuring-api-keys)
  - [Running the Application Locally](#running-the-application-locally)
- [Deployment Options](#deployment-options)
- [Deployment Method 1: Streamlit Cloud](#deployment-method-1-streamlit-cloud)
  - [Step 1: Create and Prepare GitHub Repository](#step-1-create-and-prepare-github-repository)
  - [Step 2: Deploy to Streamlit Cloud](#step-2-deploy-to-streamlit-cloud)
  - [Step 3: Monitor Deployment and Verify](#step-3-monitor-deployment-and-verify)
  - [Step 4: Post-Deployment Configuration](#step-4-post-deployment-configuration)
  - [Troubleshooting Streamlit Cloud Deployment](#troubleshooting-streamlit-cloud-deployment)
- [Deployment Method 2: Heroku](#deployment-method-2-heroku)
  - [Step 1: Install and Configure Heroku CLI](#step-1-install-and-configure-heroku-cli)
  - [Step 2: Prepare Your Application for Heroku Deployment](#step-2-prepare-your-application-for-heroku-deployment)
  - [Step 3: Create and Configure Heroku Application](#step-3-create-and-configure-heroku-application)
  - [Step 4: Deploy to Heroku](#step-4-deploy-to-heroku)
  - [Step 5: Post-Deployment Configuration and Verification](#step-5-post-deployment-configuration-and-verification)
  - [Step 6: Troubleshooting Heroku Deployment](#step-6-troubleshooting-heroku-deployment)
- [Deployment Method 3: Self-hosted Server](#deployment-method-3-self-hosted-server)
  - [Step 1: Server Preparation](#step-1-server-preparation)
  - [Step 2: Application Setup](#step-2-application-setup)
  - [Step 3: Configure Systemd Service](#step-3-configure-systemd-service)
  - [Step 4: Configure Nginx as Reverse Proxy](#step-4-configure-nginx-as-reverse-proxy)
  - [Troubleshooting Self-hosted Deployment](#troubleshooting-self-hosted-deployment)
- [Deployment Method 4: Docker Container](#deployment-method-4-docker-container)
  - [Step 1: Create Docker Configuration](#step-1-create-docker-configuration)
  - [Step 2: Build and Run Docker Container](#step-2-build-and-run-docker-container)
  - [Step 3: Docker Compose Setup (Optional)](#step-3-docker-compose-setup-optional)
  - [Troubleshooting Docker Deployment](#troubleshooting-docker-deployment)
- [Database Setup and Management](#database-setup-and-management)
  - [Embedded Data File Management](#embedded-data-file-management)
  - [Data Maintenance](#data-maintenance)
- [Security Considerations](#security-considerations)
  - [API Key Protection](#api-key-protection)
  - [Access Control](#access-control)
  - [Data Protection](#data-protection)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
  - [Health Checks](#health-checks)
  - [Logging](#logging)
  - [Backup Strategy](#backup-strategy)
- [Scaling Considerations](#scaling-considerations)
  - [Horizontal Scaling](#horizontal-scaling)
  - [Performance Optimization](#performance-optimization)
- [Customization Options](#customization-options)
  - [Environment Variables](#environment-variables)
  - [Application Configuration](#application-configuration)
- [Troubleshooting Common Deployment Issues](#troubleshooting-common-deployment-issues)
  - [OpenAI API Issues](#openai-api-issues)
  - [Application Startup Issues](#application-startup-issues)
  - [Memory Issues](#memory-issues)
- [Updating the Application](#updating-the-application)
  - [Code Updates](#code-updates)
  - [Embedding Updates](#embedding-updates)
- [Contact and Support](#contact-and-support)

This document provides comprehensive instructions for system administrators and developers to deploy the Human Design AI Assistant application in various environments. It covers all dependencies, configuration options, deployment strategies, and troubleshooting guidance.

## System Architecture Overview

The Human Design AI Assistant is built using the following core technologies:

- **Backend**: Python 3.8+ with Streamlit framework
- **API Integration**: OpenAI API (GPT and Embeddings)
- **Data Processing**: Custom Python scripts for document extraction and embedding generation
- **Database**: File-based storage (JSON) for embeddings
- **Frontend**: Streamlit UI with custom CSS styling
- **Visualizations**: Plotly, Networkx, PyVis
- **Progressive Web App**: Service worker and manifest configuration

The application consists of several interconnected components:
1. Document processor scripts
2. Embedding generator
3. Main Streamlit application
4. Knowledge graph generator
5. Progressive Web App components

## Prerequisites

### Hardware Requirements

- **CPU**: 2+ cores recommended
- **RAM**: Minimum 4GB, 8GB+ recommended
- **Storage**: 1GB minimum for application, 10GB+ recommended for document processing
- **Network**: Internet connection for OpenAI API access

### Software Dependencies

- **Python Environment**: Python 3.8 or higher
- **Package Manager**: pip (with optional venv or conda)
- **OpenAI API Key**: Valid API key with access to embedding and completion models
- **Git**: For source code management (optional for deployment)
- **External Tools**:
  - wkhtmltopdf (for PDF generation)
  - antiword (Linux) or wps (Windows) for .doc file processing

## Installation and Setup from Repository

Before exploring deployment options, this section provides comprehensive instructions for installing and setting up the Human Design AI Assistant from the existing repository on your local machine.

### Cloning the Repository

1. **Install Git** (if not already installed):
   - **For Windows**: Download and install from [git-scm.com](https://git-scm.com/download/win)
   - **For macOS**: 
     ```bash
     brew install git
     ```
   - **For Linux**:
     ```bash
     sudo apt-get update
     sudo apt-get install git
     ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/human-design-ai-assistant.git
   cd human-design-ai-assistant
   ```

3. **Install Git LFS** to properly handle large files:
   - **For Windows**: Download from [git-lfs.github.com](https://git-lfs.github.com/)
   - **For macOS**:
     ```bash
     brew install git-lfs
     ```
   - **For Linux**:
     ```bash
     sudo apt-get install git-lfs
     ```

4. **Initialize Git LFS and pull large files**:
   ```bash
   git lfs install
   git lfs pull
   ```

### Setting Up the Environment

1. **Install Python** (version 3.8 or higher required):
   - **For Windows**: Download from [python.org](https://www.python.org/downloads/windows/)
   - **For macOS**:
     ```bash
     brew install python@3.9
     ```
   - **For Linux**:
     ```bash
     sudo apt-get install python3.9 python3.9-venv python3-pip
     ```

2. **Create and activate a virtual environment**:
   - **For Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **For macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install additional system dependencies**:
   - **For Windows**:
     - Install wkhtmltopdf: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
     - Install WPS Office for .doc file processing
   
   - **For Linux**:
     ```bash
     sudo apt-get install wkhtmltopdf antiword
     ```
   
   - **For macOS**:
     ```bash
     brew install wkhtmltopdf antiword
     ```

### Configuring API Keys

1. **Create a .env file** in the root directory:
   ```bash
   touch .env  # On macOS/Linux
   # On Windows, create the file manually or use:
   # echo. > .env
   ```

2. **Add your OpenAI API key** to the .env file:
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "GPT_MODEL=gpt-4" >> .env
   echo "CONSULTANT_MODEL=gpt-4.5-preview" >> .env
   ```

3. **Verify API key configuration**:
   ```bash
   # Quick test script to verify API key
   python -c "
   import os
   from dotenv import load_dotenv
   load_dotenv()
   key = os.getenv('OPENAI_API_KEY')
   print(f'API key loaded: {"Success" if key else "Failed"}')
   "
   ```

### Running the Application Locally

1. **Start the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application** in your web browser:
   - The application will typically be available at http://localhost:8501
   - Streamlit will display the URL in the terminal

3. **Testing the application**:
   - Verify that the sidebar components load correctly
   - Test the chat functionality with a basic Human Design question
   - Confirm that embeddings are loaded properly
   - Check that knowledge graph generation works

4. **Troubleshooting common local setup issues**:
   - If you encounter `ModuleNotFoundError`, ensure all dependencies are installed:
     ```bash
     pip install -r requirements.txt
     ```
   - If the embeddings file fails to load, check that Git LFS pulled it correctly:
     ```bash
     git lfs pull
     ```
   - If OpenAI API calls fail, verify your API key in the .env file
   - For PDF generation issues, ensure wkhtmltopdf is properly installed and in your PATH

## Deployment Options

The Human Design AI Assistant can be deployed in several ways after successful local setup. The following sections provide detailed instructions for deploying the system completely from scratch in various environments:

1. **Streamlit Cloud** (easiest, recommended for quick setup)
2. **Heroku** (good for small to medium scale deployments)
3. **Self-hosted Server** (maximum control and customization)
4. **Docker Container** (consistent environment across deployments)

The following deployment methods are for administrators who need to set up the entire system from scratch:

## Deployment Method 1: Streamlit Cloud

Streamlit Cloud offers the easiest deployment path, handling most infrastructure details automatically. This section provides detailed, step-by-step instructions for deploying the Human Design AI Assistant on Streamlit Cloud.

### Step 1: Create and Prepare GitHub Repository

1. **Create a GitHub repository** (if you don't already have one):
   - Go to [GitHub.com](https://github.com) and sign in
   - Click the "+" icon in the top-right corner
   - Select "New repository"
   - Name your repository (e.g., "human-design-ai-assistant")
   - Choose public or private visibility
   - Click "Create repository"

2. **Initialize the repository locally**:
   ```bash
   mkdir human-design-ai-assistant
   cd human-design-ai-assistant
   git init
   git remote add origin https://github.com/yourusername/human-design-ai-assistant.git
   ```

3. **Set up Git LFS** (Large File Storage):
   - Install Git LFS if not already installed:
     ```bash
     # For Debian/Ubuntu
     sudo apt-get install git-lfs
     
     # For macOS with Homebrew
     brew install git-lfs
     
     # For Windows with Chocolatey
     choco install git-lfs
     
     # Initialize Git LFS
     git lfs install
     ```

4. **Create the necessary file structure**:
   Ensure your repository has the following structure:
   ```
   ├── app.py                   # Main application
   ├── requirements.txt         # Dependencies
   ├── embedded_data.json       # Embeddings data
   ├── .gitattributes           # Git LFS configuration
   ├── Embedings_gen.py         # Embedding generation script
   ├── Raw_audio_data.py        # Audio transcription script
   ├── Raw_data_extract.py      # Document extraction script
   └── static/                  # PWA assets directory
      ├── manifest.json         # PWA manifest
      ├── service-worker.js     # Service worker script
      └── pwa-installer.js      # PWA installation helper
   ```

5. **Configure Git LFS for large files**:
   - Create a `.gitattributes` file with LFS tracking:
     ```bash
     echo "embedded_data.json filter=lfs diff=lfs merge=lfs -text" > .gitattributes
     ```
   - Track the embedding file with LFS:
     ```bash
     git lfs track "embedded_data.json"
     ```
   - Add the files to Git:
     ```bash
     git add .gitattributes
     git add embedded_data.json
     git add app.py
     git add requirements.txt
     git add Embedings_gen.py
     git add Raw_audio_data.py
     git add Raw_data_extract.py
     git add static/
     ```
   - Commit the files:
     ```bash
     git commit -m "Initial commit with LFS configuration for large embedding file"
     ```
   - Push to GitHub:
     ```bash
     git push -u origin main
     ```

6. **Prepare the requirements.txt file**:
   Create a file named `requirements.txt` with all the dependencies:
   ```
   streamlit>=1.31.0
   openai==0.28.1
   numpy>=1.26.0
   pandas>=2.1.0
   requests==2.31.0
   python-dotenv>=1.0.0
   plotly>=5.18.0
   networkx>=3.2.0
   beautifulsoup4>=4.12.0
   pyvis>=0.3.1
   streamlit-elements>=0.1.0
   pdfkit>=1.0.0
   ```

### Step 2: Deploy to Streamlit Cloud

1. **Create a Streamlit Cloud account** (if you don't have one):
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "Sign up" and follow the registration process
   - Verify your email address

2. **Link your GitHub account**:
   - In Streamlit Cloud dashboard, click on your profile
   - Select "Settings"
   - Under "Connections," click "Connect GitHub"
   - Authorize Streamlit to access your GitHub repositories
   - Select which repositories to grant access to (or all repositories)

3. **Deploy your application**:
   - From the Streamlit Cloud dashboard, click "New app"
   - In the deployment dialog:
     - **Repository**: Select your "human-design-ai-assistant" repository
     - **Branch**: Choose "main" (or your default branch)
     - **Main file path**: Enter "app.py"

4. **Configure advanced settings**:
   - Click "Advanced settings" in the deployment dialog
   - Under "Python version", select "3.9" or above
   - Under "Packages", ensure requirements.txt is being used
   - Under "Secrets", add the following entries:
     - Add a new secret with key `OPENAI_API_KEY` and value set to your OpenAI API key
     - Add a new secret with key `IS_CLOUD` and value set to `True`

5. **Set resource allocation** (if available in your Streamlit Cloud tier):
   - Set memory to at least 1GB
   - Set CPU to at least 1 core

6. **Deploy the application**:
   - Click "Deploy!" to start the deployment process
   - Streamlit will show a progress indicator during deployment
   - This process typically takes 2-5 minutes, but may take longer for large repositories

### Step 3: Monitor Deployment and Verify

1. **Monitor the deployment process**:
   - Stay on the deployment page to monitor logs
   - Watch for any error messages or warnings
   - The status will change to "Running" when deployment is complete

2. **Open and test the application**:
   - Click the "Open app" button when it appears
   - Verify the application loads without errors
   - Check that the interface is rendered correctly
   - Confirm the sidebar elements are working
   - Test the chat functionality with a simple query about Human Design
   - Verify both client and consultant modes are functioning
   - Test the knowledge graph generation
   - Check for any console errors (using browser developer tools)

3. **Configure application settings**:
   - In the Streamlit Cloud dashboard, find your deployed app
   - Click the three dots next to your app and select "Settings"
   - Configure custom domain (if available on your plan)
   - Set up authentication if you want to restrict access
   - Configure automatic updates from GitHub if desired

4. **Set up health alerts** (if available on your plan):
   - In app settings, find "Health Alerts"
   - Enable email notifications for application downtime
   - Set up uptime monitoring

### Step 4: Post-Deployment Configuration

1. **Set up custom branding** (if needed):
   - Create a `config.toml` file in a `.streamlit` directory:
     ```bash
     mkdir -p .streamlit
     ```
   - Add branding configuration:
     ```toml
     # .streamlit/config.toml
     [theme]
     primaryColor = "#6C63FF"
     backgroundColor = "#1E1E2E"
     secondaryBackgroundColor = "#313244"
     textColor = "#F8F9FA"
     font = "sans serif"
     ```

2. **Configure GitHub webhook for CI/CD** (optional):
   - In GitHub repo settings, go to "Webhooks"
   - Add webhook pointing to Streamlit Cloud (if supported by your plan)
   - Set it to trigger on push events to main branch

3. **Set up usage monitoring** (if available):
   - Monitor application usage through the Streamlit Cloud dashboard
   - Track memory usage and performance metrics
   - Set up resource scaling if needed

### Troubleshooting Streamlit Cloud Deployment

#### Memory Issues
- **Problem**: Application crashes due to memory limits
- **Solution**:
  1. Reduce batch processing sizes in code:
     ```python
     # Before
     process_all_items(large_list)
     
     # After - process in smaller batches
     def batch_process(items, batch_size=50):
         for i in range(0, len(items), batch_size):
             yield items[i:i + batch_size]
     
     for batch in batch_process(large_list):
         process_items(batch)
     ```
  2. Optimize the embedded_data.json file:
     ```bash
     # Script to reduce embedding dimensions or prune less relevant entries
     python -c "
     import json
     with open('embedded_data.json', 'r') as f:
         data = json.load(f)
     
     # Keep only essential fields
     optimized_data = []
     for item in data:
         optimized_item = {
             'chunk_text': item['chunk_text'],
             'embedding': item['embedding'],
             'metadata': {
                 'chunk_index': item['metadata']['chunk_index'],
                 'file_name': item['metadata']['file_name']
             }
         }
         optimized_data.append(optimized_item)
     
     with open('embedded_data_optimized.json', 'w') as f:
         json.dump(optimized_data, f)
     "
     ```
  3. Upgrade to a higher memory tier in Streamlit Cloud

#### Timeout Errors
- **Problem**: Long-running operations cause timeouts
- **Solution**:
  1. Implement progress indicators:
     ```python
     # Add progress bar for long operations
     with st.progress(0) as progress_bar:
         for i, item in enumerate(items):
             process_item(item)
             progress_bar.progress((i+1)/len(items))
     ```
  2. Use caching for expensive operations:
     ```python
     @st.cache_data(ttl=3600)  # Cache for 1 hour
     def expensive_operation(data):
         # processing logic
         return result
     ```
  3. Split long operations into smaller steps:
     ```python
     if 'processing_step' not in st.session_state:
         st.session_state.processing_step = 0
         st.session_state.results = []
     
     # Show progress
     st.write(f"Processing step {st.session_state.processing_step + 1} of 5")
     
     # Execute current step
     if st.session_state.processing_step == 0:
         st.session_state.results.append(step_one())
         st.session_state.processing_step += 1
         st.rerun()
     elif st.session_state.processing_step == 1:
         # Continue with other steps
     ```

#### Git LFS Issues
- **Problem**: Embedded data file is missing or corrupted
- **Solution**:
  1. Verify LFS is properly configured:
     ```bash
     git lfs install
     git lfs status
     ```
  2. Check that embedded_data.json is tracked:
     ```bash
     git lfs ls-files
     ```
  3. Force push the LFS objects:
     ```bash
     git lfs push --all origin main
     ```
  4. If GitHub LFS quota is an issue, consider splitting the file:
     ```bash
     # Script to split embedding file
     python -c "
     import json
     with open('embedded_data.json', 'r') as f:
         data = json.load(f)
     
     # Split into 10MB chunks
     chunk_size = 1000  # Adjust based on file size
     for i in range(0, len(data), chunk_size):
         chunk = data[i:i + chunk_size]
         with open(f'embedded_data_part{i//chunk_size}.json', 'w') as f:
             json.dump(chunk, f)
     "
     ```
  5. Update app.py to load split files:
     ```python
     def load_all_embedded_data():
         all_data = []
         for i in range(10):  # Adjust based on number of parts
             try:
                 with open(f'embedded_data_part{i}.json', 'r') as f:
                     all_data.extend(json.load(f))
             except FileNotFoundError:
                 break
         return all_data
     ```

#### Application Crashes on Startup
- **Problem**: Application fails to start on Streamlit Cloud
- **Solution**:
  1. Check deployment logs for specific error messages
  2. Verify requirements.txt has correct versions:
     ```bash
     # Test the requirements locally first
     pip install -r requirements.txt
     ```
  3. Add explicit Python version in a runtime.txt file:
     ```
     python-3.9
     ```
  4. Try initializing Streamlit configuration:
     ```python
     # Add at top of app.py
     import streamlit as st
     
     st.set_page_config(
         page_title="Human Design AI Assistant",
         page_icon="🧠",
         layout="wide",
         initial_sidebar_state="expanded"
     )
     ```

## Deployment Method 2: Heroku

Heroku provides a flexible platform for deploying web applications with automatic scaling capabilities. This section provides detailed, step-by-step instructions for deploying the Human Design AI Assistant on Heroku.

### Step 1: Install and Configure Heroku CLI

1. **Install the Heroku Command Line Interface (CLI)**:
   - **For Windows**:
     - Download and run the installer from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
     - Or install using Chocolatey:
       ```bash
       choco install heroku-cli
       ```
   
   - **For macOS**:
     - Install using Homebrew:
       ```bash
       brew tap heroku/brew && brew install heroku
       ```
   
   - **For Ubuntu/Debian**:
     - Install using snap:
       ```bash
       sudo snap install --classic heroku
       ```
     - Or use the installation script:
       ```bash
       curl https://cli-assets.heroku.com/install.sh | sh
       ```

2. **Verify the Heroku CLI installation**:
   ```bash
   heroku --version
   ```
   You should see output like: `heroku/7.60.2 linux-x64 node-v14.19.0`

3. **Login to Heroku**:
   ```bash
   heroku login
   ```
   This will open a browser window to complete the login process. If you're in a headless environment, use:
   ```bash
   heroku login -i
   ```

4. **Install the Heroku Git LFS plugin**:
   ```bash
   heroku plugins:install heroku-builds
   ```
   This plugin will help handle Git LFS files during deployment.

### Step 2: Prepare Your Application for Heroku Deployment

1. **Create or update the Procfile**:
   Create a file named `Procfile` (no file extension) in the project root:
   ```bash
   echo "web: streamlit run app.py" > Procfile
   ```
   This file tells Heroku how to run your application.

2. **Create a runtime.txt file** to specify Python version:
   ```bash
   echo "python-3.9.13" > runtime.txt
   ```
   This ensures Heroku uses the correct Python version.

3. **Update your requirements.txt file**:
   Verify your requirements.txt includes all dependencies:
   ```bash
   pip freeze > requirements.txt
   ```
   Then edit the file to remove any unnecessary or environment-specific packages.

4. **Configure Streamlit for Heroku**:
   Create a `.streamlit` directory and add a `config.toml` file for Streamlit configuration:
   ```bash
   mkdir -p .streamlit
   ```
   
   Create `.streamlit/config.toml` with:
   ```toml
   [server]
   enableCORS = false
   enableXsrfProtection = false
   
   [browser]
   gatherUsageStats = false
   
   [theme]
   primaryColor = "#6C63FF"
   backgroundColor = "#1E1E2E"
   secondaryBackgroundColor = "#313244"
   textColor = "#F8F9FA"
   ```

5. **Handle large files with Git LFS**:
   Since Heroku has a 500MB slug size limit, you need to handle `embedded_data.json` carefully:
   
   - Option 1: If the file is small enough, include it directly
   - Option 2: For larger files, consider splitting it:
     ```python
     import json
     
     # Load the original file
     with open('embedded_data.json', 'r') as f:
         data = json.load(f)
     
     # Split into smaller chunks (adjust chunk_size as needed)
     chunk_size = 500
     for i in range(0, len(data), chunk_size):
         chunk = data[i:i + chunk_size]
         with open(f'embedded_data_part_{i//chunk_size}.json', 'w') as f:
             json.dump(chunk, f)
     ```
   
   - Option 3: Store the file externally (e.g., AWS S3) and modify app.py to download it:
     ```python
     import requests
     import json
     import os
     
     def load_embedded_data():
         # Check if file exists locally first
         if os.path.exists('embedded_data.json'):
             with open('embedded_data.json', 'r') as f:
                 return json.load(f)
         
         # Download from external storage
         url = os.environ.get('EMBEDDED_DATA_URL')
         if not url:
             raise ValueError("EMBEDDED_DATA_URL environment variable not set")
         
         response = requests.get(url)
         response.raise_for_status()
         
         # Save locally for caching
         with open('embedded_data.json', 'w') as f:
             f.write(response.text)
         
         return json.loads(response.text)
     ```

6. **Test your application locally with Heroku Local**:
   ```bash
   heroku local web
   ```
   This runs your app using the Procfile, simulating the Heroku environment.

### Step 3: Create and Configure Heroku Application

1. **Create a new Heroku application**:
   ```bash
   heroku create human-design-assistant
   ```
   This will create a new Heroku app and add a remote to your git repository.

2. **Set up environment variables**:
   ```bash
   # Set your OpenAI API key
   heroku config:set OPENAI_API_KEY=your_openai_api_key_here
   
   # Set cloud mode flag
   heroku config:set IS_CLOUD=True
   
   # Set cache directory
   heroku config:set CACHE_DIR=/tmp/streamlit_cache
   
   # If using external storage for embedded_data.json
   heroku config:set EMBEDDED_DATA_URL=https://your-storage.com/embedded_data.json
   
   # Set GPT model versions
   heroku config:set GPT_MODEL=gpt-4
   heroku config:set CONSULTANT_MODEL=gpt-4.5-preview
   ```

3. **Configure Heroku buildpacks**:
   ```bash
   # Add Python buildpack
   heroku buildpacks:set heroku/python
   
   # If you need additional buildpacks (e.g., for wkhtmltopdf)
   heroku buildpacks:add https://github.com/dscout/wkhtmltopdf-buildpack.git
   ```

4. **Configure Heroku stack**:
   ```bash
   heroku stack:set heroku-20
   ```
   This sets the Heroku stack to a compatible version.

### Step 4: Deploy to Heroku

1. **Commit all changes**:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   ```

2. **Push to Heroku**:
   If your repository already has the code and you're using standard Git:
   ```bash
   git push heroku main
   ```
   
   If you're using Git LFS for large files, use the builds API:
   ```bash
   heroku builds:create --source-url=https://github.com/yourusername/human-design-ai-assistant/archive/main.tar.gz
   ```

3. **Scale the web dyno**:
   ```bash
   heroku ps:scale web=1
   ```
   This ensures one instance of your application is running.

4. **Monitor the build process**:
   ```bash
   heroku builds:info
   ```
   or
   ```bash
   heroku logs --tail
   ```
   to watch the deployment logs in real-time.

### Step 5: Post-Deployment Configuration and Verification

1. **Open the application**:
   ```bash
   heroku open
   ```
   This will open your deployed application in a web browser.

2. **Check application logs**:
   ```bash
   heroku logs --tail
   ```
   Keep this running to monitor for any errors or issues.

3. **Configure dyno size** (if needed for larger applications):
   ```bash
   # Upgrade to a performance dyno
   heroku ps:type web=performance-m
   ```

4. **Set up Heroku Scheduler** (optional, for maintenance tasks):
   ```bash
   heroku addons:create scheduler:standard
   ```
   Then navigate to the Heroku Dashboard and configure scheduled tasks.

5. **Monitor application metrics**:
   ```bash
   heroku addons:create librato:development
   ```
   This adds monitoring capabilities to track your application's performance.

6. **Configure automated backups** (if applicable):
   ```bash
   # If you're using a database
   heroku addons:create pgbackups:auto-month
   ```

7. **Set up custom domain** (optional):
   ```bash
   heroku domains:add www.yourdomain.com
   ```
   Then configure your DNS provider to point to the Heroku DNS target.

### Step 6: Troubleshooting Heroku Deployment

#### H12 Timeout Errors
- **Problem**: Heroku terminates requests that take more than 30 seconds
- **Solution**:
  
  1. Implement background processing for long-running tasks:
     ```python
     import asyncio
     import threading
     
     def background_task(func):
         def wrapper(*args, **kwargs):
             # Create a placeholder in the UI
             result_placeholder = st.empty()
             result_placeholder.text("Processing...")
             
             # Define the threaded task
             def run_in_thread():
                 result = func(*args, **kwargs)
                 # Store result in session state
                 st.session_state.background_result = result
                 # Force a rerun to update the UI
                 st.experimental_rerun()
             
             # Start in a separate thread
             thread = threading.Thread(target=run_in_thread)
             thread.start()
             
             # If we have a result from a previous run, display it
             if 'background_result' in st.session_state:
                 return st.session_state.background_result
             else:
                 return None
         
         return wrapper
     
     # Usage
     @background_task
     def process_large_data(data):
         # Long-running operation
         return processed_result
     ```
  
  2. Split long processes into incremental steps using session state:
     ```python
     # Initialize processing state
     if 'processing_stage' not in st.session_state:
         st.session_state.processing_stage = 0
         st.session_state.results = []
     
     # Process incrementally
     if st.button("Process Data") or st.session_state.processing_stage > 0:
         if st.session_state.processing_stage == 0:
             st.write("Stage 1/3: Preparing data...")
             # Do first part of work
             st.session_state.results.append(stage1_result)
             st.session_state.processing_stage = 1
             st.experimental_rerun()
         
         elif st.session_state.processing_stage == 1:
             st.write("Stage 2/3: Processing...")
             # Do second part
             st.session_state.results.append(stage2_result)
             st.session_state.processing_stage = 2
             st.experimental_rerun()
         
         elif st.session_state.processing_stage == 2:
             st.write("Stage 3/3: Finalizing...")
             # Do final part
             final_result = process_final(st.session_state.results)
             st.session_state.processing_stage = 3
             st.session_state.final_result = final_result
             st.experimental_rerun()
         
         elif st.session_state.processing_stage == 3:
             st.write("Complete!")
             st.write(st.session_state.final_result)
     ```

#### Memory Limit Exceeded
- **Problem**: Application crashes due to exceeding Heroku's memory limits
- **Solution**:
  
  1. Optimize memory usage with generators instead of lists:
     ```python
     # Before
     all_data = [process(item) for item in large_list]
     
     # After
     def process_generator(items):
         for item in items:
             yield process(item)
     
     all_data = process_generator(large_list)
     ```
  
  2. Implement data streaming for large files:
     ```python
     def load_large_json_in_chunks(filename, chunk_size=1000):
         """Load a large JSON array file in chunks to save memory"""
         with open(filename, 'r') as f:
             # Read opening bracket
             f.read(1)
             data_exhausted = False
             chunk = []
             
             while not data_exhausted:
                 # Try to read and parse objects
                 try:
                     for _ in range(chunk_size):
                         obj = json.loads(next_json_object(f))
                         chunk.append(obj)
                 except StopIteration:
                     data_exhausted = True
                 
                 yield chunk
                 chunk = []
     
     def next_json_object(file_obj):
         """Extract next JSON object from a JSON array file"""
         obj_chars = []
         brackets_level = 0
         in_quotes = False
         escape_next = False
         
         while True:
             char = file_obj.read(1)
             if not char:
                 raise StopIteration
             
             # Logic to handle JSON syntax
             if escape_next:
                 escape_next = False
             elif char == '\\':
                 escape_next = True
             elif char == '"' and not escape_next:
                 in_quotes = not in_quotes
             elif not in_quotes:
                 if char == '{':
                     brackets_level += 1
                 elif char == '}':
                     brackets_level -= 1
                     if brackets_level == 0:
                         obj_chars.append(char)
                         return ''.join(obj_chars)
             
             if brackets_level > 0:
                 obj_chars.append(char)
     ```
  
  3. Upgrade to a larger dyno type:
     ```bash
     heroku ps:type web=performance-l
     ```

#### LFS Issues with Heroku
- **Problem**: Heroku deployment fails with Git LFS files
- **Solution**:
  
  1. Use Heroku's source-url deployment for LFS files:
     ```bash
     heroku builds:create --source-url=https://github.com/yourusername/human-design-ai-assistant/archive/refs/heads/main.zip
     ```
  
  2. Alternatively, host large files externally:
     - Upload embedded_data.json to AWS S3 or similar storage
     - Make the file publicly accessible
     - Set the URL as an environment variable:
       ```bash
       heroku config:set EMBEDDED_DATA_URL=https://your-bucket.s3.amazonaws.com/embedded_data.json
       ```
     - Modify the app to download the file at startup:
       ```python
       import requests
       import os
       import json
       
       def get_embedded_data():
           # Try to load from local cache first
           cache_path = "/tmp/embedded_data.json"
           if os.path.exists(cache_path):
               with open(cache_path, 'r')

## Deployment Method 3: Self-hosted Server

Self-hosting provides maximum control over the environment and is suitable for production deployments.

### Step 1: Server Preparation

1. Set up a server with Ubuntu 20.04 LTS or later
2. Update the system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. Install required system packages:
   ```bash
   sudo apt install -y python3 python3-pip python3-venv wkhtmltopdf git antiword
   ```

4. Create a dedicated user:
   ```bash
   sudo useradd -m -s /bin/bash assistantadmin
   sudo passwd assistantadmin
   sudo usermod -aG sudo assistantadmin
   ```

5. Switch to the new user:
   ```bash
   su - assistantadmin
   ```

### Step 2: Application Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/human-design-ai-assistant.git
   cd human-design-ai-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file:
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "IS_CLOUD=True" >> .env
   ```

### Step 3: Configure Systemd Service

1. Create a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/humandesign.service
   ```

2. Add the following content:
   ```
   [Unit]
   Description=Human Design AI Assistant
   After=network.target

   [Service]
   User=assistantadmin
   WorkingDirectory=/home/assistantadmin/human-design-ai-assistant
   ExecStart=/home/assistantadmin/human-design-ai-assistant/venv/bin/streamlit run app.py --server.port=8501
   Restart=always
   RestartSec=5
   Environment="PYTHONPATH=/home/assistantadmin/human-design-ai-assistant"
   Environment="OPENAI_API_KEY=your_openai_api_key_here"
   Environment="IS_CLOUD=True"

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl enable humandesign
   sudo systemctl start humandesign
   ```

4. Check the service status:
   ```bash
   sudo systemctl status humandesign
   ```

### Step 4: Configure Nginx as Reverse Proxy

1. Install Nginx:
   ```bash
   sudo apt install -y nginx
   ```

2. Create an Nginx configuration file:
   ```bash
   sudo nano /etc/nginx/sites-available/humandesign
   ```

3. Add the following content:
   ```
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header Host $host;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_read_timeout 86400;
       }
   }
   ```

4. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/humandesign /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. Set up SSL with Let's Encrypt:
   ```bash
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Troubleshooting Self-hosted Deployment

- **Permission Issues**: Check file ownership and permissions
- **Service Not Starting**: Examine logs with `journalctl -u humandesign`
- **Nginx Errors**: Review logs at `/var/log/nginx/error.log`
- **Connectivity Issues**: Verify firewall settings with `sudo ufw status`

## Deployment Method 4: Docker Container

Docker provides a consistent deployment environment across different systems.

### Step 1: Create Docker Configuration

1. Create a `Dockerfile` in the project root:
   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       wkhtmltopdf \
       antiword \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements and install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Expose Streamlit port
   EXPOSE 8501

   # Set environment variables
   ENV IS_CLOUD=True

   # Command to run the application
   CMD ["streamlit", "run", "app.py"]
   ```

2. Create a `.dockerignore` file:
   ```
   venv/
   __pycache__/
   .git
   .env
   ```

### Step 2: Build and Run Docker Container

1. Build the Docker image:
   ```bash
   docker build -t human-design-assistant:latest .
   ```

2. Run the container:
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e OPENAI_API_KEY=your_openai_api_key_here \
     --name human-design-assistant \
     human-design-assistant:latest
   ```

3. Verify the application is running:
   ```bash
   docker logs human-design-assistant
   ```

### Step 3: Docker Compose Setup (Optional)

1. Create a `docker-compose.yml` file:
   ```yaml
   version: '3'
   services:
     app:
       build: .
       ports:
         - "8501:8501"
       environment:
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - IS_CLOUD=True
       volumes:
         - ./embedded_data.json:/app/embedded_data.json
       restart: always
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

### Troubleshooting Docker Deployment

- **Volume Mount Issues**: Check paths and permissions
- **Environment Variables**: Verify they are correctly passed to the container
- **Container Crashes**: Examine logs with `docker logs human-design-assistant`

## Database Setup and Management

The Human Design AI Assistant uses a file-based "database" consisting of:

1. **embedded_data.json**: Contains all vector embeddings and metadata
2. **Chat history**: Stored in memory during a session (stateless)

### Embedded Data File Management

The `embedded_data.json` file is critical for search functionality. To update or manage it:

1. Generate new embeddings from source documents:
   ```bash
   python Embedings_gen.py
   ```

2. Back up the existing file:
   ```bash
   cp embedded_data.json embedded_data.json.bak
   ```

3. For large files, use Git LFS:
   ```bash
   git lfs track "embedded_data.json"
   git add .gitattributes embedded_data.json
   git commit -m "Update embedded data"
   git push
   ```

### Data Maintenance

For long-term maintenance:

1. Periodically update embeddings with new content
2. Monitor file size – large embedding files might require splitting or optimization
3. Consider implementing a proper database solution for production at scale

## Security Considerations

### API Key Protection

1. Never commit API keys to the repository
2. Use environment variables or secrets management
3. Implement API key rotation policies
4. Set up access controls and rate limiting

### Access Control

1. For internal deployments, use IP whitelisting
2. Consider adding basic authentication
3. For more advanced scenarios, implement OAuth or similar

### Data Protection

1. Ensure HTTPS/SSL is enabled for all traffic
2. Do not store user data persistently without consent
3. Implement appropriate data retention policies

## Monitoring and Maintenance

### Health Checks

Implement a basic health check endpoint:

```python
@app.route('/health')
def health_check():
    return {"status": "healthy"}
```

### Logging

Configure comprehensive logging:

1. Application logs:
   ```python
   import logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
   )
   ```

2. API request logs:
   ```python
   def log_api_request(request_type, prompt_length, success):
       logging.info(f"API Request: {request_type}, Length: {prompt_length}, Success: {success}")
   ```

### Backup Strategy

1. Regular backups of embeddings data:
   ```bash
   # Automated backup script
   mkdir -p backups
   cp embedded_data.json backups/embedded_data_$(date +%Y%m%d).json
   ```

2. Configure a retention policy for backups

## Scaling Considerations

### Horizontal Scaling

For increased traffic:

1. Deploy multiple instances behind a load balancer
2. Use shared storage for embeddings data
3. Implement session affinity if needed

### Performance Optimization

1. Optimize embeddings size
2. Implement caching for frequently asked questions
3. Batch API requests where possible

## Customization Options

### Environment Variables

The application supports these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `IS_CLOUD` | Cloud deployment mode | False |
| `CACHE_DIR` | Directory for cache files | /tmp/streamlit_cache |
| `GPT_MODEL` | Model for client queries | gpt-4 |
| `CONSULTANT_MODEL` | Model for consultant mode | gpt-4.5-preview |

### Application Configuration

Additional configuration options in `app.py`:

```python
# Customize temperature
st.session_state.gpt_temperature = st.slider("GPT Temperature", 0.0, 1.0, 0.3, 0.1)

# Change embedding model
EMBEDDING_MODEL = "text-embedding-ada-002"

# Adjust chunk sizes
CHUNK_SIZE = 700
CHUNK_OVERLAP = 50
```

## Troubleshooting Common Deployment Issues

### OpenAI API Issues

**Problem**: API key authentication failures
**Solution**: Verify the API key is correctly set and has appropriate permissions

**Problem**: Rate limit exceeded
**Solution**: Implement exponential backoff and retry logic:
```python
def call_with_retry(func, *args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except RateLimitError:
            if attempt < max_retries - 1:
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)
            else:
                raise
```

### Application Startup Issues

**Problem**: Import errors during startup
**Solution**: Verify all dependencies are installed:
```bash
pip install -r requirements.txt
```

**Problem**: File not found errors
**Solution**: Check file paths and working directory:
```bash
pwd
ls -la
```

### Memory Issues

**Problem**: Out of memory errors
**Solution**: Optimize large data handling:
```python
# Process embeddings in smaller batches
def batch_process(items, batch_size=100):
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

for batch in batch_process(large_list):
    process_batch(batch)
```

## Updating the Application

### Code Updates

To update the application code:

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Restart the application:
   ```bash
   sudo systemctl restart humandesign  # For systemd
   # OR
   docker-compose restart  # For Docker
   ```

### Embedding Updates

To update the embedded data:

1. Run the embedding generation script:
   ```bash
   python Embedings_gen.py
   ```

2. Deploy the updated embedding file

## Contact and Support

For deployment assistance or troubleshooting support:

- File issues on GitHub: [GitHub Issues](https://github.com/yourusername/human-design-ai-assistant/issues)
- Contact the development team: hyka@oregonstate.edu

---

This deployment guide is maintained by the Human Design AI Assistant development team.  
Last updated: March 14, 2025.
