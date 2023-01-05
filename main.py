from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, logout_user, login_required, login_user, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from webforms import LoginForm, UserForm, PostForm, PictureForm
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)


# add ckeditor


# Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)


ckeditor = CKEditor(app)
# add Users database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///circus_cafe.db'
# add secret key
app.config['SECRET_KEY'] = "Ja Pisi Vam Co Mohu Vice"
# initialize database
db = SQLAlchemy(app)
# Flask login management
db_init(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'static/images/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/about")
def about():
    date = datetime.now()
    return render_template("about.html", date=date)


@app.route("/add_blog_post", methods=['GET', 'POST'])
@login_required
def add_blog_post():
    date = datetime.now()
    post_form = PostForm()

    if post_form.validate_on_submit():
        poster = current_user.id
        posts = Posts(title=post_form.title.data,
                      poster_id=poster,
                      slug=post_form.slug.data,
                      content=post_form.content.data,
                      date_posted=datetime.now())

        # clear the form
        post_form.title.data = ''
        post_form.slug.data = ''
        post_form.content.data = ''

        # add post to database
        db.session.add(posts)
        db.session.commit()

        # return message
        flash("Vas prispevek byl uspesne pridan!")
        return redirect(url_for("blog_posts"))

    return render_template('add_blog_post.html',
                           post_form=post_form,
                           date=date
                           )


@app.route("/admin")
@login_required
def admin():
    date = datetime.now()
    id = current_user.id
    if id == 1:
        return render_template("admin.html", date=date)
    else:
        flash('Nemate potrebne opravneni.')
        return redirect(url_for("dashboard"))


@app.route("/blogs")
def blogs():
    date = datetime.now()
    return render_template("blogs.html", date=date)


@app.route("/blog_posts")
@login_required
def blog_posts():
    date = datetime.now()
    # grab all the posts from database
    id = current_user.id
    posts = Posts.query.filter_by(poster_id=id).all()
    return render_template("blog_posts.html", posts=posts, date=date)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    date = datetime.now()
    return render_template('dashboard.html', date=date)


@app.route("/blog_posts/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    deleted_post_to_add = Posts.query.get_or_404(id)

    poster = current_user.id
    deleted_post = DeletedPosts(title=deleted_post_to_add.title,
                                content=deleted_post_to_add.content,
                                poster_id=poster,
                                date_posted=deleted_post_to_add.date_posted,
                                slug=deleted_post_to_add.slug,
                                date_deleted=datetime.now())

    blog_post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == blog_post_to_delete.poster.id:
        try:
            db.session.add(deleted_post)
            db.session.delete(blog_post_to_delete)
            db.session.commit()
            flash("Vas prispevek byl vymazan.")
            return redirect(url_for('blog_posts'))
        except:
            flash("Neco se nepovedlo.")
    else:
        flash("Nemuzes vymazat tento prispevek!")
        return redirect(url_for('blog_posts'))


@app.route("/forum")
def forum():
    date = datetime.now()
    return render_template("forum.html", date=date)


@app.route("/")
def index():
    date = datetime.now()
    return render_template("index.html", date=date)


@app.route("/login", methods=['GET', 'POST'])
def login():
    date = datetime.now()
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

    return render_template("login.html", login_form=login_form, date=date)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Jste odhlaseni!")
    return redirect(url_for('login'))


@app.route("/news")
def news():
    date = datetime.now()
    return render_template("zpravy.html", date=date)


@app.errorhandler(404)
def page_not_found(e):
    date = datetime.now()
    return render_template("404.html", date=date)


@app.errorhandler(500)
def page_not_found(e):
    date = datetime.now()
    return render_template("500.html", date=date)


@app.route("/blog_post/<int:id>")
@login_required
def post(id):
    date = datetime.now()
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post, date=date)


@app.route("/register", methods=['GET', 'POST'])
def register():
    date = datetime.now()
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
        register_form.username.data = ''
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
        return redirect(url_for('login', register_form=register_form,
                                name=name,
                                date=date))
    our_users = Users.query.order_by(Users.date_of_registration)
    return render_template("register.html", register_form=register_form,
                           name=name,
                           our_users=our_users,
                           date=date)


# create search function
@app.route("/search", methods=["POST"])
def search():
    date = datetime.now()
    return render_template("profile.html", date=date)


@app.route("/blog_posts/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    date = datetime.now()
    post_form = PostForm()
    post_to_update = Posts.query.get_or_404(id)

    #    if post_form.validate_on_submit():
    #         post_form.title = post_form.title.data
    #         post_form.slug = post_form.slug.data
    #         post_form.content = post_form.content.data
    if post_form.validate_on_submit():
        post_to_update.title = post_form.title.data
        post_to_update.slug = post_form.slug.data
        post_to_update.content = post_form.content.data

        # post_form.title.data = ''
        # # post_form.author.data = ''
        # post_form.slug.data = ''
        # post_form.content.data = ''
        db.session.add(post_to_update)
        db.session.commit()
        flash("Tvuj prispevek byl uspesne zmenen.")
        return redirect(url_for('blog_posts', id=post_to_update.id))

    if current_user.id == post_to_update.poster_id:
        post_form.title.data = post_to_update.title
        # form.author.data = post.author
        post_form.slug.data = post_to_update.slug
        post_form.content.data = post_to_update.content
        return render_template('update_blog_post.html', post_form=post_form,
                               date=date)
    else:
        flash("Neco se nepovedlo. Zkuste to znovu.")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('blog_posts.html', posts=posts, date=date)


@app.route("/update_user/<int:id>", methods=['GET', 'POST'])
@login_required
def update_user(id):
    date = datetime.now()
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
            return redirect(url_for('dashboard', update_form=update_form,
                                    user_to_update=user_to_update, id=id))
        except:
            flash("Neco se nepovedlo. Zkuste to znovu.")
            return render_template('update_user.html', update_form=update_form,
                                   user_to_update=user_to_update, date=date, id=id)
    else:
        return render_template('update_user.html', update_form=update_form,
                               post_to_update=user_to_update, date=date, id=id)


@app.route("/upload_profile_pic", methods=['GET', 'POST'])
@login_required
def upload_profile_pic():
    date = datetime.now()
    id = current_user.id
    form = PictureForm()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("dashboard"))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("dashboard"))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_pic = str(uuid.uuid1()) + "_" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_pic))
            flash(f"Vase profilova fotografie byla zmenena! {filename_pic}")
            picture = Picture(name=filename_pic, picture=file.read(), poster_id=id)
            return redirect(url_for('dashboard',
                                    filename_pic=filename_pic))
    return render_template("upload_profile_pic.html", date=date, form=form)
    #
    # if request.method == 'POST':
    #     if file = request.files['file']

    #     # grab image name
    #     picture_filename = secure_filename(file.filename)
    #     # set uuid
    #     picture_name = str(uuid.uuid1()) + "_" + picture_filename
    #
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
    #
    #     picture = Picture(name=picture_name, picture=file.read(), poster_id=id)
    #
    #     db.session.add(picture)
    #     db.session.commit()
    #
    #     flash(f"Uploaded: {picture_name}")
    #     flash("Vase profilova fotografie byla zmenena.")
    #     return redirect(url_for('dashboard', date=date, picture_name=picture_name))
    #
    # return render_template("upload_profile_pic.html", date=date,
    #                        form=form)

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
    password2 = db.Column(db.String(100), nullable=False)
    profile_pic = db.relationship("Picture", backref="poster")
    terms_agreement = db.Column(db.String(100), nullable=False)
    blog_posts = db.relationship('Posts', backref="poster")
    date_of_registration = db.Column(db.DateTime, default=datetime.now)
    #
    # def __repr__(self):
    #     return f'<Users "{self.title}">'
    #
    # def __init__(self, name, username, surname,
    #              occupation, phone_number, gender,
    #              email, street_address, house_number,
    #              city, state, state2, zip_code, password,
    #              password2, terms_agreement, date_of_registration):
    #     self.name = name
    #     self.username = username
    #     self.surname = surname
    #     self.occupation = occupation
    #     self.phone_number = phone_number
    #     self.gender = gender
    #     self.email = email
    #     self.street_address = street_address
    #     self.house_number = house_number
    #     self.city = city
    #     self.state = state
    #     self.state2 = state2
    #     self.zip_code = zip_code
    #     self.password = password
    #     self.password2 = password2
    #     self.terms_agreement = terms_agreement
    #     self.date_of_registration = datetime.now()
    #     self.profile_pic = self.profile_pic


# blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.now)
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #
    # def __repr__(self):
    #     return f'<Posts "{self.title}">'
    #
    # def __init__(self, title, content, slug, date_posted, poster_id):
    #     self.title = title
    #     self.content = content
    #     # self.author = author
    #     self.date_posted = datetime.now()
    #     self.slug = slug
    #     self.poster_id = poster_id


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.LargeBinary)
    name = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.DateTime, default=datetime.now)
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #
    # def __init__(self, picture, poster_id, name, mimetype):
    #     self.picture = picture
    #     self.poster_id = poster_id
    #     self.name = name
    #     self.mimetype = mimetype


class DeletedPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.String(255))
    slug = db.Column(db.String(255))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_deleted = db.Column(db.DateTime, default=datetime.now)
    #
    # def __repr__(self):
    #     return f'<DeletedPosts "{self.title}">'
    #
    # def __init__(self, title, content, poster_id, slug, date_posted, date_deleted):
    #     self.title = title
    #     self.content = content
    #     # self.author = author
    #     self.date_posted = date_posted
    #     self.slug = slug
    #     self.date_deleted = datetime.now()
    #     self.poster_id = poster_id

    # Creation of the database tables if the db doesnt already exists.


with app.app_context():
    db.create_all()

# def __repr__(self):
#     return '<Name %r>' % self.name

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

if __name__ == "__main__":
    app.run(debug=True)
