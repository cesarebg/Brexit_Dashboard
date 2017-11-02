from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader, Context
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
import requests
import json


def growth(request):
    parsedData = []
    growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
    parsed_json = json.loads(growth_data.content)
    growthData = {}
    data_input = 'quarters'
    for data in parsed_json[data_input]:
            if data['date'][5:7] == 'Q1':
                data['date'] = (data['date'][0:4] + ' ' + 'Mar')
            elif data['date'][5:7] == 'Q2':
                data['date'] = (data['date'][0:4] + ' ' + 'Jun')
            elif data['date'][5:7] == 'Q3':
                data['date'] = (data['date'][0:4] + ' ' + 'Sep')
            elif data['date'][5:7] == 'Q4':
                data['date'] = (data['date'][0:4] + ' ' + 'Dec')
            growthData['date'] = data['date']
            growthData['value'] = data['value']
            parsedData.append(growthData.copy())
    return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsedData) })

# def growth(request):
#     growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
#     parsed_json = json.loads(growth_data.content)
#     return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsed_json['quarters'][60:]) })

def growth_data(request):
    parsedData = []
    if request.method == 'POST':
        growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
        parsed_json = json.loads(growth_data.content)
        services_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3e2/pgdp/data')
        services_json = json.loads(services_data.content)
        production_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/L3BG/pgdp/data')
        production_json = json.loads(production_data.content)
        construction_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3dw/pgdp/data')
        construction_json = json.loads(construction_data.content)
        manufacturing_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3bn/pgdp/data')
        manufacturing_json = json.loads(manufacturing_data.content)
        growthData = {}
        data_input = 'quarters'
        year_input = request.POST.get('years')
        year_input_int = int(year_input)

        for data_s in range(len(services_json[data_input])):
                parsed_json['quarters'][data_s+140]['services'] = services_json['quarters'][data_s]['value']
                parsed_json['quarters'][data_s+140]['alt-date'] = services_json['quarters'][data_s]['date']

        for data_p in range(len(production_json[data_input])):
                parsed_json['quarters'][data_p+140]['production'] = production_json['quarters'][data_p]['value']
                parsed_json['quarters'][data_p+140]['alt-date-p'] = production_json['quarters'][data_p]['date']

        for data_c in range(len(construction_json[data_input])):
                parsed_json['quarters'][data_c+140]['construction'] = construction_json['quarters'][data_c]['value']
                parsed_json['quarters'][data_c+140]['alt-date-c'] = construction_json['quarters'][data_c]['date']

        for data_m in range(len(manufacturing_json[data_input])):
                parsed_json['quarters'][data_m+140]['manufacturing'] = manufacturing_json['quarters'][data_m]['value']
                parsed_json['quarters'][data_m+140]['alt-date-m'] = manufacturing_json['quarters'][data_m]['date']

        for data in parsed_json[data_input][year_input_int:]:
                if data['date'][5:7] == 'Q1':
                    data['date'] = (data['date'][0:4] + ' ' + 'Mar')
                elif data['date'][5:7] == 'Q2':
                    data['date'] = (data['date'][0:4] + ' ' + 'Jun')
                elif data['date'][5:7] == 'Q3':
                    data['date'] = (data['date'][0:4] + ' ' + 'Sep')
                elif data['date'][5:7] == 'Q4':
                    data['date'] = (data['date'][0:4] + ' ' + 'Dec')
                growthData['date'] = data['date']
                growthData['value'] = data['value']
                growthData['services'] = data['services']
                growthData['alt-date'] = data['alt-date']
                growthData['production'] = data['production']
                growthData['alt-date-p'] = data['alt-date-p']
                growthData['construction'] = data['construction']
                growthData['alt-date-c'] = data['alt-date-c']
                growthData['manufacturing'] = data['manufacturing']
                growthData['alt-date-m'] = data['alt-date-m']
                parsedData.append(growthData.copy())
    return JsonResponse(parsedData, safe=False)

