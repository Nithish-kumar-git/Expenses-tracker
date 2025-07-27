#!/usr/bin/env python3
"""
AutoReminder Demo Script
Demonstrates the NLP parsing capabilities of the Smart WhatsApp Message Parser
"""

from nlp_parser import MessageParser
from calendar_utils import GoogleCalendarManager
from datetime import datetime, timedelta

def demo_nlp_parsing():
    """Demonstrate NLP parsing functionality"""
    print("🚀 AutoReminder - Smart WhatsApp Message Parser Demo")
    print("=" * 60)
    
    # Initialize parser
    parser = MessageParser()
    
    # Test messages from the requirements
    test_messages = [
        "Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs",
        "Hey, Cognizant is recruiting freshers! Apply before Aug 5 at 6 PM – use this link.",
        "You need to submit your resume by July 28th.",
        "Don't forget – Wipro interview at 10 AM on 1st August.",
        "Urgent: HCL hiring for immediate positions. Apply ASAP before Aug 10th. Contact hr@hcl.com",
        "Amazon is conducting walk-in interviews on 20th July from 9 AM to 4 PM. Bring your resume!"
    ]
    
    print("\n📝 Processing Sample Messages:")
    print("-" * 40)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Message: {message}")
        
        # Parse the message
        result = parser.extract_event_info(message)
        
        # Display results
        print(f"   📊 Extracted Information:")
        print(f"   • Title: {result['title']}")
        print(f"   • Type: {result['event_type'].title()}")
        print(f"   • Date: {result['date'] if result['date'] else 'Not specified'}")
        print(f"   • Time: {result['time'] if result['time'] else 'Not specified'}")
        print(f"   • Urgency: {result['urgency'].title()}")
        print(f"   • Keywords: {', '.join(result['keywords']) if result['keywords'] else 'None'}")
        if result['links']:
            print(f"   • Links: {', '.join(result['links'])}")

def demo_calendar_setup():
    """Demonstrate calendar setup requirements"""
    print("\n\n📅 Google Calendar Integration Setup")
    print("=" * 60)
    
    print("""
To enable Google Calendar integration, follow these steps:

1. 🌐 Go to Google Cloud Console (https://console.cloud.google.com/)
2. 📁 Create a new project or select an existing one
3. 🔧 Enable the Google Calendar API
4. 🔑 Create credentials (OAuth 2.0 Client ID)
   - Application type: Desktop application
   - Name: AutoReminder
5. 💾 Download the credentials as 'credentials.json'
6. 📂 Place the file in the AutoReminder directory

Once set up, the app will:
✅ Automatically create calendar events
✅ Set smart reminders (30 min before deadline)
✅ Include all extracted information in event details
✅ Add multiple reminder notifications
    """)
    
    # Check if credentials exist
    import os
    if os.path.exists('credentials.json'):
        print("✅ Google Calendar credentials found!")
        
        # Try to initialize calendar manager
        try:
            calendar_manager = GoogleCalendarManager()
            print("✅ Calendar manager initialized successfully")
        except Exception as e:
            print(f"⚠️ Calendar setup issue: {e}")
    else:
        print("❌ Google Calendar credentials not found")
        print("   Calendar integration will be disabled until credentials are added")

def demo_streamlit_app():
    """Show how to run the Streamlit app"""
    print("\n\n🌐 Running the Web Application")
    print("=" * 60)
    
    print("""
To start the AutoReminder web application:

1. 🖥️ Open terminal in the AutoReminder directory
2. 🐍 Activate virtual environment: source venv/bin/activate
3. 🚀 Run: streamlit run main.py
4. 🌐 Open browser to http://localhost:8501

Features available in the web app:
• 📱 Paste WhatsApp messages directly
• 📁 Upload WhatsApp chat export files (.txt)
• 🔍 Real-time NLP analysis with results display
• 📅 One-click calendar reminder creation
• 📊 History of processed messages
• 🎛️ Adjustable reminder buffer time
• 📋 Sample messages for testing

The app works even without Google Calendar credentials - 
you'll still get full NLP analysis results!
    """)

if __name__ == "__main__":
    # Run all demos
    demo_nlp_parsing()
    demo_calendar_setup()
    demo_streamlit_app()
    
    print("\n\n🎉 Demo Complete!")
    print("Ready to process your WhatsApp messages and create smart reminders!")
    print("\nFor the full experience, run: streamlit run main.py")