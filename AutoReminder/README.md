# AutoReminder – Smart WhatsApp Reminder Assistant

AutoReminder reads WhatsApp-style messages, detects important events (interviews, application deadlines, etc.), and pushes reminders to your Google Calendar.

## Quick Start
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Obtain a Google Cloud “OAuth Client ID” (Desktop) and download `credentials.json` into the project root.
4. `streamlit run main.py`

## Folder Structure
```
AutoReminder/
├── main.py            # Streamlit UI
├── nlp_parser.py      # Keyword & datetime extraction
├── calendar_utils.py  # Google Calendar helper
├── sample_chats/      # Example WhatsApp exports
├── requirements.txt   # Dependencies
└── README.md          # This file
```

## How It Works
1. Paste any WhatsApp message into the text area.
2. The NLP module extracts title, date/time and optional link.
3. The Calendar utility authenticates with Google and creates an event ~30 minutes before the detected deadline.

## Roadmap
See project specification for future enhancements such as automatic WhatsApp integration and richer ML-based classification.