import sqlite3
from users import User
db_name = 'usersInfo.sqlite'

conn=None
cursor=None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    do ("DROP table users")
    do ("DROP table category_product")
    do ("DROP table products")
    do('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY not null, 
            login VARCHAR not null,
            password VARCHAR not null, 
            email VARCHAR not null,
            phone INTEGER not null,
            name VARCHAR NOT NULL,
            surname VARCHAR NOT NULL,
            address VARCHAR NOT NULL)'''
       )
    
    do('''INSERT INTO users (login, password, email, phone, name, surname, address) values ('admin', 'admin', 'admin@corp.ru', '87775553535' , 'Админ', 'основной', 'Империя')''')

    do('''CREATE TABLE IF NOT EXISTS category_product (
        id INTEGER PRIMARY KEY NOT NULL,
        category VARCHAR NOT NULL
    )''')

    cursor.execute('''INSERT into category_product (category) VALUES ((?))''', ['Межсетевой экран'])
    cursor.execute('''INSERT into category_product (category) VALUES ((?))''', ['Коммутатор'])
    cursor.execute('''INSERT into category_product (category) VALUES ((?))''', ['Маршрутизатор'])
    cursor.execute('''INSERT into category_product (category) VALUES ((?))''', ['SIEM'])
    cursor.execute('''INSERT into category_product (category) VALUES ((?))''', ['DLP'])
    conn.commit()

    do('''CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name VARCHAR NOT NULL,
    price INTEGER NOT NULL,
    category INTEGER NOT NULL,
    desription TEXT NOT NULL,
    FOREIGN KEY (category) REFERENCES category_product (id)
    )''')

    info = [
        ('TP-LINK SafeStream ER605', 5299, 1, 'Межсетевой экран TP-LINK SafeStream ER605 открывает безопасный доступ в интернет для корпоративных и домашних нужд. Контроль и управление устройством осуществляется через мобильное приложение.'),
        ('ZYXEL USG FLEX 200', 77800 , 1, 'Для эффективной и безопасной работы каждого компьютера и всей системы в офисах необходимо использование межсетевого экрана ZYXEL USG FLEX 200. Модель выступает в качестве пограничного антивируса, детектора атак, контент- и спам-фильтра и контроллера точек доступа с «бесшовным» подключением к сети через шлюз.'),
        ('Zyxel ATP700', 308800, 1, 'Серия Zyxel ZyWALL ATP — это межсетевые экраны, предназначенные для малого и среднего бизнеса и оснащенные интеллектуальными функциями, которые повышают уровень защиты сети, особенно при борьбе с неизвестными угрозами.'),
        ('Zyxel ATP100W', 83700, 1, 'Серия Zyxel ZyWALL ATP — это межсетевые экраны, предназначенные для малого и среднего бизнеса и оснащенные интеллектуальными функциями, которые повышают уровень защиты сети, особенно при борьбе с неизвестными угрозами.'),
        ('Cisco FPR2110-NGFW-K9', 1314700, 1, 'Серия Cisco Firepower 2100 - это семейство из четырех платформ безопасности, ориентированных на угрозы, которые обеспечивают отказоустойчивость бизнеса и превосходную защиту от угроз. Они обеспечивают исключительную устойчивую производительность, когда включены расширенные функции защиты от угроз.'),
        ('Huawei USG6635E',1924000, 1, 'Межсетевой экран Huawei USG6635E позволяет предотвращать атаки на сеть компании, следить и предотвращать утечки данных. Есть возможность построения VPN-соединений. Имеется защита от DDoS-атак и спама. Предусмотрена возможность управлять полосой пропускания с помощью облачного управления'),
        ('Eltex MES2324FB', 135400, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('Cisco 9300-48P-E',1045500,2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        (' D-link DGS-1210-20/ME', 13600, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('DAHUA DH-PFS4212-8GT-96', 24390, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('TP-LINK TL-SG108E', 2750, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('MikroTik CRS326-24G-2S+RM', 26690, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('Mercusys MS105G', 930, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('Planet GSD-908HP', 13189, 2, 'Сетевой коммутатор — устройство, предназначенное для соединения нескольких узлов компьютерной сети в пределах одного или нескольких сегментов сети.'),
        ('D-Link DIR-X1530', 3780, 3, 'Маршрутизатор, роутер — специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе правил и таблиц маршрутизации. Маршрутизатор может связывать разнородные сети различных архитектур.'),
        ('D-Link DIR-825 R1A', 3780, 3, 'Маршрутизатор, роутер — специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе правил и таблиц маршрутизации. Маршрутизатор может связывать разнородные сети различных архитектур.'),
        ('TP-Link Archer C5', 3420, 3, 'Маршрутизатор, роутер — специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе правил и таблиц маршрутизации. Маршрутизатор может связывать разнородные сети различных архитектур.'),
        ('Xiaomi Mi Router 4C', 1275, 3, 'Маршрутизатор, роутер — специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе правил и таблиц маршрутизации. Маршрутизатор может связывать разнородные сети различных архитектур.'),
        ('Xiaomi Mi AIoT Router AX3600', 18300, 3, 'Маршрутизатор, роутер — специализированное устройство, которое пересылает пакеты между различными сегментами сети на основе правил и таблиц маршрутизации. Маршрутизатор может связывать разнородные сети различных архитектур.'),
        ('ViPNet TIAS', 503500, 4, 'ViPNet TIAS (Threat Intelligence Analytics System) — программно-аппаратный комплекс, предназначенный для автоматического выявления инцидентов на основе анализа событий информационной безопасности.'),
        ('MaxPatrol SIEM', 2600500, 4, 'MaxPatrol Security Information and Event Management дает полную видимость IT-инфраструктуры и выявляет инциденты информационной безопасности. Он постоянно пополняется знаниями экспертов Positive Technologies о способах детектирования актуальных угроз иадаптируется кизменениям взащищаемой сети.'),
        ('SIEM «КОМРАД»', 1700000, 4, 'KOMRAD Enterprise SIEM позволяет осуществлять централизованный сбор событий ИБ, выявлять инциденты ИБ и оперативно на них реагировать. Применение комплекса позволяет эффективно выполнять требования, предъявляемые регуляторами к защите персональных данных, к обеспечению безопасности государственных информационных систем и контролю критической информационной инфраструктуры предприятия.'),
        ('Solar Dozor', 350000, 5, 'Система предотвращения утечек информации (DLP). Блокирует передачу конфиденциальных документов, помогает выявлять признаки корпоративного мошенничества, позволяет заниматься профилактикой инцидентов безопасности.'),
        ('McAfee Total Protection for Data Loss Prevention', 250000, 5, 'McAfee Total Protection for Data Loss Prevention (DLP)— это программный комплекс, который обеспечивает надежную защиту конфиденциальной информации, независимо от места ее использования и хранения.McAfeeDLPзащищает данные, хранящиеся, как на конечных точках, так и на «облаке».'),
        ('Forcepoint DLP', 150000, 5, 'ПродуктForcepoint DLP является программным средством по контролю над вероятными утечками корпоративных данных на конечных устройствах/рабочих местах. Применяется для защиты информации, включая совместно обрабатываемые проекты. Система включает контроль контента по определенным маркерам, включая учет совокупно передаваемых данных.')
    ]

    cursor.executemany('''INSERT into products (name, price, category, desription) VALUES ((?), (?), (?), (?))''', info)
    conn.commit()

def get_succes_auth(login, pass_w):
    open()
    login = login.replace(" ", '')
    cursor.execute('''select * from users where login == (?)''', [login])
    result = cursor.fetchone()
    close()
    print(result)
    if result != None:
        return str(result[1]) == login and str(result[2]) == pass_w
    else:
        return False
    

def check_login_email(login, email):
    open()
    cursor.execute('''select * from users where login == (?) or email == (?)''', [login, email])
    result = cursor.fetchall()
    close()
    if result != None and len(result) > 0:
        return False
    else:
        return True
    
def select_all(login):
    open()
    cursor.execute('''select * from users where login = (?)''', [login])
    result = cursor.fetchone()
    close()
    if result != None:
        return result
    else:
        return False
def create_user(login, pass_w, email, phone):
    if check_login_email(login, email):
        open()
        cursor.execute('''insert into users (login, password, email, phone, name, surname, address) values (?, ?, ?, ?, 'None', 'None', 'None')''', [login, pass_w, email, phone])
        print('succesful')
        conn.commit()
        close()
        return True, login
    else:
        return False, None

def update_user_info(name, surname, address, login):
    open()
    cursor.execute('''update users set name = (?), surname = (?), address = (?) where login = (?)''', [name, surname, address, login])
    conn.commit()
    print('succesful')
    close()

def main():
    #pass
    create()

if __name__ == "__main__":
    main()