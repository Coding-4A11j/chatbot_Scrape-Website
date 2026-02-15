"""
Website Content Chatbot using OpenAI API
=========================================
This chatbot interacts with a given website URL by:
1. Scraping website content using Beautiful Soup
2. Processing and structuring the data
3. Using ChatGPT API to generate relevant responses
4. Providing an interactive console interface

Author: [Your Name]
Date: 2024
"""

import os
import sys
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Web scraping imports
import requests
from bs4 import BeautifulSoup

# OpenAI API import
from openai import OpenAI


class WebsiteScraper:
    """Handles website content extraction and processing"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_website(self, url: str) -> Dict[str, str]:
        """
        Scrape content from the given URL
        
        Args:
            url: The website URL to scrape
            
        Returns:
            Dictionary containing scraped content
        """
        try:
            print(f"📥 Fetching content from: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract different content types
            content = {
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'main_content': self._extract_main_content(soup),
                'headings': self._extract_headings(soup),
                'links': self._extract_links(soup),
                'full_text': self._extract_full_text(soup)
            }
            
            print(f"✅ Successfully scraped content from {url}")
            return content
            
        except requests.RequestException as e:
            print(f"❌ Error fetching website: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
            return {}
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else "No title found"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc.get('content')
        return "No description found"
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Try to find main content area
        main_content = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find('div', class_=lambda x: x and 'content' in x.lower()) or
            soup.body
        )
        
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
            return text[:3000] if text else "No main content found"
        
        return "No main content found"
    
    def _extract_headings(self, soup: BeautifulSoup) -> str:
        """Extract all headings (h1-h6)"""
        headings = []
        for level in range(1, 7):
            for heading in soup.find_all(f'h{level}'):
                headings.append(f"H{level}: {heading.get_text(strip=True)}")
        return '\n'.join(headings[:20]) if headings else "No headings found"
    
    def _extract_links(self, soup: BeautifulSoup) -> str:
        """Extract important links"""
        links = []
        for link in soup.find_all('a', href=True)[:15]:
            text = link.get_text(strip=True)
            href = link['href']
            if text and not href.startswith('#'):
                links.append(f"{text}: {href}")
        return '\n'.join(links) if links else "No links found"
    
    def _extract_full_text(self, soup: BeautifulSoup) -> str:
        """Extract all text from the page"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        text = soup.get_text(separator='\n', strip=True)
        # Clean up multiple newlines
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        return text[:5000] if text else "No text found"


