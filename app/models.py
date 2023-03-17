from django.db import models
import secrets

MAX_REQUEST_COUNT = 100

class Account(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    request_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def __repr__(self):
        return self.username
    
    def regenerate_api_key(self):
        self.api_key = generate_api_key()
        self.save()
        return self.api_key
    
    def increase_request_count(self):
        self.request_count += 1
        self.save()
        return self.request_count
    
    def get_request_count(self):
        return self.request_count
    
    def get_api_key(self):
        return self.api_key
    
    def get_account(self):
        return self


def generate_api_key():
    return secrets.token_urlsafe(16)