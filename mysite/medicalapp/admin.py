from django.contrib import admin
from django import forms
from django.contrib.auth import hashers
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from .models import MyUser
from .models import DrugClass
from .models import DrugSubClass
from .models import Drug
from .models import DrugInformationType
from .models import DrugInformation
from .models import DrugQuizQuestion
from .models import DrugQuizOption
from .models import DrugKeyword
from .models import DrugInformationKeyword
from .myuser import Profile
#from .models import GameBadge

class CustomModelAdminMixin(object):

  def __init__(self, model, admin_site):
      self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
      super(CustomModelAdminMixin, self).__init__(model, admin_site)

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_superuser', 'is_staff')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_superuser', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class MyUserClassAdmin(CustomModelAdminMixin, UserAdmin):
  model = MyUser
  form = UserChangeForm
  add_form = UserCreationForm
  list_display = ('email', 'password', 'is_superuser', 'is_staff', 'is_active')
  search_fields = ('email',) 

  fieldsets = (
      (None, {'fields': ('email', 'password', 'is_superuser', 'is_staff', 'is_active')}),
  )

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'password','is_superuser', 'is_staff')}
      ),
  )
  ordering = ('email',)

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
  search_fields = ('quiz_question', 'drug__drug_name', 'drug_info_type__drug_information_type')   

class DrugQuizOptionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('quiz_option','quiz__drug_quiz_id', 'quiz__quiz_question')    

class DrugKeywordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_keyword',)  

class DrugInformationKeywordAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('drug_info__drug_name','keyword__drug_keyword')  

class ProfileAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fields = ('user__email','date_of_birth')  

class PointsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fileds = ('user__email')

class BadgeAdmin(CustomModelAdminMixin, admin.ModelAdmin):
  search_fileds = ('name')

admin.site.register(MyUser, MyUserClassAdmin)  
admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(DrugSubClass, DrugSubClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(DrugInformationType, DrugInformationTypeAdmin)
admin.site.register(DrugInformation, DrugInformationAdmin)
admin.site.register(DrugQuizQuestion, DrugQuizQuestionAdmin)
admin.site.register(DrugQuizOption, DrugQuizOptionAdmin)
admin.site.register(DrugKeyword, DrugKeywordAdmin)
admin.site.register(DrugInformationKeyword, DrugInformationKeywordAdmin)
admin.site.register(Profile, ProfileAdmin)
#admin.site.register(GameBadge, BadgeAdmin)