class Chatbot:
    """Handles ChatGPT API integration and conversation management"""
    
    def __init__(self, api_key: str):
        """
        Initialize the chatbot with OpenAI API
        
        Args:
            api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        self.conversation_history: List[Dict[str, str]] = []
        self.website_content: str = ""
    
    def set_website_context(self, content: Dict[str, str]) -> None:
        """
        Set the website content as context for the chatbot
        
        Args:
            content: Dictionary containing scraped website content
        """
        self.website_content = self._format_content_for_context(content)
        print(f"📚 Website context loaded: {len(self.website_content)} characters")
    
    def _format_content_for_context(self, content: Dict[str, str]) -> str:
        """Format scraped content into a readable context string"""
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
    
    def get_response(self, user_input: str) -> str:
        """
        Generate response from ChatGPT API using website context
        
        Args:
            user_input: User's question or message
            
        Returns:
            Chatbot's response
        """
        try:
            # Create system message with website context
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

            # Prepare messages for API call
            messages = [
                {"role": "system", "content": system_message}
            ]
            
            # Add conversation history (limited to last 5 exchanges)
            messages.extend(self.conversation_history[-10:])
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            print("🤖 Processing your question...")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"❌ Error generating response: {e}"
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []


class ConsoleInterface:
    """Handles user interaction through console"""
    
    def __init__(self, chatbot: Chatbot):
        """
        Initialize console interface
        
        Args:
            chatbot: Instance of Chatbot class
        """
        self.chatbot = chatbot
        self.running = True
    
    def display_welcome(self) -> None:
        """Display welcome message and instructions"""
        print("\n" + "="*70)
        print("🤖 WEBSITE CONTENT CHATBOT")
        print("="*70)
        print("\nThis chatbot can answer questions based on website content.")
        print("\n📋 Commands:")
        print("  • Type your question and press Enter")
        print("  • Type 'clear' to clear conversation history")
        print("  • Type 'exit' or 'quit' to end the session")
        print("\n💡 Example questions:")
        print("  • What is this website about?")
        print("  • What are the main features mentioned?")
        print("  • What products or services are offered?")
        print("  • How can I contact them?")
        print("\n" + "="*70 + "\n")
    
    def get_user_input(self) -> str:
        """Get user input from console"""
        try:
            user_input = input("❓ Your question: ").strip()
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def display_response(self, response: str) -> None:
        """Display chatbot response"""
        print(f"\n🤖 Chatbot:\n{response}\n")
    
    def run(self) -> None:
        """Main console interaction loop"""
        self.display_welcome()
        
        while self.running:
            try:
                user_input = self.get_user_input()
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit']:
                    print("\n👋 Thank you for using the chatbot. Goodbye!\n")
                    self.running = False
                elif user_input.lower() == 'clear':
                    self.chatbot.clear_history()
                    print("✅ Conversation history cleared.\n")
                elif not user_input:
                    print("⚠️ Please enter a question.\n")
                else:
                    # Get chatbot response
                    response = self.chatbot.get_response(user_input)
                    self.display_response(response)
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!\n")
                self.running = False
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


def setup_environment():
    """
    Setup and validate the environment
    
    Returns:
        tuple: (api_key, success)
    """
    print("🔧 Setting up environment...")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("\n📝 Setup Instructions:")
        print("1. Create a .env file in the project directory")
        print("2. Add your OpenAI API key: OPENAI_API_KEY=your-api-key-here")
        print("3. Run the script again")
        return None, False
    
    print("✅ Environment setup complete.")
    return api_key, True


def main():
    """Main function to run the website chatbot"""
    print("\n" + "="*70)
    print("🚀 WEBSITE CONTENT CHATBOT - STARTING")
    print("="*70 + "\n")
    
    # Step 1: Setup Environment
    api_key, success = setup_environment()
    if not success:
        sys.exit(1)
    
    # Step 2: Get Website URL from user
    print("\n📌 Step 2: Enter Website URL")
    print("-" * 70)
    while True:
        url = input("Enter the website URL to scrape: ").strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            break
        print("⚠️ Please enter a valid URL.\n")
    
    # Step 3: Scrape Website Content
    print("\n📌 Step 3: Scraping Website Content")
    print("-" * 70)
    scraper = WebsiteScraper()
    website_content = scraper.scrape_website(url)
    
    if not website_content:
        print("\n❌ Failed to scrape website content. Please check the URL and try again.")
        sys.exit(1)
    
    # Display scraped content summary
    print("\n📊 Scraped Content Summary:")
    print(f"  • Title: {website_content.get('title', 'N/A')[:60]}...")
    print(f"  • Description: {website_content.get('description', 'N/A')[:60]}...")
    print(f"  • Main Content Length: {len(website_content.get('main_content', ''))} characters")
    print(f"  • Headings Found: {len(website_content.get('headings', '').split('\\n'))}")
    print(f"  • Links Found: {len(website_content.get('links', '').split('\\n'))}")
    
    # Step 4: Initialize Chatbot with Website Context
    print("\n📌 Step 4: Initializing Chatbot")
    print("-" * 70)
    chatbot = Chatbot(api_key)
    chatbot.set_website_context(website_content)
    
    # Step 5: Start Console Interface
    print("\n📌 Step 5: Starting Console Interface")
    print("-" * 70)
    console = ConsoleInterface(chatbot)
    console.run()


if __name__ == "__main__":
    main()