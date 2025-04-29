from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import os
import re


options = Options()
options.add_argument("--lang=pt-BR") # Definir o idioma para Br

# Inicializa o Chrome e abre a página principal do IMDB
driver = webdriver.Chrome(options=options)
driver.get("https://www.imdb.com")
driver.maximize_window()

# Abre o menu de navegação
menu = driver.find_element(By.XPATH, r"//*[@id='imdbHeader-navDrawerOpen']")  # botão do menu
menu.click()
time.sleep(1)

# Seleciona o link para as 250 séries mais populares
link_populares = driver.find_element(By.LINK_TEXT, r'250 séries mais populares')
url = link_populares.get_attribute("href")  # captura a URL do link
driver.get(url)

# Localiza a lista de séries na página
tag_ul = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')  # lista em <ul>
lista_series = tag_ul.find_elements(By.TAG_NAME, "li")  # cada <li> é uma série

series_list = []
i = 0
for serie in lista_series:
    i += 1
    print(f"{i}/{len(lista_series)}", end="\r")  # mostra progresso

    titulo = str(serie.find_element(By.CLASS_NAME, "ipc-title__text").text.split(".", 1)[-1]).strip()
    link = serie.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute('href')
    ano = serie.find_element(By.XPATH, r'./div/div/div/div/div[2]/div[2]/span[1]').text
    imdb = float(serie.find_elements(By.CSS_SELECTOR, ".ipc-rating-star--imdb")[0].text.split("\n")[0].replace(",", "."))  # converte nota para float
    ep = int(serie.find_element(By.XPATH, r'./div/div/div/div/div[2]/div[2]/span[2]').text.split(" ")[0])  # número de episódios
    
    series_list.append({
        "titulo": titulo,
        "anolancamento": ano,
        "episodios": ep,
        "imdb": imdb,
        "link": link
    })

# Coleta detalhes de cada série (popularidade, elenco)
i = 0
for serie in series_list:
    i += 1
    print(f"Detalhando {i}/{len(series_list)}", end="\r")
    try:
        driver.get(serie['link'])  # abre página da série
        
        # Popularidade: formatação de milhar com pontos
        tag = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/section/section/div[3]/section/section/div[2]/div[2]/div/div[3]/a/span/div/div[2]/div').text
        serie['popularidade'] = int(tag.replace(".", ""))  # remove pontos e converte

        # Coleta elenco completo
        lista_elenco = driver.find_elements(By.CSS_SELECTOR, "[data-testid='title-cast-item']")
        elenco = [ator.find_element(By.CSS_SELECTOR, "[data-testid='title-cast-item__actor']").text for ator in lista_elenco]  # nomes dos atores
        serie["atores"] = elenco

        # Coleta personagens correspondentes
        personagens = [personagem.find_elements(By.CSS_SELECTOR, "[data-testid='cast-item-characters-link']")[0].text for personagem in lista_elenco]
        serie["personagens"] = personagens
    except Exception:
        print(f"Ator ou personagem vazio. {serie.get('titulo')}")  # log de erro
        continue

# Garante existência da pasta para salvar JSON
os.makedirs("json", exist_ok=True)
for serie in series_list:
    try:
        filename = re.sub('[^A-Za-z0-9]+', '', serie.get('titulo'))  # remove caracteres inválidos
        with open(f"json/{filename}.json", "w", encoding="utf-8") as arquivo:
            json.dump(serie, arquivo, ensure_ascii=False, indent=4)
    except FileNotFoundError as e:
        print(e)  # caso o nome seja inválido
        continue

# Encerra sessão do navegador
driver.quit()