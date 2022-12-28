from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz


app = Flask(__name__)
# add database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
# add secret key
app.config['SECRET_KEY'] = "Ja Pisi Vam Co Mohu Vice"
# initialize database
db = SQLAlchemy(app)



# create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    street_address = db.Column(db.String(100), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    password2 = db.Column(db.String(100), nullable=False)
    terms_agreement = db.Column(db.String(100), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.now)

    # create a string
    def __init__(self, name, surname, gender, email, street_address, house_number, city, state, zip_code, password, password2, terms_agreement, date_of_registration):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.email = email
        self.street_address = street_address
        self.house_number = house_number
        self.city = city
        self.zip_code = zip_code
        self.password = password
        self.password2 = password2
        self.terms_agreement = terms_agreement
        self.date_of_registration = date_of_registration
    def __repr__(self):
        return '<Name %r>' %self.name

 # Creation of the database tables within the application context.
with app.app_context():
    db.create_all()
# create a Form Class

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])

    submit = SubmitField("submit")

class UserForm(FlaskForm):
    name =StringField("Name", validators=[DataRequired()])
    surname =StringField("Surname", validators=[DataRequired()])
    gender =StringField("Gender", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    street_address = StringField("Street address", validators=[DataRequired()])
    house_number = db.Column("House number", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip_code = db.Column("Zip-code", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    password2 = StringField("Password repeat", validators=[DataRequired()])
    terms_agreement = StringField("Terms and condition", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blogs")
def blogs():
    return render_template("blog.html")


@app.route("/forum")
def forum():
    return render_template("forum.html")


# create search function
@app.route("/search", methods=["POST"])
def search():
    return render_template("profile.html")


@app.route("/news")
def news():
    return render_template("zpravy.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    email = None
    password = None
    form = loginForm()
    # validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''
    return render_template("login.html", email=email, password=password, form=form)


@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
