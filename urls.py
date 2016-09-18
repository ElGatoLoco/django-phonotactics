from django.conf.urls import url

from .views import CalculatorWizard

urlpatterns = [
    url(r'^$', CalculatorWizard.as_view(), name='calculator'),
]