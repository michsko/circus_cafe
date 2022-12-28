from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "Ja Pisi Vam Co Mohu Vice"


# create a Form Class
class loginForm(FlaskForm):
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
