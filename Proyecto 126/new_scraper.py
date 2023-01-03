from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

# Enlace a NASA Exoplanet
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Controlador web
browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

new_planets_data = []

def scrape_more_data(hyperlink):
    try:
        ## AGREGA CÓDIGO AQUÍ ##
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []

        for tr_tag in soup.find_all("tr"):
            td_tags = tr_tag.find_all("td")

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs = {"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")

        new_planets_data.append(temp_list)
    
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

planet_df_1 = pd.read_csv("scraped_data.csv")

# Llamar al método
for index, row in planet_df_1.iterrows():

    ## ADGREGA CÓDIGO AQUÍ ##
    print(row["hyperlink"])
    scrape_more_data(row["hyperlink"])

    print(f"La extracción de datos del hipervínculo {index+1} se ha completado")

print(new_planets_data)

# Remover el carácter '\n' de los datos extraídos
scraped_data = []

for row in new_planets_data:
    replaced = []

    ## AGREGAR EL CÓDIGO AQUÍ ##
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)

    scraped_data.append(replaced)

df = df.drop(columns = ["NaN"], inplace = True)
df["Radius"] = df["Radius"] * (0.102763)
df["mass"] = df["mass"] * (0.000954588  )
print(scraped_data)

headers = ["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convertir a CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

merge_df = pd.merge("new_scraped_data.csv", "scraped_data.csv")
df.tail(10)

merge_df.to_csv("merge_df.csv")