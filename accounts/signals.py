from django.db.models.signals import post_save
from django.contrib.auth.models import Group, User
from .models import Customer


def customer_profile(sender, instance, created, *args, **kwargs):
    if created:
        group = Group.objects.get(name = 'customer') #query the group and add the user to that group
        instance.groups.add(group) # like we did user.groups.add earlier. Here user is the instance
        Customer.objects.create(user = instance, name = instance.username) # Added to the Customer

post_save.connect(customer_profile, sender = User)        
