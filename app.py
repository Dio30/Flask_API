from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from pytz import timezone
import locale

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscar_pokemon', methods= ['GET', 'POST'])
def buscar_pokemon():
    pesquisar = request.form["nome"].lower()
    try:
        link = json.loads(requests.get(f'https://pokeapi.co/api/v2/pokemon/{pesquisar}').text)
        id=link['id']
        nome_pokemon = link['name']
        
        resultado = link['sprites']
        foto = resultado['front_default']
        
        result = link['types'][0]
        result1 = result['type']
        tipo = result1['name']
        
        result2 = link['abilities'][1]
        result3 = result2['ability']
        abilidades = result3['name']
        return render_template('index.html', nome_pokemon=nome_pokemon, foto=foto, tipo=tipo, id=id, abilidades=abilidades)
    
    except:
       return render_template('index.html')
    
@app.route('/buscar_cep', methods= ['GET', 'POST'])
def buscar_cep():
    cep = request.form['cep']
    try:
        link = requests.get(f'https://cep.awesomeapi.com.br/json/{cep}')
        resposta = link.json()
        cidade = resposta['city']
        endereco = resposta['address']
        bairro = resposta['district']
        estado = resposta['state']
        return render_template('index.html', cidade=cidade, endereco=endereco, bairro=bairro, estado=estado)
    
    except:
        return render_template('index.html')
    
@app.route('/consultar_dolar', methods=['GET','POST'])
def consultar_dolar():
    link = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'
    moeda = 'USDBRL'
    requisicao = requests.get(link)
    resposta = requisicao.json()
    nome = resposta[moeda]['name']
    valor = float(resposta[moeda]['high']).__round__(2)
    return render_template('conversor_moeda.html', nome=nome, valor=valor)

@app.route('/consultar_euro', methods=['GET','POST'])
def consultar_euro():
    link = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'
    moeda = 'EURBRL'
    requisicao = requests.get(link)
    resposta = requisicao.json()
    nome_euro = resposta[moeda]['name']
    valor_euro = float(resposta[moeda]['high']).__round__(2)
    return render_template('conversor_moeda.html', nome_euro=nome_euro, valor_euro=valor_euro)

@app.route('/previsao_tempo', methods=['GET', 'POST'])
def previsao_tempo():
    API_key = 'd7c5eb336a9f9bea2f44c4e2cc117f48'
    try:
        cidade = request.form["cidade"].lower()
        link = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_key}&units=metric&lang=pt_br'
        requisicao = requests.get(link)
        resposta = requisicao.json()
        tempo = float(resposta['main']['temp']).__round__()
        maxima = float(resposta['main']['temp_max']).__round__(1)
        minima = float(resposta['main']['temp_min']).__round__(1)
        país = resposta['sys']['country']
        umidade = resposta['main']['humidity']
        nome = resposta['name']
        descricao = resposta['weather'][0]['description']
        imagem = resposta['weather'][0]['icon']
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone('America/Sao_Paulo')
        data_fuso = data_e_hora_atuais.astimezone(fuso_horario)
        data_e_hora = data_fuso.strftime('%A - %d de %B de %Y').capitalize()
        return render_template('previsao_tempo.html', tempo=tempo, nome=nome, país=país, descricao=descricao, 
        maxima=maxima, minima=minima, imagem=imagem, umidade=umidade, data_e_hora=data_e_hora)
    except:
        return render_template('previsao_tempo.html')
    
@app.route('/temperatura_atual', methods=['GET', 'POST'])
def temperatura_atual():
    API_key ='69ff49bb1923631054fc3297f5f230df'
    try:
        cidade = request.form["temperatura"].lower()
        link = f'http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={cidade}&token={API_key}'
        requisicao = requests.get(link)
        resposta = requisicao.json()
        nome = resposta['name']
        return render_template('temperatura_atual.html', nome=nome)
    except:
        return render_template('temperatura_atual.html')
    
if __name__ == '__main__':
    app.run(debug=True)