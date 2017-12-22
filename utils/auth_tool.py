
# from django.conf import settings
from rbac import models
def my_auth(**kwargs):
    user = models.User.objects.filter(**kwargs).first()
    return user