# def growth_data(request):
#     parsedData = []
#     if request.method == 'POST':
#         growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
#         parsed_json = json.loads(growth_data.content)
#         services_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3e2/pgdp/data')
#         services_json = json.loads(services_data.content)
#         production_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/L3BG/pgdp/data')
#         production_json = json.loads(production_data.content)
#         construction_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3dw/pgdp/data')
#         construction_json = json.loads(construction_data.content)
#         manufacturing_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3dw/pgdp/data')
#         manufacturing_json = json.loads(manufacturing_data.content)
#         growthData = {}
#         data_input = 'quarters'
#         year_input = request.POST.get('years')
#         year_input_int = int(year_input)
#
#         for data_s in range(len(services_json[data_input])):
#                 parsed_json['quarters'][data_s+140]['services'] = services_json['quarters'][data_s]['value']
#
#         for data_s in range(len(production_json[data_input])):
#                 parsed_json['quarters'][data_s+140]['production'] = production_json['quarters'][data_s]['value']
#
#         for data_s in range(len(construction_json[data_input])):
#                 parsed_json['quarters'][data_s+140]['construction'] = construction_json['quarters'][data_s]['value']
#
#         for data_s in range(len(manufacturing_json[data_input])):
#                 parsed_json['quarters'][data_s+140]['construction'] = manufacturing_json['quarters'][data_s]['value']
#
#         for data in parsed_json[data_input][year_input_int:]:
#                 if data['date'][5:7] == 'Q1':
#                     data['date'] = (data['date'][0:4] + ' ' + 'Mar')
#                 elif data['date'][5:7] == 'Q2':
#                     data['date'] = (data['date'][0:4] + ' ' + 'Jun')
#                 elif data['date'][5:7] == 'Q3':
#                     data['date'] = (data['date'][0:4] + ' ' + 'Sep')
#                 elif data['date'][5:7] == 'Q4':
#                     data['date'] = (data['date'][0:4] + ' ' + 'Dec')
#                 growthData['date'] = data['date']
#                 growthData['gdp'] = data['value']
#                 growthData['services'] = data['services']
#                 growthData['production'] = data['production']
#                 growthData['construction'] = data['construction']
#                 growthData['manufacturing'] = data['construction']
#                 parsedData.append(growthData.copy())
#     return JsonResponse(parsedData, safe=False)


# def growth_data(request):
#     parsedData = []
#     if request.method == 'POST':
#         growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
#         year_input = request.POST.get('years')
#         year_input_int = int(year_input)
#         parsed_json = json.loads(growth_data.content)
#         growthData = {}
#         data_input = 'years'
#         for data in parsed_json[data_input][year_input_int:]:
#             growthData['date'] = data['date']
#             growthData['value'] = data['value']
#             growthData['year'] = data['year']
#             parsedData.append(growthData.copy())
#     return JsonResponse(parsedData, safe=False)

# growth_index
def growth_index():
    growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
    parsed_json = json.loads(growth_data.content)
    json_growth = json.dumps(parsed_json['years'][60:])
    return json_growth
# 3
def inflation(request):
    inflation_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23/data')
    parsed_json = json.loads(inflation_data.content)
    return render(request, 'dashboard/inflation.html', { 'inflation_json': json.dumps(parsed_json['months'][80:]) })
# 4
def debt(request):
    debt_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/hf6x/pusf/data')
    parsed_json = json.loads(debt_data.content)
    return render(request, 'dashboard/debt.html', { 'debt_json': json.dumps(parsed_json['months']) })
#5
def trade(request):
    trade_data = trade.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23/data')
    parsed_json = json.loads(trade_data.content)
    return render(request, 'dashboard/trade.html', { 'trade_json': json.dumps(parsed_json['months'][80:]) })
# 1
def index(request):
    template = loader.get_template('dashboard/index.html')
    growth_indicator = growth_index()
    context = { 'growth_json': growth_indicator }
    return HttpResponse(template.render(context))


# Stack solution

# def growth(request):
#     template_name = "dashboard/growth.html"
#     parsedData = []
#     if request.method == 'POST':
#         year_input = request.POST.get('years')
#         year_input_int = int(year_input)
#         growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
#         parsed_json = json.loads(growth_data.content)
#         growthData = {}
#         data_input = 'years'
#         for data in parsed_json[data_input][year_input_int:]:
#             growthData['date'] = data['date']
#             growthData['value'] = data['value']
#             growthData['year'] = data['year']
#             parsedData.append(growthData.copy())
#         context = { 'growth_json': json.dumps(parsedData), 'success': False }
#         context.update({'success': True})
#         return render(request, template_name, context)
#     context = { 'growth_json': json.dumps(parsedData), 'success': False }
#     return render(request, template_name, context)

# def growth(request):
#     template_name = "dashboard/growth.html"
#     parsedData = []
#     context = { 'growth_json': json.dumps(parsedData), 'success': False }
#     if request.method == 'POST':
#         growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
#         year_input = request.POST.get('years')
#         year_input_int = int(year_input)
#         parsed_json = json.loads(growth_data.content)
#         growthData = {}
#         data_input = 'years'
#         context = { 'growth_json': json.dumps(parsedData), 'success': False }
#         for data in parsed_json[data_input][year_input_int:]:
#             growthData['date'] = data['date']
#             growthData['value'] = data['value']
#             growthData['year'] = data['year']
#             parsedData.append(growthData.copy())
#         context.update({'success': True})
#         return render(request, template_name, context)
#     context = { 'growth_json': json.dumps(parsedData), 'success': False }
#     return render(request, template_name, context)

# Data Solution

# def growth_data(request):
#     parsedData = []
#     if request.method == 'GET':
#         growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
#         year_input = request.GET.get('years')
#         year_input_int = int(year_input)
#         parsed_json = json.loads(growth_data.content)
#         growthData = {}
#         data_input = 'years'
#         for data in parsed_json[data_input][year_input_int:]:
#             growthData['date'] = data['date']
#             growthData['value'] = data['value']
#             growthData['year'] = data['year']
#             parsedData.append(growthData.copy())
#     return JsonResponse(parsedData, safe=False)
