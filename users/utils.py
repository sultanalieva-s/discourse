from django.core.mail import send_mail


def send_activation_code(email, activation_code, status):
    if status == 'register':
        url = f'http://localhost:8000/users/activate/{activation_code}'
        message = f'activation link: {url}'
        send_mail('Discourse account activation', message, 'saadatssu@gmail.com', [email, ],
                  fail_silently=False )

    elif status == 'reset_password':
        send_mail(
            'Reset Your password',
            f'Код активации: {activation_code}',
            'stackoverflow_admin@gmail.com',
            [email, ],
            fail_silently=False
        )

