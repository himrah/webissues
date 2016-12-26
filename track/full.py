__author__ = 'rahul'
from django.contrib.auth.models import User
class fullname(User):
    def __str__(self):
        return User.get_full_name(self)
