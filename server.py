from flask import Flask, session, request, redirect, url_for, render_template
import os
from startSqlite import get_succes_auth, create_user
def get_auth():
    login = request.form.get('auth_login')
    pass_w = request.form.get('auth_pass')
    return get_succes_auth(str(login), str(pass_w))
def index():
    if request.method == "POST":
        print(request.form.get('btn_cap'))
        if str(request.form.get('btn_cap')) == '1':
            return render_template('catalog.html') 
    return render_template('main.html')

def auth():
    if request.method == "POST":
        if get_auth(): 
            return redirect(url_for('index'))

    return render_template('authorization.html')

def catalog():
    return render_template('catalog.html')    

def reg():
    result = True
    if request.method == "POST":
        print('reg')
        result = create_user(request.form.get('auth_login'),request.form.get('auth_pass'), request.form.get('auth_email'), request.form.get('auth_number'))
        if result:    
            return render_template('main.html')   
    return render_template('register.html', status = result) 
    
folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/auth', 'auth', auth, methods=['post', 'get'])
app.add_url_rule('/catalog', 'catalog', catalog, methods=['post', 'get'])
app.add_url_rule('/reg', 'reg', reg, methods=['post', 'get'])

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()


