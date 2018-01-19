from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/learningflask'
app.secret_key = "development-key"

db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template("signup.html", form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))
    else:
        return render_template("signup.html", form=form)


@app.route("/logout")
def signout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    form = AddressForm()
    places = []
    my_coordinates = (37.4221, -122.0844)

    if request.method == 'POST':
        if not form.validate():
            return render_template("home.html", form=form)
        else:
            # get the address
            address = form.address.data 

            # query for places around it
            p = Place()
            my_coordinates = p.address_to_latlng(address)
            places = p.query(address)

            # return results
            return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)
    else:
        return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

    # return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))

    login_form = LoginForm()

    if request.method == 'POST':
        if not login_form.validate():
            return render_template("login.html", form=login_form)

        email = login_form.email.data
        password = login_form.password.data

        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            session['email'] = login_form.email.data
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
