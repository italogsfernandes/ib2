import subprocess
from django.views.generic import ListView, TemplateView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        context = self.get_context_data()
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


def sensores_conectados_extra_view(request):
    try:
        result = subprocess.run(
            ['i2cdetect', '-y', '1'],
            stdout=subprocess.PIPE
        )
        resposta_i2cdetect = str(result.stdout.decode('utf-8'))
        resposta_final = (
            "<h1> Teste Sensores </h1>" +
            "<p> Endereços I2C:" +
            "<ul><li>TMP117: 0x48</li><li>MAX30100: 0x57</li></ul>" +
            "</p>" +
            "<h2> I2C Scanner: </h2>" +
            "<pre>\n" + resposta_i2cdetect + "\n</pre>"
        )
        if "57" in resposta_i2cdetect:
            from vitalis.max30100 import MAX30100
            max30100_teste = MAX30100()
            resposta_final = (
                resposta_final +
                "<h2> MAX30100: </h2>" +
                "<pre>" +
                str(max30100_teste.get_registers()).replace(
                    ', ', ',\n '
                ).replace('}', '\n}') +
                "</pre>"
            )
        if "48" in resposta_i2cdetect:
            from vitalis.tmp117 import TMP117
            tmp117_teste = TMP117()
            resposta_final = (
                resposta_final +
                "<h2> TMP117: </h2>" +
                "<h3>Registers</h3>" +
                "<pre>" +
                str(tmp117_teste.get_registers_as_hex()).replace(
                    ', ', ',\n '
                ).replace('}', '\n}') +
                "</pre>" +
                "<h3>Configuration Register</h3>" +
                "<pre>" +
                str(tmp117_teste.get_configuration_dict()).replace(
                    ', ', ',\n '
                ).replace('}', '\n}') +
                "</pre>" +
                "<ul>" +
                "<li>Data Ready: " +
                str(tmp117_teste.get_configuration_dict()["Data_Ready"] == 1) +
                "</li>" +
                "<li><strong>Temperatura: " +
                str(tmp117_teste.get_temperature()) +
                " ºC </strong></li>" +
                "<li style='display: none;'>High Limit: " +
                str(tmp117_teste.get_high_limit()) +
                " ºC </li>" +
                "<li style='display: none;'>Low Limit: " +
                str(tmp117_teste.get_low_limit()) +
                " ºC </li>" +
                "<li>Temperature Offset: " +
                str(tmp117_teste.get_temperature_offset()) +
                " ºC </li>" +
                "<li>Revision: " +
                str(tmp117_teste.get_device_id_dict()["Rev[3:0]_HEX"]) +
                "</li>" +
                "<li>Device ID: " +
                str(tmp117_teste.get_device_id_dict()["DID[11:0]_HEX"]) +
                "</li>" +
                "</ul>"
            )

    except FileNotFoundError:
        resposta_final = "Error in cmd: i2cdetect -y 1"
    return HttpResponse(resposta_final)
