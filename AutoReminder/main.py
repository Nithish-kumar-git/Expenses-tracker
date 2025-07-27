import streamlit as st
from datetime import datetime, timedelta
import os
import sys

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_parser import MessageParser
from calendar_utils import GoogleCalendarManager

# Page configuration
st.set_page_config(
    page_title="AutoReminder - Smart WhatsApp Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'parser' not in st.session_state:
        st.session_state.parser = MessageParser()
    if 'calendar_manager' not in st.session_state:
        st.session_state.calendar_manager = GoogleCalendarManager()
    if 'extracted_events' not in st.session_state:
        st.session_state.extracted_events = []
    if 'created_events' not in st.session_state:
        st.session_state.created_events = []

def main():
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🚀 AutoReminder</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Smart Message Parser for Event Detection and Calendar Integration</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Features")
        st.markdown("""
        ✅ **Message Input** - Paste WhatsApp text  
        ✅ **Event Detection** - AI-powered NLP  
        ✅ **Calendar Integration** - Google Calendar  
        ✅ **Smart Reminders** - Automated scheduling  
        """)
        
        st.header("📊 Statistics")
        st.metric("Messages Processed", len(st.session_state.extracted_events))
        st.metric("Events Created", len(st.session_state.created_events))
        
        # Sample messages
        st.header("📝 Sample Messages")
        sample_messages = [
            "Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs",
            "Hey, Cognizant is recruiting freshers! Apply before Aug 5 at 6 PM",
            "Don't forget – Wipro interview at 10 AM on 1st August.",
            "You need to submit your resume by July 28th."
        ]
        
        selected_sample = st.selectbox("Choose a sample:", ["None"] + sample_messages)
        if st.button("Use Sample"):
            if selected_sample != "None":
                st.session_state.sample_message = selected_sample
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📱 Message Input")
        
        # Text input methods
        input_method = st.radio("Choose input method:", ["Paste Text", "Upload File"])
        
        message_text = ""
        
        if input_method == "Paste Text":
            # Use sample message if selected
            default_text = st.session_state.get('sample_message', '')
            message_text = st.text_area(
                "Paste your WhatsApp message here:",
                value=default_text,
                height=150,
                placeholder="Example: Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs"
            )
        else:
            uploaded_file = st.file_uploader("Upload WhatsApp chat export (.txt)", type=['txt'])
            if uploaded_file is not None:
                message_text = str(uploaded_file.read(), "utf-8")
                st.text_area("File content preview:", value=message_text[:500] + "...", height=100, disabled=True)
        
        # Process message button
        if st.button("🔍 Analyze Message", type="primary", use_container_width=True):
            if message_text.strip():
                with st.spinner("Analyzing message with AI..."):
                    try:
                        # Extract event information
                        event_info = st.session_state.parser.extract_event_info(message_text)
                        st.session_state.extracted_events.append(event_info)
                        
                        # Display results
                        st.success("✅ Message analyzed successfully!")
                        
                        # Show extracted information
                        st.subheader("📊 Extracted Information")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.write("**Title:**", event_info['title'])
                            st.write("**Event Type:**", event_info['event_type'].title())
                            st.write("**Urgency:**", event_info['urgency'].title())
                            
                        with col_b:
                            st.write("**Date:**", event_info['date'] if event_info['date'] else "Not specified")
                            st.write("**Time:**", event_info['time'] if event_info['time'] else "Not specified")
                            st.write("**Keywords:**", ", ".join(event_info['keywords']) if event_info['keywords'] else "None")
                        
                        if event_info['links']:
                            st.write("**Links found:**")
                            for link in event_info['links']:
                                st.write(f"• {link}")
                        
                        # Store in session for calendar creation
                        st.session_state.current_event = event_info
                        
                    except Exception as e:
                        st.error(f"❌ Error analyzing message: {str(e)}")
            else:
                st.warning("⚠️ Please enter a message to analyze.")
    
    with col2:
        st.header("📅 Calendar Integration")
        
        # Calendar setup status
        credentials_exist = os.path.exists('credentials.json')
        
        if not credentials_exist:
            st.markdown("""
            <div class="info-box">
            <h4>🔧 Setup Required</h4>
            <p>To use Google Calendar integration:</p>
            <ol>
            <li>Go to <a href="https://console.cloud.google.com/" target="_blank">Google Cloud Console</a></li>
            <li>Enable Calendar API</li>
            <li>Create OAuth 2.0 credentials</li>
            <li>Download as 'credentials.json'</li>
            <li>Place in project folder</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ Google Calendar credentials found!")
        
        # Create reminder button
        if hasattr(st.session_state, 'current_event'):
            st.subheader("Create Reminder")
            
            # Buffer time setting
            buffer_minutes = st.slider("Reminder buffer (minutes before deadline):", 15, 120, 30)
            
            if st.button("📅 Create Calendar Reminder", type="primary", use_container_width=True):
                if credentials_exist:
                    with st.spinner("Creating calendar event..."):
                        try:
                            created_event = st.session_state.calendar_manager.create_reminder_event(
                                st.session_state.current_event, 
                                buffer_minutes
                            )
                            
                            if created_event:
                                st.success("✅ Reminder created successfully!")
                                st.session_state.created_events.append(created_event)
                                
                                # Show event details
                                st.write("**Event ID:**", created_event.get('id', 'N/A'))
                                if created_event.get('htmlLink'):
                                    st.markdown(f"[📅 View in Google Calendar]({created_event['htmlLink']})")
                            else:
                                st.error("❌ Failed to create calendar event. Check your credentials and try again.")
                                
                        except Exception as e:
                            st.error(f"❌ Error creating event: {str(e)}")
                else:
                    st.error("❌ Google Calendar credentials not found. Please set up credentials first.")
    
    # Recent events section
    if st.session_state.extracted_events:
        st.header("📋 Recent Analysis")
        
        # Display events without pandas
        for i, event in enumerate(st.session_state.extracted_events[-5:]):  # Show last 5
            with st.expander(f"Event {i+1}: {event['title'][:30]}{'...' if len(event['title']) > 30 else ''}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Type:**", event['event_type'].title())
                    st.write("**Date:**", str(event['date']) if event['date'] else "Not specified")
                    st.write("**Time:**", str(event['time']) if event['time'] else "Not specified")
                with col2:
                    st.write("**Urgency:**", event['urgency'].title())
                    st.write("**Links:**", len(event['links']))
                    if event['links']:
                        for link in event['links']:
                            st.write(f"• {link}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
    <p>🚀 AutoReminder MVP - Smart WhatsApp Message Parser</p>
    <p>Built with Streamlit, spaCy, and Google Calendar API</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()