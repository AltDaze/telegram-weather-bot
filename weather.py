import localization as loc
import requests
import config

key = config.owm_key

class Weather():
	def today(city, lang):
		data = Weather.data(city, lang)
		return data

	def forecast():
		pass

	def data(place, lang, forecast = None):
		if type(place) == list and forecast == None:
			r = requests.get('http://api.openweathermap.org/data/2.5/weather?&units=metric&lat=%s&lon=%s&appid=%s&lang=%s' % (place[0], place[1], key, lang))
		if type(place) == str and forecast == None:
			r = requests.get('http://api.openweathermap.org/data/2.5/weather?&units=metric&q=%s&appid=%s&lang=%s' % (place, key, lang))
		if type(place) == tuple:
			r = requests.get('http://api.openweathermap.org/data/2.5/weather?&units=metric&q=%s&appid=0c9f3c052f1d81b7062750ff0926f345&lang=%s' % (place[0], lang))

		data = r.json()
		temp = data["main"]["temp"]
		temp_min = data["main"]["temp_min"]
		temp_max = data["main"]["temp_max"]
		describe = data["weather"][0]["description"]
		humidity = data["main"]["humidity"]
		wind = data["wind"]["speed"]
		visible = data["visibility"]

		return f'\
	🏡 {str(describe)}, {str(temp)}°C\n\
	🌡 MIN: {str(temp_min)}°C | MAX: {str(temp_max)}°C\n\
	💧 {loc.air_humidity[lang]} {str(humidity)}%\n\
	💨 {loc.wind_speed[lang]} {str(wind)} м/с\n\
	👀 {loc.visible[lang]} {str(visible)}м'
