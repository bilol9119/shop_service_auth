from django.contrib import admin
from .models import MicroServiceToken, OneTimeToken

admin.site.register(MicroServiceToken)
admin.site.register(OneTimeToken)
