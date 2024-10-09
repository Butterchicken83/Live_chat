from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Route for the login page (asks for a username)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            session['username'] = username
            return redirect(url_for('chat'))  # Redirect to the chat page
    return render_template('login.html')

# Route for the chat page
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect back if no username is set
    return render_template('chat.html', username=session['username'])

# Handle incoming messages
@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    full_message = f"{username}: {msg}"
    print(f"Message: {full_message}")
    send(full_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
