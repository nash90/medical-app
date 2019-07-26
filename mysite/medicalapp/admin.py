from django.contrib import admin

# Register your models here.
from .models import DrugClass
from .models import DrugSubClass

admin.site.register(DrugClass)
admin.site.register(DrugSubClass)