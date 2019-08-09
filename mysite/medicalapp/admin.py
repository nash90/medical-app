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
from .models import DrugInformationKeyword

class CustomModelAdminMixin(object):

  def __init__(self, model, admin_site):
      self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
      super(CustomModelAdminMixin, self).__init__(model, admin_site)

class DrugClassAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_class_name',) 

class DrugSubClassAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_subclass_name',) 

class DrugAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_name',)  

class DrugInformationTypeAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_information_type',)   

class DrugInformationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug__drug_name','drug_info_type__drug_information_type','information',)   

class DrugQuizQuestionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('quiz_question',)   

class DrugQuizOptionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('quiz_option',)    

class DrugKeywordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_keyword',)  

class DrugInformationKeywordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_info__drug_name','keyword__drug_keyword')  

  
admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(DrugSubClass, DrugSubClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(DrugInformationType, DrugInformationTypeAdmin)
admin.site.register(DrugInformation, DrugInformationAdmin)
admin.site.register(DrugQuizQuestion, DrugQuizQuestionAdmin)
admin.site.register(DrugQuizOption, DrugQuizOptionAdmin)
admin.site.register(DrugKeyword, DrugKeywordAdmin)
admin.site.register(DrugInformationKeyword, DrugInformationKeywordAdmin)
