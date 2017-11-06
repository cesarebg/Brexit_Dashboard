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
    url(r'^indicators/inflation/$', views.inflation, name='inflation'),
    # data from second indicator
    url(r'^data/inflation/$', views.inflation_data, name='inflation_data'),

    url(r'^data/productivity/$', views.productivity, name='productivity'),

    url(r'^data/income/$', views.income, name='income'),
    # third indicator
    url(r'^indicators/trade/$', views.trade, name='trade'),
    # fourth indicator
    url(r'^indicators/debt/$', views.debt, name='debt'),
    ]
