import os
from twilio.rest import Client
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
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


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))


token_generator=AppTokenGenerator()        

