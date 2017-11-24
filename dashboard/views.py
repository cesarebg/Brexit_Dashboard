from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import loader, Context
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse
from pyjstat import pyjstat
import requests
import json
import pandas as pd

###############################################

# DATA FUNCTIONS

# SECTIONS

# 1.- Index Page

# 2.- Automated Report

# 3.- GROWTH

# 4.- INFLATION, PRODUCTIVITY AND REAL INCOME

# 5.- CONFIDENCE AND INVESTMENT

# 6.- TRADE

# 7.- DEBT AND DEFICIT

###############################################

# 1.- Index Page

def index(request):
    return render(request, 'dashboard/index.html')

# 2.- Automated report

def UK_economy(request):
        # Growth Text
        parsedData = []
        growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
        growth_json = json.loads(growth_data.content)
        services_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3e2/pgdp/data')
        services_json = json.loads(services_data.content)
        production_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/L3BG/pgdp/data')
        production_json = json.loads(production_data.content)
        construction_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3dw/pgdp/data')
        construction_json = json.loads(construction_data.content)
        manufacturing_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3bn/pgdp/data')
        manufacturing_json = json.loads(manufacturing_data.content)
        growthData = {}
        textData = {}
        data_input = 'quarters'

        for data_s in range(len(services_json[data_input])):
                growth_json['quarters'][data_s+140]['services'] = services_json['quarters'][data_s]['value']

        for data_p in range(len(production_json[data_input])):
                growth_json['quarters'][data_p+140]['production'] = production_json['quarters'][data_p]['value']

        for data_c in range(len(construction_json[data_input])):
                growth_json['quarters'][data_c+140]['construction'] = construction_json['quarters'][data_c]['value']

        for data_m in range(len(manufacturing_json[data_input])):
                growth_json['quarters'][data_m+140]['manufacturing'] = manufacturing_json['quarters'][data_m]['value']

        for data in growth_json[data_input][241:]:
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
            growthData['production'] = data['production']
            growthData['construction'] = data['construction']
            growthData['manufacturing'] = data['manufacturing']
            parsedData.append(growthData.copy())

        last_value = pd.to_numeric(growth_json['quarters'][-1]['value'])
        last_services = pd.to_numeric(services_json['quarters'][-1]['value'])
        last_production = pd.to_numeric(production_json['quarters'][-1]['value'])
        last_construction = pd.to_numeric(construction_json['quarters'][-1]['value'])
        last_manufacturing = pd.to_numeric(manufacturing_json['quarters'][-1]['value'])


        if last_value > 0:
            trade_text = 'The UK economy reported a quarterly growth of ' + str(last_value) + '% in ' + str(growth_json['quarters'][-1]['date']) + ". "
        else:
            trade_text = 'The UK economy reported a quarterly slowdown of ' + str(last_value) + '% in ' + str(growth_json['quarters'][-1]['date']) + ". "

        # services

        if last_services > 0:
            services_text_1 = "Services grew " + str(last_services) + "% in " + str(services_json['quarters'][-1]['date']) + ", when compared with the previous quarter. "
        else:
            services_text_1 = "Services grew " + str(last_services) + "% in " + str(services_json['quarters'][-1]['date']) + ", when compared with the previous quarter. "
        services_text_3 = services_text_1

        # production

        if last_production > 0:
            production_text_1 = "Production expanded " + str(last_production) + "% in the same period. "
        else:
            production_text_1 = "Production contracted " + str(last_production) + "% in the same period. "
        production_text_3 = production_text_1

        # construction

        if last_construction > 0:
            construction_text_1 = "Construction spiked " + str(last_construction) + "%. "
        else:
            construction_text_1 = "Construction decreased " + str(last_construction) + "%. "
        construction_text_3 = construction_text_1

        if last_manufacturing > 0:
            manufacturing_text_1 = "Manufacturing increased " + str(last_manufacturing) + "%. "
        else:
            manufacturing_text_1 = "Manufacturing decreased " + str(last_manufacturing) + "%. "
        manufacturing_text_3 = manufacturing_text_1

        growth_text_final = trade_text + services_text_3 + production_text_3 + construction_text_3 + manufacturing_text_3

        # Inflation Text

        parsedData = []
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
        inflationData = {}
        textData = {}
        data_input = 'months'
        input_int = 126

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['cpih'] = cpih_json[data_input][data_s]['value']

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['food'] = food_json[data_input][data_s]['value']

        for data_p in range(len(alcohol_json[data_input])):
                cpih_json[data_input][data_p]['alcohol'] = alcohol_json[data_input][data_p]['value']

        for data_c in range(len(clothing_json[data_input])):
                cpih_json[data_input][data_c]['clothing'] = clothing_json[data_input][data_c]['value']

        for data_m in range(len(housing_json[data_input])):
                cpih_json[data_input][data_m]['housing'] = housing_json[data_input][data_m]['value']

        for data_m in range(len(furniture_json[data_input])):
                cpih_json[data_input][data_m]['furniture'] = furniture_json[data_input][data_m]['value']

        for data_m in range(len(health_json[data_input])):
                cpih_json[data_input][data_m]['health'] = health_json[data_input][data_m]['value']

        for data_m in range(len(transport_json[data_input])):
                cpih_json[data_input][data_m]['transport'] = transport_json[data_input][data_m]['value']

        for data_m in range(len(communication_json[data_input])):
                cpih_json[data_input][data_m]['communication'] = communication_json[data_input][data_m]['value']

        for data_m in range(len(recreation_json[data_input])):
                cpih_json[data_input][data_m]['recreation'] = recreation_json[data_input][data_m]['value']

        for data in cpih_json[data_input][input_int:]:
                inflationData['date'] = data['date']
                inflationData['cpih'] = data['cpih']
                inflationData['food'] = data['food']
                inflationData['alcohol'] = data['alcohol']
                inflationData['clothing'] = data['clothing']
                inflationData['housing'] = data['housing']
                inflationData['furniture'] = data['furniture']
                inflationData['health'] = data['health']
                inflationData['transport'] = data['transport']
                inflationData['communication'] = data['communication']
                inflationData['recreation'] = data['recreation']
                parsedData.append(inflationData.copy())

        last_cpih = pd.to_numeric(cpih_json['months'][-1]['value'])
        last_food = pd.to_numeric(food_json['months'][-1]['value'])
        last_alcohol = pd.to_numeric(alcohol_json['months'][-1]['value'])
        last_clothing = pd.to_numeric(clothing_json['months'][-1]['value'])
        last_housing = pd.to_numeric(housing_json['months'][-1]['value'])
        last_furniture = pd.to_numeric(furniture_json['months'][-1]['value'])
        last_health = pd.to_numeric(health_json['months'][-1]['value'])
        last_transport = pd.to_numeric(transport_json['months'][-1]['value'])
        last_communication = pd.to_numeric(communication_json['months'][-1]['value'])
        last_recreation = pd.to_numeric(recreation_json['months'][-1]['value'])


        if last_cpih > 0:
            trade_text = 'CPIH reported an annual increase of ' + str(last_cpih) + '% in ' + str(cpih_json['months'][-1]['date']) + ". "
        else:
            trade_text = 'CPIH reported an annual decrease of' + str(last_cpih) + '% in ' + str(cpih_json['months'][-1]['date']) + ". "

        # Food

        if last_food > 0:
            food_text_1 = "Food and non-alcoholic beverages increased " + str(last_food) + "% in " + str(food_json['months'][-1]['date']) + ", after a 12-month period. "
        else:
            food_text_1 = "Food and non-alcoholic beverages decreased " + str(last_food) + "% in " + str(food_json['months'][-1]['date']) + ", after a 12-month period. "
        food_text_3 = food_text_1

        # Alcohol

        if last_alcohol > 0:
            alcohol_text_1 = "The price of alcohol increased " + str(last_alcohol) + "% in the same period; "
        else:
            alcohol_text_1 = "The price of alcohol decreased " + str(last_alcohol) + "% in the same period; "
        alcohol_text_3 = alcohol_text_1

        # Clothing

        if last_clothing > 0:
            clothing_text_1 = "Clothing increased " + str(last_clothing) + "%; "
        else:
            clothing_text_1 = "Clothing decreased " + str(last_clothing) + "%; "
        clothing_text_3 = clothing_text_1

        # Housing

        if last_housing > 0:
            housing_text_1 = "Housing increased " + str(last_housing) + "%; "
        else:
            housing_text_1 = "Housing decreased " + str(last_housing) + "%; "
        housing_text_3 = housing_text_1

        # Furniture

        if last_furniture > 0:
            furniture_text_1 = "Furniture increased " + str(last_furniture) + "%; "
        else:
            furniture_text_1 = "Furniture decreased " + str(last_furniture) + "%; "
        furniture_text_3 = furniture_text_1

        # Health

        if last_health > 0:
            health_text_1 = "Health increased " + str(last_health) + "%; "
        else:
            health_text_1 = "Health decreased " + str(last_health) + "%; "
        health_text_3 = health_text_1

        # Transport

        if last_transport > 0:
            transport_text_1 = "Transport increased " + str(last_transport) + "%; "
        else:
            transport_text_1 = "Transport decreased " + str(last_transport) + "%; "
        transport_text_3 = transport_text_1

        # Communication

        if last_communication > 0:
            communication_text_1 = "Communication increased " + str(last_communication) + "%; "
        else:
            communication_text_1 = "Communication decreased " + str(last_communication) + "%; "
        communication_text_3 = communication_text_1

        # Recreation

        if last_recreation > 0:
            recreation_text_1 = "Recreation increased " + str(last_recreation) + "%. "
        else:
            recreation_text_1 = "Recreation decreased " + str(last_recreation) + "%. "
        recreation_text_3 = recreation_text_1


        inflation_text_final = trade_text + food_text_3 + alcohol_text_3 + clothing_text_3 + housing_text_3 + furniture_text_3 + health_text_3 + transport_text_3 + communication_text_3 + recreation_text_3

        # Confidence Text

        parsedData = []
        confidence_URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/teibs020?geo=DK&geo=FI&geo=LU&geo=NL&geo=SE&geo=UK&geo=IE&precision=1&indic=BS-CSMCI-BAL&s_adj=SA'
        dataset = pyjstat.Dataset.read(confidence_URL)
        df = dataset.write('dataframe')
        json_confidence = df.to_json(orient='records')
        json_confidence_final = json.loads(json_confidence)
        confidenceData = {}
        textData = {}
        for data in json_confidence_final:
            if data['time'][4:7] == 'M12':
                data['time'] = (data['time'][0:4] + ' ' + 'Dec')
            if data['time'][4:7] == 'M11':
                data['time'] = (data['time'][0:4] + ' ' + 'Nov')
            if data['time'][4:7] == 'M10':
                data['time'] = (data['time'][0:4] + ' ' + 'Oct')
            if data['time'][4:7] == 'M09':
                data['time'] = (data['time'][0:4] + ' ' + 'Sep')
            if data['time'][4:7] == 'M08':
                data['time'] = (data['time'][0:4] + ' ' + 'Aug')
            if data['time'][4:7] == 'M07':
                data['time'] = (data['time'][0:4] + ' ' + 'Jul')
            if data['time'][4:7] == 'M06':
                data['time'] = (data['time'][0:4] + ' ' + 'Jun')
            if data['time'][4:7] == 'M05':
                data['time'] = (data['time'][0:4] + ' ' + 'May')
            if data['time'][4:7] == 'M04':
                data['time'] = (data['time'][0:4] + ' ' + 'Apr')
            if data['time'][4:7] == 'M03':
                data['time'] = (data['time'][0:4] + ' ' + 'Mar')
            if data['time'][4:7] == 'M02':
                data['time'] = (data['time'][0:4] + ' ' + 'Feb')
            if data['time'][4:7] == 'M01':
                data['time'] = (data['time'][0:4] + ' ' + 'Jan')
            confidenceData['date'] = data['time']
            confidenceData['value'] = data['value']
            confidenceData['Country'] = data['geo']
            parsedData.append(confidenceData.copy())
        df = pd.DataFrame(parsedData).pivot('date','Country','value')
        sort = pd.to_datetime(df.index).sort_values().strftime('%Y %b')
        parsedDataFinal = df.reindex(sort).reset_index().to_dict('r')
        df = pd.DataFrame(data = parsedDataFinal)
        df['date'] = pd.to_datetime(df['date'])
        mean_Denmark = round(df['Denmark'].mean(), 1)
        mean_Finland = round(df['Finland'].mean(), 1)
        mean_Luxembourg = round(df['Luxembourg'].mean(), 1)
        mean_Netherlands = round(df['Netherlands'].mean(), 1)
        mean_Sweden = round(df['Sweden'].mean(), 1)
        mean_United_Kingdom = round(df['United Kingdom'].mean(), 1)
        less_list = []
        more_list = []
        if mean_United_Kingdom < mean_Denmark:
            less_list.append('Denmark')
        else:
            more_list.append('Denmark')
        if mean_United_Kingdom < mean_Finland:
            less_list.append('Finland')
        else:
            more_list.append('Finland')
        if mean_United_Kingdom < mean_Luxembourg:
            less_list.append('Luxembourg')
        else:
            more_list.append('Luxembourg')
        if mean_United_Kingdom < mean_Netherlands:
            less_list.append('Netherlands')
        else:
            more_list.append('Netherlands')
        if mean_United_Kingdom < mean_Sweden:
            less_list.append('Sweden')
        else:
            more_list.append('Sweden')
        less_list_text = ", ".join(less_list)
        more_list_text = ", ".join(more_list)
        if more_list == []:
            text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + less_list_text + " reported a superior consumer confidence in the same period."
        elif less_list == []:
            text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + more_list_text + " reported an inferior consumer confidence in the same period."
        else:
            text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + less_list_text + " reported an inferior consumer confidence in the same period. "
        text_mean_countries = ' Between ' + str(parsedDataFinal[0]['date']) + ' and ' + str(parsedDataFinal[-1]['date']) + ' Denmark had a consumer confidence index of ' + str(mean_Denmark) + '; Finland, ' + str(mean_Finland) + '; Luxembourg, ' + str(mean_Luxembourg) + '; Netherlands, ' + str(mean_Netherlands) + ' and Sweden, ' + str(mean_Sweden) + '. '

        confidence_text_final = text + text_mean_countries

        # Trade text

        parsedData = []
        balance_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret/data')
        balance_json = json.loads(balance_data.content)
        imports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbi/mret/data')
        imports_json = json.loads(imports_data.content)
        exports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbh/mret/data')
        exports_json = json.loads(exports_data.content)
        tradeData = {}
        textData = {}
        data_input = 'years'
        input_int = 63

        for data_s in range(len(imports_json[data_input])):
                balance_json[data_input][data_s]['balance'] = balance_json[data_input][data_s]['value']
                balance_json[data_input][data_s]['alt-date'] = balance_json[data_input][data_s]['date']

        for data_s in range(len(imports_json[data_input])):
                balance_json[data_input][data_s]['imports'] = imports_json[data_input][data_s]['value']
                balance_json[data_input][data_s]['alt-date-s'] = imports_json[data_input][data_s]['date']

        for data_p in range(len(exports_json[data_input])):
                balance_json[data_input][data_p]['exports'] = exports_json[data_input][data_p]['value']
                balance_json[data_input][data_p]['alt-date-p'] = exports_json[data_input][data_p]['date']

        for data in balance_json[data_input][input_int:]:
                tradeData['date'] = data['date']
                tradeData['balance'] = data['balance']
                tradeData['imports'] = data['imports']
                tradeData['exports'] = data['exports']
                parsedData.append(tradeData.copy())
        last_balance = pd.to_numeric(balance_json['years'][-1]['value'])
        last_imports = pd.to_numeric(imports_json['years'][-1]['value'])
        penu_imports = pd.to_numeric(imports_json['years'][-2]['value'])
        first_imports = pd.to_numeric(imports_json['years'][63]['value'])
        last_exports = pd.to_numeric(exports_json['years'][-1]['value'])
        penu_exports = pd.to_numeric(exports_json['years'][-2]['value'])
        first_exports = pd.to_numeric(exports_json['years'][63]['value'])
        df = pd.DataFrame(data=parsedData)
        df['date'] = pd.to_datetime(df['date'])
        df['balance'] = pd.to_numeric(df['balance'])
        df['imports'] = pd.to_numeric(df['imports'])
        df['exports'] = pd.to_numeric(df['exports'])
        balance_change = round(100*(df['balance'].iloc[-1]/df['balance'].iloc[0]-1), 1)
        imports_change = round(100*(df['imports'].iloc[-1]/df['imports'].iloc[0]-1), 1)
        exports_change = round(100*(df['exports'].iloc[-1]/df['exports'].iloc[0]-1), 1)

        if (last_balance < 0):
            trade_text = 'The trade deficit was £' + str(balance_json['years'][-1]['value']) + ' million in ' + str(balance_json['years'][-1]['date']) + ", an increase of " + str(balance_change) + '% since ' + str(balance_json['years'][63]['date']) + ". "
        else:
            trade_text = 'The trade balance is positive with £' + str(balance_json['years'][-1]['value']) + ' million in ' + str(balance_json['years'][-1]['date']) + ", an increase of " + str(balance_change) + '% since ' + str(balance_json['years'][63]['date']) + ". "

        if last_imports > penu_imports:
            imports_text_1 = "Imports reached £" + str(last_imports) + " million in " + str(imports_json['years'][-1]['date']) + ". "
        else:
            imports_text_1 = "Imports decreased to £" + str(last_imports) + " million in " + str(imports_json['years'][-1]['date']) + ". "
        if last_imports > first_imports:
            imports_text_2 = "That is an increase of " + str(imports_change) + "% since " + str(imports_json['years'][63]['date']) + ". "
        imports_text_3 = imports_text_1 + imports_text_2

        if last_exports > penu_exports:
            exports_text_1 = "Exports reached £" + str(last_exports) + " million in " + str(exports_json['years'][-1]['date']) + ". "
        else:
            imports_text_1 = "Imports decreased to £" + str(last_exports) + " million in " + str(exports_json['years'][-1]['date']) + ". "
        if last_exports > first_exports:
            exports_text_2 = "That is an increase of " + str(exports_change) + "% since " + str(exports_json['years'][63]['date']) + ". "
        exports_text_3 = exports_text_1 + exports_text_2

        trade_text_final = trade_text + imports_text_3 + exports_text_3

        # Debt Text

        parsedData = []
        parsedDataText = []
        debt_datasets = {}
        debt_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/hf6x/pusf/data')
        debt_json = json.loads(debt_data.content)
        debtData = {}
        textData = {}
        data_input = 'quarters'
        year_input_int = 132
        for data in debt_json[data_input][year_input_int:]:
            if data['date'][5:7] == 'Q1':
                data['date'] = (data['date'][0:4] + ' ' + 'Mar')
            elif data['date'][5:7] == 'Q2':
                data['date'] = (data['date'][0:4] + ' ' + 'Jun')
            elif data['date'][5:7] == 'Q3':
                data['date'] = (data['date'][0:4] + ' ' + 'Sep')
            elif data['date'][5:7] == 'Q4':
                data['date'] = (data['date'][0:4] + ' ' + 'Dec')
            debtData['date'] = data['date']
            debtData['value'] = data['value']
            parsedData.append(debtData.copy())
        df = pd.DataFrame(data=parsedData)
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'])
        debt_increase_2008 = df.iloc[-1,1] - df.iloc[0,1]
        debt_increase_2016 = df.iloc[-1,1] - df.iloc[34,1]
        if (debt_increase_2008 > 0) and (debt_increase_2016 > 0):
            debt_text_compare = 'Government debt has increased after the financial crisis of 2008, and the Brexit vote of 2016. '
        else:
            if (debt_increase_2008) < 0 and (debt_increase_2016 < 0):
                debt_text_compare = 'Government debt has decreased after the financial crisis of 2008, and the Brexit vote of 2016. '
            elif (debt_increase_2008) < 0 and (debt_increase_2016 > 0):
                debt_text_compare = 'Government debt has decreased since the financial crisis, but increased after the Brexit vote. '
            elif (debt_increase_2008) > 0 and (debt_increase_2016 < 0):
                debt_text_compare = 'Government debt has increased decreased since the financial crisis, but decreased after the Brexit vote. '
        if debt_increase_2008 > 0:
            debt_text_2008 = 'UK debt increased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
        else:
            debt_text_2008 = 'UK debt decreased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
        if debt_increase_2016 > 0:
            debt_text_2016 = 'After the Brexit vote, the UK debt has increased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
        else:
            debt_text_2016 = 'After the Brexit vote, the UK debt has decreased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
        debt_text_total = str(debt_text_compare) + str(debt_text_2008) + str(debt_text_2016)

        final_text = growth_text_final + ' ///// ' + inflation_text_final + ' ///// ' + confidence_text_final + '  /////  ' + trade_text_final + '  ///// ' + debt_text_total
        tradeData['text'] = final_text
        parsedDataText.append(tradeData.copy())

        return render(request, 'dashboard/UK_economy.html', { 'automated_report_json': parsedDataText })




