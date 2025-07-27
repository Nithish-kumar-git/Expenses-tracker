import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class MessageParser:
    def __init__(self):
        # Using basic NLP without spaCy
        self.nlp = None
        
        # Keywords for different event types
        self.job_keywords = [
            'hiring', 'recruiting', 'job', 'apply', 'application', 'interview', 
            'position', 'vacancy', 'career', 'employment', 'resume', 'cv'
        ]
        
        self.deadline_keywords = [
            'before', 'by', 'deadline', 'last date', 'due', 'expires', 
            'until', 'closing date', 'final date', 'submit by'
        ]
        
        self.urgency_keywords = [
            'urgent', 'asap', 'immediately', 'soon', 'quickly', 'today', 
            'tomorrow', 'this week', 'don\'t forget', 'reminder'
        ]
        
        # Date patterns
        self.date_patterns = [
            r'\b(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})\b',  # DD/MM/YYYY or MM/DD/YYYY
            r'\b(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{2,4})\b',  # DD Month YYYY
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2}),?\s+(\d{2,4})\b',  # Month DD, YYYY
            r'\b(today|tomorrow|yesterday)\b',  # Relative dates
            r'\b(\d{1,2})(st|nd|rd|th)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\b',  # 1st January
        ]
        
        # Time patterns
        self.time_patterns = [
            r'\b(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)\b',  # 10:30 AM
            r'\b(\d{1,2})\s*(AM|PM|am|pm)\b',  # 10 AM
            r'\b(\d{1,2}):(\d{2})\b',  # 24-hour format
        ]
        
        # URL pattern
        self.url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        self.simple_url_pattern = r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b'
    
    def extract_event_info(self, message_text):
        """
        Extract event information from message text
        Returns a dictionary with extracted information
        """
        result = {
            'title': '',
            'date': None,
            'time': None,
            'description': message_text,
            'links': [],
            'event_type': 'general',
            'urgency': 'normal',
            'keywords': []
        }
        
        message_lower = message_text.lower()
        
        # Extract URLs
        urls = re.findall(self.url_pattern, message_text)
        simple_urls = re.findall(self.simple_url_pattern, message_text)
        result['links'] = list(set(urls + simple_urls))
        
        # Determine event type
        if any(keyword in message_lower for keyword in self.job_keywords):
            result['event_type'] = 'job'
            result['keywords'].extend([kw for kw in self.job_keywords if kw in message_lower])
        
        # Check urgency
        if any(keyword in message_lower for keyword in self.urgency_keywords):
            result['urgency'] = 'high'
            result['keywords'].extend([kw for kw in self.urgency_keywords if kw in message_lower])
        
        # Extract dates
        dates = self.extract_dates(message_text)
        if dates:
            result['date'] = dates[0]  # Take the first date found
        
        # Extract times
        times = self.extract_times(message_text)
        if times:
            result['time'] = times[0]  # Take the first time found
        
        # Generate title
        result['title'] = self.generate_title(message_text, result['event_type'])
        
        return result
    
    def extract_dates(self, text):
        """Extract dates from text"""
        dates = []
        
        # Try different date patterns
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    date_str = match.group(0)
                    
                    # Handle relative dates
                    if date_str.lower() == 'today':
                        dates.append(datetime.now().date())
                    elif date_str.lower() == 'tomorrow':
                        dates.append((datetime.now() + timedelta(days=1)).date())
                    elif date_str.lower() == 'yesterday':
                        dates.append((datetime.now() - timedelta(days=1)).date())
                    else:
                        # Try to parse the date
                        parsed_date = date_parser.parse(date_str, fuzzy=True)
                        dates.append(parsed_date.date())
                except:
                    continue
        
        # spaCy not available, using basic regex patterns only
        
        return list(set(dates))  # Remove duplicates
    
    def extract_times(self, text):
        """Extract times from text"""
        times = []
        
        for pattern in self.time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    time_str = match.group(0)
                    parsed_time = date_parser.parse(time_str, fuzzy=True)
                    times.append(parsed_time.time())
                except:
                    continue
        
        return times
    
    def generate_title(self, text, event_type):
        """Generate a title for the event based on the message content"""
        sentences = sent_tokenize(text)
        first_sentence = sentences[0] if sentences else text
        
        # Truncate if too long
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:100] + "..."
        
        # Add prefix based on event type
        if event_type == 'job':
            if 'apply' in text.lower():
                return f"Apply: {first_sentence}"
            elif 'interview' in text.lower():
                return f"Interview: {first_sentence}"
            else:
                return f"Job Opportunity: {first_sentence}"
        else:
            return f"Reminder: {first_sentence}"
    
    def extract_company_name(self, text):
        """Extract company name from job-related messages"""
        # Common company patterns
        company_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is\s+)?(?:hiring|recruiting)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:job|interview|position)\b',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        # spaCy not available, using basic patterns only
        
        return None

# Example usage and testing
if __name__ == "__main__":
    parser = MessageParser()
    
    # Test messages
    test_messages = [
        "Infosys is hiring! Apply before July 30, 2025 at 5 PM. Link: infosys.com/jobs",
        "Hey, Cognizant is recruiting freshers! Apply before Aug 5 at 6 PM – use this link.",
        "You need to submit your resume by July 28th.",
        "Don't forget – Wipro interview at 10 AM on 1st August."
    ]
    
    for msg in test_messages:
        print(f"\nMessage: {msg}")
        result = parser.extract_event_info(msg)
        print(f"Extracted Info: {result}")