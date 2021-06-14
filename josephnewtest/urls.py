"""filtermodal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from demoapp.filterviews import HistoriepropertyFilterView, HistorietypeFilterView, HistoriesubtypeFilterView, HistoriesourceFilterView
from demoapp.views import home, EditHistorie
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('historieproperty_link/', HistoriepropertyFilterView.as_view(), name='historieproperty_search'),
    path('historietypelink/', HistorietypeFilterView.as_view(), name='historietype_search'),
    path('historiesubtype_link/', HistoriesubtypeFilterView.as_view(), name='historiesubtype_search'),
    path('historiesource_link/', HistoriesourceFilterView.as_view(), name='historiesource_search'),
    path('form/add/', EditHistorie.as_view(), name='add'),
    path('form/edit/', EditHistorie.as_view(), name='edit'),
]
