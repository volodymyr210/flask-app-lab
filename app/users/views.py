from . import bp
from flask import request, redirect, url_for, render_template, abort
from datetime import timedelta, datetime
from flask import session, request, make_response
from flask import flash

@bp.route("/profile", methods=["GET", "POST"])
def get_profile():
    if "username" not in session:
        flash("Error: Please log in to access your profile.", "danger")
        return redirect(url_for("user_name.login"))

    username_value = session["username"]

   
    if request.method == "POST":
        action = request.form.get("action")
        cookie_key = request.form.get("cookie_key")
        cookie_value = request.form.get("cookie_value")
        cookie_age = request.form.get("cookie_age", type=int)

        if action == "add":
            response = make_response(redirect(url_for("user_name.get_profile")))
            response.set_cookie(cookie_key, cookie_value, max_age=cookie_age)
            flash(f"Success: Cookie '{cookie_key}' added successfully.", "success")
            return response
        elif action == "delete":
            response = make_response(redirect(url_for("user_name.get_profile")))
            response.set_cookie(cookie_key, '', expires=0)
            flash(f"Success: Cookie '{cookie_key}' deleted successfully.", "success")
            return response

    
    cookies = request.cookies
    return render_template("profile.html", username=username_value, cookies=cookies)  


@bp.route("/login", methods=['GET', 'POST'])
def login():
    
    valid_username = "admin"
    valid_password = "secret"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

    
        if username == valid_username and password == valid_password:
            session["username"] = username
            flash("Success: session added successfully.", "success")
            return redirect(url_for("user_name.get_profile"))
        else:
            flash("Error: Invalid username or password.", "danger")

        if request.method == 'POST':
            username = request.form['username']
            session['username'] = username
            return redirect(url_for('add_post'))
    
    return render_template("login.html")


@bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('user_name.get_profile'))


@bp.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", 
                           name=name, age=age)

@bp.route("/admin")
def admin():
    to_url = url_for("user_name.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

@bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response

