from api import models, db
from datetime import datetime
from api.lib.schedule.schedule_funcs import get_session_users

def send_message(user_id, message_info):
    """
    This function will send a message to the specified username
    {
        "USERNAME": str,
        "MESSAGE": str
    }
    """

    sender_id = user_id
    message = message_info["MESSAGE"]
    username = message_info["USERNAME"]

    recipient = models.LoginInformation.query.filter(models.LoginInformation.username == username).one_or_none()

    if recipient is not None:
        recipient_id = recipient.id
        new_message = models.Messaging(sender_id, recipient_id, message, datetime.utcnow())

        db.session.add(new_message)
        db.session.commit()

        return {"SUCCESS": True}
        
    return {"SUCCESS": False}

def get_all_messages(user_id):
    """
    This function will get all the messages sent to the current user
    """

    messages = models.Messaging.query.filter(models.Messaging.receiver_id == user_id).distinct().all()
    
    unique_senders = []
    for message in messages:
        if message.sender_id not in unique_senders:
            unique_senders.append(message.sender_id)
    


    inbox = []

    for sender_id in unique_senders:
        sender_login_info = models.LoginInformation.query.filter(models.LoginInformation.id == sender_id).one_or_none()
        sender_personal_info = models.PersonalInformation.query.filter(models.PersonalInformation.user_id == sender_id).one_or_none()
        
        sender_username = sender_login_info.username
        sender_first_name = sender_personal_info.first_name
        sender_last_name = sender_personal_info.last_name
        sender_full_name = f"{sender_first_name} {sender_last_name}"

        sender_messages = [received_message.message for received_message in messages if received_message.sender_id == sender_id]

        message_timestamps = [received_message.time_sent for received_message in messages if received_message.sender_id == sender_id]
        
        inbox.append({"USERNAME": sender_username, "FULL_NAME": sender_full_name, "MESSAGES": sender_messages, "TIMESTAMPS": message_timestamps})
        

    return {"INBOX": inbox}


def get_conversation(user_id, recipient_username):
    """
    Retrieve all messages between the current user and the recipient,
    including the sender's username and full name, ordered by time_sent.
    """
    # Get recipient's user ID from username
    recipient = models.LoginInformation.query.filter(
        models.LoginInformation.username == recipient_username
    ).one_or_none()

    if recipient is None:
        return {"error": "Recipient not found"}, 404 # Should never happen if we get this far, but just in case

    recipient_id = recipient.id

    # Query messages sent by current user to recipient
    sent_messages = models.Messaging.query.filter(
        models.Messaging.sender_id == user_id,
        models.Messaging.receiver_id == recipient_id
    ).all()

    # Query messages sent by recipient to current user
    received_messages = models.Messaging.query.filter(
        models.Messaging.sender_id == recipient_id,
        models.Messaging.receiver_id == user_id
    ).all()

    # Combine and sort by time_sent
    all_messages = sent_messages + received_messages
    all_messages.sort(key=lambda msg: msg.time_sent)

    # Construct response with sender details
    conversation = []
    for message in all_messages:
        sender = models.LoginInformation.query.filter(
            models.LoginInformation.id == message.sender_id
        ).one_or_none()

        sender_personal_info = models.PersonalInformation.query.filter(
            models.PersonalInformation.user_id == message.sender_id
        ).one_or_none()

        sender_username = sender.username if sender else "Unknown"
        sender_full_name = (
            f"{sender_personal_info.first_name} {sender_personal_info.last_name}"
            if sender_personal_info
            else "Unknown User"
        )

        conversation.append({
            "MESSAGE": message.message,
            "SENDER_USERNAME": sender_username,
            "SENDER_FULL_NAME": sender_full_name,
            "TIMESTAMP": message.time_sent.strftime("%Y-%m-%dT%H:%M:%SZ")
        })

    return {"CONVERSATION": conversation}

