from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from azure.communication.email import EmailClient
from django.conf import settings


class AzureCustomEmailBackend(BaseEmailBackend):

    connection_string = settings.AZURE_COMM_SRV_CONN_STR

    def send_messages(self, email_messages):
        if self.connection_string != '':
            client = EmailClient.from_connection_string(self.connection_string)
        for msg in email_messages:
            client.send(msg)



