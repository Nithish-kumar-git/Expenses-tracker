import streamlit as st

from nlp_parser import parse_message
from calendar_utils import create_calendar_event

st.set_page_config(page_title="AutoReminder", layout="centered")

st.title("📅 AutoReminder – Smart WhatsApp Reminder Assistant")

st.markdown(
    "Paste a WhatsApp message below. The app will detect any deadline/interview date and schedule a reminder in your Google Calendar."
)

message = st.text_area("Message text", height=200)

if st.button("Create Reminder"):
    if not message.strip():
        st.error("Please paste a message first.")
    else:
        with st.spinner("Parsing message …"):
            event_data = parse_message(message)
        st.success("Parsed details:")
        st.json({k: str(v) for k, v in event_data.items() if k != "raw"})

        if not event_data.get("datetime"):
            st.warning("Could not find a date/time in the message – no reminder created.")
        else:
            try:
                link = create_calendar_event(event_data)
                st.success(f"Event created ✔️  [Open in Calendar]({link})")
            except Exception as e:
                st.error(f"Failed to create event: {e}")