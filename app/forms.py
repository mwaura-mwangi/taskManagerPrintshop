# app/forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField,
    SelectField, DateField, SubmitField, TextAreaField   # ← added TextAreaField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf.file import FileField, FileAllowed

# Keep this in sync with your .env ALLOWED_EXT
ALLOWED = ["pdf", "png", "jpg", "jpeg", "tif", "tiff", "ai", "eps"]

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Create Account")

class JobForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    priority = SelectField(
        "Priority",
        choices=[("low","Low"),("normal","Normal"),("high","High")],
        default="normal",
        validators=[DataRequired()],
    )
    due_date = DateField("Due date", validators=[Optional()])
    file = FileField("Source file", validators=[Optional(), FileAllowed(ALLOWED, "Unsupported file type.")])
    note = TextAreaField("Initial Note", validators=[Optional(), Length(max=1000)])  # ← NEW
    submit = SubmitField("Create Job")