# 3.- GROWTH

def growth(request):
    parsedData = []
    growth_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/ihyq/pgdp/data')
    growth_json = json.loads(growth_data.content)
    services_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3e2/pgdp/data')
    services_json = json.loads(services_data.content)
    production_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/L3BG/pgdp/data')
    production_json = json.loads(production_data.content)
    construction_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3dw/pgdp/data')
    construction_json = json.loads(construction_data.content)
    manufacturing_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/l3bn/pgdp/data')
    manufacturing_json = json.loads(manufacturing_data.content)
    growthData = {}
    textData = {}
    data_input = 'quarters'

    for data_s in range(len(services_json[data_input])):
            growth_json['quarters'][data_s+140]['services'] = services_json['quarters'][data_s]['value']

    for data_p in range(len(production_json[data_input])):
            growth_json['quarters'][data_p+140]['production'] = production_json['quarters'][data_p]['value']

    for data_c in range(len(construction_json[data_input])):
            growth_json['quarters'][data_c+140]['construction'] = construction_json['quarters'][data_c]['value']

    for data_m in range(len(manufacturing_json[data_input])):
            growth_json['quarters'][data_m+140]['manufacturing'] = manufacturing_json['quarters'][data_m]['value']

    for data in growth_json[data_input][241:]:
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
        growthData['production'] = data['production']
        growthData['construction'] = data['construction']
        growthData['manufacturing'] = data['manufacturing']
        parsedData.append(growthData.copy())

    last_value = pd.to_numeric(growth_json['quarters'][-1]['value'])
    last_services = pd.to_numeric(services_json['quarters'][-1]['value'])
    last_production = pd.to_numeric(production_json['quarters'][-1]['value'])
    last_construction = pd.to_numeric(construction_json['quarters'][-1]['value'])
    last_manufacturing = pd.to_numeric(manufacturing_json['quarters'][-1]['value'])


    if last_value > 0:
        trade_text = 'The UK economy reported a quarterly growth of ' + str(last_value) + '% in ' + str(growth_json['quarters'][-1]['date']) + ". "
    else:
        trade_text = 'The UK economy reported a quarterly slowdown of ' + str(last_value) + '% in ' + str(growth_json['quarters'][-1]['date']) + ". "

    # services

    if last_services > 0:
        services_text_1 = "Services grew " + str(last_services) + "% in " + str(services_json['quarters'][-1]['date']) + ", when compared with the previous quarter. "
    else:
        services_text_1 = "Services grew " + str(last_services) + "% in " + str(services_json['quarters'][-1]['date']) + ", when compared with the previous quarter. "
    services_text_3 = services_text_1

    # production

    if last_production > 0:
        production_text_1 = "Production expanded " + str(last_production) + "% in the same period. "
    else:
        production_text_1 = "Production contracted " + str(last_production) + "% in the same period. "
    production_text_3 = production_text_1

    # construction

    if last_construction > 0:
        construction_text_1 = "Construction spiked " + str(last_construction) + "%. "
    else:
        construction_text_1 = "Construction decreased " + str(last_construction) + "%. "
    construction_text_3 = construction_text_1

    if last_manufacturing > 0:
        manufacturing_text_1 = "Manufacturing increased " + str(last_manufacturing) + "%. "
    else:
        manufacturing_text_1 = "Manufacturing decreased " + str(last_manufacturing) + "%. "
    manufacturing_text_3 = manufacturing_text_1


    trade_text_final = trade_text + services_text_3 + production_text_3 + construction_text_3 + manufacturing_text_3
    textData['text'] = trade_text_final
    parsedData.append(textData.copy())
    return render(request, 'dashboard/growth.html', { 'growth_json': json.dumps(parsedData) })

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
        year_input_int = 243

        for data_s in range(len(services_json[data_input])):
                parsed_json['quarters'][data_s+140]['services'] = services_json['quarters'][data_s]['value']

        for data_p in range(len(production_json[data_input])):
                parsed_json['quarters'][data_p+140]['production'] = production_json['quarters'][data_p]['value']

        for data_c in range(len(construction_json[data_input])):
                parsed_json['quarters'][data_c+140]['construction'] = construction_json['quarters'][data_c]['value']

        for data_m in range(len(manufacturing_json[data_input])):
                parsed_json['quarters'][data_m+140]['manufacturing'] = manufacturing_json['quarters'][data_m]['value']

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
                growthData['production'] = data['production']
                growthData['construction'] = data['construction']
                growthData['manufacturing'] = data['manufacturing']
                parsedData.append(growthData.copy())
    return JsonResponse(parsedData, safe=False)


