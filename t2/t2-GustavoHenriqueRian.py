from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
import os
import re

driver = webdriver.Firefox()
driver.get("https://www.imdb.com")
driver.maximize_window()

menu = driver.find_element(By.XPATH, r"//*[@id='imdbHeader-navDrawerOpen']")
menu.click()
time.sleep(1)

link_populares = driver.find_element(By.LINK_TEXT, r'250 séries mais populares')
url = link_populares.get_attribute("href")
driver.get(url)

tag_ul = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')
lista_series = tag_ul.find_elements(By.TAG_NAME, "li")

series_list = []
i=0
for serie in lista_series:
    i+=1
    print(f"{i}/{len(series_list)}", end="\r")

    titulo = str(serie.find_element(By.CLASS_NAME, "ipc-title__text").text.split(".", 1)[-1]).strip()
    link = serie.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute('href')
    ano = serie.find_element(By.XPATH, r'./div/div/div/div/div[2]/div[2]/span[1]').text
    imdb = float(serie.find_elements(By.CSS_SELECTOR, ".ipc-rating-star--imdb")[0].text.split("\n")[0].replace(",","."))
    ep = int(serie.find_element(By.XPATH, r'./div/div/div/div/div[2]/div[2]/span[2]').text.split(" ")[0])
    
    series_list.append({
         "titulo": titulo,
         "anolancamento": ano,
         "episodios": ep,
         "imdb": imdb,
         "link": link
        })
    
i=0
for serie in series_list:
    i+=1
    print(f"{i}/{len(series_list)}", end="\r")
    try:
        driver.get(serie['link'])
        
        tag = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/section/section/div[3]/section/section/div[2]/div[2]/div/div[3]/a/span/div/div[2]/div').text
        serie['popularidade'] = int(tag.replace(".",""))

        lista_elenco = driver.find_elements(By.CSS_SELECTOR, "[data-testid='title-cast-item']")
        
        elenco = [ator.find_element(By.CSS_SELECTOR, "[data-testid='title-cast-item__actor']").text for ator in lista_elenco]
        serie["atores"] = elenco

        personagens = [personagem.find_elements(By.CSS_SELECTOR, "[data-testid='cast-item-characters-link']")[0].text for personagem in lista_elenco]
        serie["personagens"] = personagens
    except:
        print(f"Ator ou personagem vazio. {serie.get('titulo')}")
        continue

os.makedirs("json", exist_ok=True)
for serie in series_list:
    try:
        with open(f"json/{re.sub('[^A-Za-z0-9]+', '', serie.get('titulo'))}.json", "w", encoding="utf-8") as arquivo:
            json.dump(serie, arquivo, ensure_ascii=False, indent=4)
    except FileNotFoundError as e:
        print(e)
        continue

driver.quit()