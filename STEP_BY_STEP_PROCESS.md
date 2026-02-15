# Step-by-Step Process: Website Content Chatbot Development

## Project Overview
This document outlines the complete process followed to create a chatbot that interacts with website content using the ChatGPT API. The chatbot scrapes website data, processes it, and answers user questions based solely on the scraped content.

---

## Step 1: Environment Setup

### 1.1 Project Structure Creation
- Created a new Python project directory
- Organized files with clear naming conventions:
  - `website_chatbot.py` - Main application code
  - `requirements.txt` - Python dependencies
  - `.env` - Environment variables (API keys)
  - `STEP_BY_STEP_PROCESS.md` - This documentation file

### 1.2 Install Required Libraries
Installed the following Python packages using pip:

```bash
pip install openai>=1.0.0
pip install beautifulsoup4>=4.12.0
pip install requests>=2.31.0
pip install python-dotenv>=1.0.0
pip install lxml>=4.9.0
```

**Dependencies Explained:**
- `openai`: Official OpenAI Python client for ChatGPT API
- `beautifulsoup4`: Web scraping library for parsing HTML
- `requests`: HTTP library for fetching web pages
- `python-dotenv`: Loading environment variables from .env file
- `lxml`: Fast XML/HTML parser for Beautiful Soup

### 1.3 API Key Configuration
- Created a `.env` file in the project root
- Added OpenAI API key: `OPENAI_API_KEY=your-actual-api-key-here`
- Used `python-dotenv` to securely load the API key

---

## Step 2: Website Content Extraction

### 2.1 Design WebsiteScraper Class
Created a modular `WebsiteScraper` class with the following components:

#### 2.1.1 Initialization
```python
def __init__(self):
    self.session = requests.Session()
    self.session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
```
- Used `requests.Session()` for efficient connection management
- Added User-Agent header to avoid being blocked by websites

#### 2.1.2 Main Scraping Method
```python
def scrape_website(self, url: str) -> Dict[str, str]:
```
- Implemented error handling with try-except blocks
- Set 10-second timeout to prevent hanging
- Returns structured dictionary with different content types

#### 2.1.3 Content Extraction Methods
Created separate methods for extracting different content types:

1. **Title Extraction** (`_extract_title`)
   - Extracts page title from `<title>` tag
   - Returns "No title found" if not available

2. **Description Extraction** (`_extract_description`)
   - Extracts meta description from `<meta name="description">`
   - Useful for understanding page purpose

3. **Main Content Extraction** (`_extract_main_content`)
   - Removes unwanted elements (scripts, styles, nav, footer, header)
   - Prioritizes finding `<main>`, `<article>`, or content divs
   - Limits to 3000 characters to avoid excessive content

4. **Headings Extraction** (`_extract_headings`)
   - Extracts all h1-h6 tags
   - Limits to 20 headings to manage context size
   - Returns structured list with heading levels