# 4.- INFLATION, PRODUCTIVITY AND REAL INCOME

def inflation(request):
    parsedData = []
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
    inflationData = {}
    textData = {}
    data_input = 'months'
    input_int = 126

    for data_s in range(len(food_json[data_input])):
            cpih_json[data_input][data_s]['cpih'] = cpih_json[data_input][data_s]['value']

    for data_s in range(len(food_json[data_input])):
            cpih_json[data_input][data_s]['food'] = food_json[data_input][data_s]['value']

    for data_p in range(len(alcohol_json[data_input])):
            cpih_json[data_input][data_p]['alcohol'] = alcohol_json[data_input][data_p]['value']

    for data_c in range(len(clothing_json[data_input])):
            cpih_json[data_input][data_c]['clothing'] = clothing_json[data_input][data_c]['value']

    for data_m in range(len(housing_json[data_input])):
            cpih_json[data_input][data_m]['housing'] = housing_json[data_input][data_m]['value']

    for data_m in range(len(furniture_json[data_input])):
            cpih_json[data_input][data_m]['furniture'] = furniture_json[data_input][data_m]['value']

    for data_m in range(len(health_json[data_input])):
            cpih_json[data_input][data_m]['health'] = health_json[data_input][data_m]['value']

    for data_m in range(len(transport_json[data_input])):
            cpih_json[data_input][data_m]['transport'] = transport_json[data_input][data_m]['value']

    for data_m in range(len(communication_json[data_input])):
            cpih_json[data_input][data_m]['communication'] = communication_json[data_input][data_m]['value']

    for data_m in range(len(recreation_json[data_input])):
            cpih_json[data_input][data_m]['recreation'] = recreation_json[data_input][data_m]['value']

    for data in cpih_json[data_input][input_int:]:
            inflationData['date'] = data['date']
            inflationData['cpih'] = data['cpih']
            inflationData['food'] = data['food']
            inflationData['alcohol'] = data['alcohol']
            inflationData['clothing'] = data['clothing']
            inflationData['housing'] = data['housing']
            inflationData['furniture'] = data['furniture']
            inflationData['health'] = data['health']
            inflationData['transport'] = data['transport']
            inflationData['communication'] = data['communication']
            inflationData['recreation'] = data['recreation']
            parsedData.append(inflationData.copy())

    last_cpih = pd.to_numeric(cpih_json['months'][-1]['value'])
    last_food = pd.to_numeric(food_json['months'][-1]['value'])
    last_alcohol = pd.to_numeric(alcohol_json['months'][-1]['value'])
    last_clothing = pd.to_numeric(clothing_json['months'][-1]['value'])
    last_housing = pd.to_numeric(housing_json['months'][-1]['value'])
    last_furniture = pd.to_numeric(furniture_json['months'][-1]['value'])
    last_health = pd.to_numeric(health_json['months'][-1]['value'])
    last_transport = pd.to_numeric(transport_json['months'][-1]['value'])
    last_communication = pd.to_numeric(communication_json['months'][-1]['value'])
    last_recreation = pd.to_numeric(recreation_json['months'][-1]['value'])


    if last_cpih > 0:
        trade_text = 'CPIH reported an annual increase of ' + str(last_cpih) + '% in ' + str(cpih_json['months'][-1]['date']) + ". "
    else:
        trade_text = 'CPIH reported an annual decrease of' + str(last_cpih) + '% in ' + str(cpih_json['months'][-1]['date']) + ". "

    # Food

    if last_food > 0:
        food_text_1 = "Food and non-alcoholic beverages increased " + str(last_food) + "% in " + str(food_json['months'][-1]['date']) + ", after a 12-month period. "
    else:
        food_text_1 = "Food and non-alcoholic beverages decreased " + str(last_food) + "% in " + str(food_json['months'][-1]['date']) + ", after a 12-month period. "
    food_text_3 = food_text_1

    # Alcohol

    if last_alcohol > 0:
        alcohol_text_1 = "The price of alcohol increased " + str(last_alcohol) + "% in the same period; "
    else:
        alcohol_text_1 = "The price of alcohol decreased " + str(last_alcohol) + "% in the same period; "
    alcohol_text_3 = alcohol_text_1

    # Clothing

    if last_clothing > 0:
        clothing_text_1 = "Clothing increased " + str(last_clothing) + "%; "
    else:
        clothing_text_1 = "Clothing decreased " + str(last_clothing) + "%; "
    clothing_text_3 = clothing_text_1

    # Housing

    if last_housing > 0:
        housing_text_1 = "Housing increased " + str(last_housing) + "%; "
    else:
        housing_text_1 = "Housing decreased " + str(last_housing) + "%; "
    housing_text_3 = housing_text_1

    # Furniture

    if last_furniture > 0:
        furniture_text_1 = "Furniture increased " + str(last_furniture) + "%; "
    else:
        furniture_text_1 = "Furniture decreased " + str(last_furniture) + "%; "
    furniture_text_3 = furniture_text_1

    # Health

    if last_health > 0:
        health_text_1 = "Health increased " + str(last_health) + "%; "
    else:
        health_text_1 = "Health decreased " + str(last_health) + "%; "
    health_text_3 = health_text_1

    # Transport

    if last_transport > 0:
        transport_text_1 = "Transport increased " + str(last_transport) + "%; "
    else:
        transport_text_1 = "Transport decreased " + str(last_transport) + "%; "
    transport_text_3 = transport_text_1

    # Communication

    if last_communication > 0:
        communication_text_1 = "Communication increased " + str(last_communication) + "%; "
    else:
        communication_text_1 = "Communication decreased " + str(last_communication) + "%; "
    communication_text_3 = communication_text_1

    # Recreation

    if last_recreation > 0:
        recreation_text_1 = "Recreation increased " + str(last_recreation) + "%. "
    else:
        recreation_text_1 = "Recreation decreased " + str(last_recreation) + "%. "
    recreation_text_3 = recreation_text_1


    trade_text_final = trade_text + food_text_3 + alcohol_text_3 + clothing_text_3 + housing_text_3 + furniture_text_3 + health_text_3 + transport_text_3 + communication_text_3 + recreation_text_3
    textData['text'] = trade_text_final
    parsedData.append(textData.copy())
    return render(request, 'dashboard/inflation.html', { 'inflation_json': json.dumps(parsedData) })

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
        input_int = 120

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['cpih'] = cpih_json[data_input][data_s]['value']

        for data_s in range(len(food_json[data_input])):
                cpih_json[data_input][data_s]['food'] = food_json[data_input][data_s]['value']

        for data_p in range(len(alcohol_json[data_input])):
                cpih_json[data_input][data_p]['alcohol'] = alcohol_json[data_input][data_p]['value']

        for data_c in range(len(clothing_json[data_input])):
                cpih_json[data_input][data_c]['clothing'] = clothing_json[data_input][data_c]['value']

        for data_m in range(len(housing_json[data_input])):
                cpih_json[data_input][data_m]['housing'] = housing_json[data_input][data_m]['value']

        for data_m in range(len(furniture_json[data_input])):
                cpih_json[data_input][data_m]['furniture'] = furniture_json[data_input][data_m]['value']

        for data_m in range(len(health_json[data_input])):
                cpih_json[data_input][data_m]['health'] = health_json[data_input][data_m]['value']

        for data_m in range(len(transport_json[data_input])):
                cpih_json[data_input][data_m]['transport'] = transport_json[data_input][data_m]['value']

        for data_m in range(len(communication_json[data_input])):
                cpih_json[data_input][data_m]['communication'] = communication_json[data_input][data_m]['value']

        for data_m in range(len(recreation_json[data_input])):
                cpih_json[data_input][data_m]['recreation'] = recreation_json[data_input][data_m]['value']

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

