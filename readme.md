# Expiring Movies on your Netflix My List

## Annoyed at Netflix for taking away your movies? 

### This tool checks your My List with movies that are about to expire. 

------
## Installation instructions
Install selenium

Choose your webdriver by commenting out the one you do not need. (Pre confiugured for Edge and Chrome drivers).

Create a .env file with:

- email= "yournetflixemail@gmail.com"
- pw= "password"
- user_profile= "Kids"
- api_key= "RAPID API KEY HERE" 
- country= "000" 

Get your free UNOGSNG rapid API key here: https://rapidapi.com/unogs/api/unogsng/

List of countries:
(if your country is not there, choose one that is geographically closest.)

{'Argentina ': 21, 'Australia ': 23, 'Belgium ': 26, 'Brazil ': 29, 'Canada ': 33, 'Switzerland ': 34, 'Germany ': 39, 'France ': 45, 'United Kingdom': 46, 'Mexico ': 65, 'Netherlands ': 67, 'Sweden ': 73, 'United States': 78, 'Iceland ': 265, 'Japan ': 267, 'Portugal ': 268, 'Italy ': 269, 'Spain ': 270, 'Czech Republic ': 307, 'Greece ': 327, 'Hong Kong ': 331, 'Hungary ': 334, 'Israel ': 336, 'India ': 337, 'South Korea': 348, 'Lithuania ': 357, 'Poland ': 392, 'Romania ': 400, 'Russia': 402, 'Singapore ': 408, 'Slovakia ': 412, 'Thailand ': 425, 'Turkey ': 432, 'South Africa': 447}

## Run main.py. 

###Should work on lists up to 1000 titles. If you have more, clean that list up! 