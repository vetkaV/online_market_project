from flask import Flask, session, request, redirect, url_for, render_template
import os
from startSqlite import get_succes_auth, create_user, select_all, update_user_info,get_content
from users import User


def get_auth():
    login = request.form.get('auth_login')
    pass_w = request.form.get('auth_pass')
    status = get_succes_auth(str(login), str(pass_w))
    if status:
        session['login'] = str(login)
        return True
    else:
        return False


def index():
    if request.method == "POST":
        print(request.form.get('btn_cap'))
        if str(request.form.get('btn_cap')) == '1':
            return render_template('catalog.html') 
    return render_template('main.html')

def auth():
    if request.method == "POST":
        if get_auth():
            print('login', session['login']) 
            return redirect(url_for('profile'))
    return render_template('authorization.html')

def catalog():
    session['content']=get_content()
    print(session['content'])
    return render_template('detail.html', content_list = session['content'])    

def reg():
    result = True
    if request.method == "POST":
        print('reg')
        result, session['login'] = create_user(request.form.get('auth_login'),request.form.get('auth_pass'), request.form.get('auth_email'), request.form.get('auth_number'))
        print(session['login'])
        if result:    
            return redirect(url_for('profile'))   
    return render_template('register.html', status = result) 
    

def detail():
    content=get_content()
    try:
        if request.method == "POST":
            
            if request.form.get('auth_text') == "Войти":
                return redirect(url_for('auth'))
            else:
                return redirect(url_for('profile'))
            
        if request.method == "GET":
            query = request.args.get('id_product')
            print(query)
        return render_template('detail.html', content_list = content, login = session['login'])
    except:
        session['login'] = None
        return render_template('detail.html', content_list = content, login = session['login'])

def profile():
    if request.method == "GET":
        try:
            if session['login'] != None:
                session["profile_info"] = select_all(session['login'])
                return render_template('profile.html', username = session['profile_info'][1], 
                                                        email = session['profile_info'][3], 
                                                        phone = session['profile_info'][4],
                                                        name = session['profile_info'][5],
                                                        surname = session['profile_info'][6],
                                                        address = session['profile_info'][7])
            else: return redirect(url_for('auth'))
        except:
            session['login'] = None
            return redirect(url_for('auth'))

    if request.method == "POST":
        if request.form.get('save_change') == 'Сохранить':
            print(request.form.get('save_change'))
            update_user_info(request.form.get('name_user'), 
                             request.form.get('surname_user'), 
                             request.form.get('address_user'),
                             session['profile_info'][1])
            return redirect(url_for('profile'))
    return render_template('profile.html')    


folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index, methods=['post', 'get'])
app.add_url_rule('/auth', 'auth', auth, methods=['post', 'get'])
app.add_url_rule('/catalog', 'catalog', catalog, methods=['post', 'get'])
app.add_url_rule('/reg', 'reg', reg, methods=['post', 'get'])
app.add_url_rule('/detail', 'detail', detail, methods=['post', 'get'])
app.add_url_rule('/profile', 'profile', profile, methods=['post', 'get'])

app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()


