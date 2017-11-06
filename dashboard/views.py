from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader, Context
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
import requests
import json


# def growth(request):
#     growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/pgdp/data')
#     parsed_json = json.loads(growth_data.content)
#     data_input = 'years'
#     return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsed_json[data_input])})


def growth(request):
    parsedData = []
    growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/pgdp/data')
    parsed_json = json.loads(growth_data.content)
    growthData = {}
    data_input = 'years'
    for data in parsed_json[data_input][56:]:
            growthData['date'] = data['date']
            growthData['value'] = data['value']
            parsedData.append(growthData.copy())
    return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsedData) })

# def growth(request):
#     parsedData = []
#     growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
#     parsed_json = json.loads(growth_data.content)
#     growthData = {}
#     data_input = 'quarters'
#     for data in parsed_json[data_input]:
#             if data['date'][5:7] == 'Q1':
#                 data['date'] = (data['date'][0:4] + ' ' + 'Mar')
#             elif data['date'][5:7] == 'Q2':
#                 data['date'] = (data['date'][0:4] + ' ' + 'Jun')
#             elif data['date'][5:7] == 'Q3':
#                 data['date'] = (data['date'][0:4] + ' ' + 'Sep')
#             elif data['date'][5:7] == 'Q4':
#                 data['date'] = (data['date'][0:4] + ' ' + 'Dec')
#             growthData['date'] = data['date']
#             growthData['value'] = data['value']
#             parsedData.append(growthData.copy())
#     return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsedData) })

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
# def growth_index():
#     growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyp/qna/data')
#     parsed_json = json.loads(growth_data.content)
#     json_growth = json.dumps(parsed_json['years'][60:])
#     return json_growth
# 3
def inflation(request):
    inflation_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23/data')
    parsed_json = json.loads(inflation_data.content)
    return render(request, 'dashboard/inflation.html', { 'inflation_json': json.dumps(parsed_json['months'][80:]) })

def inflation_data(request):
    parsedData = []
    if request.method == 'POST':
        cpih_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23/data')
        cpih_json = json.loads(cpih_data.content)
        food_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55p/mm23/data')
        food_json = json.loads(food_data.content)
        alcohol_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55q/mm23/data')
        alcohol_json = json.loads(alcohol_data.content)
        clothing_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55r/mm23/data')
        clothing_json = json.loads(clothing_data.content)
        housing_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55s/mm23/data')
        housing_json = json.loads(housing_data.content)
        furniture_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55t/mm23/data')
        furniture_json = json.loads(furniture_data.content)
        health_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55u/mm23/data')
        health_json = json.loads(health_data.content)
        transport_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55v/mm23/data')
        transport_json = json.loads(transport_data.content)
        communication_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55w/mm23/data')
        communication_json = json.loads(communication_data.content)
        recreation_data = requests.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55x/mm23/data')
        recreation_json = json.loads(recreation_data.content)
        growthData = {}
        data_input = 'months'
        date_input = request.POST.get('years')
        input_int = int(date_input)

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['cpih'] = cpih_json[data_input][data_s]['value']
                cpih_json[data_input][data_s]['alt-date'] = cpih_json[data_input][data_s]['date']

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['food'] = food_json[data_input][data_s]['value']
                cpih_json[data_input][data_s]['alt-date-s'] = food_json[data_input][data_s]['date']

        for data_p in range(len(alcohol_json[data_input])):
                cpih_json[data_input][data_p]['alcohol'] = alcohol_json[data_input][data_p]['value']
                cpih_json[data_input][data_p]['alt-date-p'] = alcohol_json[data_input][data_p]['date']

        for data_c in range(len(clothing_json[data_input])):
                cpih_json[data_input][data_c]['clothing'] = clothing_json[data_input][data_c]['value']
                cpih_json[data_input][data_c]['alt-date-c'] = clothing_json[data_input][data_c]['date']

        for data_m in range(len(housing_json[data_input])):
                cpih_json[data_input][data_m]['housing'] = housing_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = housing_json[data_input][data_m]['date']

        for data_m in range(len(furniture_json[data_input])):
                cpih_json[data_input][data_m]['furniture'] = furniture_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = furniture_json[data_input][data_m]['date']

        for data_m in range(len(health_json[data_input])):
                cpih_json[data_input][data_m]['health'] = health_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = health_json[data_input][data_m]['date']

        for data_m in range(len(transport_json[data_input])):
                cpih_json[data_input][data_m]['transport'] = transport_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = transport_json[data_input][data_m]['date']

        for data_m in range(len(communication_json[data_input])):
                cpih_json[data_input][data_m]['communication'] = communication_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = communication_json[data_input][data_m]['date']

        for data_m in range(len(recreation_json[data_input])):
                cpih_json[data_input][data_m]['recreation'] = recreation_json[data_input][data_m]['value']
                cpih_json[data_input][data_m]['alt-date-m'] = recreation_json[data_input][data_m]['date']

        for data in cpih_json[data_input][input_int:]:
                growthData['date'] = data['date']
                growthData['cpih'] = data['cpih']
                growthData['food'] = data['food']
                growthData['alcohol'] = data['alcohol']
                growthData['clothing'] = data['clothing']
                growthData['housing'] = data['housing']
                growthData['furniture'] = data['furniture']
                growthData['health'] = data['health']
                growthData['transport'] = data['transport']
                growthData['communication'] = data['communication']
                growthData['recreation'] = data['recreation']
                # growthData['alt-date'] = data['alt-date']
                # growthData['alt-date-m'] = data['alt-date-m']
                # growthData['alt-date-s'] = data['alt-date-s']
                # growthData['alt-date-p'] = data['alt-date-p']
                # growthData['alt-date-c'] = data['alt-date-c']
                parsedData.append(growthData.copy())
    return JsonResponse(parsedData, safe=False)

