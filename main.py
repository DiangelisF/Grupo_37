from flask import Flask, request, jsonify
#from uteis.load_file import MotorEmbrapaGrupo37
import logging
import pandas as pd
import requests
import csv
#import awswrangler as wr

app = Flask(__name__)

class MotorEmbrapaGrupo37:
  def __init__(self, file_name):
    self.file_name = file_name

  def getDataEmbrapa(self):
    try:
      urls = pd.read_json('urls.json')
      url = urls.loc[urls.database == self.file_name, "url"].values[0]
      sep = urls.loc[urls.database == self.file_name, "sep"].values[0]

      response = requests.get(url)

      if response.status_code == 200:
        content = response.content
        decoded_content = content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=sep)
        dados = list(cr)
        logging.info("CSV baixado com sucesso. Iniciando upload para o S3.")
        
        # # Salvar o DataFrame no S3 como CSV
        # path = f's3://fabricio-my-tf-test-bucket/fiap_testes/{self.file_name}'
        # wr.s3.to_csv(dados, path, index=False)
        logging.info("Upload para o S3 concluído com sucesso.")
        message = "DataFrame atualizado e enviado para o S3 com sucesso!"
        return message
      
    except Exception as e:
      logging.error(f"Erro ao fazer upload para o S3: {e}")
      return f"Erro ao fazer upload para o S3: {e}"


@app.route('/upload-file', methods=['GET'])
def get_s3():
    """
    Rota GET para baixar um arquivo CSV de uma URL e salvar no S3.

    O nome do arquivo CSV é passado como um parâmetro de consulta na URL.
    Exemplo: http://127.0.0.1:5000/upload-file?file_name=producao

    Returns
    -------
    Response
        Resposta JSON com mensagem indicando o sucesso ou falha da operação e o código de status HTTP.
    """
    logging.info("Recebida solicitação GET para baixar o arquivo e salvar no S3.")

    file_name = request.args.get('file_name', default='producao')

    message = MotorEmbrapaGrupo37(file_name).getDataEmbrapa()

    print(dados)
    
    return jsonify(message=message), 200


if __name__ == '__main__':
    """
    Inicializa o servidor Flask.
    """
    logging.info("Iniciando o servidor Flask.")
    app.run(debug=True)