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

# Here is the code for the user input dialog, where we call 'modify_url' multiple times and provide CSV commands
modify_url(url, "Search Term")
modify_url(url, "Free 2-Day Shipping")
modify_url(url, "Price Range")
modify_url(url, "Handmade Only")
modify_url(url, "Reverb Credits")
modify_url(url, "Preferred Sellers")
output_csv = False
while True:
    try:
        csv_status = input("Output CSV file? [Y/N]\n")
        if csv_status.replace(' ', '').lower() not in {'y', 'n'}:
            raise InvalidInputException
    except InvalidInputException:
        print("Invalid input, please try again.\n")
        continue
    else:
        if csv_status.replace(' ', '').lower() == 'y':
            output_csv = True
        break

# Here, chromium headless browser is invoked (and downloaded upon first-time use) and scraping is performed
session = HTMLSession()
response = session.get(url)
response.html.render(sleep=1, keep_page=True, scrolldown=2) # sleep and scrolldown values may noy work, experiment further
products = response.html.find('.grid-card')

count = 0 # For testing purposes only (this value should be 60)
pedal_data = []
if output_csv is True:
    # Here, the data stored in 'products' will be parsed
    csv_file = ""
    csv_header = "name,price,condition,country,shipping,link\n"
    csv_observations = ""
    for product in products:
        csv_line = ""
        text = product.text # product text that will be parsed
        if text[:12] == "Reverb Bump\n": # this step removes "Reverb Bump\n" if it exists, because we don't need it
            text = text[12:]
        link_set = product.absolute_links # the set containing the link to the product
        link = "" # the link to the product
        for link_str in link_set: # extracting the link from the set with the link
            link = link_str
        csv_line_list = text.split('\n')

        # cleaning up price values in csv_line_list
        for token in csv_line_list:
            if token[0] == '$':
                if "% Off" in token or "% price drop" in token:
                    csv_line_list.remove(token)
                else:
                    if ',' in token:
                        new_token = token.replace(',', '')
                        csv_line_list[csv_line_list.index(token)] = new_token

        # adding to pedal_data
        pedal_data.append(csv_line_list)

        name, price, condition, country, shipping = csv_line_list[0], csv_line_list[1], csv_line_list[2], \
            csv_line_list[3], "Paid"
        if "Free Shipping" in csv_line_list or "Free 2-Day Shipping" in csv_line_list:
            shipping = csv_line_list[4]
        csv_line += name + ',' + price + ',' + condition + ',' + country + ',' + shipping + ',' + link + '\n'
        csv_observations += csv_line
        count += 1
        print(text + '\n')
    # Note: the last line of the CSV file is just a newline character (blank line)
    csv_file = open("pedal-scraper.csv", "w")
    csv_file.write(csv_header)
    csv_file.write(csv_observations)
    csv_file.close()
    print(str(count) + " products scraped.\nThe outputted CSV file is in the same parent directory as this script.")
else:
    print(str(count) + " products scraped.\n")

# This section of code writes the statistical summary of the pedals to stdout
print(pedal_data)


# The first line in pedal['name'] (the part before the first occurring '\n' character) is either 'Reverb Bump' or the
# name of the pedal. This means that we must first check to see if the first line in 'Reverb Bump' or not. However, we
# have no use for 'Reverb Bump' concerning our purposes, so we only check for the purposes of accurately extracting the
# name of the pedal.
# We need:
    # name (always)
    # price (always)
        # '$xCAD'. We know that currency codes are always 3 characters long and the dollar sign is one character long
    # condition (always)
        # Brand New
        # Used - B-Stock
        # Used - Mint
        # Used - Excellent
        # Used - Very Good
        # Used - Good
        # Used - Fair
        # Used - Poor
        # Used - Non Functioning
    # country (always)
    # shipping (optional)
        # Free 2-Day Shipping
        # Free Shipping
        # Paid
    # link (always)