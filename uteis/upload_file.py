import logging
import pandas as pd
import requests
import csv
import awswrangler as wr

class MotorEmbrapaGrupo37:
    def __init__(self, file_name):
        self.file_name = file_name

    def getDataEmbrapa(self):
        try:
            # Ler o arquivo JSON que contém as URLs e separadores
            urls = pd.read_json('urls.json')
            url = urls.loc[urls.database == self.file_name, "url"].values[0]
            sep = urls.loc[urls.database == self.file_name, "sep"].values[0]

            # Fazer uma solicitação GET para a URL
            response = requests.get(url)
            if response.status_code == 200:
                # Obter o conteúdo da resposta
                content = response.content
                decoded_content = content.decode('utf-8')
                # Ler o conteúdo decodificado como um arquivo CSV usando o separador especificado
                cr = csv.reader(decoded_content.splitlines(), delimiter=sep)
                dados = list(cr)
                logging.info("CSV baixado com sucesso. Iniciando upload para o S3.")
                
                # Salvar o DataFrame no S3 como CSV
                path = f's3://nome-bucket/nome_pasta/{self.file_name}'
                wr.s3.to_csv(dados, path, index=False)
                logging.info("Upload para o S3 concluído com sucesso.")
                message = "DataFrame atualizado e enviado para o S3 com sucesso!"
                return message
        except Exception as e:
            logging.error(f"Erro ao fazer upload para o S3: {e}")
            return f"Erro ao fazer upload para o S3: {e}"