def income(request):
    parsedData = []
    final_json = []
    if request.method == 'POST':
        income_datasets = {}
        income_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/crsf/ukea/data')
        income_json = json.loads(income_data.content)
        incomeData = {}
        data_input = 'quarters'
        # year_input_int = 48
        year_input_int = 76
        # date_input = request.POST.get('years')
        # input_int = int(date_input)
        # year_input_int = int(year_input)
        for data in income_json[data_input][year_input_int:]:
            if data['date'][5:7] == 'Q1':
                data['date'] = (data['date'][0:4] + ' ' + 'Mar')
            elif data['date'][5:7] == 'Q2':
                data['date'] = (data['date'][0:4] + ' ' + 'Jun')
            elif data['date'][5:7] == 'Q3':
                data['date'] = (data['date'][0:4] + ' ' + 'Sep')
            elif data['date'][5:7] == 'Q4':
                data['date'] = (data['date'][0:4] + ' ' + 'Dec')
            incomeData['date'] = data['date']
            incomeData['value'] = int(data['value'])
            parsedData.append(incomeData.copy())

        pandas_data = pd.DataFrame(parsedData)
        pandas_data['growth'] = ((pandas_data['value'].pct_change(4))*100).round(1)
        json_income = pandas_data.to_json(orient='records')
        final_json = json.loads(json_income)
    return JsonResponse(final_json[4:], safe=False)


