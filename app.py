from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscar', methods= ['GET', 'POST'])
def buscar():
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
    return render_template('index.html', nome=nome, valor=valor)

@app.route('/consultar_euro', methods=['GET','POST'])
def consultar_euro():
    link = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL'
    moeda = 'EURBRL'
    requisicao = requests.get(link)
    resposta = requisicao.json()
    nome_euro = resposta[moeda]['name']
    valor_euro = float(resposta[moeda]['high']).__round__(2)
    return render_template('index.html', nome_euro=nome_euro, valor_euro=valor_euro)
    
if __name__ == '__main__':
    app.run(debug=True)