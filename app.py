from flask import Flask

app = Flask(__name__)


@app.route('/negozio', methods=['POST'])
def crea_negozio():
    pass


@app.route('/negozio/<string:nome>')
def vedi_negozio(nome):
    pass


@app.route('/negozi')
def vedi_negozi():
    pass


if __name__ == '__main__':
    app.run()