# 5.- CONSUMER CONFIDENCE AND INVESTMENT

def confidence(request):
    parsedData = []
    confidence_URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/teibs020?geo=DK&geo=FI&geo=LU&geo=NL&geo=SE&geo=UK&geo=IE&precision=1&indic=BS-CSMCI-BAL&s_adj=SA'
    dataset = pyjstat.Dataset.read(confidence_URL)
    df = dataset.write('dataframe')
    json_confidence = df.to_json(orient='records')
    json_confidence_final = json.loads(json_confidence)
    confidenceData = {}
    textData = {}
    for data in json_confidence_final:
        if data['time'][4:7] == 'M12':
            data['time'] = (data['time'][0:4] + ' ' + 'Dec')
        if data['time'][4:7] == 'M11':
            data['time'] = (data['time'][0:4] + ' ' + 'Nov')
        if data['time'][4:7] == 'M10':
            data['time'] = (data['time'][0:4] + ' ' + 'Oct')
        if data['time'][4:7] == 'M09':
            data['time'] = (data['time'][0:4] + ' ' + 'Sep')
        if data['time'][4:7] == 'M08':
            data['time'] = (data['time'][0:4] + ' ' + 'Aug')
        if data['time'][4:7] == 'M07':
            data['time'] = (data['time'][0:4] + ' ' + 'Jul')
        if data['time'][4:7] == 'M06':
            data['time'] = (data['time'][0:4] + ' ' + 'Jun')
        if data['time'][4:7] == 'M05':
            data['time'] = (data['time'][0:4] + ' ' + 'May')
        if data['time'][4:7] == 'M04':
            data['time'] = (data['time'][0:4] + ' ' + 'Apr')
        if data['time'][4:7] == 'M03':
            data['time'] = (data['time'][0:4] + ' ' + 'Mar')
        if data['time'][4:7] == 'M02':
            data['time'] = (data['time'][0:4] + ' ' + 'Feb')
        if data['time'][4:7] == 'M01':
            data['time'] = (data['time'][0:4] + ' ' + 'Jan')
        confidenceData['date'] = data['time']
        confidenceData['value'] = data['value']
        confidenceData['Country'] = data['geo']
        parsedData.append(confidenceData.copy())
    df = pd.DataFrame(parsedData).pivot('date','Country','value')
    sort = pd.to_datetime(df.index).sort_values().strftime('%Y %b')
    parsedDataFinal = df.reindex(sort).reset_index().to_dict('r')
    df = pd.DataFrame(data = parsedDataFinal)
    df['date'] = pd.to_datetime(df['date'])
    mean_Denmark = round(df['Denmark'].mean(), 1)
    mean_Finland = round(df['Finland'].mean(), 1)
    mean_Luxembourg = round(df['Luxembourg'].mean(), 1)
    mean_Netherlands = round(df['Netherlands'].mean(), 1)
    mean_Sweden = round(df['Sweden'].mean(), 1)
    mean_United_Kingdom = round(df['United Kingdom'].mean(), 1)
    less_list = []
    more_list = []
    if mean_United_Kingdom < mean_Denmark:
        less_list.append('Denmark')
    else:
        more_list.append('Denmark')
    if mean_United_Kingdom < mean_Finland:
        less_list.append('Finland')
    else:
        more_list.append('Finland')
    if mean_United_Kingdom < mean_Luxembourg:
        less_list.append('Luxembourg')
    else:
        more_list.append('Luxembourg')
    if mean_United_Kingdom < mean_Netherlands:
        less_list.append('Netherlands')
    else:
        more_list.append('Netherlands')
    if mean_United_Kingdom < mean_Sweden:
        less_list.append('Sweden')
    else:
        more_list.append('Sweden')
    less_list_text = ", ".join(less_list)
    more_list_text = ", ".join(more_list)
    if more_list == []:
        text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + less_list_text + " reported a superior consumer confidence in the same period."
    elif less_list == []:
        text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + more_list_text + " reported an inferior consumer confidence in the same period."
    else:
        text = "The United Kingdom reported an average consumer confidence index of " + str(mean_United_Kingdom) + " from " + str(parsedDataFinal[0]['date']) + ' to ' + str(parsedDataFinal[-1]['date']) + '. Countries such as ' + less_list_text + " reported an inferior consumer confidence in the same period. "
    text_mean_countries = ' Between ' + str(parsedDataFinal[0]['date']) + ' and ' + str(parsedDataFinal[-1]['date']) + ' Denmark had a consumer confidence index of ' + str(mean_Denmark) + '; Finland, ' + str(mean_Finland) + '; Luxembourg, ' + str(mean_Luxembourg) + '; Netherlands, ' + str(mean_Netherlands) + ' and Sweden, ' + str(mean_Sweden) + '. '
    text_final_confidence = text + text_mean_countries
    textData['text'] = text_final_confidence
    parsedDataFinal.append(textData.copy())
    return render(request, 'dashboard/confidence.html', { 'confidence_json': json.dumps(parsedDataFinal) })

