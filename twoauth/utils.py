import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = '#Update from Twilio account'
auth_token = '#Update from Twilio account'
client = Client(account_sid, auth_token)


def send_sms(user_code):
    message = client.messages.create(
                                body=f'Hi there! The OTP is {user_code}',
                                from_='+12018977234',
                                to='+919116880783'
                            )

    print(message.sid)
