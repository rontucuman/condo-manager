from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from azure.communication.email import EmailClient
from django.conf import settings


class AzureCustomEmailBackend(BaseEmailBackend):

    connection_string = settings.EMAIL_BACKEND
    print('ron ' + connection_string)
    client = EmailClient.from_connection_string(connection_string)

    def send_messages(self, email_messages):
        for msg in email_messages:
            msg.send()


