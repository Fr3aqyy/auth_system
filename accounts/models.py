from django.db import models
import bcrypt

class User(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.ForeignKey('access_control.Role', on_delete=models.SET_NULL, null=True)

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))