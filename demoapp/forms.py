from .widgets import selectfilterwidget, multiselectfilterwidget
from django import forms
from .models import *
#from .filterviews import HistoriepropertyFilterView, HistoriesubtypeFilterView, HistorietypeFilterView, HistoriesourceFilterView
#Demoform for normal Selectfield. User can click on this selectfield and then a modal is open. In models.py in address_link the related table is address so now
# ajax loads adress table but shows only the columns fields=['properties_link','country','birthdate','change_date','letter_salutation','status'] in this order
# and shows ist as a listview. In Modal Pagination 25 per site is shown in bottom right corner. filter=['country','birthdate','properties_link','status'] shows
# in modal on left side a box with a filter form where country,birthdate,properties_link and status is shown.
#Attention this here is a example. I want that the widget with name selectfilterwidget works for all foreignkey relations which i create in future.

class Estatesform(forms.ModelForm):
    class Meta:
        model = Estates
        fields = ('name','datetimefield','estateowner','address_link' )
        widgets = {
            'name': forms.TextInput,
            'datetimefield':forms.DateTimeInput,
            'estateowner': selectfilterwidget(fields=['username',],filter=['username']),
            'address_link':multiselectfilterwidget(fields=['birthdate','country','user_link','properties_link'],filter=['birthdate','country','user_link','properties_link']),

        }