def confidence_data(request):
    parsedData = []
    parsedDataFinal = []
    if request.method == 'POST':
        confidence_URL = 'http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/teibs020?geo=DK&geo=FI&geo=LU&geo=NL&geo=SE&geo=UK&precision=1&indic=BS-CSMCI-BAL&s_adj=SA'
        dataset = pyjstat.Dataset.read(confidence_URL)
        df = dataset.write('dataframe')
        json_confidence = df.to_json(orient='records')
        json_confidence_final = json.loads(json_confidence)
        confidenceData = {}
        for data in json_confidence_final:
            if data['time'][4:7] == 'M12':
                data['time'] = (data['time'][0:4] + ' ' + 'Dec')
            if data['time'][4:7] == 'M11':
                data['time'] = (data['time'][0:4] + ' ' + 'Nov')
            if data['time'][4:7] == 'M10':
                data['time'] = (data['time'][0:4] + ' ' + 'Oct')
            if data['time'][4:7] == 'M09':
                data['time'] = (data['time'][0:4] + ' ' + 'Sep')
            if data['time'][4:7] == 'M08':
                data['time'] = (data['time'][0:4] + ' ' + 'Aug')
            if data['time'][4:7] == 'M07':
                data['time'] = (data['time'][0:4] + ' ' + 'Jul')
            if data['time'][4:7] == 'M06':
                data['time'] = (data['time'][0:4] + ' ' + 'Jun')
            if data['time'][4:7] == 'M05':
                data['time'] = (data['time'][0:4] + ' ' + 'May')
            if data['time'][4:7] == 'M04':
                data['time'] = (data['time'][0:4] + ' ' + 'Apr')
            if data['time'][4:7] == 'M03':
                data['time'] = (data['time'][0:4] + ' ' + 'Mar')
            if data['time'][4:7] == 'M02':
                data['time'] = (data['time'][0:4] + ' ' + 'Feb')
            if data['time'][4:7] == 'M01':
                data['time'] = (data['time'][0:4] + ' ' + 'Jan')
            confidenceData['date'] = data['time']
            confidenceData['value'] = data['value']
            confidenceData['Country'] = data['geo']
            parsedData.append(confidenceData.copy())
        df = pd.DataFrame(parsedData).pivot('date','Country','value')
        sort = pd.to_datetime(df.index).sort_values().strftime('%Y %b')
        parsedDataFinal = df.reindex(sort).reset_index().to_dict('r')
    return JsonResponse(parsedDataFinal, safe=False)

