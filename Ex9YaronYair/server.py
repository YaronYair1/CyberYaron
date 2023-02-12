from flask import Flask, request
import random

app = Flask(__name__)

@app.route('/port', methods=['GET'])
def generate_port():
    port = random.randint(10000, 60000)
    return '', 200, {'Port Number': str(port)}

if __name__ == '__main__':
    app.run(debug=True)