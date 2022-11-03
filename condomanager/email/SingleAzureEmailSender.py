from django.core.mail import EmailMessage
from condomanager.email import AzureCustomEmailBackend
from django.core import mail


class SingleAzureEmailSender:
    subject = 'User create successfully'
    from_email = 'DoNotReply@8d2b0bcc-ae7f-4fb7-ac4e-df13bf2dd7f8.azurecomm.net'
    connection = mail.get_connection()

    def send_message(self, email_message):
        mail.EmailMessage(self.subject, email_message, self.from_email, 'ronald.tucuman@outlook.com',
                          connection=self.connection).send()