def business_data(request):
    parsedData = []
    final_json = []
    if request.method == 'POST':
        business_datasets = {}
        business_data = requests.get('https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/npem/cxnv/data')
        business_json = json.loads(business_data.content)
        businessData = {}
        data_input = 'quarters'
        #     year_input = request.POST.get('years')
        #     year_input_int = 48
        year_input_int = 116
        #     year_input_int = int(year_input)
        for data in business_json[data_input][year_input_int:]:
            if data['date'][5:7] == 'Q1':
                data['date'] = (data['date'][0:4] + ' ' + 'Mar')
            elif data['date'][5:7] == 'Q2':
                data['date'] = (data['date'][0:4] + ' ' + 'Jun')
            elif data['date'][5:7] == 'Q3':
                data['date'] = (data['date'][0:4] + ' ' + 'Sep')
            elif data['date'][5:7] == 'Q4':
                data['date'] = (data['date'][0:4] + ' ' + 'Dec')
            businessData['date'] = data['date']
            businessData['value'] = int(data['value'])
            parsedData.append(businessData.copy())
        pandas_data = pd.DataFrame(parsedData)
        pandas_data
        pandas_data['growth'] = ((pandas_data['value'].pct_change(4))*100).round(1)
        json_income = pandas_data.to_json(orient='records')
        final_json = json.loads(json_income)
    return JsonResponse(final_json[4:], safe=False)


# 6.- TRADE

def trade(request):
    parsedData = []
#     if request.method == 'POST':
    balance_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbj/mret/data')
    balance_json = json.loads(balance_data.content)
    imports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbi/mret/data')
    imports_json = json.loads(imports_data.content)
    exports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbh/mret/data')
    exports_json = json.loads(exports_data.content)
    tradeData = {}
    textData = {}
    data_input = 'years'
    input_int = 63

    for data_s in range(len(imports_json[data_input])):
            balance_json[data_input][data_s]['balance'] = balance_json[data_input][data_s]['value']

    for data_s in range(len(imports_json[data_input])):
            balance_json[data_input][data_s]['imports'] = imports_json[data_input][data_s]['value']

    for data_p in range(len(exports_json[data_input])):
            balance_json[data_input][data_p]['exports'] = exports_json[data_input][data_p]['value']

    for data in balance_json[data_input][input_int:]:
            tradeData['date'] = data['date']
            tradeData['balance'] = data['balance']
            tradeData['imports'] = data['imports']
            tradeData['exports'] = data['exports']
            parsedData.append(tradeData.copy())
    last_balance = pd.to_numeric(balance_json['years'][-1]['value'])
    last_imports = pd.to_numeric(imports_json['years'][-1]['value'])
    penu_imports = pd.to_numeric(imports_json['years'][-2]['value'])
    first_imports = pd.to_numeric(imports_json['years'][63]['value'])
    last_exports = pd.to_numeric(exports_json['years'][-1]['value'])
    penu_exports = pd.to_numeric(exports_json['years'][-2]['value'])
    first_exports = pd.to_numeric(exports_json['years'][63]['value'])
    df = pd.DataFrame(data=parsedData)
    df['date'] = pd.to_datetime(df['date'])
    df['balance'] = pd.to_numeric(df['balance'])
    df['imports'] = pd.to_numeric(df['imports'])
    df['exports'] = pd.to_numeric(df['exports'])
    balance_change = round(100*(df['balance'].iloc[-1]/df['balance'].iloc[0]-1), 1)
    imports_change = round(100*(df['imports'].iloc[-1]/df['imports'].iloc[0]-1), 1)
    exports_change = round(100*(df['exports'].iloc[-1]/df['exports'].iloc[0]-1), 1)

    if (last_balance < 0):
        trade_text = 'The trade deficit was £' + str(balance_json['years'][-1]['value']) + ' million in ' + str(balance_json['years'][-1]['date']) + ", an increase of " + str(balance_change) + '% since ' + str(balance_json['years'][63]['date']) + ". "
    else:
        trade_text = 'The trade balance is positive with £' + str(balance_json['years'][-1]['value']) + ' million in ' + str(balance_json['years'][-1]['date']) + ", an increase of " + str(balance_change) + '% since ' + str(balance_json['years'][63]['date']) + ". "

    if last_imports > penu_imports:
        imports_text_1 = "Imports reached £" + str(last_imports) + " million in " + str(imports_json['years'][-1]['date']) + ". "
    else:
        imports_text_1 = "Imports decreased to £" + str(last_imports) + " million in " + str(imports_json['years'][-1]['date']) + ". "
    if last_imports > first_imports:
        imports_text_2 = "That is an increase of " + str(imports_change) + "% since " + str(imports_json['years'][63]['date']) + ". "
    imports_text_3 = imports_text_1 + imports_text_2

    if last_exports > penu_exports:
        exports_text_1 = "Exports reached £" + str(last_exports) + " million in " + str(exports_json['years'][-1]['date']) + ". "
    else:
        imports_text_1 = "Imports decreased to £" + str(last_exports) + " million in " + str(exports_json['years'][-1]['date']) + ". "
    if last_exports > first_exports:
        exports_text_2 = "That is an increase of " + str(exports_change) + "% since " + str(exports_json['years'][63]['date']) + ". "
    exports_text_3 = exports_text_1 + exports_text_2

    trade_text_final = trade_text + imports_text_3 + exports_text_3
    textData['text'] = trade_text_final
    parsedData.append(textData.copy())
    return render(request, 'dashboard/trade.html', { 'trade_json': json.dumps(parsedData) })

def imports_data(request):
    parsedData = []
    if request.method == 'POST':
        imports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbi/mret/data')
        imports_json = json.loads(imports_data.content)
        exports_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbh/mret/data')
        exports_json = json.loads(exports_data.content)
        tradeData = {}
        data_input = 'years'
        input_int = 60

        for data_s in range(len(imports_json[data_input])):
                imports_json[data_input][data_s]['imports'] = imports_json[data_input][data_s]['value']

        for data_p in range(len(exports_json[data_input])):
                imports_json[data_input][data_p]['exports'] = exports_json[data_input][data_p]['value']

        for data in imports_json[data_input][input_int:]:
                tradeData['date'] = data['date']
                tradeData['imports'] = data['imports']
                tradeData['exports'] = data['exports']
                parsedData.append(tradeData.copy())
    return JsonResponse(parsedData, safe=False)

