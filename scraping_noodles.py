from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as to_file

# Download driver for Firefox from:
# https://github.com/mozilla/geckodriver/releases
driver = webdriver.Firefox()
# Download driver for Chrome from:
# https://chromedriver.chromium.org/downloads

# Declaration of container data types for our extracted data.
names, statuses, dealers, stock_numbers, lengths, sleep_places, slide_outs, mileages, prices = [], [], [], [], [], [], [], [], []

# Variable that stores the number of current page.
page = 1
# Variable that stores the id of tag element which contains the data to extract.
pagination_container_id = 1


# Function that checks if tag element exists in the content of the extracted data.
def check_if_none(tag_element):
    if tag_element is not None:
        if len(tag_element.text) >= 1:
            return tag_element.text.strip()
        else:
            return tag_element
    else:
        # if tag element is None, return N/A (not applicable)
        return "(N/A)"


# Function that eliminates the unnecessary blank spaces from extracted text data, taking in consideration each new line.
def string_space_reductor(str_object):
    spaceless_str = []
    for line in str_object.split("\n"):
        spaceless_str.append(line.strip())
    # merge the list to a string
    return ("".join(spaceless_str))


# Function that formats spec element text, and strips it from the title,
# leaving only the value that we are interested in.
def return_formatted(spec_el):
    if check_if_none(spec_el) == "(N/A)":
        return check_if_none(spec_el)
    else:
        el_title = spec_el.find('span').text
        el_stripped = string_space_reductor(spec_el.text)
        el_formatted = el_stripped.strip(el_title)
        return el_formatted


# Function that adds a specific extracted data to its assigned container.
def append_specs(specs_list, lengths, sleep_places, slide_outs, mileages):
    specs_results_list = [lengths, sleep_places, slide_outs, mileages]
    # if elements status is "New" then the specs list does not include mileages
    if len(specs_list) == 3:
        specs_list.append(None)
    spec_index = 0
    while spec_index != len(specs_list):
        for spec in specs_list:
            specs_results_list[spec_index].append(return_formatted(spec))
            spec_index += 1


# Main logic for scraping our data.
while page != 51:
    base_url = "https://rv.campingworld.com/searchresults?external_assets=false&rv_type=motorized&condition=new_used&subtype=A,AD,B,BP,C&floorplans=class-a,cafl,cabh,cab2,carb,cath,carl,class-b,cbbh,cbfl,cbrb,cbrl,class-c,ccbh,ccfl,ccth,ccbaah,ccrb,ccrl&slides_max=&fueltype=diesel&sort=price_desc&zipsearch=true&zip=10001&forcedistance=Any&search_mode=advanced&locations=nationwide&page={0}".format(
        page)
    driver.get(base_url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    while pagination_container_id > 0:
        for element in soup.findAll('div',
                                    attrs={'id': 'pagination_container_{0}'.format(str(pagination_container_id))}):
            name = element.find('span', attrs={'itemprop': 'name'})
            status = element.find('span', attrs={'class': 'status'})
            dealer = element.find('span', attrs={'class': 'stock-results'})
            stock_number = dealer.find_next_sibling('span')
            price = element.find('span', attrs={'class': 'price-info low-price'})
            specs_list = element.findAll('div', attrs={'class': 'specs'})
            append_specs(specs_list, lengths, sleep_places, slide_outs, mileages)
            names.append(check_if_none(name))
            statuses.append(check_if_none(status))
            dealers.append(string_space_reductor(check_if_none(dealer)))
            stock_numbers.append(string_space_reductor(check_if_none(stock_number)))
            prices.append(check_if_none(price))
            pagination_container_id += 1
        if pagination_container_id == 21:
            break
    page += 1
    pagination_container_id = 1

# Use of pandas module to create a dataframe based on our data containers.
to_file = to_file.DataFrame(
    {'RVS Name:': names, 'New or Used:': statuses, 'Dealer location': dealers, 'Stock number': stock_numbers,
     'Length in feet:': lengths, 'Sleep places': sleep_places,
     'Slide Outs:': slide_outs, 'Milage': mileages, 'Sale Price': prices})
# Exporting our data to a CSV file.
to_file.to_csv('rvs_campingworld.csv', index=True, encoding='utf-8')
# Exporting our data to a Excel file.
to_file.to_excel('rvs_campingworld.xlsx')

# Uncomment this line if you want the browser to close after execution of this code.
driver.close()
