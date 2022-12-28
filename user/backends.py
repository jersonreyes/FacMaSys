from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class CustomUserBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        try:
            user = User.objects.get(Q(username__exact=username) | Q(email__exact=username))
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            print(f'No user found with username/email: {username}')