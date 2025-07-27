import os
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarManager:
    def __init__(self, credentials_file='credentials.json', token_file='token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.creds = None
        
    def authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    return False
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"""
                    Google Calendar credentials not found!
                    
                    To set up Google Calendar integration:
                    1. Go to Google Cloud Console (https://console.cloud.google.com/)
                    2. Create a new project or select existing one
                    3. Enable the Google Calendar API
                    4. Create credentials (OAuth 2.0 Client ID)
                    5. Download the credentials as '{self.credentials_file}'
                    6. Place the file in the same directory as this script
                    """)
                    return False
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during authentication: {e}")
                    return False
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.creds = creds
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"Error building calendar service: {e}")
            return False
    
    def create_reminder_event(self, event_info, buffer_minutes=30):
        """
        Create a reminder event in Google Calendar
        
        Args:
            event_info (dict): Dictionary containing event information
            buffer_minutes (int): Minutes before the actual deadline to set reminder
        
        Returns:
            dict: Created event details or None if failed
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            # Prepare event datetime
            event_datetime = self.prepare_event_datetime(event_info, buffer_minutes)
            if not event_datetime:
                print("Could not determine event date/time")
                return None
            
            # Prepare event description
            description = self.prepare_description(event_info)
            
            # Create event object
            event = {
                'summary': event_info.get('title', 'Reminder'),
                'description': description,
                'start': {
                    'dateTime': event_datetime['start'],
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': event_datetime['end'],
                    'timeZone': 'UTC',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before
                        {'method': 'popup', 'minutes': 10},       # 10 minutes before
                    ],
                },
            }
            
            # Add location if links are available
            if event_info.get('links'):
                event['location'] = event_info['links'][0]
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            print(f"Event created: {created_event.get('htmlLink')}")
            return created_event
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def prepare_event_datetime(self, event_info, buffer_minutes):
        """Prepare start and end datetime for the event"""
        try:
            # Get date and time from event_info
            event_date = event_info.get('date')
            event_time = event_info.get('time')
            
            if not event_date:
                # Default to tomorrow if no date specified
                event_date = (datetime.now() + timedelta(days=1)).date()
            
            if not event_time:
                # Default to 9 AM if no time specified
                event_time = datetime.strptime("09:00", "%H:%M").time()
            
            # Combine date and time
            event_datetime = datetime.combine(event_date, event_time)
            
            # Subtract buffer time for reminder
            reminder_datetime = event_datetime - timedelta(minutes=buffer_minutes)
            
            # Event duration (30 minutes)
            end_datetime = reminder_datetime + timedelta(minutes=30)
            
            return {
                'start': reminder_datetime.isoformat() + 'Z',
                'end': end_datetime.isoformat() + 'Z'
            }
            
        except Exception as e:
            print(f"Error preparing datetime: {e}")
            return None
    
    def prepare_description(self, event_info):
        """Prepare event description with all relevant information"""
        description_parts = []
        
        # Original message
        if event_info.get('description'):
            description_parts.append(f"Original Message:\n{event_info['description']}")
        
        # Event type and urgency
        if event_info.get('event_type'):
            description_parts.append(f"Type: {event_info['event_type'].title()}")
        
        if event_info.get('urgency') == 'high':
            description_parts.append("⚠️ HIGH PRIORITY")
        
        # Keywords found
        if event_info.get('keywords'):
            description_parts.append(f"Keywords: {', '.join(event_info['keywords'])}")
        
        # Links
        if event_info.get('links'):
            description_parts.append("Links:")
            for link in event_info['links']:
                description_parts.append(f"• {link}")
        
        # Additional instructions
        description_parts.append("\n📝 Action Required:")
        if event_info.get('event_type') == 'job':
            description_parts.append("• Check application requirements")
            description_parts.append("• Prepare resume/documents")
            description_parts.append("• Submit application")
        else:
            description_parts.append("• Review the message details")
            description_parts.append("• Take necessary action")
        
        return "\n\n".join(description_parts)
    
    def list_upcoming_events(self, max_results=10):
        """List upcoming events from the calendar"""
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(
                calendarId='primary', 
                timeMin=now,
                maxResults=max_results, 
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return events
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def delete_event(self, event_id):
        """Delete an event from the calendar"""
        if not self.service:
            if not self.authenticate():
                return False
        
        try:
            self.service.events().delete(
                calendarId='primary', 
                eventId=event_id
            ).execute()
            print(f"Event {event_id} deleted successfully")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

# Demo function for testing without GUI
def demo_calendar_integration():
    """Demo function to test calendar integration"""
    calendar_manager = GoogleCalendarManager()
    
    # Test event info
    test_event = {
        'title': 'Apply: Infosys Hiring Opportunity',
        'date': (datetime.now() + timedelta(days=2)).date(),
        'time': datetime.strptime("17:00", "%H:%M").time(),
        'description': 'Infosys is hiring! Apply before July 30, 2025 at 5 PM.',
        'links': ['https://infosys.com/jobs'],
        'event_type': 'job',
        'urgency': 'high',
        'keywords': ['hiring', 'apply']
    }
    
    print("Testing Google Calendar integration...")
    
    # Create event
    created_event = calendar_manager.create_reminder_event(test_event)
    if created_event:
        print("✅ Event created successfully!")
        print(f"Event ID: {created_event.get('id')}")
        print(f"Event Link: {created_event.get('htmlLink')}")
    else:
        print("❌ Failed to create event")
    
    # List upcoming events
    print("\nUpcoming events:")
    events = calendar_manager.list_upcoming_events(5)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"• {event['summary']} - {start}")

if __name__ == "__main__":
    demo_calendar_integration()