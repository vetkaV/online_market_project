from flask import Flask, session, request, redirect, url_for, render_template
import os
from startSqlite import get_succes_auth, create_user, select_all, update_user_info,get_content, get_info, get_category,get_filtered_content, add_order, get_order
from startSqlite import delete_order, start_pages_category


'''
#функция авторизации
Получаем логин и пароль, вызываем функцию проверки логина и пароля.
Если она совпадает, то возвращает True, иначе False
Далее создаем сессию для пользователя, где запоминаем его логин
и возвращаем результат успеха
'''
def get_auth():
    login = request.form.get('auth_login')
    pass_w = request.form.get('auth_pass')
    status = get_succes_auth(str(login), str(pass_w))
    if status:
        session['login'] = str(login)
        return True
    else:
        return False


'''
Функция главной страница, она управляет контентом на ней.
Мы получаем список всех категорий с их минимальной ценой,
загружаем шаблон страницы, где указываем категорию и 
мин цену с этого списка в спец блоках, которые перенаправляют в каталог
'''
def index():
    start_content = start_pages_category()
    return render_template('main.html', 
                           start_content=start_content,
                           )


'''
Функция авторизации
В шаблоне есть блок авторизации и кнопка
кнопка отправляет запрос POST, если мы его получаем,
то вызываем функцию проверки пароля. Если в ответ True,
то переадресация на страницу профиля,
если False, збрасываем строки и заного на авторизацю
'''
def auth():
    if request.method == "POST":
        if get_auth():
            print('login', session['login']) 
            return redirect(url_for('profile'))
    return render_template('authorization.html')



'''
Функция регистрации
похожая форма, что и у авторизации, только для регистрации
Получили запрос POST, отправили запрос в БД
Там идет проверка на такой же логин или почту,
если совпадений не найдено, то возвращает True
и вносятся изменения в БД, переадресация на профиль.
Если есть совпадения, то False и данные не вносятся
'''   
def reg():
    result = True
    if request.method == "POST":
        print('reg')
        result, session['login'] = create_user(request.form.get('auth_login'),
                                               request.form.get('auth_pass'), 
                                               request.form.get('auth_email'), 
                                               request.form.get('auth_number'))
        print(session['login'])
        if result:    
            return redirect(url_for('profile'))   
    return render_template('register.html', status = result) 
    


'''
Функция страницы каталога
загружаем весь каталог и категории
загружаем страницу туда передаем данные для заполнения
если мы выбрали товар, нажимаем подробнее.
После чего отправялется заппрос GET с данными id продукта
Мы его обрабатываем и переадресуем на страницу информации
id продукта запоминаем в сессии пользователя

тут же работает фильтр
если выбрали нужный, снова GET запрос
обработаем его с помощью sql запроса, в ответ получаем отфильтрованный список
загружаем страницу заного, но уже с фильтром
'''
def detail():
    content=get_content()
    category=get_category()
    try:
        if request.method == "POST":
            
            if request.form.get('auth_text') == "Войти":
                return redirect(url_for('auth'))
            else:
                return redirect(url_for('profile'))
            
        if request.method == "GET":
            session['info'] = request.args.get('id_product')
            print(session['info'])
            session['filter']=request.args.get('filter')
            print('filter', session['filter'])
            if session['filter'] != None:
                content=get_filtered_content(session['filter'])
                return render_template('detail.html', 
                               content_list = content, 
                               login = session['login'], 
                               category=category)
            if session['info'] != None and int(session['info']) > 0:
                session['info_product'] = get_info(session['info'])
                return redirect(url_for('info'))
        return render_template('detail.html', 
                               content_list = content, 
                               login = session['login'], 
                               category=category)
    except:
        session['login'] = None
        return render_template('detail.html', 
                               content_list = content, 
                               login = session['login'], 
                               category=category)

'''
функция пользователя
Отвечает за страницу пользователя
Когда заходим на страницу ,автоматически подгружаем информацию о пользователе
заполняем пустые поля шаблона этими данными
Также получаем список всех заказов и выводим их на странице

Если попытаться попасть на страницу не авторизовавшись, через строку поиска, то возвращает на страницу авторизации

здесь же есть форма заполнения данных имени, фамилии и адреса
Если мы их вводим и нажимаем СОХРАНИТЬ, то запрос POST, который мы обработаем и запишем в БД изменения
Кнопка DELETE удаляет заказ пользователя. Если логин и id заказа совпадает, то удачно
Если попытаться удалить чужой заказ, то не получиться
'''
def profile():
    if request.method == "GET":
        try:
            if session['login'] != None and request.args.get('delete_id') == None:
                session["profile_info"] = select_all(session['login'])
                return render_template('profile.html', username = session['profile_info'][1], 
                                                            email = session['profile_info'][3], 
                                                            phone = session['profile_info'][4],
                                                            name = session['profile_info'][5],
                                                            surname = session['profile_info'][6],
                                                            address = session['profile_info'][7],
                                                            orders= get_order(session['login'])
                                                            )
            
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
        if request.form.get('delete_btn') == 'delete':
            print('delete')
            if delete_order(session['login'], request.form.get('delete_id')):
                return redirect(url_for('profile'))
            else:
                print('Ошибка')
                return redirect(url_for('profile'))
    return render_template('profile.html')    



'''
Функция информации
отвечает за страницу описания продукта
на ней отображается, то что пользователь выбрал на станице каталог
Получает id выбранного продукта, отправляет запрос на получение информации
Получает и заполняет форму.

Кнопка купить позволяет добавить заказ пользователю, если он авторизован
Если он не авторизован, то кидает на страницу авторизации
'''
def info():
    print(session['info_product'])
    
    if request.method == 'GET':
        if str(request.args.get('buy_btn')) == "КУПИТЬ":
            print('prod_id -',request.args.get('prod_id'))
            if not add_order(request.args.get('prod_id'), session['login']):
                return redirect(url_for('auth'))
    return render_template('info.html', images=session['info_product'][0][3],
                                        name=session['info_product'][0][1], 
                                        desk=session['info_product'][0][4], 
                                        price=session['info_product'][0][2],
                                        id_product=session['info_product'][0][0],
                                        login=session['login'])


folder = os.getcwd() #полчаем статичную папку
app = Flask(__name__, template_folder=os.path.join(folder, 'templates'), static_folder=folder)#создаем сервер 
app.add_url_rule('/', 'index', index, methods=['post', 'get']) #создание правил
app.add_url_rule('/auth', 'auth', auth, methods=['post', 'get'])#создание правил
app.add_url_rule('/reg', 'reg', reg, methods=['post', 'get'])#создание правил
app.add_url_rule('/detail', 'detail', detail, methods=['post', 'get'])#создание правил
app.add_url_rule('/profile', 'profile', profile, methods=['post', 'get'])#создание правил
app.add_url_rule('/info', 'info', info, methods=['post', 'get'])#создание правил
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife' #секретный пароль для шифрования сессии

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()


