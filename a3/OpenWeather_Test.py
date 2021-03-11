from OpenWeather import OpenWeather

zipcode = "92660"
ccode = "US"
apikey = "965cf2e5bf9db105ac06164bddce42d6"

open_weather = OpenWeather(zipcode,ccode,apikey)
print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
print(f"The current weather for {zipcode} is {open_weather.description}")
print(f"The current humidity for {zipcode} is {open_weather.humidity}")
print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")

message = "the weather is @weather today"
print(open_weather.transclude(message))
