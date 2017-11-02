from django.conf.urls import url

from . import views

app_name = 'dashboard'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # first indicator
    url(r'^indicators/growth/$', views.growth, name='growth'),
    # data from first indicator
    url(r'^data/growth/$', views.growth_data, name='growth_data'),
    # second indicator
    url(r'^indicators/debt/$', views.debt, name='debt'),
    # third indicator
    url(r'^indicators/inflation/$', views.inflation, name='inflation'),
    # fourth indicator
    url(r'^indicators/trade/$', views.trade, name='trade'),
]