def productivity(request):
    parsedData = []
    if request.method == 'POST':
        productivity_datasets = {}
        productivity_data = requests.get('http://stats.oecd.org/SDMX-JSON/data/PDB_LV/GBR+EU28+G-7+OECD.T_GDPHRS.VPVOB/all?startTime=2008&endTime=2016&dimensionAtObservation=allDimensions')
        productivity_json = json.loads(productivity_data.content)
        productivity_dict = {}
        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "0":
                if data[0] == "0":
                    productivity_dict['date'] = "2008"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "1":
                if data[0] == "0":
                    productivity_dict['date'] = "2009"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "2":
                if data[0] == "0":
                    productivity_dict['date'] = "2010"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "3":
                if data[0] == "0":
                    productivity_dict['date'] = "2011"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "4":
                if data[0] == "0":
                    productivity_dict['date'] = "2012"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "5":
                if data[0] == "0":
                    productivity_dict['date'] = "2013"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "6":
                if data[0] == "0":
                    productivity_dict['date'] = "2014"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())

        for data in productivity_json['dataSets'][0]['observations']:
            if data[6] == "7":
                if data[0] == "0":
                    productivity_dict['date'] = "2015"
                    productivity_dict['UK'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "1":
                    productivity_dict['OECD'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "2":
                    productivity_dict['EU'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                elif data[0] == "3":
                    productivity_dict['G7'] = str(round(productivity_json['dataSets'][0]['observations'][data][0], 1))
                    parsedData.append(productivity_dict.copy())
    return JsonResponse(parsedData, safe=False)

#3
def debt(request):
    debt_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/hf6x/pusf/data')
    parsed_json = json.loads(debt_data.content)
    return render(request, 'dashboard/debt.html', { 'debt_json': json.dumps(parsed_json['months']) })
#4
def trade(request):
    trade_data = trade.get('https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/l55o/mm23/data')
    parsed_json = json.loads(trade_data.content)
    return render(request, 'dashboard/trade.html', { 'trade_json': json.dumps(parsed_json['months'][80:]) })
#1
def index(request):
    # template = loader.get_template('dashboard/index.html')
    # growth_indicator = growth_index()
    # context = { 'growth_json': growth_indicator }
    return render(request, 'dashboard/index.html')


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
