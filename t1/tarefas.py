# %%
import requests
from bs4 import BeautifulSoup
import time
import os
import csv
import json
import re

# %% [markdown]
# ## Tarefa 1

# %%
link_inicial = "https://pt.wikipedia.org"
limite_paginas = 5300

# %%
def coletar_links(url, limite):
    # Fila contém uma série de links (todos os links das páginas acessadas). Set contém os links únicos já visitados.
    fila = [url]
    visitados = set()
    salvos = 0

    # Se menos de 5k links foram guardados, conitnua execução
    while salvos < limite:
        try:
            # Acessa o último link inserido na fila
            atual = fila.pop()

            # Verifica se esse link já foi acessado. Se não, continua a execução e adiciona a lista de visitados.
            if atual in visitados: 
                continue

            # Carrega a página atual.
            req = requests.get(atual)
            soup = BeautifulSoup(req.text, 'html.parser')

            titulo = soup.select(".mw-page-title-main")
            nome_arquivo = titulo[0].text

            with open(f"pages/{nome_arquivo}.html", "w", encoding="utf-8") as file:
                conteudo = req.content.decode("utf-8")
                file.write(conteudo)
                visitados.add(atual)
                salvos += 1

            # Itera sobre todos os links da página atual.
            for link in soup.find_all('a', href=True):

                # Verifica se a página é um verbete.
                pagina = link['href']
                if pagina.startswith('/wiki/') and ':' not in pagina:

                    # Se algum dos links da página carregada já tiver sido visitada, pula.
                    link_atual = 'https://pt.wikipedia.org' + pagina
                    if link_atual in visitados:
                        continue
                    # Adiciona todos que forem verbetes à fila. O último link coletado será a próxima página a ser aberta.
                    fila.append('https://pt.wikipedia.org' + pagina)

            print(f"{salvos} - {salvos-len(os.listdir("pages/"))}", end="\r")
            # time.sleep(0.6)

        # Evita páginas sem título (titulo[0].text)
        except IndexError:
            continue

        # Evita erros de mal formatação de título
        except FileNotFoundError:
            continue

    return list(visitados)

links = coletar_links(link_inicial, limite_paginas)

# %%
with open("links.csv", "w", newline="") as file:
    writer = csv.writer(file)
    fields = ["links"]
    writer.writerow(fields)
    for link in links:
        writer.writerow([link])

# %% [markdown]
# ## Tarefa 2

# %%
def create_json(url):
    
    # Carrega a página atual
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser")
    
    # Busca e verifica se há infobox na página carregada
    conteudo_principal = bs.find("div", class_="mw-parser-output")
    tabela = conteudo_principal.find("table", class_="infobox infobox_v2") if conteudo_principal else None
    
    if tabela:
        trs = tabela.find_all("tr")
        
        # Limpa e formata o título para ser usado como nome do arquivo
        titulo = trs[0].text.strip()
        titulo = re.sub(r'[^\w\s-]', '', titulo)  # remove caracteres especiais
        titulo = re.sub(r'\s+', '_', titulo)      # substitui espaços por underlines
        
        
        dicionario = {}
        
        # Itera sobre as linhas da infobox pegando chave e valor
        for tr in trs[1:]:
            tds = tr.find_all('td')
            if len(tds) == 2:
                chave = tds[0].text.strip()
                
                # extrai o texto da célula usando \n como separador
                valor = tds[1].get_text(separator='\n', strip=True)
                valor = re.sub(r'\[\d+\]', '', valor)  # Remove referências como [1], [2], etc.
                
                # divide o valor em uma lista e remove as linhas vazias e espaços em branco
                itens = valor.split('\n')
                itens = [item.strip() for item in itens]
                itens = [item for item in itens if item]
                
                
                if len(itens) == 1:
                    dicionario[chave] = itens[0]
                else:
                    dicionario[chave] = itens
        
        
        with open(f"jsons/{titulo}.json", 'w') as f:
            json.dump(dicionario, f, indent=2, ensure_ascii=False)

# %%
# Executa a função para cada link gerado pelo crawler.
i = 0
for link in links:
    create_json(link)
    print(i, end="\r")
    i+=1