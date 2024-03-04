from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars"

browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)

scraped_data = []

soup = BeautifulSoup()

def scrape():
    bright_star_table = soup.find("table", attrs={"class", "wikitable"})
    table_body = bright_star_table.find("tbody")
    table_rows = table_body.find_all("tr")

    for row in table_rows:
        table_cols = row.find_all("td")
        print(table_cols)

        temp_list=[]

        for col_data in table_cols:
            print(col_data.text)

            data = col_data.text.strip()
            print(data)

            temp_list.append(data)

        scraped_data.append(temp_list)

stars_data=[]

for i in range(0,len(scraped_data)):
    Star_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]

    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)

headers = ["Star_name", "Distance", "Mass", "Radius", "Luminosity"]
star_df_1 = pd.DataFrame(stars_data, columns = headers)

star_df_1.to_csv("scraped_data.csv", index=True, index_label = "id")

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        
        stars_data.append(temp_list) 

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

    Star_name=[]
    Distance=[]
    Mass=[]
    Radius=[]
    Luminosity=[]

    for i in range(1,6):
        Star_name.append(temp_list[i][1])
        Distance.append(temp_list[i][2])
        Mass.append(temp_list[i][3])
        Radius.append(temp_list[i][4])
        Luminosity.append(temp_list[i][5])

new_stars_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_stars_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")