from azure.communication.email import EmailClient, EmailMessage, EmailContent, EmailAddress, EmailRecipients
from azure.communication.email import EmailAttachment, EmailAttachmentType
from django.conf import settings
from django.core.mail import send_mail

import base64


class SingleAzureEmailSender:
    email_sender = settings.REGISTERED_EMAIL_SENDER
    connection_string = settings.AZURE_COMM_SRV_CONN_STR

    def send_message(self, subject, content_plain, content_html, mail_to):
        if self.connection_string == '':
            send_mail(
                subject=subject,
                message=content_plain,
                from_email=self.email_sender,
                recipient_list=[mail_to])
        else:
            client = EmailClient.from_connection_string(conn_str=self.connection_string)
            content = EmailContent(
                subject=subject,
                plain_text=content_plain,
                html=content_html
            )

            address = EmailAddress(email=mail_to)

            message = EmailMessage(
                sender=self.email_sender,
                content=content,
                recipients=EmailRecipients(to=[address])
            )

            client.send(message)

    def send_message_attachment(self, subject, content_plain, content_html, mail_to, filepath):
        if self.connection_string == '':
            send_mail(
                subject=subject,
                message=content_plain,
                from_email=self.email_sender,
                recipient_list=[mail_to])
        else:
            client = EmailClient.from_connection_string(conn_str=self.connection_string)
            content = EmailContent(
                subject=subject,
                plain_text=content_plain,
                html=content_html
            )

            address = EmailAddress(email=mail_to)

            with open(filepath, 'r') as file:
                file_contents = file.read()
            print('archivo pdf abierto')
            file_bytes_64 = base64.b64encode(bytes(file_contents, 'utf-8'))
            print('convertido a base 64')
            print(file_bytes_64)
            attachment = EmailAttachment(
                name='receipt.pdf',
                attachment_type=EmailAttachmentType.PDF,
                content_bytes_base64=file_bytes_64)
            print('objeto attachment creado')
            message = EmailMessage(
                sender=self.email_sender,
                content=content,
                recipients=EmailRecipients(to=[address]),
                attachments=[attachment]
            )
            print('objeto message creado')
            client.send(message)
            print('email enviado')
