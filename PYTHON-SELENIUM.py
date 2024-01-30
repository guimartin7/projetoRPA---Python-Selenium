from datetime import datetime
import csv
import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def carregar_dados():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    service = Service(executable_path='/usr/lib/chromium-browser/chromedriver')

    driver = webdriver.Chrome(options=options)

    driver.get('https://loja.nadir.com.br/?utm_source=Site_Coca&utm_medium=Coca-Cola-Brasil&utm_campaign=Site_Coca')

    titulos = driver.find_elements(By.XPATH, "//a[@class='product-item-link']")
    precos = driver.find_elements(By.XPATH, "//span[@class='price']")

    lista_titulos = [titulo.text for titulo in titulos]
    lista_precos = [preco.text for preco in precos]

    driver.quit()

    return lista_titulos, lista_precos

def imprimir_recibo(nome_arquivo):
    nome = input("Informe o nome: ")
    cpf = input("Informe o CPF: ")
    valor = input("Informe o valor do recibo: ")
    data = input("Informe a data do recibo (DD/MM/AAAA): ")
    data = datetime.strptime(data, "%d/%m/%Y")

    mes_extenso = retornar_mes_extenso(data.month)

    recibo_texto = f"""RECIBO DO PAGAMENTO
Recebi de {nome} 
CPF N º {cpf}
Valor R$ {valor}

Bauru, {data.day} de {mes_extenso} de {data.year}
"""

    with open(nome_arquivo, 'w') as file:
        file.write(recibo_texto)

def retornar_mes_extenso(mes):
    meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril',
        'Maio', 'Junho', 'Julho', 'Agosto',
        'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    return meses[mes - 1]

# Exemplo de utilização
lista_titulos = []
lista_precos = []

while True:
    print("\nMenu:")
    print("1 - CARREGAR DADOS DO SITE")
    print("2 - GERAR ARQUIVO CSV")
    print("3 - GERAR ARQUIVO XLSX")
    print("4 - IMPRIMIR RECIBO")
    print("5 - ENCERRAR SCRIPT")

    opcao = input("ESCOLHA UMA OPCAO: ")

    if opcao == '1':
        lista_titulos, lista_precos = carregar_dados()
        print("Dados do site carregados com sucesso!")

    elif opcao == '2':
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Produtos'
        sheet['A1'] = 'Produto'
        sheet['B1'] = 'Preço'
        for idx, (titulo, preco) in enumerate(zip(lista_titulos, lista_precos), start=2):
            sheet[f'A{idx}'] = titulo
            sheet[f'B{idx}'] = preco
        workbook.save('produtos.csv')
        print("Arquivo Excel 'produtos.xlsx' gerado com sucesso!")
        print("Arquivo CSV 'produtos.csv' gerado com sucesso!")

    elif opcao == '3':
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Produtos'
        sheet['A1'] = 'Produto'
        sheet['B1'] = 'Preço'
        for idx, (titulo, preco) in enumerate(zip(lista_titulos, lista_precos), start=2):
            sheet[f'A{idx}'] = titulo
            sheet[f'B{idx}'] = preco
        workbook.save('produtos.xlsx')
        print("Arquivo Excel 'produtos.xlsx' gerado com sucesso!")

    elif opcao == '4':
        nome_arquivo_recibo = input("Digite o nome do arquivo de recibo a ser gerado (ex: recibo.txt): ")
        imprimir_recibo(nome_arquivo_recibo)
        print(f"Arquivo de recibo '{nome_arquivo_recibo}' gerado com sucesso!")
        ## GERA UM ARQUIVO .TXT SALVO NO LOCAL DO ARQUIVO .PY

    elif opcao == '5':
        print("Encerrando o script...")
        break

    else:
        print("Opção inválida. Escolha uma opção válida.")
