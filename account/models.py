from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string

# Create your models here.


class UserManager(BaseUserManager):

    def _create(self, email, password, **extra):

        if not email:
            raise ValueError('Поле имэйл не может быть пустым')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra):

        # extra.setdefault('is_active', True)
        return self._create(email, password, **extra)
        
    def create_superuser(self, email, password, **extra):

        extra.setdefault('is_staff', True)
        extra.setdefault('is_active', True)
        return self._create(email, password, **extra)


class User(AbstractBaseUser):

    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    activation_code = models.CharField(max_length=20, blank=True)

    objects=UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    def has_perm(self,perm, obj=None):
        return self.is_staff
    
    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()
    
