from azure.communication.email import EmailClient, EmailMessage, EmailContent, EmailAddress, EmailRecipients
from django.conf import settings


class SingleAzureEmailSender:
    subject = 'User create successfully'
    from_email = 'DoNotReply@8d2b0bcc-ae7f-4fb7-ac4e-df13bf2dd7f8.azurecomm.net'
    connection_string = settings.AZURE_COMM_SRV_CONN_STR

    def send_message(self, email_message):
        if self.connection_string != '':
            client = EmailClient.from_connection_string(conn_str=self.connection_string)
            content = EmailContent(
                subject=self.subject,
                plain_text='this is the body',
                html='<html><h1>This is the body</h1></html>'
            )

            address = EmailAddress(email='ronald.tucuman@outlook.com', display_name='RonTucumanTest01')

            message = EmailMessage(
                sender='DoNotReply@8d2b0bcc-ae7f-4fb7-ac4e-df13bf2dd7f8.azurecomm.net',
                content=content,
                recipients=EmailRecipients(to=[address])
            )

            response = client.send(message)
