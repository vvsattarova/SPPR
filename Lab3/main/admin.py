from django.contrib import admin
from .models import Task
from .models import Prediction

admin.site.register(Task)
admin.site.register(Prediction)