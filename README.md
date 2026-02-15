# Website Content Chatbot

A Python-based chatbot that interacts with website content using the OpenAI ChatGPT API. The chatbot scrapes website data, processes it, and answers user questions based solely on the scraped content.

## Features

- 🔍 **Web Scraping**: Extracts content from any website using Beautiful Soup
- 🤖 **AI-Powered**: Uses OpenAI's ChatGPT API for intelligent responses
- 💬 **Console Interface**: Interactive command-line interface for easy use
- 📚 **Context-Aware**: Answers questions based only on scraped website content
- 🛡️ **Error Handling**: Robust error handling and user-friendly messages
- 📝 **Conversation History**: Maintains context across multiple questions

## Requirements

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation

### Step 1: Clone or Download the Project

```bash
cd website-chatbot
```

### Step 2: Install Required Packages

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install openai beautifulsoup4 requests python-dotenv lxml
```

### Step 3: Set Up Your API Key

1. Create a `.env` file in the project directory
2. Add your OpenAI API key:

```env
OPENAI_API_KEY=your-actual-api-key-here
```

⚠️ **Important**: Never share your API key or commit `.env` to version control!

### Step 4: Run the Chatbot

```bash
python website_chatbot.py
```

## Usage

### Starting the Chatbot

1. Run the script: `python website_chatbot.py`
2. Enter a website URL when prompted
3. Wait for the content to be scraped
4. Start asking questions!

### Example Session

```
🚀 WEBSITE CONTENT CHATBOT - STARTING
======================================================================

🔧 Setting up environment...
✅ Environment setup complete.

📌 Step 2: Enter Website URL
----------------------------------------------------------------------
Enter the website URL to scrape: https://example.com

📌 Step 3: Scraping Website Content
----------------------------------------------------------------------
📥 Fetching content from: https://example.com
✅ Successfully scraped content from https://example.com

📊 Scraped Content Summary:
  • Title: Example Domain
  • Description: This domain is for use in illustrative examples...
  • Main Content Length: 1234 characters
  • Headings Found: 3
  • Links Found: 5

📌 Step 4: Initializing Chatbot
----------------------------------------------------------------------
📚 Website context loaded: 2456 characters

📌 Step 5: Starting Console Interface
----------------------------------------------------------------------

======================================================================
🤖 WEBSITE CONTENT CHATBOT
======================================================================

This chatbot can answer questions based on website content.

📋 Commands:
  • Type your question and press Enter
  • Type 'clear' to clear conversation history
  • Type 'exit' or 'quit' to end the session

💡 Example questions:
  • What is this website about?
  • What are the main features mentioned?
  • What products or services are offered?
  • How can I contact them?

======================================================================

❓ Your question: What is this website about?

🤖 Chatbot:
This website is example.com, which is provided for use in illustrative examples in documents. It's a demonstration domain that can be used without prior coordination or asking for permission.

❓ Your question: exit

👋 Thank you for using the chatbot. Goodbye!
```

### Console Commands

- **Type your question**: Ask anything about the website content
- **`clear`**: Clear the conversation history
- **`exit`** or **`quit`**: End the chatbot session

## How It Works

### Architecture

1. **WebsiteScraper Class**: Handles web scraping and content extraction
2. **Chatbot Class**: Manages OpenAI API integration and conversation
3. **ConsoleInterface Class**: Provides user interaction via console

### Workflow

1. User provides a website URL
2. Chatbot scrapes the website content
3. Content is processed and structured
4. Chatbot initializes with website context
5. User asks questions via console
6. Chatbot generates responses using only scraped content
7. Responses are displayed to the user

### Content Extraction

The scraper extracts the following from websites:
- Page title
- Meta description
- Main content (prioritizes `<main>`, `<article>`, or content divs)
- Headings (h1-h6)
- Important links

## Important Notes

- The chatbot answers questions **only** using information from the scraped website
- If information is not available on the website, it will respond: "The requested information is not available on the provided website."
- The chatbot does not use external knowledge or information beyond the website content
- Some websites may block scraping or have dynamic content that requires JavaScript

## Troubleshooting

### API Key Not Found
```
❌ Error: OPENAI_API_KEY not found in environment variables.
```
**Solution**: Ensure you have created a `.env` file with your API key.

### Website Not Accessible
```
❌ Error fetching website: [error message]
```
**Solution**: 
- Check if the URL is correct
- Ensure the website is accessible
- Some websites may block automated scraping

### No Content Extracted
```
❌ Failed to scrape website content.
```
**Solution**:
- Try a different website
- Some websites use JavaScript for content loading
- Verify the website structure

## Project Structure

```
website-chatbot/
├── website_chatbot.py           # Main application code
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── STEP_BY_STEP_PROCESS.md      # Detailed development process
├── .env                         # API key (create this)
└── .env.example                 # Environment variable template
```

## Technical Details

### Dependencies

- **openai**: OpenAI Python client for ChatGPT API
- **beautifulsoup4**: HTML parsing library
- **requests**: HTTP library for web scraping
- **python-dotenv**: Environment variable management
- **lxml**: Fast XML/HTML parser

### OpenAI API Configuration

- Model: `gpt-3.5-turbo`
- Temperature: `0.7` (balanced creativity)
- Max Tokens: `500` (response length limit)
- Conversation History: Last 10 messages

## License

This project is created for educational and demonstration purposes.

## Author

Created as an assignment demonstrating web scraping, AI integration, and console application development.

---

**Happy Chatting! 🤖**# chatbot_Scrape-Website
# chatbot_Scrape-Website
