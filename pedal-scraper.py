from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Remove BeautifulSoup from dependencies/requirements.txt

url = "https://reverb.com/ca/marketplace?category=reverb&product_type=effects-and-pedals&ships_to=CA&item_region=XX"

# User input

# MODIFY ALL CODE CHUNK BELOW S.T. ONLY Y OR N ARE ACCEPTED AS STATUS INPUTS AND NOTHING ELSE.
class InvalidInputException(Exception):
    """Raised when the user's input is neither Y nor N"""
    pass

def modify_url(link: str, preference: str) -> None:
    """Modifies the url 'link' according to the user preference 'preference'
    :param link: the url for modification
    :type link: str
    :param preference: the user's preference
    :type preference: str
    :return: Nothing
    :rtype: None
    """
    first_message = ""
    if preference == "Search Term":
        first_message = "Enter search term? [Y/N]\n"
    elif preference == "Free 2-Day Shipping":
        first_message = "Get products with free 2-day shipping only? [Y/N]\n"
    elif preference == "Price Range":
        first_message = "Enter price range? [Y/N]\n"
    elif preference == "Handmade Only":
        first_message = "Get handmade pedals only? [Y/N]\n"
    elif preference == "Reverb Credits":
        first_message = "Only get products that accept reverb credits?\n"
    elif preference == "Preferred Sellers":
        first_message = "Get products from preferred sellers only?\n"
    while True:
        try:
            first_input = input(first_message)
            if first_input.replace(' ', '').lower() not in {'y', 'n'}:
                raise InvalidInputException
        except InvalidInputException:
            print("Invalid input, please try again.\n")
            continue
        else:
            if first_input.replace(' ', '').lower() == 'y':
                # Simplest 3 cases below (Handmade Only, Reverb Credits, Preferred Sellers)
                if preference == "Handmade Only":
                    link += "&handmade=true"
                elif preference == "Reverb Credits":
                    link += "&accepts_gift_cards=true"
                elif preference == "Preferred Sellers":
                    link += "&preferred_seller=true"
                # Less simple case (Search Term)
                elif preference == "Search Term":
                    search_term = input("Enter search term:\n")
                    search_term = search_term.replace(' ', '%20')
                    link += f"&query={search_term}"
                # Complex case below (Shipping)
                elif preference == "Free 2-Day Shipping":
                    link += "&free_expedited_shipping=true"
                # Most complex case below (Price Range)
                elif preference == "Price Range":
                    price_min = 0.00
                    price_max = 0.00
                    while True:
                        try:
                            price_min = float(input("Enter minimum price (No signs ($/-/+)):\n"))
                        except ValueError:
                            print("Please enter a valid price (No signs ($/-/+)).\n")
                            continue
                        else:
                            break
                    while True:
                        try:
                            price_max = float(input("Enter maximum price (No signs ($/-/+)):\n"))
                        except ValueError:
                            print("Please enter a valid price (No signs ($/-/+)).\n")
                            continue
                        else:
                            break
                    link += f"&price_min={price_min}&price_max={price_max}"
            # Complex case continued below (Shipping)
            elif first_input.replace(' ', '').lower() == 'n' and preference == "Free 2-Day Shipping":
                while True:
                    try:
                        shipping_free_status = input("Get products with free shipping (including 2-day) only? [Y/N]\n")
                        if shipping_free_status.replace(' ', '').lower() not in {'y', 'n'}:
                            raise InvalidInputException
                    except InvalidInputException:
                        print("Invalid input, please try again.\n")
                        continue
                    else:
                        if shipping_free_status.replace(' ', '').lower() == 'y':
                            link += "&free_shipping=true"
                        break
            break

# Here we call 'modify_url' multiple times
modify_url(url, "Search Term")
modify_url(url, "Free 2-Day Shipping")
modify_url(url, "Price Range")
modify_url(url, "Handmade Only")
modify_url(url, "Reverb Credits")
modify_url(url, "Preferred Sellers")

# Here, chromium headless browser is invoked (and downloaded upon first-time use) and scraping is performed
session = HTMLSession()
response = session.get(url)
response.html.render(sleep=1, keep_page=True, scrolldown=2) # sleep and scrolldown values may noy work, experiment further
products = response.html.find('.grid-card')

# Here, testing is done (will be removed when project completed)
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