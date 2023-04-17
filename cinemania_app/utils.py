from django.conf import settings
from django.core.mail import send_mail 

def send_verification_email(email, token):
    try:
        subject = 'welcome to Cinemania'
        message = f'''
        Hi {email}, thank you for registering in Cinemania
        click this link to verfiy your account 👇🏼
        http://127.0.0.1:8000/verfiy_email/{token}/'''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail( subject, message, email_from, recipient_list )
    except Exception as e:
        print(e)
        return False 
    
    return True