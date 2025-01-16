from flask import Blueprint, render_template, redirect, url_for
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


from app.auth.forms import LoginForm, RegisterForm
from app.extensions import db

auth = Blueprint('auth', __name__, template_folder="templates")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()    

    if form.validate_on_submit():   
        username = form.email.data
        password = form.password.data   

        cur = db.connection.cursor()
        sql = "SELECT * FROM users WHERE email = %s"
        cur.execute(sql, (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password'], password):
            #token = create_access_token(identity={'username': username})
            #return {'access_token': token}, 200 
            return redirect(url_for('main.index'))
        else:
            return 'Usuario o contraseña incorrecta'
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, hashed_password))
            db.connection.commit()
            cursor.close()

            return 'Usuario registrado correctamente'
        except Exception as e:
            print(e)
            return 'Error al registrar usuario'
        
    return render_template('register.html', form=form)
            