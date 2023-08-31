import requests
import requests as rq
from bs4 import BeautifulSoup as bs

url = "https://reverb.com/ca/marketplace?category=reverb&product_type=effects-and-pedals&ships_to=CA"

response = rq.get(url)

print(response.text)