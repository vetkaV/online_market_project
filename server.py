from flask import Flask, session, request, redirect, url_for, render_template
import os
from startSqlite import get_succes_auth
def get_auth():
    login = request.form.get('auth_login')
    pass_w = request.form.get('auth_pass')
    return get_succes_auth(str(login), str(pass_w))
def index():
    if request.method == "POST":
        if get_auth(): 
            return redirect(url_for('main'))

    return render_template('authorization.html')

def main():
    return render_template('main.html')

folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/main', 'main', main, methods=['post', 'get'])

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()


