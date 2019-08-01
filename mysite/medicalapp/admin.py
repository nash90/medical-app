from django.contrib import admin

# Register your models here.
from .models import DrugClass
from .models import DrugSubClass
from .models import Drug
from .models import DrugInformationType
from .models import DrugInformation
from .models import DrugQuizQuestion
from .models import DrugQuizOption
from .models import DrugKeyword

admin.site.register(DrugClass)
admin.site.register(DrugSubClass)
admin.site.register(Drug)
admin.site.register(DrugInformationType)
admin.site.register(DrugInformation)
admin.site.register(DrugQuizQuestion)
admin.site.register(DrugQuizOption)
admin.site.register(DrugKeyword)