def services_data(request):
    parsedData = []
    if request.method == 'POST':
        services_data = requests.get('https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/timeseries/ikbd/ukea/data')
        services_json = json.loads(services_data.content)
        tradeData = {}
        data_input = 'years'
        input_int = 60
        for data in services_json[data_input][input_int:]:
                tradeData['date'] = data['date']
                tradeData['value'] = data['value']
                parsedData.append(tradeData.copy())
    return JsonResponse(parsedData, safe=False)


# 7.- DEBT AND DEFICIT

def debt(request):
    parsedData = []
    debt_datasets = {}
    debt_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/hf6x/pusf/data')
    debt_json = json.loads(debt_data.content)
    debtData = {}
    textData = {}
    data_input = 'quarters'
    year_input_int = 132
    for data in debt_json[data_input][year_input_int:]:
        if data['date'][5:7] == 'Q1':
            data['date'] = (data['date'][0:4] + ' ' + 'Mar')
        elif data['date'][5:7] == 'Q2':
            data['date'] = (data['date'][0:4] + ' ' + 'Jun')
        elif data['date'][5:7] == 'Q3':
            data['date'] = (data['date'][0:4] + ' ' + 'Sep')
        elif data['date'][5:7] == 'Q4':
            data['date'] = (data['date'][0:4] + ' ' + 'Dec')
        debtData['date'] = data['date']
        debtData['value'] = data['value']
        parsedData.append(debtData.copy())
    df = pd.DataFrame(data=parsedData)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'])
    debt_increase_2008 = df.iloc[-1,1] - df.iloc[0,1]
    debt_increase_2016 = df.iloc[-1,1] - df.iloc[34,1]
    if (debt_increase_2008 > 0) and (debt_increase_2016 > 0):
        debt_text_compare = 'Government debt has increased after the financial crisis of 2008, and the Brexit vote of 2016. '
    else:
        if (debt_increase_2008) < 0 and (debt_increase_2016 < 0):
            debt_text_compare = 'Government debt has decreased after the financial crisis of 2008, and the Brexit vote of 2016. '
        elif (debt_increase_2008) < 0 and (debt_increase_2016 > 0):
            debt_text_compare = 'Government debt has decreased since the financial crisis, but increased after the Brexit vote. '
        elif (debt_increase_2008) > 0 and (debt_increase_2016 < 0):
            debt_text_compare = 'Government debt has increased decreased since the financial crisis, but decreased after the Brexit vote. '
    if debt_increase_2008 > 0:
        debt_text_2008 = 'UK debt increased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    else:
        debt_text_2008 = 'UK debt decreased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    if debt_increase_2016 > 0:
        debt_text_2016 = 'After the Brexit vote, the UK debt has increased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    else:
        debt_text_2016 = 'After the Brexit vote, the UK debt has decreased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    debt_text_total = str(debt_text_compare) + str(debt_text_2008) + str(debt_text_2016)
    textData['text'] = debt_text_total
    parsedData.append(textData.copy())
    return render(request, 'dashboard/debt.html', { 'debt_json': json.dumps(parsedData) })

def debt_data(request):
    parsedData = []
    # if request.method == 'POST':
    debt_datasets = {}
    debt_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/hf6x/pusf/data')
    debt_json = json.loads(debt_data.content)
    debtData = {}
    textData = {}
    data_input = 'quarters'
    year_input_int = 132
#     year_input_int = int(year_input)
    for data in debt_json[data_input][year_input_int:]:
        if data['date'][5:7] == 'Q1':
            data['date'] = (data['date'][0:4] + ' ' + 'Mar')
        elif data['date'][5:7] == 'Q2':
            data['date'] = (data['date'][0:4] + ' ' + 'Jun')
        elif data['date'][5:7] == 'Q3':
            data['date'] = (data['date'][0:4] + ' ' + 'Sep')
        elif data['date'][5:7] == 'Q4':
            data['date'] = (data['date'][0:4] + ' ' + 'Dec')
        debtData['date'] = data['date']
        debtData['value'] = data['value']
        parsedData.append(debtData.copy())
    df = pd.DataFrame(data=parsedData)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'])
    debt_increase_2008 = df.iloc[-1,1] - df.iloc[0,1]
    debt_increase_2016 = df.iloc[-1,1] - df.iloc[34,1]
    if (debt_increase_2008 > 0) and (debt_increase_2016 > 0):
        debt_text_compare = 'Government debt has increased after the financial crisis of 2008, and the Brexit vote of 2016. '
    else:
        if (debt_increase_2008) < 0 and (debt_increase_2016 < 0):
            debt_text_compare = 'Government debt has decreased after the financial crisis of 2008, and the Brexit vote of 2016. '
        elif (debt_increase_2008) < 0 and (debt_increase_2016 > 0):
            debt_text_compare = 'Government debt has decreased since the financial crisis, but increased after the Brexit vote. '
        elif (debt_increase_2008) > 0 and (debt_increase_2016 < 0):
            debt_text_compare = 'Government debt has increased decreased since the financial crisis, but decreased after the Brexit vote. '
    if debt_increase_2008 > 0:
        debt_text_2008 = 'UK debt increased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    else:
        debt_text_2008 = 'UK debt decreased ' + str(debt_increase_2008) + ' percentage points since the financial crisis of 2008, from ' + str(debt_json[data_input][132]['value']) + '% of GDP in ' +  str(debt_json[data_input][132]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    if debt_increase_2016 > 0:
        debt_text_2016 = 'After the Brexit vote, the UK debt has increased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    else:
        debt_text_2016 = 'After the Brexit vote, the UK debt has decreased ' + str(debt_increase_2016) + ' pp from ' + str(debt_json[data_input][166]['value']) + '% of GDP in ' +  str(debt_json[data_input][166]['date']) + ' to ' + str(debt_json[data_input][-1]['value']) + '% in ' + str(debt_json[data_input][-1]['date']) + '. '
    debt_text_total = str(debt_text_compare) + str(debt_text_2008) + str(debt_text_2016)
    textData['text'] = debt_text_total
    parsedData.append(textData.copy())
    return JsonResponse(parsedData, safe=False)

def deficit_data(request):
    parsedData = []
    if request.method == 'POST':
        deficit_datasets = {}
        deficit_data = requests.get('https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/timeseries/j5ij/pusf/data')
        deficit_json = json.loads(deficit_data.content)
        deficitData = {}
        data_input = 'quarters'
        year_input_int = 206
    #     year_input_int = int(year_input)
        for data in deficit_json[data_input][year_input_int:]:
            if data['date'][5:7] == 'Q1':
                data['date'] = (data['date'][0:4] + ' ' + 'Mar')
                deficitData['date'] = data['date']
                deficitData['value'] = data['value']
                parsedData.append(deficitData.copy())
    return JsonResponse(parsedData, safe=False)
