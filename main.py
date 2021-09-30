import requests
import selenium as s
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
import os
import subprocess
import sys
# delete this or change the path to load your own .env file (pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv("C:/New/.env")
#-------------------------------------

# enter your Netflix email/phone number
email = os.getenv("email")
# enter your Netflix password
pw = os.getenv("pw")
# enter your profile name exactly as it appears on Netflix
user_profile = os.getenv("user_profile")
# enter your rapid api key (it's free)
api_key = os.getenv("api_key")
# Change your country code (see readme for list of countries)
country = "425"


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("webdriver-manager")
from webdriver_manager.chrome import ChromeDriverManager

def get_my_list():
    # selenium setup- change path to your webdriver
    op = s.webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)

    # go to netflix
    print("Going to Netflix...")
    driver.get("https://www.netflix.com")

    # click login button
    print("Entering Login info")
    current_url = driver.current_url
    login_button = driver.find_element_by_class_name("authLinks")
    login_button.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # sign in
    current_url = driver.current_url
    email_input = driver.find_element_by_name("userLoginId")
    pw_input = driver.find_element_by_name("password")
    email_input.send_keys(email)
    pw_input.send_keys(pw)
    sign_in_button = driver.find_element_by_class_name("login-button")
    sign_in_button.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # choose profile by profile name
    print("Choosing your profile")
    profiles = driver.find_elements_by_class_name("profile")
    for profile in profiles:
        name = profile.find_element_by_class_name("profile-name").text
        if name == user_profile:
            profile_link = profile.find_element_by_class_name("profile-link")
            profile_link.click()
            break
    sleep(2)

    # click my list
    print("Finding your list")
    current_url = driver.current_url
    my_list = driver.find_element_by_link_text("My List")
    my_list.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # scroll down my list to load all titles
    logo = driver.find_element_by_class_name("logo")
    for n in range(1, 10):
        print("Getting list of movies...")
        logo.send_keys(Keys.END)
        sleep(1)

    # return list of movies:
    movies_div = driver.find_elements_by_class_name("title-card")
    movie_titles = [div.find_element_by_css_selector('a').get_attribute("aria-label") for div in movies_div]
    return movie_titles

def get_expiring_movies():
    url = "https://unogsng.p.rapidapi.com/expiring"
    # CHANGE COUNTRY TO YOUR ID FROM API
    querystring = {"countrylist":country}

    headers = {
        'x-rapidapi-host': "unogsng.p.rapidapi.com",
        # GET YOUR OWN KEY FOOL
        'x-rapidapi-key': api_key
        }
    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    movie_dicts = data["results"]
    expiring_movies = {movie["title"]:movie["expiredate"] for movie in movie_dicts}
    return expiring_movies

my_list = get_my_list()
expiring_movies = get_expiring_movies()

my_expiring_movies = {}
for movie in expiring_movies:
    if movie in my_list:
        my_expiring_movies[movie] = expiring_movies[movie]

if len(my_expiring_movies) > 0:
    print(my_expiring_movies)
else:
    print("Lucky you! Nothing is about to expire. Check back in a week.")











