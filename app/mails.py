from flask.ext.mail import Message
from flask import render_template
from app import mail
from decorators import async

@async
def send_async_email(msg):
    mail.send(msg)

def send_invite_email(email, addresseeName, senderName, senderEmail):
	msg = Message("You have been challenged by " + senderName + " to a texting contest!",
                  sender="MixedMessage challenges <" + senderEmail + ">",
                  recipients=[email])
	msg.html = render_template("createmail.html", 
							name=addresseeName, 
							challenger=senderName)
	send_async_email(msg)