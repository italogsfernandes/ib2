import subprocess
from django.views.generic import ListView, TemplateView, View
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from vitalis.max30100 import MAX30100
from vitalis.tmp117 import TMP117
from ib2.settings import mx30, mx30_error

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


class GetTMPDataView(View):
    tmp117 = TMP117()

    def get(self, request, *args, **kwargs):
        temperature = 0
        connected = 1
        error_msg = ""
        try:
            temperature = self.tmp117.get_temperature()
        except Exception as e:  # NOQA
            connected = 0
            error_msg = str(e)
        data = {
            'temperature': temperature,
            'connected': connected,
            'error_msg': error_msg,
        }
        return JsonResponse(data)


class GetMAX30100DataView(View):
    def get(self, request, *args, **kwargs):
        bpm = 0
        spo2 = 0
        buffer_red = []
        buffer_ir = []
        connected_bpm = 1
        error_bpm = ""
        if mx30 is not None:
            try:
                # No need to read sensor beacause i'm using a interrupt to
                # automatic read the sensor
                # mx30.read_sensor()
                (bpm, spo2) = mx30.calculate_heart_rate_and_spo2(400)
                # (buffer_red, buffer_ir) = mx30.get_autoclean_buffers()
                (buffer_red, buffer_ir) = (
                    mx30.buffer_red[-100:], mx30.buffer_ir[-100:])
            except Exception as e:  # NOQA
                connected_bpm = 0
                error_bpm = str(e)
        else:
            # Caso não esteja conectado mostre dados FALSOS
            # connected_bpm = 0
            # error_bpm = mx30_error
            import numpy
            (bpm, spo2) = (
                int(numpy.random.normal(loc=70, scale=5, size=1)[0]),
                int(numpy.random.normal(loc=98, scale=0.5, size=1)[0]),
            )
            time_vector = numpy.linspace(0, 1, 100)
            buffer_ir = list(
                100 * numpy.sin(2*numpy.pi*1*time_vector) +
                55 * numpy.sin(2*numpy.pi*2*time_vector) + 100 +
                numpy.random.normal(loc=0, scale=5, size=100)
            )
            buffer_red = list(
                100 * numpy.sin(2*numpy.pi*1*time_vector) +
                50 * numpy.sin(2*numpy.pi*2*time_vector) + 130 +
                numpy.random.normal(loc=0, scale=5, size=100)
            )
            buffer_ir = [int(x) for x in buffer_ir]
            buffer_red = [int(x) for x in buffer_red]

        data = {
            'bpm': bpm,
            'spo2': spo2,
            'connected_bpm': connected_bpm,
            'error_bpm': error_bpm,
            'buffer_red': buffer_red,
            'buffer_ir': buffer_ir,
        }
        return JsonResponse(data)


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
            # max30100_teste = MAX30100()
            resposta_final = (
                resposta_final +
                "<h2> MAX30100: </h2>" +
                "<pre>" +
                str(mx30.get_registers()).replace(
                    ', ', ',\n '
                ).replace('}', '\n}') +
                "</pre>"
            )
        if "48" in resposta_i2cdetect:
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
