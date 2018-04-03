#!/usr/bin/env python3
from spyre import server
import re
import glob
import pandas as pd
import json
import  urllib2


class StockExample(server.App):
	title = "LABA2 | spyre"

	inputs = [{ "type":'dropdown',
                "label": 'Index',
                "options" : [   {"label": "All", "value":"All"},
								{"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"}],
                "key": 'index',
                "action_id": "update_data"
				},
				
			  { "type": 'dropdown',
				"label": 'Province',
				"options": [
				{"label": "Vinnytsya", "value": "1"},
				{"label": "Volyn", "value": "2"},
				{"label": "Dnipropetrovs", "value": "3"},
				{"label": "Donets", "value": "4"},
				{"label": "Zhytomyr", "value": "5"},
				{"label": "Transcarpathia", "value": "6"},
				{"label": "Zaporizhzhya", "value": "7"},
				{"label": "Ivano-Frankivs", "value": "8"},
				{"label": "Kievska", "value": "9"},
				{"label": "Kirovohrad", "value": "10"},
				{"label": "Luhans", "value": "11"},
				{"label": "Lvivska", "value": "12"},
				{"label": "Mykolayivska", "value": "13"},
				{"label": "Odessa", "value": "14"},
				{"label": "Poltava", "value": "15"},
				{"label": "Rivne", "value": "16"},
				{"label": "Sumy", "value": "17"},
				{"label": "Ternopil", "value": "18"},
				{"label": "Kharkiv", "value": "19"},
				{"label": "Kherson", "value": "20"},
				{"label": "Khmelnitska", "value": "21"},
				{"label": "Cherkasy", "value": "22"},
				{"label": "Chernivtsi", "value": "23"},
				{"label": "Chernihiv", "value": "24"},
				{"label": "Crimea", "value": "25"}],
				"key": 'p_id',
				"action_id": "update_data"},
				
			  { "input_type":"text",
                "variable_name":"year",
                "label": "Year",
                "value":2013,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'Week1',
                "min" : 1,
				"max" : 52,
				"value" : 1,
                "key": 'week1',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Week2',
                "min" : 1,
				"max" : 52,
				"value" : 52,
                "key": 'week2',
                "action_id": 'update_data'}]

	controls = [{
		"type": "hidden",
		"id": "update_data"
	}]

	tabs = [ "Table","Plot",]

	outputs = [
		{
			"type": "plot",
			"id": "plot",
			"control_id": "update_data",
			"tab": "Plot"
		}, {
			"type": "table",
			"id": "table_id",
			"control_id": "update_data",
			"tab": "Table",
			"on_page_load": True
		}
	]

	def getData(self,params):
		index = params['index']
		p_id = params['p_id']
		year = params['year']
		week1 = params['week1']
		week2 = params['week2']
		url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID="+str(p_id)+"&year1=1981&year2=2018&type=Mean"
		vhi_url = urllib2.urlopen(url)
		df1 = pd.DataFrame()
		dfile = pd.read_csv(vhi_url, index_col=False, skiprows=1,
				 sep=r'\s+,*|,\s*', 
				 names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'], engine = 'python')
		dfile=dfile[:-1]
		df1 = df1.append(dfile)
		url2="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID="+str(p_id)+"&year1=1981&year2=2018&type=VHI_Parea"
		vhi_url2 = urllib2.urlopen(url2)
		df2 = pd.DataFrame()
		dfile = pd.read_csv(vhi_url2, index_col=False, skiprows=1,
				 sep=r'\s+,*|,\s*', 
				 names=['year', 'week', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95','100'], engine = 'python')
		dfile=dfile[:-1]
		df2 = df2.append(dfile)
		df = pd.concat([df1.iloc[:,:], df2.iloc[:,2:]], axis=1)
		result = df.loc[(df['year']==str(year)) & (df['week']>=week1) & (df['week']<=week2)]
		if (index == "All"):
				result = result[['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95','100']]
		else:
				result = result[['week',index]]
		return result

	def getPlot(self,params):
		index = params['index']
		year = params['year']
		week1 = params['week1']
		week2 = params['week2']
		df = self.getData(params).set_index('week')
		df=df.astype(float)
		plt_obj = df.plot(color='r')
		plt_obj.set_ylabel(index)
		plt_obj.set_title("Table for {}".format(index))
		fig = plt_obj.get_figure()
		return fig

app = StockExample()
app.launch(port=9094)
