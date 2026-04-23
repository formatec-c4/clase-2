from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>¡Hola Clase de Cloud!</h1><p>Servidor funcionando en local.</p>"


if __name__ == "__main__":
    # El servidor escucha pedidos en el puerto 5000.
    app.run(host="0.0.0.0", port=5000)
