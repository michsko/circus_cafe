from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, equal_to
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wtforms.widgets import TextArea
from flask_login import UserMixin, LoginManager, logout_user, login_required, current_user, login_required, login_user

app = Flask(__name__)
# add Users database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///circus_cafe.db'

# add secret key
app.config['SECRET_KEY'] = "Ja Pisi Vam Co Mohu Vice"
# initialize database
db = SQLAlchemy(app)
# Flask login management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# create a model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
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
    blog_posts = db.relationship('Posts', backref="users")
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

    def __init__(self, name, username, surname, occupation, phone_number, gender, email, street_address, house_number,
                 city,
                 state, state2, zip_code, password,
                 password2, terms_agreement, date_of_registration):
        self.name = name
        self.username = username
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


# create a Form Class

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Heslo", validators=[DataRequired()])
    submit = SubmitField("Log in")


class UserForm(FlaskForm):
    username = StringField("Uzivatelske jméno", validators=[DataRequired()])
    name = StringField("Jméno", validators=[DataRequired()])
    surname = StringField(" Příjmení", validators=[DataRequired()])
    occupation = StringField(' Povolani', validators=[DataRequired()])
    phone_number = StringField(' Telefon', validators=[DataRequired()])
    gender = SelectField(" Gender", choices=[('Žena'), ('Muž'), ('Jiné')], validators=[DataRequired()])
    email = StringField(" E-mail", validators=[DataRequired()])
    street_address = StringField(" Ulice", validators=[DataRequired()])
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
    submit = SubmitField("Sign up")


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
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, title, content, author, slug, date_posted):
        self.title = title
        self.content = content
        self.author = author
        self.date_posted = datetime.now()
        self.slug = slug


class DeletedPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_deleted = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, title, content, author, slug, date_posted, date_deleted):
        self.title = title
        self.content = content
        self.author = author
        self.date_posted = date_posted
        self.slug = slug
        self.date_deleted = datetime.now()


# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()


# create post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit post")


@app.route("/add_blog_post", methods=['GET', 'POST'])
@login_required
def add_blog_post():
    title = None
    author = None
    slug = None
    content = None
    post_form = PostForm()

    if post_form.validate_on_submit():
        posts = Posts(title=post_form.title.data,
                      author=post_form.author.data,
                      slug=post_form.slug.data,
                      content=post_form.content.data,
                      date_posted=datetime.now())

        # clear the form
        post_form.title.data = ''
        post_form.author.data = ''
        post_form.slug.data = ''
        post_form.content.data = ''

        # add post to database
        db.session.add(posts)
        db.session.commit()

        # return message
        flash("Vas prispevek byl uspesne pridan!")

    return render_template('add_blog_post.html',
                           post_form=post_form,
                           title=title)


@app.route("/blog_posts")
@login_required
def blog_posts():
    # grab all the posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("blog_posts.html", posts=posts)


@app.route("/blog_post/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)


@app.route("/blog_posts/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post_form = PostForm()
    post_to_update = Posts.query.get_or_404(id)

    if request.method == "POST":
        post_to_update.title = request.form['title']
        post_to_update.author = request.form['author']
        post_to_update.slug = request.form['slug']
        post_to_update.content = request.form['content']

        post_form.title.data = ''
        post_form.author.data = ''
        post_form.slug.data = ''
        post_form.content.data = ''
        try:
            db.session.commit()
            flash("Tvuj prispevek byl uspesne zmenen.")
            return redirect(url_for('blog_posts', post_form=post_form,
                                    post_to_update=post_to_update))
        except:
            flash("Neco se nepovedlo. Zkuste to znovu.")
            return render_template('update_blog_post.html', post_form=post_form,
                                   post_to_update=post_to_update)
    else:
        return render_template('update_blog_post.html', post_form=post_form,
                               post_to_update=post_to_update)


@app.route("/blog_posts/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    deleted_post_to_add = Posts.query.get_or_404(id)
    deleted_post = DeletedPosts(title=deleted_post_to_add.title,
                                content=deleted_post_to_add.content,
                                author=deleted_post_to_add.author,
                                date_posted=deleted_post_to_add.date_posted,
                                slug=deleted_post_to_add.slug,
                                date_deleted=datetime.now())

    blog_post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.add(deleted_post)
        db.session.delete(blog_post_to_delete)
        db.session.commit()
        flash("Vas prispevek byl vymazan.")
        return redirect(url_for('blog_posts'))
    except:
        flash("Neco se nepovedlo.")


@app.route("/blogs")
def blogs():
    return render_template("blogs.html")


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
    login_form = LoginForm()
    # validate Form
    if login_form.validate_on_submit():
        # look up user by email
        user = Users.query.filter_by(email=login_form.email.data).first()

        if user:
            # check password hash
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                flash('Vase prihlaseni probehlo uspesne!')
                return redirect(url_for('dashboard'))

            else:
                flash("Vas email nebo heslo nesouhlasi!")

        else:
            flash("Vas email nebo heslo nesouhlasi. Prosim zkuste to znovu!")

    return render_template("login.html", login_form=login_form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Jste odhlaseni!")
    return redirect(url_for('login'))


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    name = None
    username = None
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
                         username=register_form.username.data,
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
        register_form.username = ''
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


@app.route("/update_user/<int:id>", methods=['GET', 'POST'])
@login_required
def update_user(id):
    update_form = UserForm()
    user_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.username = request.form['username']
        user_to_update.surname = request.form['surname']
        user_to_update.occupation = request.form['occupation']

        user_to_update.phone_number = request.form['phone_number']
        user_to_update.gender = request.form['gender']
        user_to_update.email = request.form['email']
        user_to_update.street_address = request.form['street_address']

        user_to_update.house_number = request.form['house_number']
        user_to_update.city = request.form['city']
        user_to_update.zip_code = request.form['zip_code']
        user_to_update.state = request.form['state']

        try:
            db.session.commit()
            flash("Tvoje osobni informace byly zmeneny.")
            return render_template('update', update_form=update_form,
                                   user_to_update=user_to_update)
        except:
            flash("Neco se nepovedlo. Zkuste to znovu.")
            return render_template('update_user.html', update_form=update_form,
                                   user_to_update=user_to_update)
    else:
        return render_template('update_user.html', update_form=update_form,
                               post_to_update=user_to_update)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(debug=True)
