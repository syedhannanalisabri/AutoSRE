from flask import Flask
import os

app = Flask(__name__)
leak_list = []

@app.route('/')
def home():
    return "System Normal"

@app.route('/leak')
def leak():
    global leak_list
    # Simulate partial memory leak (append ~10MB string)
    leak_list.append(' ' * 10 * 1024 * 1024)
    print("WARNING: Memory spike", flush=True)
    return "Memory spike simulated", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
