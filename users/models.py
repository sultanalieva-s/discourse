from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

# Create your models here.

# We override the manager class in order to user email instead of username during user registration
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra):
        if not email:
            raise ValueError('Email is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra):
        if not email:
            raise ValueError('Email is not provided')

        email = self.normalize_email(email)

        user = self.model(email=email)

        user.set_password(password)

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class OrganizationType(models.Model):
    slug = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(OrganizationType, on_delete=models.PROTECT, related_name='organizations')


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=255, blank=True)

    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)

    status = models.CharField(max_length=50)
    about = models.CharField(max_length=255)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True)
    avatar = models.ImageField(upload_to='users/images')

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        import hashlib
        string = self.email + str(self.id)
        encode = string.encode()
        activation_code = hashlib.md5(encode).hexdigest()
        self.activation_code = activation_code

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

