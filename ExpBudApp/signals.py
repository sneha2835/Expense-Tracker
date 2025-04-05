from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction
from django.core.cache import cache
import hashlib
import json

def generate_cache_key(user_id):
    key_string = json.dumps({
        "user_id": user_id,
        "start_date": "",
        "end_date": "",
        "category": ""
    }, sort_keys=True)
    return "user_analytics_" + hashlib.md5(key_string.encode()).hexdigest()

@receiver([post_save, post_delete], sender=Transaction)
def clear_user_analytics_cache(sender, instance, **kwargs):
    cache_key = generate_cache_key(instance.user.id)
    cache.delete(cache_key)