import json
import os
from datetime import datetime


class Message:
    FILE_PATH = "data/messages.json"

    def __init__(
        self,
        message_id,
        sender_id,
        recipient_id,
        content,
        is_announcement=False
    ):
        self.message_id = str(message_id)
        self.sender_id = str(sender_id)
        self.recipient_id = str(recipient_id)
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.read = False
        self.is_announcement = is_announcement

    def validate(self):    
       if not self.sender_id:
            raise ValueError("Sender ID is required.")

        if not self.recipient_id:
            raise ValueError("Recipient ID is required.")

        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty.")

        return True

    def save(self):
        
        self.validate()

        # Create data directory if it does not exist
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)

        # Create an empty JSON file if it does not exist
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump({}, f, indent=4)

        # Load existing messages
        with open(self.FILE_PATH, "r") as f:
            data = json.load(f)

        # Store the new message
        data[self.message_id] = {
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "content": self.content,
            "timestamp": self.timestamp,
            "read": self.read,
            "is_announcement": self.is_announcement
        }

        # Rewrite JSON file safely
        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, message_id):
        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        message_id = str(message_id)

        if message_id not in data:
            return None

        message_data = data[message_id]

        message = cls(
            message_id=message_id,
            sender_id=message_data["sender_id"],
            recipient_id=message_data["recipient_id"],
            content=message_data["content"],
            is_announcement=message_data.get("is_announcement", False)
        )

        message.timestamp = message_data["timestamp"]
        message.read = message_data.get("read", False)

        return message

    @classmethod
    def get_conversation(cls, user1_id, user2_id):

        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        user1_id = str(user1_id)
        user2_id = str(user2_id)

        conversation = []

        for message_id, message_data in data.items():

            sender = str(message_data["sender_id"])
            recipient = str(message_data["recipient_id"])

            if (
                (sender == user1_id and recipient == user2_id)
                or
                (sender == user2_id and recipient == user1_id)
            ):
                message = cls(
                    message_id=message_id,
                    sender_id=sender,
                    recipient_id=recipient,
                    content=message_data["content"],
                    is_announcement=message_data.get(
                        "is_announcement", False
                    )
                )

                message.timestamp = message_data["timestamp"]
                message.read = message_data.get("read", False)

                conversation.append(message)

        # Oldest messages first
        conversation.sort(key=lambda message: message.timestamp)

        return conversation

    @classmethod
    def get_inbox(cls, user_id):
        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        user_id = str(user_id)

        inbox = []

        for message_id, message_data in data.items():

            if str(message_data["recipient_id"]) == user_id:

                message = cls(
                    message_id=message_id,
                    sender_id=message_data["sender_id"],
                    recipient_id=message_data["recipient_id"],
                    content=message_data["content"],
                    is_announcement=message_data.get(
                        "is_announcement", False
                    )
                )

                message.timestamp = message_data["timestamp"]
                message.read = message_data.get("read", False)

                inbox.append(message)

        # Newest messages first
        inbox.sort(
            key=lambda message: message.timestamp,
            reverse=True
        )

        return inbox

    @classmethod
    def get_unread_messages(cls, user_id):
        """
        Return all unread messages belonging to a user.
        """

        messages = cls.get_inbox(user_id)

        return [
            message
            for message in messages
            if not message.read
        ]

    def mark_as_read(self):
        """
        Mark this message as read in messages.json.
        """

        with open(self.FILE_PATH, "r") as f:
            data = json.load(f)

        if self.message_id not in data:
            raise ValueError("Message does not exist.")

        data[self.message_id]["read"] = True

        self.read = True

        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def search_by_user(cls, user_id):
        """
        Find messages sent by or received by a specific user.
        """

        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        user_id = str(user_id)

        results = []

        for message_id, message_data in data.items():

            sender = str(message_data["sender_id"])
            recipient = str(message_data["recipient_id"])

            if sender == user_id or recipient == user_id:

                message = cls(
                    message_id=message_id,
                    sender_id=sender,
                    recipient_id=recipient,
                    content=message_data["content"],
                    is_announcement=message_data.get(
                        "is_announcement", False
                    )
                )

                message.timestamp = message_data["timestamp"]
                message.read = message_data.get("read", False)

                results.append(message)

        results.sort(
            key=lambda message: message.timestamp,
            reverse=True
        )

        return results

    @classmethod
    def search_by_date(cls, date):
        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        results = []

        for message_id, message_data in data.items():

            timestamp = message_data["timestamp"]

            if timestamp.startswith(date):

                message = cls(
                    message_id=message_id,
                    sender_id=message_data["sender_id"],
                    recipient_id=message_data["recipient_id"],
                    content=message_data["content"],
                    is_announcement=message_data.get(
                        "is_announcement", False
                    )
                )

                message.timestamp = timestamp
                message.read = message_data.get("read", False)

                results.append(message)

        results.sort(
            key=lambda message: message.timestamp,
            reverse=True
        )

        return results

    def __repr__(self):
        return (
            f"Message("
            f"id={self.message_id}, "
            f"sender={self.sender_id}, "
            f"recipient={self.recipient_id}, "
            f"read={self.read}"
            f")"
        )
