# ScrapinNoodles 

Hello, 

in this project we will be working in a scraping tool written in Python and using very powerfull tools to extract data from a website without the need to 
click and see each page at the time. 

To run this project we will require the following modules to be installed.

- selenium 4.6,
- pandas 1.5.1,
- beautifulsoup4 4.11.1

## As the project is written in Python, these packages can be easily installed by running the commands:
	python - m pip install selenium
	python - m pip install beautifulsoup 4
	python - m pip install pandas

# We also require a driver for the search engine to use during the scraping proccess.
Here you can find the links to the downloads. Remember to place the drivers in the same directory where you store the script.

## Download driver for Firefox from:
https://github.com/mozilla/geckodriver/releases

## Download driver for Chrome from:
https://chromedriver.chromium.org/downloads

### Before diving into the few lines of code, please consider the following: 

1. The first thing to do before trying to write a crawler or a scraping script is to check the website from which you are going top extract the data.
See if the website offers you any tool to minimize your work.

2. In our test case, the website give us an "advance search" tool which we can use to minimize the range of criteria for our code to match in order to fetch 
a certain amount of data which we want to extract.

3. By doing so, and using the "advance search" we will not just gain knowledge of the website but also some interesting intel:
	a. A base url for us to use as an starting point.
	b. A quantity of items/results for us to use as a goal.
	c. To determine weather or not we will have to fecth data from the HTML or if we can do it from the API as a Json format.

### The project contains 4 helpers methods which functionalities are explained in the code. 
### Below are examples of 2 of them:

#### a. def string_space_reductor() is a function that takes a extracted string like:

    """Stock 

        # 
            1168CWY"""

and returns it like:

    """Stock#1168CWY""".

#### b. def return_formatted(spec_el) ia a function that takes a string like:


    "Length (ft) 8 in 0", or "(N/A)" 
    
and if string is not equal to "(N/A)" it:

1. Finds a title which is located in span, nested in a div of class "specs"
2. it reduce all the spaces of the string 
3. it strip() the string of the title
 
and return spec value (without the spec title), or ("N/A").


#### Once the code is executed, it will export a CSV and XLSX files with the extracted data for analisis.
#### The execution of this code generates results for 1000 RVS.



