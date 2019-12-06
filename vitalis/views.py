from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import MultiparametricReading


def get_multiparametric_reading_dict():
    import random
    heart_rate = random.randint(35, 220)
    oxygen_saturation = random.uniform(80, 99)
    # https://en.wikipedia.org/wiki/Human_body_temperature#Temperature_variation
    body_temperature = random.uniform(24, 45)
    return {
        'heart_rate': heart_rate,
        'oxygen_saturation': oxygen_saturation,
        'body_temperature': body_temperature,
    }


def index(request):
    context = {
        'information': 'tudo bom?',
    }
    return render(request, 'vitalis/index.html', context)


class MyReadingsListView(ListView):
    template_name = 'vitalis/my-readings.html'
    model = MultiparametricReading
    ordering = '-created_date'
    paginate_by = 50

    def get_queryset(self):
        qs = super(MyReadingsListView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def post(self, request, *args, **kwargs):
        data_dict = get_multiparametric_reading_dict()
        data_dict['user'] = request.user
        new_reading = MultiparametricReading(**data_dict)
        new_reading.save()
        r = super(MyReadingsListView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            return self.post_ajax(request, *args, **kwargs)
        return r

    def post_ajax(self, request, *args, **kwargs):
        readings_list_content = render_to_string(
            'vitalis/_readings_list.html',
            context=context,
            request=request,
        )
        m = render_to_string('vitalis/_messages.html', request=request)
        return JsonResponse({
         'readings_list_div': readings_list_content,
         'messages': m
        })


class AboutView(TemplateView):
    template_name = "vitalis/about.html"

class LoginView(TemplateView):
    template_name = "vitalis/login.html"

class LogoutView(TemplateView):
    template_name = "vitalis/logout.html"

class SingUpView(TemplateView):
    template_name = "vitalis/sing-up.html"
