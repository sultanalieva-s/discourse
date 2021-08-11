from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    url = f'http://localhost:8000/users/activate/{activation_code}'
    message = f'activation link: {url}'
    send_mail('Discourse account activation', message, 'saadatssu@gmail.com', [email, ],
              fail_silently=False )




