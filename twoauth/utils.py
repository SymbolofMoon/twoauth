import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACffc6b2f2eaf362348570dfbc9c934e5c'
auth_token = 'a530363e3071ba65cc7acfd12eb6111c'
client = Client(account_sid, auth_token)


def send_sms(user_code):
    message = client.messages.create(
                                body=f'Hi there! The OTP is {user_code}',
                                from_='+12018977234',
                                to='+919116880783'
                            )

    print(message.sid)