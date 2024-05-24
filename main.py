from flask import Flask, request, jsonify
import logging
from uteis.upload_file import MotorEmbrapaGrupo37

app = Flask(__name__)

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
    
    return jsonify(message=message), 200


if __name__ == '__main__':
    """
    Inicializa o servidor Flask.
    """
    logging.info("Iniciando o servidor Flask.")
    app.run(debug=True)
