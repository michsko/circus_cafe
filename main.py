from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, equal_to
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.widgets import TextArea


app = Flask(__name__)
# add Users database
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
    occupation = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    street_address = db.Column(db.String(100), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    state2 = db.Column(db.String(100))
    zip_code = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    terms_agreement = db.Column(db.String(100), nullable=False)
    date_of_registration = db.Column(db.DateTime, default=datetime.now)

    # pasword hashing and checking
    # @property
    # def password(self):
    #     raise AttributeError('Nelze precist heslo!')
    # @password.setter
    # def password(self, password):
    #     self.password = generate_password_hash(password)
    #
    # def verify_password(self, password):
    #     return check_password_hash(self.password, password)
    #

    def __init__(self, name, surname, occupation, phone_number, gender, email, street_address, house_number, city,
                 state, state2, zip_code, password,
                 password2, terms_agreement, date_of_registration):
        self.name = name
        self.surname = surname
        self.occupation = occupation
        self.phone_number = phone_number
        self.gender = gender
        self.email = email
        self.street_address = street_address
        self.house_number = house_number
        self.city = city
        self.state = state
        self.state2 = state2
        self.zip_code = zip_code
        self.password = password
        self.password2 = password2
        self.terms_agreement = terms_agreement
        self.date_of_registration = datetime.now()

    # def __repr__(self):
    #     return '<Name %r>' % self.name


# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()

# create a Form Class

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Heslo", validators=[DataRequired()])
    submit = SubmitField("submit")


class UserForm(FlaskForm):
    name = StringField(" Jméno", validators=[DataRequired()])
    surname = StringField(" Příjmení", validators=[DataRequired()])
    occupation = StringField(' Povolani', validators=[DataRequired()])
    phone_number = StringField(' Telefon', validators=[DataRequired()])
    gender = SelectField(" Gender", choices=[('Žena'), ('Muž'), ('Jiné')], validators=[DataRequired()])
    email = StringField(" E-mail", validators=[DataRequired()])
    street_address = StringField(" Adresa", validators=[DataRequired()])
    house_number = StringField(" c.p.", validators=[DataRequired()])
    city = StringField(" Mesto", validators=[DataRequired()])
    state = SelectField(" Stat", choices=[(" "), ("Belgické království"),
                                          ("Bulharská republika"),
                                          ("Česká republika"),
                                          ("Dánské království"),
                                          ("Estonská republika"),
                                          ("Finská republika"),
                                          ("Francouzská republika"),
                                          ("Chorvatská republika"),
                                          ("Irsko"),
                                          ("Italská republika"),
                                          ("Kyperská republika"),
                                          ("Litevská republika"),
                                          ("Lotyšská republika"),
                                          ("Lucemburské velkovévodství"),
                                          ("Maďarsko"),
                                          ("Maltská republika"),
                                          ("Spolková republika Německo"),
                                          ("Nizozemské království"),
                                          ("Polská republika"),
                                          ("Portugalská republika"),
                                          ("Rakouská republika"),
                                          ("Rumunsko"),
                                          ("Řecká republika"),
                                          ("Slovenská republika"),
                                          ("Slovinská republika"),
                                          ("Španělské království"),
                                          ("Švédské království"),
                                          ("jiny stat")])
    state2 = StringField(" jiny stat")
    zip_code = StringField(" PSC", validators=[DataRequired()])
    password = PasswordField(" Heslo",
                             validators=[DataRequired(), equal_to("password2", message="Hesla musi souhlasit.")])
    password2 = PasswordField(" Opakovat heslo", validators=[DataRequired()])
    terms_agreement = BooleanField(" Souhlasím s podmínkami", validators=[DataRequired()])
    submit = SubmitField("Submit form")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# blog post model
class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(255))

    def __init__(self, title, content, author, slug, date_posted):
        self.title = title
        self.content = content
        self.author = author
        self.date_posted = datetime.now()
        self.slug = slug

    # create post form


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit", validators=[DataRequired()])


@app.route("/add_blog_post", methods=['GET', 'POST'])
def add_blog_post():
    post_form = PostForm()

    if post_form.validate_on_submit():
        post = Posts(title=post_form.title,
                     author=post_form.author,
                     slug=post_form.slug,
                     content=post_form.content,
                     date_posted=datetime.now())
        # clear the form
        post_form.title = ''
        post_form.author = ''
        post_form.slug = ''
        post_form.content = ''

        # add post to database
        db.session.add(post)
        db.session.commit()


        # return message
        flash("Vas prispevek byl uspesne pridan!")

    return render_template('add_blog_post.html', post_form=post_form)


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
    password_to_check = None
    passed = None
    login_form = LoginForm()

    # validate Form
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data

        # clear the form
        login_form.email.data = ''
        login_form.password.data = ''

        # look up user by email
        password_to_check = Users.query.filter_by(email=email).first()

        # chacked hashed password
        passed = check_password_hash(password_to_check.password, password)
        if passed == True:
            flash("Prihlaseni probehlo uspesne.")
        else:
            flash("Vase heslo nebo email nesouhlasi!")
            email = ''
            name = ''

    return render_template("login.html", email=email,
                           password=password,
                           password_to_check=password_to_check,
                           passed=passed,
                           login_form=login_form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    name = None
    surname = None
    occupation = None
    phone_number = None
    gender = None
    email = None
    street_address = None
    house_number = None
    city = None
    state = None
    state2 = None
    zip_code = None
    password = None
    password2 = None
    terms_agreement = None
    register_form = UserForm()
    if register_form.validate_on_submit():
        user = Users.query.filter_by(email=register_form.email.data).first()
        if user is None:
            # hash password
            hashed_pw = generate_password_hash(register_form.password.data, "sha256")
            hashed_pw2 = generate_password_hash(register_form.password2.data, "sha256")

            user = Users(name=register_form.name.data,
                         surname=register_form.surname.data,
                         occupation=register_form.occupation.data,
                         phone_number=register_form.phone_number.data,
                         gender=register_form.gender.data,
                         email=register_form.email.data,
                         street_address=register_form.street_address.data,
                         house_number=register_form.house_number.data,
                         city=register_form.city.data,
                         state=register_form.state.data,
                         state2=register_form.state2.data,
                         zip_code=register_form.zip_code.data,
                         password=hashed_pw,
                         password2=hashed_pw2,
                         terms_agreement=register_form.terms_agreement.data,
                         date_of_registration=datetime.now())

            db.session.add(user)
            db.session.commit()
        name = register_form.name.data
        register_form.name.data = ''
        register_form.surname.data = ''
        register_form.occupation.data = ''
        register_form.phone_number.data = ''
        register_form.gender.data = ''
        register_form.email.data = ''
        register_form.street_address.data = ''
        register_form.house_number.data = ''
        register_form.city.data = ''
        register_form.state.data = ''
        register_form.zip_code.data = ''
        register_form.password.data = ''
        register_form.password2.data = ''
        register_form.terms_agreement.data = ''
        register_form.date_of_registration = ''

        flash("Registrace probehla uspesne.")
    our_users = Users.query.order_by(Users.date_of_registration)
    return render_template("register.html", register_form=register_form,
                           name=name,
                           our_users=our_users)


if __name__ == "__main__":
    app.run(debug=True)
