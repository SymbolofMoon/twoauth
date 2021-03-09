import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = '#Update from  twilio account'
auth_token = '#Update from  twilio account'
client = Client(account_sid, auth_token)


def send_sms(user_code,phone_number):
    message = client.messages.create(
                                body=f'Hi there! The OTP is {user_code}',
                                from_='+12018977234',
                                to=f'{phone_number}'
                            )

    print(message.sid)
