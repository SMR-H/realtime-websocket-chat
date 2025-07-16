from django.db import models
from django.contrib.auth import get_user_model
import shortuuid

# Get the custom User model
User = get_user_model()

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='groupchats', null=True, blank=True)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'

    class Meta:
        ordering = ['-created']