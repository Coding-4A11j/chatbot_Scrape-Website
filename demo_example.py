"""
Demo Example - Website Content Chatbot
======================================
This script demonstrates how to use the website_chatbot module
without requiring user interaction during testing.
"""

import sys
from website_chatbot import WebsiteScraper, Chatbot


def demo_scraping():
    """Demonstrate web scraping functionality"""
    print("="*70)
    print("📊 DEMO: Web Scraping Functionality")
    print("="*70 + "\n")
    
    scraper = WebsiteScraper()
    
    # Example website to scrape
    test_url = "https://example.com"
    
    print(f"🔗 Scraping URL: {test_url}\n")
    
    content = scraper.scrape_website(test_url)
    
    if content:
        print("✅ Scraping Successful!\n")
        print("📄 Extracted Content:")
        print("-" * 70)
        print(f"\n📌 Title:\n{content.get('title', 'N/A')}\n")
        print(f"📌 Description:\n{content.get('description', 'N/A')}\n")
        print(f"📌 Main Content (first 500 chars):\n{content.get('main_content', 'N/A')[:500]}...\n")
        print(f"📌 Headings:\n{content.get('headings', 'N/A')}\n")
        print(f"📌 Links (first 3):\n{chr(10).join(content.get('links', 'N/A').split(chr(10))[:3])}\n")
    else:
        print("❌ Scraping failed\n")
    
    return content


def demo_content_processing(content):
    """Demonstrate content processing"""
    print("="*70)
    print("📊 DEMO: Content Processing")
    print("="*70 + "\n")
    
    if not content:
        print("⚠️ No content to process\n")
        return ""
    
    # Simulate content formatting
    context_parts = []
    
    if content.get('title'):
        context_parts.append(f"Title: {content['title']}")
        print(f"✅ Title added: {content['title'][:50]}...")
    
    if content.get('description'):
        context_parts.append(f"Description: {content['description']}")
        print(f"✅ Description added: {content['description'][:50]}...")
    
    if content.get('main_content'):
        context_parts.append(f"Main Content: {content['main_content'][:200]}...")
        print(f"✅ Main content added ({len(content['main_content'])} chars)")
    
    formatted_content = '\n'.join(context_parts)
    
    print(f"\n📊 Total Context Length: {len(formatted_content)} characters\n")
    
    return formatted_content


def demo_chatbot_structure(api_key=None):
    """Demonstrate chatbot class structure"""
    print("="*70)
    print("📊 DEMO: Chatbot Class Structure")
    print("="*70 + "\n")
    
    if not api_key:
        print("⚠️ No API key provided - showing structure only\n")
        print("🏗️ Chatbot Class Components:")
        print("-" * 70)
        print("  • __init__(api_key): Initialize with OpenAI API key")
        print("  • set_website_context(content): Set scraped website content")
        print("  • get_response(user_input): Generate response using ChatGPT")
        print("  • clear_history(): Clear conversation history")
        print("\n📝 Key Features:")
        print("  • Maintains conversation history")
        print("  • Uses website content as context")
        print("  • Enforces answers based only on scraped content")
        print("  • Handles errors gracefully")
        print()
    else:
        print("✅ API key provided - chatbot would be functional\n")
        print("💡 To use the chatbot:")
        print("  1. Run: python website_chatbot.py")
        print("  2. Enter a website URL")
        print("  3. Start asking questions!")
        print()


def demo_console_interface():
    """Demonstrate console interface structure"""
    print("="*70)
    print("📊 DEMO: Console Interface Structure")
    print("="*70 + "\n")
    
    print("🖥️ ConsoleInterface Class Components:")
    print("-" * 70)
    print("  • display_welcome(): Show welcome message and instructions")
    print("  • get_user_input(): Get user questions")
    print("  • display_response(): Show chatbot responses")
    print("  • run(): Main interaction loop")
    print("\n📋 Available Commands:")
    print("  • Type your question: Ask about website content")
    print("  • 'clear': Clear conversation history")
    print("  • 'exit' or 'quit': End session")
    print("\n💡 Example Questions:")
    print("  • What is this website about?")
    print("  • What are the main features?")
    print("  • How can I contact them?")
    print("  • What products/services are offered?")
    print()


def main():
    """Main demo function"""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "WEBSITE CHATBOT DEMO" + " "*31 + "║")
    print("╚" + "═"*68 + "╝")
    print("\n")
    print("This demo shows the structure and functionality of the website chatbot.")
    print("To use the full chatbot, run: python website_chatbot.py")
    print("\n")
    
    # Check for API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("⚠️ Note: No OPENAI_API_KEY found in environment variables.")
        print("The demo will show structure and web scraping, but not AI responses.")
        print("To enable AI responses, add your API key to a .env file.")
        print()
    
    input("Press Enter to start the demo...")
    print()
    
    # Demo 1: Web Scraping
    content = demo_scraping()
    input("\nPress Enter to continue...")
    print()
    
    # Demo 2: Content Processing
    formatted_content = demo_content_processing(content)
    input("\nPress Enter to continue...")
    print()
    
    # Demo 3: Chatbot Structure
    demo_chatbot_structure(api_key)
    input("\nPress Enter to continue...")
    print()
    
    # Demo 4: Console Interface
    demo_console_interface()
    input("\nPress Enter to continue...")
    print()
    
    # Final Summary
    print("="*70)
    print("📊 DEMO SUMMARY")
    print("="*70 + "\n")
    print("✅ Web Scraping: Demonstrated")
    print("✅ Content Processing: Demonstrated")
    print("✅ Chatbot Structure: Demonstrated")
    print("✅ Console Interface: Demonstrated")
    print("\n🚀 Ready to Use!")
    print("Run: python website_chatbot.py")
    print("\n📝 Setup Instructions:")
    print("1. Create .env file with OPENAI_API_KEY")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python website_chatbot.py")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}\n")
        sys.exit(1)