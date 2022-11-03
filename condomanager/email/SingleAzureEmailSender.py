from azure.communication.email import EmailContent, EmailAddress
from django.core.mail import EmailMessage
from condomanager.email import AzureCustomEmailBackend
from django.conf import settings
from django.core import mail


class SingleAzureEmailSender:
    subject = 'User create successfully'
    from_email = 'DoNotReply@8d2b0bcc-ae7f-4fb7-ac4e-df13bf2dd7f8.azurecomm.net'
    connection_string = settings.AZURE_COMM_SRV_CONN_STR

    def send_message(self, email_message):
        content = EmailContent(
            subject=self.subject,
            plain_text='this is the body',
            html='<html><h1>This is the body</h1></html>'
        )

        address = EmailAddress(email='donotreplay@condo-manager.com', display_name='Condo Manager Admin')

        

