from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BusinessElement(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    can_read = models.BooleanField(default=False)
    can_read_all = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_update_all = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_delete_all = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')

    def __str__(self):
        return f"{self.role.name} -> {self.element.name}"