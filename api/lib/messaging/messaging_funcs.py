from api import models, db
from datetime import datetime

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
            "TIMESTAMP": message.time_sent         # I'm returning this so I can try to implement timestamps in the UI side, but they won't be exactly right without some modification to account for timezones
        })

    return {"CONVERSATION": conversation}

def fetch_contacts(user_id):
    """
    Retrieve all users who have had a conversation with the given user.
    """
    # Find all users who sent messages to or received messages from the current user
    sent_to_user = db.session.query(models.Messaging.receiver_id).filter(
        models.Messaging.sender_id == user_id
    ).distinct()

    received_from_user = db.session.query(models.Messaging.sender_id).filter(
        models.Messaging.receiver_id == user_id
    ).distinct()

    # Combine results to find all unique contacts (use a set to avoid duplicates)
    contact_ids = set([row[0] for row in sent_to_user] + [row[0] for row in received_from_user])

    # Query user details for all contact IDs in the set
    contacts = db.session.query(models.LoginInformation, models.PersonalInformation).filter(
        models.LoginInformation.id.in_(contact_ids),
        models.LoginInformation.id == models.PersonalInformation.user_id
    ).all()

    # Construct response
    contact_list = []
    for login_info, personal_info in contacts:
        contact_list.append({
            "FIRSTNAME": personal_info.first_name,
            "LASTNAME": personal_info.last_name,
            "USERNAME": login_info.username
        })

    # We will return these values so that we can dynamically create users on the messaging screen.
    return {"CONTACTS": contact_list}
