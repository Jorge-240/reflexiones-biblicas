from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(max=80)])
    username = StringField("Nombre de usuario", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas deben coincidir.")],
    )
    submit = SubmitField("Crear cuenta")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.strip()).first():
            raise ValidationError("Ese nombre de usuario ya está en uso.")

    def validate_email(self, field):
        if User.query.filter_by(email=(field.data or "").strip().lower()).first():
            raise ValidationError("Ese correo ya está registrado.")


class LoginForm(FlaskForm):
    username = StringField("Usuario o correo", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember = BooleanField("Recordarme")
    submit = SubmitField("Entrar")


class ForgotPasswordForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar enlace de recuperación")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Nueva contraseña", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas deben coincidir.")],
    )
    submit = SubmitField("Guardar nueva contraseña")


class ProfileForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(max=80)])
    username = StringField("Nombre de usuario", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email(), Length(max=255)])
    save_profile = SubmitField("Guardar perfil")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_username = original_username
        self._original_email = original_email

    def validate_username(self, field):
        u = field.data.strip()
        if u != self._original_username and User.query.filter_by(username=u).first():
            raise ValidationError("Ese nombre de usuario ya está en uso.")

    def validate_email(self, field):
        e = (field.data or "").strip().lower()
        orig = (self._original_email or "").strip().lower()
        if e != orig and User.query.filter_by(email=e).first():
            raise ValidationError("Ese correo ya está registrado.")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Contraseña actual", validators=[DataRequired()])
    password = PasswordField("Nueva contraseña", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Confirmar nueva contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas deben coincidir.")],
    )
    change_password = SubmitField("Cambiar contraseña")


class GeminiReflectionForm(FlaskForm):
    tema = StringField(
        "Tema o petición (opcional)",
        validators=[Optional(), Length(max=500)],
        description="Ej.: gratitud en familia, paz en el trabajo, perdón…",
    )
    submit = SubmitField("Generar reflexión e imagen")


class SupportForm(FlaskForm):
    contact_email = StringField("Correo de contacto", validators=[DataRequired(), Email(), Length(max=255)])
    asunto = StringField("Asunto", validators=[DataRequired(), Length(max=200)])
    descripcion = TextAreaField(
        "Describe el problema",
        validators=[DataRequired(), Length(min=10, max=8000)],
    )
    submit = SubmitField("Enviar reporte")
