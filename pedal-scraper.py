from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Remove BeautifulSoup from dependencies/requirements.txt

url = "https://reverb.com/ca/marketplace?category=reverb&product_type=effects-and-pedals&ships_to=CA&item_region=XX"

# User input

# MODIFY ALL CODE CHUNK BELOW S.T. ONLY Y OR N ARE ACCEPTED AS STATUS INPUTS AND NOTHING ELSE.
invalid_input_msg = "Invalid input, please try again.\n"
search_term_status = input("Enter search term? [Y/N]\n")
if search_term_status.replace(' ', '').lower() == 'y':
    search_term = input("Enter search term:\n")
    url += f"&query={search_term}"
shipping_2d_free_status = input("Get products with free 2-day shipping only? [Y/N]\n")
if shipping_2d_free_status.replace(' ', '').lower() == 'y':
    url += "&free_expedited_shipping=true"
else:
    shipping_free_status = input("Get products with free shipping (including 2-day) only? [Y/N]\n")
    if shipping_free_status.replace(' ', '').lower() == 'y':
        url += "&free_shipping=true"
price_range_status = input("Enter price range? [Y/N]\n")
if price_range_status.replace(' ', '').lower() == 'y':
    price_min = input("Enter minimum price:\n") # MODIFY THIS PART (check input validity)
    price_max = input("Enter maximum price:\n") # MODIFY THIS PART (check input validity)
    url += f"&price_min={price_min}&price_max={price_max}"
handmade_status = input("Get handmade pedals only? [Y/N]\n")
if handmade_status.replace(' ', '').lower() == 'y':
    url += "&handmade=true"
reverb_credits_status = input("Only get products that accept reverb credits?\n")
if reverb_credits_status.replace(' ', '').lower() == 'y':
    url += "&accepts_gift_cards=true"
preferred_seller_status = input("Get products from preferred sellers only?\n")
if preferred_seller_status.replace(' ', '').lower() == 'y':
    url += "&preferred_seller=true"

session = HTMLSession()
response = session.get(url)
response.html.render(sleep=0.25, keep_page=True, scrolldown=2) # sleep and scrolldown values may noy work, experiment further
products = response.html.find('.grid-card')

count = 0
for product in products:
    pedal = {
        'name': product.text,
        'link': product.absolute_links
    }
    count += 1
    print(pedal)
    print('\n')
print(count)