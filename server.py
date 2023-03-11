from flask import Flask, session, request, redirect, url_for, render_template
import os


def index():
    return render_template('authorization.html')



folder = os.getcwd()
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index)

if __name__ == "__main__":
    # Запускаем веб-сервер:
    app.run()


