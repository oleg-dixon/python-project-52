from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'