def fetch_contacts(user_id):
    """
    Retrieve all users who have had a conversation with the given user,
    Also include users whom the current user is matched with in the current session period.
    Prioritize matched users, and sort all users by the most recent message timestamp.

    So, it should look like this
    [matching period users sorted by most recent, including those that haven't been messaged]
    [...]
    [...]
    [historical users sorted by most recent]
    [...]
    [...]
    """
    # Fetch matched users
    matched_users = get_session_users(user_id)

    # Convert matched users to a dictionary for lookup
    matched_usernames = {user["USERNAME"]: user for user in matched_users}

    # Initialize matched users list with most recent message timestamps
    matched_with_messages = []
    for matched_user in matched_users:
        username = matched_user["USERNAME"]

        # Check for most recent message with this matched user
        recent_message = db.session.query(models.Messaging).filter(
            (models.Messaging.sender_id == user_id) & (models.Messaging.receiver_id == username) |
            (models.Messaging.sender_id == username) & (models.Messaging.receiver_id == user_id)
        ).order_by(models.Messaging.time_sent.desc()).first()

        if recent_message:
            # Add matched user with message history
            matched_with_messages.append({
                "FIRSTNAME": matched_user["FIRST_NAME"],
                "LASTNAME": matched_user["LAST_NAME"],
                "USERNAME": username,
                "LASTMESSAGE": recent_message.message,
                "TIMESTAMP": recent_message.time_sent.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
        else:
            # Add matched user with placeholder message
            matched_with_messages.append({
                "FIRSTNAME": matched_user["FIRST_NAME"],
                "LASTNAME": matched_user["LAST_NAME"],
                "USERNAME": username,
                "LASTMESSAGE": "SYSTEM: You have a match!", # Add a message notifying users of their new matches they haven't yet spoken to
                "TIMESTAMP": ""  # No timestamp for new matches (hopefully this doesn't break the android side)
            })

    # Sort matched users by timestamp (newest first)
    matched_with_messages.sort(
        key=lambda x: x["TIMESTAMP"] or "0000-00-00T00:00:00Z", reverse=True
    )

    # Fetch historical contacts
    sent_to_user = db.session.query(models.Messaging.receiver_id).filter(
        models.Messaging.sender_id == user_id
    ).distinct()

    received_from_user = db.session.query(models.Messaging.sender_id).filter(
        models.Messaging.receiver_id == user_id
    ).distinct()

    contact_ids = set([row[0] for row in sent_to_user] + [row[0] for row in received_from_user])

    # Filter out users already in matched list (since current matches you've already spoken to would appear in both)
    contact_ids -= set(matched_usernames.keys())

    historical_contacts = []
    for contact_id in contact_ids:
        # Get the most recent message with this contact
        recent_message = db.session.query(models.Messaging).filter(
            (models.Messaging.sender_id == user_id) & (models.Messaging.receiver_id == contact_id) |
            (models.Messaging.sender_id == contact_id) & (models.Messaging.receiver_id == user_id)
        ).order_by(models.Messaging.time_sent.desc()).first()

        if recent_message:
            contact_login_info = models.LoginInformation.query.filter_by(id=contact_id).one_or_none()
            contact_personal_info = models.PersonalInformation.query.filter_by(user_id=contact_id).one_or_none()

            if contact_login_info and contact_personal_info:
                historical_contacts.append({
                    "FIRSTNAME": contact_personal_info.first_name,
                    "LASTNAME": contact_personal_info.last_name,
                    "USERNAME": contact_login_info.username,
                    "LASTMESSAGE": recent_message.message,
                    "TIMESTAMP": recent_message.time_sent.strftime("%Y-%m-%dT%H:%M:%SZ")
                })

    # Sort historical contacts by timestamp (newest first)
    historical_contacts.sort(
        key=lambda x: x["TIMESTAMP"], reverse=True
    )

    # Combine matched users and historical contacts so that the current matches are first
    combined_contacts = matched_with_messages + historical_contacts

    return {"CONTACTS": combined_contacts}

# NEED TO CREATE AN ACCOUNT THAT IS MATCHED WITH SOME USERS, BUT ALSO HAS HISTORICAL CONVERSATIONS WITH OTHER USERS SO I CAN PROPERLY TEST THIS