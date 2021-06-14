from demoapp.models import *
from .filterview import FilterView
from . import forms, filters, models, helpers

class HistorietypeFilterView(FilterView):
    sorting = {0 : ['name'], 1: ['status'], 2: ['charfield'], 3: ['integerfield'], 4:['datetimefield'], 5: ['selectfield']}
    values = ('pk',)
    object_class = Estates
    filter_class = filters.HistorietypeFilter
    template_name = 'historie_filter.html'

    @staticmethod
    def result_function(qs):
        result = []

        for b in qs:
            object = models.Historietype.objects.get(pk=b['pk'])
            col = {"id":  object.pk,"name":  object.name,
                   "status": object.status, "charfield": object.charfield, "integerfield": object.integerfield, "datetimefield": object.datetimefield, "selectfield": object.selectfield.status}
            result.append(col)
        return result
		
class HistoriesubtypeFilterView(FilterView):
    sorting = {0 : ['name'], 1: ['status'], 2: ['charfield']}
    values = ('pk',)
    object_class = Estates
    filter_class = filters.HistoriesubtypeFilter
    template_name = 'historie_filter.html'

    @staticmethod
    def result_function(qs):
        result = []

        for b in qs:
            object = models.Historiesubtype.objects.get(pk=b['pk'])
            col = {"id":  object.pk,"name":  object.name,
                   "status": object.status, "charfield": object.charfield}
            result.append(col)
        return result
class HistoriesourceFilterView(FilterView):
    sorting = {0 : ['name'], 1: ['status'], 2: ['charfield'], 3: ['integerfield'], 4:['datetimefield'], 5: ['selectfield']}
    values = ('pk',)
    object_class = Estates
    filter_class = filters.HistoriesourceFilter
    template_name = 'historie_filter.html'

    @staticmethod
    def result_function(qs):
        result = []

        for b in qs:
            object = models.Historiesource.objects.get(pk=b['pk'])
            col = {"id":  object.pk,"name":  object.name,
                   "status": object.status, "charfield": object.charfield, "integerfield": object.integerfield, "datetimefield": object.datetimefield, "selectfield": object.selectfield.status}
            result.append(col)
        return result
class HistoriepropertyFilterView(FilterView):
    sorting = {0 : ['name'], 1: ['status'], 2: ['charfield']}
    values = ('pk',)
    object_class = Estates
    filter_class = filters.HistoriepropertyFilter
    template_name = 'historie_filter.html'

    @staticmethod
    def result_function(qs):
        result = []

        for b in qs:
            object = models.Historieproperty.objects.get(pk=b['pk'])
            col = {"id":  object.pk,"name":  object.name,
                   "status": object.status, "charfield": object.charfield }
            result.append(col)
        return result
