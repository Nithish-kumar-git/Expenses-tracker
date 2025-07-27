# 🚀 AutoReminder: Smart WhatsApp Message Parser

A Smart Message Parser for Event Detection and Calendar Integration that automatically identifies important events like job applications or interviews from WhatsApp messages and creates reminders in Google Calendar.

## 📌 Features

### ✅ Core MVP Features
- **Message Input**: Paste message text from WhatsApp or upload .txt exported chat
- **Event Detection using NLP**: Identify keywords like "interview", "register before", "last date", "apply by" and extract date/time
- **Reminder Creation**: Use Google Calendar API to create reminders with extracted info
- **Simple User Interface**: Beautiful Streamlit web interface with:
  - Text box to paste message
  - Button: "Create Reminder"
  - Output: Confirmation + scheduled time

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| 🖥️ Interface | Python + Streamlit |
| 🧠 NLP Processing | spaCy, NLTK, regex |
| 📅 Calendar Integration | Google Calendar API (OAuth) |
| 📤 Data Input | Manual paste or .txt file upload |

## 📁 Project Structure

```
AutoReminder/
│
├── main.py                # Streamlit application
├── nlp_parser.py          # Extract dates, links, keywords
├── calendar_utils.py      # Code to create reminders via API
├── sample_chats/          # Folder for WhatsApp text samples
│   └── job_messages.txt   # Sample job-related messages
├── templates/             # For UI templates (future use)
├── requirements.txt       # All dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd AutoReminder

# Install dependencies
pip install -r requirements.txt

# Download spaCy model (optional, for better NLP)
python -m spacy download en_core_web_sm
```

### 2. Google Calendar Setup (Optional)

To enable Google Calendar integration:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials as `credentials.json`
6. Place the file in the AutoReminder directory

### 3. Run the Application

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## 📊 Example Workflow

### Step 1: Input Message
```
Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs
```

### Step 2: NLP Extraction
- **Title**: Apply: Infosys is hiring!
- **Date**: July 30, 2025
- **Time**: 5 PM
- **Link**: infosys.com/jobs
- **Event Type**: Job
- **Urgency**: Normal

### Step 3: Calendar Reminder
- **Title**: "Apply: Infosys Hiring"
- **Time**: July 30, 2025 – 4:30 PM (30min buffer before deadline)
- **Notes**: Job link attached + action items

## 🧠 NLP Capabilities

The system can detect:

### Event Types
- **Job-related**: hiring, recruiting, job, apply, application, interview, position, vacancy
- **General**: deadlines, appointments, meetings, reminders

### Date Formats
- `July 30, 2025`
- `30/07/2025`
- `30th July`
- `tomorrow`, `today`
- `1st August`

### Time Formats
- `5 PM`, `17:00`
- `10:30 AM`
- `9 AM to 4 PM`

### Links
- HTTP/HTTPS URLs
- Simple domain formats (e.g., `infosys.com/jobs`)

## 🎯 Usage Examples

### Sample Messages (included in app)
1. `Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs`
2. `Hey, Cognizant is recruiting freshers! Apply before Aug 5 at 6 PM`
3. `Don't forget – Wipro interview at 10 AM on 1st August.`
4. `You need to submit your resume by July 28th.`

### File Upload
You can also upload WhatsApp chat exports (.txt files) for batch processing.

## 🔧 Configuration

### Buffer Time
- Default: 30 minutes before deadline
- Adjustable: 15-120 minutes
- Purpose: Get reminded before the actual deadline

### Reminder Settings
- **Email**: 1 day before
- **Popup**: 1 hour before
- **Popup**: 10 minutes before

## 📈 Future Enhancements

### 🌱 Post-MVP Features
- 🗣️ Voice assistant integration
- 📥 Auto-read from WhatsApp backup
- 📎 Smart link saving/bookmarking
- ⏰ Reminder categories (job, fee payment, event)
- 🧠 ML model for better message classification
- 📱 Mobile app version
- 🔔 Push notifications
- 📊 Analytics dashboard

## 🐛 Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Google Calendar authentication fails**
   - Check if `credentials.json` is in the correct location
   - Ensure Calendar API is enabled in Google Cloud Console
   - Try deleting `token.json` and re-authenticating

3. **Date/time not detected**
   - The system works best with explicit dates and times
   - Try different date formats
   - Check if the message contains deadline keywords

### Error Messages
- `"spaCy model not found. Using basic NLP."` - Non-critical, basic NLP will still work
- `"Google Calendar credentials not found!"` - Calendar integration disabled, but NLP analysis still works

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample messages
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review sample messages for format examples
3. Ensure all dependencies are installed correctly

---

**Built with ❤️ using Python, Streamlit, spaCy, and Google Calendar API**