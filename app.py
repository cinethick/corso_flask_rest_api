from flask import Flask, jsonify, request

app = Flask(__name__)

negozi = [
    {
        'nome': 'Il mio negozio',
        'oggetti': [
            {
                'nome': 'Il mio oggetto',
                'prezzo': 15.99
            }
        ]
    }
]


@app.post('/negozio')
def crea_negozio():
    dati_richiesta = request.get_json()
    nuovo_negozio = {
        'nome': dati_richiesta['nome'],
        'oggetti': dati_richiesta.get('oggetti', [])
    }
    negozi.append(nuovo_negozio)
    return jsonify(nuovo_negozio)


@app.route('/negozio/<string:nome>')
def vedi_negozio(nome):
    negozio_richiesto = [negozio for negozio in negozi if negozio['nome'] == nome]

    if negozio_richiesto:
        return jsonify(negozio_richiesto[0])
    else:
        return jsonify({'errore': 'Negozio non trovato'})


@app.route('/negozi')
def vedi_negozi():
    return jsonify({'negozi': negozi})


@app.post('/negozio/<string:nome>/oggetto')
def crea_oggetto_negozio(nome):
    dati_richiesta = request.get_json()
    nuovo_oggetto = {
        'nome': dati_richiesta['nome'],
        'prezzo': float(dati_richiesta['prezzo'])
    }
    negozio_richiesto = [negozio for negozio in negozi if negozio['nome'] == nome]

    if negozio_richiesto:
        negozio_richiesto[0]['oggetti'].append(nuovo_oggetto)
        return jsonify(nuovo_oggetto)
    else:
        return jsonify({'errore': 'Negozio non trovato'})


@app.route('/negozio/<string:nome>/oggetto')
def vedi_oggetti_negozio(nome):
    negozio_richiesto = [negozio for negozio in negozi if negozio['nome'] == nome]

    if negozio_richiesto:
        return jsonify(negozio_richiesto[0]['oggetti'])
    else:
        return jsonify({'errore': 'Negozio non trovato'})


if __name__ == '__main__':
    app.run()
