from django.core.mail import EmailMessage
import os

'''
This Script is used without any email template format.
'''

# class Util:
#     @staticmethod
#     def sendEmail(data):
#         email = EmailMessage(
#             subject= data['subject'],
#             body = data['body'],
#             from_email=os.environ.get('EMAIL_FROM'),
#             to = [data['to_email']],
#         )
#         email.send()


'''
This Code is used for Send EMail with template.
 
'''


from django.template.loader import render_to_string


class Util:
    @staticmethod
    def sendEmail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],  # This will contain the rendered HTML
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']],
        )
        email.content_subtype = "html"  # Set the email content to HTML
        email.send()
