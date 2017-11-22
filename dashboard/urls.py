from django.conf.urls import url

from . import views

app_name = 'dashboard'
urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^indicators/UK_economy/$', views.UK_economy, name='UK_economy'),

    url(r'^indicators/growth/$', views.growth, name='growth'),

    url(r'^data/growth/$', views.growth_data, name='growth_data'),

    url(r'^indicators/inflation/$', views.inflation, name='inflation'),

    url(r'^data/inflation/$', views.inflation_data, name='inflation_data'),

    url(r'^data/productivity/$', views.productivity, name='productivity'),

    url(r'^data/income/$', views.income, name='income'),

    url(r'^indicators/confidence/$', views.confidence, name='confidence'),

    url(r'^data/confidence/$', views.confidence_data, name='confidence_data'),

    url(r'^data/business/$', views.business_data, name='business_data'),

    url(r'^indicators/trade/$', views.trade, name='trade'),

    url(r'^data/imports/$', views.imports_data, name='imports_data'),

    url(r'^data/services/$', views.services_data, name='services_data'),

    url(r'^indicators/debt/$', views.debt, name='debt'),

    url(r'^data/debt/$', views.debt_data, name='debt_data'),

    url(r'^data/deficit/$', views.deficit_data, name='deficit_data'),

    ]
