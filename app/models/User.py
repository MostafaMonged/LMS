from app import db
from datetime import datetime
import uuid
import json

# User Model (Members and Librarians)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('Member', 'Librarian'), nullable=False)
    barcode = db.Column(db.String(10), unique=True, nullable=False)  # Unique barcode for member identification
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notifications = db.Column(db.Text, default='[]')  # Store notifications as a JSON string

    def add_notification(self, subject, body,book_title=None):
        """
        Add a notification to the user's notifications list.
        
        Arguments:
        - subject: The subject of the notification.
        - body: The body of the notification.
        """
        # Deserialize the existing notifications from JSON
        notifications = json.loads(self.notifications)
        
        # Add the new notification
        notifications.append({
            "subject": subject,
            "body": body,
            "book_title": book_title, #optional
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        })
        
        # Serialize the updated notifications back to JSON
        self.notifications = json.dumps(notifications)
        db.session.commit()

    def generate_barcode(self):
        # Generate a unique barcode for each user using UUID
        return str(uuid.uuid4())