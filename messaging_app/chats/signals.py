from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model

CustomUser = get_user_model() # Get the currently active user model

@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    """
    Signal receiver function to set user's status to online and update last_seen on login.
    """
    # Ensure the 'user' object is an instance of your CustomUser model
    if isinstance(user, CustomUser):
        user.update_is_online_status(True)

@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    """
    Signal receiver function to set user's status to offline on logout.
    """
    # Ensure the 'user' object is an instance of your CustomUser model
    if isinstance(user, CustomUser):
        user.update_is_online_status(False)
