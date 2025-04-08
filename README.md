# Coleta de Dados na Wikipedia

#### Gustavo Losch do Amaral, Henrique Mayer e Rian Cordoni

---

### Descrição

Este projeto tem como objetivo realizar a coleta de dados da Wikipedia em português. A partir de um link inicial, o programa percorre páginas, coleta os HTMLs e extrai informações presentes nas infoboxes.

 - Link para o repositório com as páginas HTML e infoboxes JSON. [OneDrive PUCRS](https://brpucrs-my.sharepoint.com/:f:/g/personal/g_losch_edu_pucrs_br/Eo7XukX5plRArdYoi2k1VU0BWd2qCfNOJWd0uSHKvZz2vQ?e=IvaoZ7)

---

### Instruções para o uso do programa

1. Crie um ambiente virtual utilizando o `python 3.12` com o gerenciador de pacotes `anaconda`:

```shell
conda create --name <nome-do-ambiente> python=3.12
conda activate <nome-do-ambiente>
```

2. Estando na pasta raíz do projeto, instale as dependências necessárias para que o código funcione com o seguinte comando:

```shell
pip install -r requirements.txt
```

3. Crie as pastas `pages` e `jsons` na pasta raíz do projeto, nesses diretórios as páginas HTML e JSON serão salvos.

4.  Abra o arquivo `t1cpa.ipynb` (notebook) no Jupyter.

5.  Modifique os seguintes parâmetros:
    - `link_inicial`: O link da página inicial da Wikipedia que deseja começar a coleta.
    - `limite_paginas`: O limite de páginas a serem coletadas pelo crawler.

    Exemplo de uso:

    ```python
    pagina_inicial = "https://pt.wikipedia.org"
    limite_paginas = 5000
    ```

6. Execute os blocos do notebook em ordem.

**Resultado**

- Os links coletados ficarão salvos em um arquivo `links.csv` para que seja possível acessar os links salvos sem ter que executar o código novamente.
- Os HTMLs das páginas serão salvos em arquivos `.html` na pasta `pages/`.
- As infobox extraídas serão salvas em arquivos `.json` na pasta `jsons/`.