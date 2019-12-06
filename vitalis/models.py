from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MultiparametricReading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    # bpm
    heart_rate = models.IntegerField(blank=True, null=True)

    # SpO2 in %
    oxygen_saturation = models.DecimalField(
        decimal_places=2, max_digits=4, blank=True, null=True,
    )

    # Body temperature
    body_temperature = models.DecimalField(
        decimal_places=1, max_digits=3, blank=True, null=True,
    )

    def __str__(self):
        return (
            "{user} on {date} - "
            "HR: {hr:3d} bpm, SpO2: {spo2}%, Temp: {temp} ºC".format(
                user=self.user,
                date=self.created_date.strftime("%d/%m/%Y at %H:%M:%S"),
                hr=self.heart_rate,
                spo2=self.oxygen_saturation,
                temp=self.body_temperature,
            )
        )
