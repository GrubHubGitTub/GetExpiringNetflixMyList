import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#   -----------CHOOSE WEBDRIVER (REMOVE HEADLESS OPTION TO SEE SELENIUM RUNNING)------------
install("webdriver-manager")

# # CHROME DRIVER USE THIS:
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # EDGE DRIVER USES THIS:
# from selenium.webdriver.edge.service import Service
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.edge.options import Options
# options = Options()
# options.add_argument("headless")
# driver = webdriver.Edge(service = Service(EdgeChromiumDriverManager().install()), options=options)

#-------change env path and variables------------
install("python-dotenv")
from dotenv import load_dotenv
load_dotenv(".env")

# enter your Netflix email/phone number
email = os.getenv("email")
# enter your Netflix password
pw = os.getenv("pw")
# enter your profile name exactly as it appears on Netflix
user_profile = os.getenv("user_profile")
# enter your rapid api key (it's free)
api_key = os.getenv("api_key")
# Change your country code (see readme for list of countries)
country = os.getenv("country")


def get_my_list():

    # go to netflix
    print("Going to Netflix...")
    driver.get("https://www.netflix.com")

    # click login button
    print("Entering Login info")
    current_url = driver.current_url
    login_button = driver.find_element(By.CLASS_NAME, "authLinks")
    login_button.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # sign in
    current_url = driver.current_url
    email_input = driver.find_element(By.NAME, "userLoginId")
    pw_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(email)
    pw_input.send_keys(pw)

    sign_in_button = driver.find_element(By.CLASS_NAME, "login-button")
    sign_in_button.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # choose profile by profile name
    print("Choosing your profile")
    profiles = driver.find_elements(By.CLASS_NAME, "profile")
    for profile in profiles:
        name = profile.find_element(By.CLASS_NAME, "profile-name").text
        if name == user_profile:
            profile_link = profile.find_element(By.CLASS_NAME, "profile-link")
            profile_link.click()
            break
    sleep(2)

    # click my list
    print("Finding your list")
    current_url = driver.current_url
    my_list = driver.find_element(By.LINK_TEXT,"My List")
    my_list.click()
    WebDriverWait(driver, 15).until(EC.url_changes(current_url))

    # scroll down my list to load all titles
    logo = driver.find_element(By.CLASS_NAME,"logo")
    for n in range(1, 10):
        print("Getting list of movies...")
        logo.send_keys(Keys.END)
        sleep(1)

    # return list of movies:
    movies_div = driver.find_elements(By.CLASS_NAME,"title-card")
    movie_titles = [div.find_element(By.CSS_SELECTOR, 'a').get_attribute("aria-label") for div in movies_div]
    driver.quit()
    return movie_titles

def get_expiring_movies():
    url = "https://unogsng.p.rapidapi.com/expiring"
    querystring = {"countrylist":country}
    headers = {
        'x-rapidapi-host': "unogsng.p.rapidapi.com",
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











