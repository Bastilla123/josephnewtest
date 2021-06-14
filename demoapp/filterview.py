import logging
from django.http import QueryDict
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

logger = logging.getLogger('util_views')
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class FilterView(View):
    # these variables needs to be defined in child class
    sorting = None
    values = None
    object_class = None
    filter_class = None
    template_name = None

    @staticmethod
    def result_function(qs):
        raise NotImplementedError(
            'AjaxSearchView class requires .result_function() to be implemented'
        )

    @staticmethod
    def json_sort_helper(columns, sorting):
        order_list = []
        for column in columns:
            if column['name'] in sorting.keys():
                for item in sorting[column['name']]:
                    # reverse order
                    if '-' in item:
                        if column['direction'] == 'asc':
                            order_list.append(item)
                        else:
                            # remove '-'
                            order_list.append(item.replace('-', ''))

                    # normal order
                    else:
                        if column['direction'] == 'asc':
                            order_list.append(item)
                        else:
                            order_list.append("-{}".format(item))
        return order_list

    def get(self, request):
        return render(request, self.template_name, {'filter': self.filter_class()})
    
    def post(self, request):
        columns = []
        # could be sorting by multiple columns
        for i in range(len(self.sorting)):

            direction = request.POST.get("order[{}][dir]".format(i), None)
            if direction:
                column = int(request.POST.get("order[{}][column]".format(i), '0'))
                columns.append({'name': column, 'direction': direction})

        order_list = self.json_sort_helper(columns, self.sorting)

        draw = int(request.POST.get('draw', '0'))
        start = int(request.POST.get('start', '0'))
        length = int(request.POST.get('length', '0'))
        values = QueryDict(request.body.decode('utf-8').replace('%5B%5D', ''))
        print(values)

        f = (
            self.filter_class(values, queryset=self.object_class.objects.all())
                .qs.values(*self.values)
                .order_by(*order_list)
        )
        count = len(f)

        # -1 is the all option
        if length == -1:
            results = f
        else:
            results = f[start: length + start]

        r = {
            "draw": draw,
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": self.result_function(results),
        }
        print(r)
        return JsonResponse(r)
