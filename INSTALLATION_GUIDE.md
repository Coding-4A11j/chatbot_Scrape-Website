# Quick Installation & Usage Guide

## 🚀 Quick Start (5 Minutes)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install openai beautifulsoup4 requests python-dotenv lxml
```

### 2. Set Up API Key

Create a `.env` file in the project directory:

```bash
# .env file content
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get your API key**: https://platform.openai.com/api-keys

### 3. Run the Chatbot

```bash
python website_chatbot.py
```

### 4. Start Chatting!

1. Enter a website URL (e.g., https://example.com)
2. Wait for content to be scraped
3. Ask questions about the website
4. Type `exit` to quit

---

## 📋 Common Commands

### Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Check installed packages
pip list
```

### Running the Application
```bash
# Main chatbot
python website_chatbot.py

# Demo (shows structure and scraping)
python demo_example.py
```

### Environment Setup
```bash
# Create .env file
touch .env

# Edit .env file
nano .env  # or use your preferred editor

# Verify .env file exists
ls -la .env
```

---

## 🔧 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution**: 
1. Ensure `.env` file exists in project directory
2. Check that the file contains: `OPENAI_API_KEY=your-key-here`
3. Make sure there are no spaces around the `=` sign

### Issue: "Module not found"
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Website not scraping
**Solution**:
- Try a different website (some block scraping)
- Check your internet connection
- Verify the URL is correct

---

## 💡 Example Websites to Test

Good websites for testing:
- `https://example.com` - Simple demonstration site
- `https://httpbin.org/html` - Testing HTML structure
- `https://www.scrapethissite.com/pages/` - Scraping practice site

---

## 📊 Project Structure

```
website-chatbot/
├── website_chatbot.py       # Main application ⭐
├── demo_example.py          # Demo script
├── requirements.txt         # Dependencies
├── README.md                # Full documentation
├── INSTALLATION_GUIDE.md    # This file
├── STEP_BY_STEP_PROCESS.md  # Development process
├── .env                     # API key (you create this)
├── .env.example             # Example .env file
└── .gitignore               # Git ignore rules
```

---

## 🎯 Usage Tips

1. **Start with simple websites** - e.g., example.com
2. **Ask specific questions** - "What is this about?" is better than "Tell me everything"
3. **Use clear commands** - `exit`, `clear`
4. **Check your API usage** - Monitor OpenAI dashboard

---

## 📞 Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review STEP_BY_STEP_PROCESS.md for implementation details
3. Verify your setup using demo_example.py

---

**Ready to chat? Run `python website_chatbot.py` now! 🤖**