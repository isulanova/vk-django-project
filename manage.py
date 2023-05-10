from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_users = models.ManyToManyField(User, related_name='to_users')
    status_choices = [('0', 'Normal'),
                      ('1', 'Accepted'),
                      ('2', 'Rejected')]
    status = models.CharField(choices=status_choices, default='0', max_length=1)

    def accept(self):
        self.status = '1'
        self.save()
        self.to_users.friends.add(self.from_user)
        self.from_user.friends.add(self.to_users)
        self.save()

    def reject(self):
        self.status = '2'
        self.save()