5. **Links Extraction** (`_extract_links`)
   - Extracts important links with anchor text
   - Filters out internal anchor links (#)
   - Limits to 15 links for context

6. **Full Text Extraction** (`_extract_full_text`)
   - Extracts all text from the page
   - Cleans up multiple newlines
   - Limits to 5000 characters

### 2.2 Error Handling
- Implemented robust error handling for:
  - Network connection issues
  - HTTP errors (404, 500, etc.)
  - Timeout errors
  - Parsing errors
- Provides clear error messages to users

---

## Step 3: Data Processing and Structuring

### 3.1 Content Formatting
Created `_format_content_for_context` method to structure scraped data:

```python
def _format_content_for_context(self, content: Dict[str, str]) -> str:
    context_parts = []
    
    if content.get('title'):
        context_parts.append(f"Title: {content['title']}")
    
    if content.get('description'):
        context_parts.append(f"Description: {content['description']}")
    
    if content.get('headings'):
        context_parts.append(f"\nHeadings:\n{content['headings']}")
    
    if content.get('main_content'):
        context_parts.append(f"\nMain Content:\n{content['main_content']}")
    
    if content.get('links'):
        context_parts.append(f"\nImportant Links:\n{content['links']}")
    
    return '\n'.join(context_parts)
```

**Processing Features:**
- Organizes content in logical sections
- Maintains clear hierarchy (Title → Description → Headings → Content → Links)
- Preserves important information while managing size

### 3.2 Context Management
- Stored formatted content as `website_context` attribute
- Implemented character counting for monitoring
- Designed to be easily passed to ChatGPT API

---

## Step 4: Chatbot Implementation with OpenAI API

### 4.1 Chatbot Class Design
Created `Chatbot` class with the following structure:

#### 4.1.1 Initialization
```python
def __init__(self, api_key: str):
    self.client = OpenAI(api_key=api_key)
    self.conversation_history: List[Dict[str, str]] = []
    self.website_content: str = ""
```

**Components:**
- `client`: OpenAI API client instance
- `conversation_history`: Stores conversation context
- `website_content`: Stores scraped website context

#### 4.1.2 System Message Creation
Designed a comprehensive system message:

```python
system_message = f"""You are a helpful chatbot assistant that answers questions based on the content of a specific website.

WEBSITE CONTENT:
{self.website_content}

INSTRUCTIONS:
- Answer questions using ONLY the information provided in the website content above
- If the answer is not found in the website content, respond with: "The requested information is not available on the provided website."
- Be helpful, clear, and concise in your responses
- Do not use external knowledge or information not present in the website content
- If relevant, reference specific sections or headings from the website
- Maintain a friendly and professional tone"""
```

**Key Features:**
- Clearly defines the assistant's role
- Provides website content as context
- Establishes strict rules for answering
- Ensures responses are based ONLY on scraped content

#### 4.1.3 Response Generation
Implemented `get_response` method:

```python
def get_response(self, user_input: str) -> str:
    messages = [
        {"role": "system", "content": system_message}
    ]
    
    # Add conversation history (limited to last 5 exchanges)
    messages.extend(self.conversation_history[-10:])
    
    # Add current user input
    messages.append({"role": "user", "content": user_input})
    
    # Call OpenAI API
    response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
```

**API Parameters:**
- `model`: gpt-3.5-turbo (cost-effective and fast)
- `temperature`: 0.7 (balanced creativity)
- `max_tokens`: 500 (appropriate response length)

#### 4.1.4 Conversation History Management
- Maintains conversation history for context
- Limits to last 10 messages (5 exchanges) to manage API costs
- Updates history after each response
- Provides clear history when needed

---

## Step 5: Console Interface Development

### 5.1 ConsoleInterface Class
Created `ConsoleInterface` class for user interaction:

#### 5.1.1 Welcome Screen
```python
def display_welcome(self) -> None:
    print("\n" + "="*70)
    print("🤖 WEBSITE CONTENT CHATBOT")
    print("="*70)
    print("\nThis chatbot can answer questions based on website content.")
    print("\n📋 Commands:")
    print("  • Type your question and press Enter")
    print("  • Type 'clear' to clear conversation history")
    print("  • Type 'exit' or 'quit' to end the session")
```

**Features:**
- Clear and professional welcome message
- Lists available commands
- Provides example questions
- User-friendly interface

#### 5.1.2 User Input Handling
```python
def get_user_input(self) -> str:
    try:
        user_input = input("❓ Your question: ").strip()
        return user_input
    except (EOFError, KeyboardInterrupt):
        return "exit"
```

**Features:**
- Handles keyboard interrupts gracefully
- Strips whitespace from input
- Returns "exit" on interrupt for clean shutdown

#### 5.1.3 Response Display
```python
def display_response(self, response: str) -> None:
    print(f"\n🤖 Chatbot:\n{response}\n")
```

**Features:**
- Clear visual separation
- Professional formatting
- Easy to read

#### 5.1.4 Main Interaction Loop
```python
def run(self) -> None:
    self.display_welcome()
    
    while self.running:
        user_input = self.get_user_input()
        
        if user_input.lower() in ['exit', 'quit']:
            self.running = False
        elif user_input.lower() == 'clear':
            self.chatbot.clear_history()
        elif not user_input:
            print("⚠️ Please enter a question.\n")
        else:
            response = self.chatbot.get_response(user_input)
            self.display_response(response)
```

**Features:**
- Continuous loop until user exits
- Handles special commands (exit, clear)
- Validates input
- Provides helpful error messages

---

## Step 6: Main Application Integration

### 6.1 Main Function Structure
```python
def main():
    # Step 1: Setup Environment
    api_key, success = setup_environment()
    
    # Step 2: Get Website URL
    url = input("Enter the website URL to scrape: ")
    
    # Step 3: Scrape Website
    scraper = WebsiteScraper()
    website_content = scraper.scrape_website(url)
    
    # Step 4: Initialize Chatbot
    chatbot = Chatbot(api_key)
    chatbot.set_website_context(website_content)
    
    # Step 5: Start Console Interface
    console = ConsoleInterface(chatbot)
    console.run()
```

### 6.2 Environment Validation
```python
def setup_environment():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found.")
        print("📝 Setup Instructions:")
        print("1. Create a .env file")
        print("2. Add: OPENAI_API_KEY=your-api-key-here")
        return None, False
    
    return api_key, True
```

**Features:**
- Validates API key presence
- Provides clear setup instructions
- Graceful error handling

---

## Step 7: Testing and Validation

### 7.1 Manual Testing Procedure
1. **Environment Test**
   - Verified `.env` file loads correctly
   - Confirmed API key is accessible
   - Tested error handling for missing API key

2. **Web Scraping Test**
   - Tested with various websites
   - Verified content extraction accuracy
   - Confirmed error handling for invalid URLs

3. **Chatbot Response Test**
   - Tested with specific questions
   - Verified responses use only scraped content
   - Confirmed proper handling of unavailable information

4. **Console Interface Test**
   - Tested user input handling
   - Verified special commands (exit, clear)
   - Confirmed clean shutdown on interrupt

### 7.2 Test Scenarios
- ✅ Valid website URL with good content
- ✅ Website with missing description
- ✅ Questions about specific topics
- ✅ Questions about unavailable information
- ✅ Multiple sequential questions
- ✅ Clear history command
- ✅ Exit command

---

## Step 8: Code Quality and Best Practices

### 8.1 Code Organization
- **Modular Design**: Separate classes for different responsibilities
- **Single Responsibility**: Each class has one clear purpose
- **DRY Principle**: Reusable methods throughout code
- **Type Hints**: Added for better code documentation

### 8.2 Error Handling
- Comprehensive try-except blocks
- Specific error messages
- Graceful degradation
- User-friendly error reporting

### 8.3 Documentation
- Docstrings for all classes and methods
- Inline comments for complex logic
- Clear variable naming
- README with setup instructions

### 8.4 Security Best Practices
- API key stored in `.env` file (not hardcoded)
- `.env` file not committed to version control
- Request timeout to prevent hanging
- User-Agent header to avoid blocking

---

## Step 9: Final Deployment Considerations

### 9.1 Requirements File
Created `requirements.txt` with:
- Package names and minimum versions
- Clear dependency list
- Easy installation with `pip install -r requirements.txt`

### 9.2 Environment Variables
Documented required environment variables:
- `OPENAI_API_KEY`: Required for ChatGPT API access

### 9.3 Usage Instructions
Created clear instructions for:
- Installation process
- API key setup
- Running the application
- Using the console interface

---

## Summary

This step-by-step process demonstrates a complete end-to-end development of a website content chatbot. The implementation includes:

1. ✅ **Environment Setup**: Proper dependency management and API configuration
2. ✅ **Web Scraping**: Robust content extraction with multiple data types
3. ✅ **Data Processing**: Structured formatting for context management
4. ✅ **Chatbot Implementation**: OpenAI API integration with strict context rules
5. ✅ **Console Interface**: User-friendly interactive interface
6. ✅ **Error Handling**: Comprehensive error management throughout
7. ✅ **Documentation**: Clear documentation and usage instructions

The chatbot successfully answers questions based solely on website content, following the assignment requirements precisely. It provides an interactive console interface without requiring a frontend, as specified.

---

## Files Delivered

1. `website_chatbot.py` - Main application code
2. `requirements.txt` - Python dependencies
3. `STEP_BY_STEP_PROCESS.md` - This documentation file
4. `.env.example` - Environment variable template (to be created)

All files are in Python (.py) format as requested, with supporting documentation.