import os
import dotenv 
import base64
import requests
import pandas as pd
import json
import html
from PIL import Image
from pathlib import Path
from openai import OpenAI
from html import unescape
from markdown import markdown
from bs4 import BeautifulSoup


from src.Categories import Category



#Cria string com palavras chaves que serão utilizadas para definir as categorias
categories_string = "; ".join([f"{category['slug']}: {category['keywords']}" for category in Category.all()])

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def encode_image(image_path):
    """função para codificar a imagem em base64""" 

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_image_base64(image_base64):

    response = client.chat.completions.create(
        model= "gpt-4-vision-preview",
        max_tokens=1000,
        messages= [
            {
                "role" : "system",
                "content" : [
                    {"type": "text", "text": "Return only JSON without any Markdown formatting or additional text."}
                ]
            },
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text", 
                        "text":   """
                            Return only JSON without any Markdown formatting or additional text.
                            Extraia dados deste recibo.

                            Retorne os dados como um objeto JSON com as seguintes chaves:
                            - 'date': A data da compra no formato americano, separado por traços
                            - 'store': O nome do negócio ou loja de onde é o recibo. Corrija se não estiver devidamente escrito ou capitalizado.
                            - 'amount': O total geral do recibo sem pontos ou símbolos de moeda. Se não tiver certeza, defina isso como uma string vazia; não tente calcular;
                            - 'description': Uma descrição geral do que foi comprado em português.
                            - 'category': Whichever category is most appropriate {categories_string}.
                            - 'payment-method': tente identificar os últimos 4 dígitos do cartão de crédito. Se não tiver certeza, defina isso como uma string vazia;
                            - 'items': uma lista com o nome de todos os itens comprados, com nome, categoria do produto, quantidade, valor unitário e valor total da linha
                            

                            converter números e datas para padrão americano
                            If you are unsure about any values, set them to an empty string
                            """
                    
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}",
                        },
                    },
                ],
            },
        ],
    )

    json_str = response.choices[0].message.content
    html_content = markdown(json_str)
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    text_content = html.unescape(text_content)

    data = json.loads(text_content)

    return data



def process_images_in_folder(folder_path):
    """Função para iterar sobre os arquivos em uma pasta e processá-los"""

    results = []  # Lista para guardar os objetos JSON retornados para cada imagem
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):

            image_base64 = encode_image(file_path) # Codificar a imagem para base64
            
            result_json = process_image_base64(image_base64) # Processar a imagem base64 e obter o objeto JSON
            results.append(result_json)
    
    df = pd.json_normalize(results) #Converter a lista de objetos JSON em um DataFrame do Pandas
    return df



# Processar as imagens e obter o DataFrame
folder_path = Path('./PFM-Python/upload')
df = process_images_in_folder(folder_path)


# Exportar o DataFrame para um arquivo Excel
excel_file_path = Path('./PFM-Python/output/arquivo.xlsx')
df.to_excel(excel_file_path, index=False)
