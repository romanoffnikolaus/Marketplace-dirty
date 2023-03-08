from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code
from django.core.mail import send_mail
User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length = 4, required = True)
    password_confirm = serializers.CharField(min_length =4, required = True)
    name = serializers.CharField(required = True)
    last_name = serializers.CharField(required = True)


    def validate_email(self, email):

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с указанной почтой уже зарегистрирован')
        return email

    def validate(self, attr):

        password = attr.get('password')
        password2 = attr.pop('password_confirm')
        if password != password2:
            raise serializers.ValidationError('Введенные пароли не совпадают')
        return attr

    def create(self, validater_data):
        user = User.objects.create_user(**validater_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return data

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active=True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_emial(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, data):
        request = self.context.get('request')
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(
                username=email,
                password=password,
                request=request
            )
            if not user:
                raise serializers.ValidationError('Введены некорректные данные')
        else:
            raise serializers.ValidationError('Email и пароль обязательны к заполнению')
        data['user'] = user
        return data


class ChangePasswordSerializer(
    serializers.Serializer):
    old_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password_confirm = serializers.CharField(
        min_length=4, required=True
    )

    def validate_old_password(self, old_pass):
        request = self.context.get('request')
        user = request.user

        if not user.check_password(old_pass):
            raise serializers.ValidationError(
                'Введите корректный пароль'
            )
        return old_pass
    
    def validate(self,attrs): #в ATTRS хранятся данный прошедшие часть валидации
        old_pass = attrs.get('old_password')
        new_password1 = attrs.get('new_password')
        new_password2 = attrs.get('new_password_confirm')

        if new_password1!=new_password2:
            raise serializers.ValidationError('Введенные пароли не совпадают')
        
        if old_pass==new_password1:
            raise serializers.ValidationError('Введеный Вами пароль соответствует старому паролю. Измените пароль.')
        
        return attrs
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким паролем не зарегистрирован')
        return email
    
    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail('Восстановление пароля', f'Вам код восстановления {user.activation_code}', 'example@gmail.com', [user.email])
        

class RebuildForgottenPasswordSerializer(serializers.Serializer):
    
    code = serializers.CharField(required = True)
    email=serializers.EmailField(required=True)
    password = serializers.CharField(min_length = 4,required = True)
    password_confirm = serializers.CharField(min_length = 4,required = True)

    def validate(self, attrs):
        email= attrs.get('email')
        code = attrs.get('code')
        password = attrs.get('password')
        password2 = attrs.get('password_confirm')

        if not User.objects.filter(email=email, 
                                    activation_code=code).exists():
            raise serializers.ValidationError('Пользователь с таким кодом активации не найден')
        
        if password!=password2:
            raise serializers.ValidationError('Введенные пароли не совпадают')
        
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()
