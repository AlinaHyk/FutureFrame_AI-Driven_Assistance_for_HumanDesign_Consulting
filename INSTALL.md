# Human Design AI Assistant - Installation and User Guide

This document provides comprehensive instructions for installing, accessing, and using the Human Design AI Assistant application. 

## Live Application

The Human Design AI Assistant is currently deployed and accessible at:

**[https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app](https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app)**

This live version is fully functional and can be accessed from any modern web browser without any installation required on your part.

## System Requirements (for accessing the web application)

- **Device**: Desktop, laptop, tablet, or mobile phone
- **Operating System**: Any operating system (Windows, macOS, Linux, iOS, Android)
- **Web Browser**: Modern web browser with JavaScript enabled
  - Google Chrome (version 90+)
  - Mozilla Firefox (version 88+)
  - Safari (version 14+)
  - Microsoft Edge (version 90+)
- **Internet Connection**: Broadband connection (1 Mbps or faster)
- **Screen Resolution**: Minimum 1280x720 (responsive design adapts to various screen sizes)

## Accessing the Application

1. Open your web browser
2. Navigate to [https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app](https://futureframeai-drivenassistanceforhumandesignconsulting-gvuhiel.streamlit.app)
3. The application will load automatically
4. No login is required to use the basic features

## User Interface Guide

The Human Design AI Assistant features a sophisticated yet intuitive interface designed to provide both casual users and professional consultants with appropriate tools. Below is a detailed breakdown of each interface component and its functionality.

### 1. Main Navigation

The application employs a tabbed interface with three distinct sections at the top of the main content area:

- **Chat Tab**: 
  - The primary interface for direct interaction with the AI
  - Features a conversational UI with message bubbles
  - Displays both user queries and AI responses in chronological order
  - Includes timestamps for each message
  - Located prominently as the default/first tab

- **Analysis Tab**: 
  - Available primarily in Consultant mode (appears grayed out in Client mode)
  - Provides detailed data visualizations and metrics
  - Organized in expandable card components for different analysis types
  - Updates dynamically based on the current conversation
  - Accessible by clicking the second tab in the navigation bar

- **Knowledge Graph Tab**: 
  - Visual exploration tool for Human Design concepts and relationships
  - Features an interactive, force-directed graph visualization
  - Contains search and filtering tools for concept exploration
  - Includes detailed information panels for selected concepts
  - Located as the third tab in the main navigation

### 2. Sidebar

The sidebar is positioned on the left side of the screen (can be collapsed/expanded) and contains numerous controls and settings:

- **Expertise Level Selector**:
  - Located at the top of the sidebar
  - Features a radio button group with two options: "Client" and "Consultant"
  - Client mode provides simplified responses and interface
  - Consultant mode unlocks advanced features, detailed source citations, and technical insights
  - Changes take effect immediately upon selection

- **Chat Controls Section**:
  - Located below the expertise selector
  - "Clear Conversation" button: Erases the current chat history and starts fresh
  - Warning: This action cannot be undone
  - Confirmation prompt appears before clearing to prevent accidental data loss

- **Data Management**:
  - File uploader component for embedding data
  - Accepts JSON format files containing vector embeddings
  - "Upload new embedded data JSON" label above the upload area
  - Success message appears after successful upload
  - Error handling for invalid or corrupted files

- **API Settings**:
  - Temperature slider: Controls the creativity/randomness of AI responses
  - Range from 0.0 (deterministic) to 1.0 (maximum creativity)
  - Default value: 0.3 (balanced responses)
  - Changes take effect on the next AI response
  - Tooltip explains the impact of different temperature settings

- **Download Section**:
  - "Download Chat History" button: Exports conversation as JSON
  - File is named "chat_history.json" by default
  - Contains complete message history with timestamps
  - Save dialog appears to select download location
  - Download button is disabled if chat history is empty

- **About Section**:
  - Located at the bottom of the sidebar
  - Contains brief application description
  - Displays version information
  - Shows feature badges (e.g., "GPT-4 Powered", "Semantic Search")
  - Links to additional resources (if applicable)

### 3. Chat Interface

The chat interface in the Chat tab provides an intuitive conversational experience:

- **Header Area**:
  - Application title with animated logo at the top
  - Subtle animation effect on the logo for visual interest
  - Clean, modern typography for headings

- **Chat Container**:
  - Scrollable area with smooth scrolling behavior
  - Automatically scrolls to the bottom when new messages arrive
  - Glass-morphism design with subtle transparency effects
  - Custom scrollbar styling for better visual integration

- **Message Bubbles**:
  - User messages:
    - Right-aligned message bubbles in a distinct color (purple/blue)
    - "You:" prefix for clarity
    - Rounded corners with drop shadow
    - Displays timestamp in small text at the top right
  
  - AI Assistant messages:
    - Left-aligned bubbles in a contrasting color
    - "AI Assistant:" prefix
    - Markdown formatting support for rich text rendering
    - Code block support with syntax highlighting
    - Citations in consultant mode appear as indented blocks
    - Timestamps shown at the top right of each message

- **Input Area**:
  - Located at the bottom of the chat container
  - Multi-line text input field that expands as you type
  - Placeholder text: "What would you like to know about Human Design?"
  - Submit button with hover effects
  - Support for keyboard submission (Enter key)
  - Character counter (optional)
  - Loading animation appears during AI processing:
    - "Thinking..." indicator with animated dots
    - Progress indicator for longer operations

- **Error Handling**:
  - Error messages appear as system messages in the chat
  - Retry options provided when applicable
  - Network connection status indicators

### 4. Analysis Dashboard (Consultant Mode)

The Analysis Dashboard provides advanced insights and metrics, only fully accessible in Consultant mode:

- **Metrics Overview**:
  - Located at the top of the Analysis tab
  - Four metric cards displaying key statistics:
    - Total Messages count with numerical display
    - User Messages count shown prominently
    - Average Query Length with character count
    - Session Time with minutes/seconds counter
  - Each metric features a descriptive label and prominent value
  - Cards use subtle animation on hover
  - Auto-updating as the conversation progresses

- **Keyword Visualization**:
  - Horizontal bar chart showing expanded keywords
  - Interactive hover tooltips showing relevance scores
  - Color gradient indicating relevance (green/blue for high relevance)
  - Y-axis labels showing each keyword
  - X-axis showing relevance score from 0.0 to 1.0
  - Title: "Query Expansion Keywords"
  - Responsive sizing that adjusts to screen width

- **Source Relevance Visualization**:
  - Radar/spider chart showing relevance scores for top sources
  - Each spoke represents a different source document
  - Distance from center indicates relevance score (0.0-1.0)
  - Filled polygon area in semi-transparent color
  - Interactive tooltip on hover showing exact values
  - Title: "Source Relevance Scores"
  - Legend explaining the visualization

- **Raw Analysis Data**:
  - Expandable accordion section at the bottom
  - Collapsed by default to avoid overwhelming users
  - "Show Raw Analysis Data" header with expansion arrow
  - When expanded, displays formatted JSON data
  - Includes:
    - Original top chunks with scores
    - Secondary top chunks with scores
    - Expanded keywords list
    - Expanded query text
  - Syntax highlighting for better readability
  - Copy button to copy the entire JSON structure

### 5. Knowledge Graph Interface

The Knowledge Graph tab provides an interactive visualization of Human Design concepts:

- **Control Panel**:
  - Located on the left side of the Knowledge Graph tab
  - "Generate Knowledge Graph" button:
    - Prominent button to initiate graph generation
    - Loading indicator during processing
    - Disabled after graph is generated to prevent duplicate processing
  
  - Search functionality:
    - Search input field with placeholder "Search concepts"
    - Real-time filtering as you type
    - Results counter showing number of matching concepts
    - Empty state handling for no results

  - Concept Selection:
    - Dropdown for selecting concepts from filtered list
    - Alphabetical sorting of concept options
    - Keyboard navigation support
    - Immediate graph update on selection

  - Related Concepts Section:
    - Updates when a concept is selected
    - Shows up to 10 related concepts as interactive cards
    - Each card displays:
      - Concept name in bold
      - Distance (connection proximity) indicator
      - Relationship strength metric
    - Cards are clickable to navigate to that concept
    - Sorted by relevance (strongest connections first)

  - Concept Statistics:
    - Metric card showing connection count
    - Visual representation of concept centrality
    - Updates when selection changes

- **Graph Visualization Area**:
  - Occupies the majority of the right side of the tab
  - Interactive network graph with:
    - Nodes representing concepts (varying sizes based on connections)
    - Edges representing relationships between concepts
    - Color coding by concept category or connection strength
    - Physics-based simulation for natural arrangement
    - Zoom controls (mouse wheel or buttons)
    - Pan functionality (click and drag)
    - Node selection by clicking
    - Hover tooltips showing concept information
  
  - Graph Controls:
    - Zoom in/out buttons at the bottom right
    - Reset view button to center the graph
    - Fullscreen toggle option
    - Physics simulation toggle (freeze/unfreeze)
    - Graph density adjustment slider
  
  - Visualization Guide:
    - Expandable help section explaining the visualization
    - Legend for node sizes and colors
    - Explanation of interaction controls
    - Link to more detailed documentation

### 6. Response Visualization and Formatting

The AI responses feature sophisticated formatting to enhance readability:

- **Text Formatting**:
  - Rich markdown support including:
    - Headings of different levels with appropriate hierarchy
    - Bold and italic text for emphasis
    - Bulleted and numbered lists with proper indentation
    - Block quotes for referenced material
    - Horizontal rules for section separation
  
  - Code Formatting:
    - Syntax highlighting for code blocks
    - Support for multiple programming languages
    - Monospace font for inline code
    - Copy button for code blocks
    - Line numbers for longer snippets

- **Source Citations** (Consultant Mode):
  - Indented, bordered citation blocks
  - Source number and relevance score displayed
  - First few lines of the source text
  - Visual differentiation between primary and secondary sources
  - Collapsible for longer citations

- **Special Elements**:
  - Definition boxes for Human Design terms
  - Warning/notice blocks for important information
  - Example sections with distinct styling
  - Tooltips for technical terms
  - Buttons for actions (e.g., "Learn more about this concept")

### 7. Responsive Design Elements

The interface adapts intelligently to different screen sizes:

- **Desktop View** (1024px and above):
  - Three-column layout with sidebar, main content, and detail panels
  - Horizontal tabs for main navigation
  - Expanded visualization options
  - Full keyboard shortcut support

- **Tablet View** (768px to 1023px):
  - Two-column layout with collapsible sidebar
  - Slightly compressed visualizations
  - Touch-optimized controls with larger tap targets
  - Swipe gestures for tab navigation

- **Mobile View** (below 768px):
  - Single column layout with hidden sidebar (accessible via menu button)
  - Stacked vertical sections instead of columns
  - Simplified visualizations optimized for smaller screens
  - Bottom navigation bar for tab switching
  - Floating action button for key actions
  - Pull-to-refresh functionality

## Using the Application

### Getting Started

1. When you first access the application, you'll see the welcome screen
2. Select your expertise level in the sidebar (Client or Consultant)
   - **Client Mode**: Simplified responses for general users
   - **Consultant Mode**: Detailed responses with source citations and visualizations
3. Begin by typing a question about Human Design in the chat input field
4. Click "Submit" or press Enter to send your query

### Asking Questions

The Human Design AI Assistant can answer questions on various aspects of Human Design, including:
- Basic Human Design concepts
- Types, Authorities, Profiles and Centers
- Gates and Channels
- Definition types
- Strategies and Authorities
- Personal Human Design readings interpretation

Example questions:
- "What is Human Design?"
- "Can you explain the difference between Generators and Projectors?"
- "How does my Emotional Authority work?"
- "What are the characteristics of a 5/1 Profile?"

### Working with the Knowledge Graph

1. Navigate to the "Knowledge Graph" tab
2. Click "Generate Knowledge Graph" to build the visualization
3. Use the search box to find specific concepts
4. Click on any concept to see its relationships
5. Explore related concepts to navigate the knowledge base

### Using the Analysis Dashboard (Consultant Mode)

1. Set your expertise level to "Consultant" in the sidebar
2. Ask a question in the chat interface
3. Navigate to the "Analysis" tab to see:
   - Visualization of keywords extracted from your query
   - Relevance scores of the sources used to generate the response
   - Expanded search terms used to enhance the response
4. Expand "Raw Analysis Data" to see technical details

### Exporting Data

The application allows you to export your conversation data:
1. Use the "Download Chat History" button in the sidebar
2. The chat history will be saved as a JSON file to your device

## Supported Features

### Core Features

- **Semantic Search**: The application searches through embedded knowledge to find relevant information
- **Contextual Responses**: AI generates responses based on the most relevant content
- **Client/Consultant Modes**: Different detail levels based on user expertise
- **Knowledge Graph**: Visual exploration of Human Design concepts
- **Source Citations**: References to information sources (consultant mode)
- **Progressive Web App**: Can be installed for offline access

### Additional Features

- **Conversation History**: Persistent chat history during your session
- **Analytics Dashboard**: Visualizations of relevance and keyword data
- **Temperature Control**: Adjust the creativity of AI responses
- **Export Capabilities**: Download your conversation history

## Troubleshooting

### Common Issues

#### Application Not Loading

**Issue**: The application doesn't load or displays an error screen.
**Solution**: 
1. Ensure you have a stable internet connection
2. Try refreshing the page
3. Clear your browser cache
4. Try a different browser

#### Slow Response Times

**Issue**: AI responses take a long time to generate.
**Solution**:
1. For complex questions, the AI may take longer to process
2. Try simplifying your query
3. Check your internet connection
4. Try during non-peak hours if the service is experiencing high traffic

#### Display Issues

**Issue**: The interface appears distorted or elements are misaligned.
**Solution**:
1. Try adjusting your browser zoom level
2. Ensure your browser is updated to the latest version
3. If on mobile, try rotating your device
4. Clear browser cache and reload

#### Knowledge Limitations

**Issue**: The AI doesn't know about very recent Human Design concepts or developments.
**Solution**:
1. The AI's knowledge has a cutoff date and may not include very recent developments
2. Try asking about established concepts
3. Be specific in your questions

### Contacting Support

If you encounter persistent issues with the application:
1. Check the GitHub repository for known issues: [GitHub Issues](https://github.com/yourusername/human-design-ai-assistant/issues)
2. Create a new issue with detailed description of your problem
3. Include browser information, device type, and steps to reproduce the issue

## Privacy Information

The Human Design AI Assistant:
- Does not permanently store user conversations beyond the current session
- Does not collect personal information
- Uses temporary storage for conversation context during your session
- Any downloaded chat history is stored locally on your device only

## Limitations

The application has certain limitations to be aware of:
- Knowledge cutoff date limits information on very recent developments
- Cannot directly read your Human Design chart (would need to be uploaded)
- May occasionally provide general responses to highly specific questions
- Does not retain conversation history between browser sessions
- Is not a replacement for professional Human Design readings

## Additional Resources

For more information about Human Design:
- [International Human Design School](https://www.ihdschool.com/)
- [Jovian Archive](https://www.jovianarchive.com/)
- [Human Design America](https://humandesignamerica.com/)

For technical details about this application:
- [GitHub Repository](https://github.com/yourusername/human-design-ai-assistant)
- [README Documentation](https://github.com/yourusername/human-design-ai-assistant/blob/main/README.md)

## Legal and Attribution

The Human Design AI Assistant is an educational tool and is not affiliated with the official Human Design organizations. Human Design was developed by Ra Uru Hu (Robert Allan Krakower).

The application uses:
- OpenAI API for embeddings and completions
- Streamlit for the web interface
- Various open-source libraries for data processing

## Version Information

This installation guide applies to version 1.0.0 of the Human Design AI Assistant.
Last updated: March 14, 2025.
