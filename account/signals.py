from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from account.models import Profile
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def set_user_group(sender, instance, created, **kwargs):
    if created:
        user_group, _ = Group.objects.get_or_create(name="User")
        author_group, _ = Group.objects.get_or_create(name="Author")
        if user_group:
            instance.groups.add(user_group)
        if author_group:
            instance.groups.add(author_group)