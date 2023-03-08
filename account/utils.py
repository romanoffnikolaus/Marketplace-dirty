"будет отвечать за то, что отправлять емэйл"

from django.core.mail import send_mail

def send_activation_code(email, activate_code):
    message = f'Подздравляем! Вы зарегестрировались на нашем сайте. Активируйте аккаунт. Ваш код активации {activate_code} для подтверждения аккаунта'

    send_mail(
        'Заголовок: Активация аккаунта',
        message,
        'test@gmail.com',
        [email]
    )