from flask import render_template, url_for, flash, redirect, request
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, BuyForm
from game_store.models import Customer, Order, Run, Platform
from flask_login import login_user, current_user, logout_user, login_required
from game_store.models import Game, Publisher



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/gamelist")
def gl():
    publishers = Publisher.query.all()
    games = Game.query.all()
    return render_template('gamelist.html', games=games, publishers=publishers)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/genres")
def genre():
    return render_template('genres.html')

@app.route("/publisher")
def publish():
    return render_template('publisher.html')

@app.route("/platforms")
def platform():
    return render_template('platforms.html')

@app.route('/aa')
def actionadv():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre = 'action-adventure').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/ps4')
def ps4():
    runs = Run.query.filter_by(platform_id = 12).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=12))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/switch')
def switch():
    runs = Run.query.filter_by(platform_id = 13).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=13))
    flash("Games that are on the Nintendo Switch")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/3ds')
def n3ds():
    runs = Run.query.filter_by(platform_id = 14).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=14))
    flash("Games that are on the Nintendo 3ds")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/arp')
def arp():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='action role-playing').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/fps')
def fps():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='first-person shooter').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/platform')
def plat():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='platform').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/sports')
def sports():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='sports').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/fight')
def fight():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='fighting').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/tps')
def tps():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='third-person shooter').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/social')
def social():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='social simulation').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/ubisoft")
def ubisoft():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=1).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/ea")
def ea():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=2).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/sony")
def sony():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=4).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/nintendo")
def nintendo():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=5).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/activision")
def activision():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=3).all()
    return render_template('gamelist.html', games=games, publishers=publishers)


@app.route("/game", methods=['GET', 'POST'])
def game():
    form = BuyForm()
    if not current_user.is_authenticated:
        flash('Please login before you can view this page. If you do not have an account, then please register.')
        return redirect(url_for('login'))

    return render_template('game.html', game=request.args.get('selected_game'), form=form, title='Game')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, balance=40.00)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')