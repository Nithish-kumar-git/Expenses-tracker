# 🚀 AutoReminder - Usage Guide

## Quick Start

### 1. Installation & Setup
```bash
# Navigate to project directory
cd AutoReminder

# Activate virtual environment
source venv/bin/activate

# Dependencies are already installed, but if needed:
# pip install -r requirements_minimal.txt
```

### 2. Run the Application
```bash
# Start the web application
streamlit run main.py

# Open browser to: http://localhost:8501
```

### 3. Test with Demo
```bash
# Run the demo to see NLP parsing in action
python demo.py
```

## 🎯 Core Features

### ✅ What Works Right Now
- **Message Analysis**: Paste WhatsApp messages and get instant NLP analysis
- **Event Detection**: Automatically identifies job applications, interviews, deadlines
- **Date/Time Extraction**: Parses various date and time formats
- **Link Detection**: Finds URLs and domain names in messages
- **Urgency Classification**: Identifies urgent messages with keywords like "ASAP", "urgent"
- **File Upload**: Upload WhatsApp chat export files (.txt)
- **Sample Messages**: Built-in examples for testing

### 📊 NLP Capabilities
The system can extract:
- **Event Types**: Job applications, interviews, general reminders
- **Dates**: "July 30, 2025", "Aug 5", "1st August", "tomorrow"
- **Times**: "5 PM", "10:30 AM", "9 AM to 4 PM"
- **Companies**: Infosys, Cognizant, Wipro, etc.
- **Keywords**: hiring, apply, interview, deadline, urgent
- **Links**: Both full URLs and simple domains

## 📅 Google Calendar Integration

### Setup (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download as `credentials.json`
6. Place in AutoReminder directory

### Features (When Setup)
- ✅ Automatic calendar event creation
- ✅ Smart reminder timing (30 min before deadline)
- ✅ Detailed event descriptions with all extracted info
- ✅ Multiple reminder notifications (email + popup)

## 📱 Using the Web Interface

### Message Input
1. **Paste Text**: Copy-paste WhatsApp messages directly
2. **Upload File**: Upload WhatsApp chat export (.txt files)
3. **Use Samples**: Try built-in sample messages

### Analysis Results
After clicking "🔍 Analyze Message", you'll see:
- **Title**: Auto-generated event title
- **Event Type**: Job, Interview, or General
- **Date/Time**: Extracted scheduling information
- **Urgency**: Normal or High priority
- **Keywords**: Relevant terms found
- **Links**: URLs and domains detected

### Calendar Integration
1. Analyze a message first
2. Adjust "Reminder buffer" (15-120 minutes before deadline)
3. Click "📅 Create Calendar Reminder"
4. View created event in Google Calendar

## 📝 Sample Messages for Testing

```
Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs

Hey, Cognizant is recruiting freshers! Apply before Aug 5 at 6 PM

Don't forget – Wipro interview at 10 AM on 1st August.

Urgent: HCL hiring for immediate positions. Apply ASAP before Aug 10th.

Amazon is conducting walk-in interviews on 20th July from 9 AM to 4 PM.
```

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **NLP Engine**: NLTK + regex patterns + dateutil
- **Calendar API**: Google Calendar API with OAuth
- **Data Processing**: Pure Python with datetime handling

### File Structure
```
AutoReminder/
├── main.py              # Streamlit web application
├── nlp_parser.py        # NLP processing engine
├── calendar_utils.py    # Google Calendar integration
├── demo.py             # Demo script
├── sample_chats/       # Sample WhatsApp messages
├── venv/              # Python virtual environment
└── requirements_minimal.txt  # Dependencies
```

### Dependencies
- **streamlit**: Web interface
- **nltk**: Natural language processing
- **python-dateutil**: Date/time parsing
- **google-api-python-client**: Calendar integration
- **google-auth**: Authentication

## 🐛 Troubleshooting

### Common Issues

1. **NLTK Data Missing**
   ```bash
   python -c "import nltk; nltk.download('punkt_tab'); nltk.download('punkt')"
   ```

2. **Calendar Authentication Fails**
   - Check `credentials.json` is in correct location
   - Ensure Calendar API is enabled in Google Cloud Console
   - Delete `token.json` and re-authenticate

3. **Date Not Detected**
   - Use explicit date formats: "July 30, 2025" works better than "next week"
   - Include time information: "5 PM" or "17:00"
   - Add deadline keywords: "before", "by", "due"

4. **Streamlit Port Issues**
   ```bash
   streamlit run main.py --server.port 8502  # Try different port
   ```

## 🚀 Future Enhancements

### Planned Features
- 🗣️ Voice message processing
- 📱 Mobile app version
- 🤖 Advanced AI/ML models
- 📊 Analytics dashboard
- 🔔 Push notifications
- 📎 File attachment handling
- 🌐 Multi-language support

### Contributing
The codebase is modular and extensible:
- Add new date patterns in `nlp_parser.py`
- Extend calendar features in `calendar_utils.py`
- Enhance UI in `main.py`

## 📞 Support

### Getting Help
1. Check this usage guide
2. Run `python demo.py` to verify setup
3. Review error messages in terminal
4. Ensure all dependencies are installed

### Performance Tips
- The app works offline for NLP analysis
- Calendar integration requires internet connection
- Processing is near-instantaneous for typical messages
- File uploads support standard WhatsApp export format

---

**🎉 Ready to turn your WhatsApp messages into smart calendar reminders!**