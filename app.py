from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho_total'] = sum(float(item['preco']) for item in session['carrinho'])
    return render_template('index.html')

@app.route('/adicionar_ao_carrinho', methods=['POST'])
def adicionar_ao_carrinho():
    item = request.form.to_dict()
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append(item)
    session['carrinho_total'] = sum(float(item['preco']) for item in session['carrinho'])
    return redirect(url_for('index'))

@app.route('/remover_item', methods=['POST'])
def remover_item():
    index = int(request.form['index'])
    if 'carrinho' in session:
        session['carrinho'].pop(index)
        session['carrinho_total'] = sum(float(item['preco']) for item in session['carrinho'])
    return redirect(url_for('index'))

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    whatsapp_number = request.form.get('whatsapp_number')
    if whatsapp_number:
        mensagem = 'Pedido:\n' + '\n'.join(
            f"{item['nome']} - R$ {item['preco']}\nMassa: {item['massa']}\nCobertura: {item['cobertura']}\nConfeitos: {item['confeitos']}"
            for item in session.get('carrinho', [])
        )
        mensagem += f"\nTotal: R$ {session.get('carrinho_total', 0):.2f}"
        return redirect(f"https://wa.me/{whatsapp_number}?text={mensagem}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
