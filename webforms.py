from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, equal_to
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

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
    gender = SelectField(" Gender", choices=['Žena', 'Muž', 'Jiné'], validators=[DataRequired()])
    email = StringField(" E-mail", validators=[DataRequired()])
    street_address = StringField(" Ulice", validators=[DataRequired()])
    house_number = StringField(" c.p.", validators=[DataRequired()])
    city = StringField(" Mesto", validators=[DataRequired()])
    state = SelectField(" Stat", choices=[" ", "Belgické království",
                                          "Bulharská republika",
                                          "Česká republika",
                                          "Dánské království",
                                          "Estonská republika",
                                          "Finská republika",
                                          "Francouzská republika",
                                          "Chorvatská republika",
                                          "Irsko",
                                          "Italská republika",
                                          "Kyperská republika",
                                          "Litevská republika",
                                          "Lotyšská republika",
                                          "Lucemburské velkovévodství",
                                          "Maďarsko",
                                          "Maltská republika",
                                          "Spolková republika Německo",
                                          "Nizozemské království",
                                          "Polská republika",
                                          "Portugalská republika",
                                          "Rakouská republika",
                                          "Rumunsko",
                                          "Řecká republika",
                                          "Slovenská republika",
                                          "Slovinská republika",
                                          "Španělské království",
                                          "Švédské království",
                                          "jiny stat"])
    state2 = StringField(" jiny stat")
    zip_code = StringField(" PSC", validators=[DataRequired()])
    password = PasswordField(" Heslo",
                             validators=[DataRequired(), equal_to("password2", message="Hesla musi souhlasit.")])
    password2 = PasswordField(" Opakovat heslo", validators=[DataRequired()])
    profile_pic = FileField('Profilove foto')
    terms_agreement = BooleanField(" Souhlasím s podmínkami", validators=[DataRequired()])
    submit = SubmitField("Sign up")


# create post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    # content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField("Submit post")
