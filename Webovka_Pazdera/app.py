from flask import Flask, render_template, request, redirect, url_for, session, flash
# from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = (
    b"\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0"
    b"\xe3\x84t\x8b\x02\x1c\xfb\x82PH\x19\xe8\x98\x05\x90\xa8\xc83\xf1\xe2\xf4v\xfe\xf0"
)
# app.secret_key = os.urandom()

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            flash(
                f"Pro zobrazení této stránky ({request.path}) je nutné se přihlásit!"
                "err"
            )
            return redirect(url_for("login", next=request.path))
    wrapper.__name__=f.__name__
    wrapper.__doc__=f.__doc__
    return wrapper


@app.route("/")
def index():
    return render_template("base.html.j2", a=12, b=3.14)


@app.route("/siláž/")
def siláž():
    if 'user' in session:
        return render_template("siláž.html.j2")
    else: 
        flash(f'Pro zobrazení této stránky ({request.path}) se musíš příhlásit!', 'err')
        return redirect(url_for('login', next=request.path))


@app.route("/silo/")
def silo():
    return render_template("silo.html.j2")


@app.route("/kejda/")
def kejda():
    if 'user' in session:
        return render_template("kejda.html.j2")
    else: 
        flash(f'Pro zobrazení této stránky ({request.path}) se musíš přihlásit!', 'err')
        return redirect(url_for('login', next=request.path))


@app.route("/login/", methods=["GET"])
def login():
    if request.method == "GET":  # nemá funkčí význam -- jen ukázka
        login = request.args.get("login")
        passwd = request.args.get("passwd")
        print(login, passwd)
    return render_template("login.html.j2")


@app.route("/login/", methods=["POST"])
def login_post():
    login = request.form.get("login")
    passwd = request.form.get("passwd")
    next = request.args.get('next')
    if passwd == "farma":
        session["user"] = login
        flash("Úspěšně jsi se přihlásil", "pass")
        if next:
            return redirect(next)
    else:
        flash("Špatné uživatelské jméno nebo heslo", "err")
    if next: 
        return redirect(url_for("login", next=next))
    else:
        return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Právě jsi se odhlásil", "pass")
    return redirect(url_for("index"))
