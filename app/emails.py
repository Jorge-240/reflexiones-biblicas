from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_welcome_email(user):
    msg = Message(
        subject="Bienvenido/a a Fe y Reflexión — tu caminar comienza aquí",
        recipients=[user.email],
    )
    msg.html = render_template(
        "email/welcome.html",
        user=user,
        base_url=current_app.config["APP_BASE_URL"],
    )
    msg.body = (
        f"Hola {user.nombre},\n\n"
        "Gracias por unirte. Explora reflexiones bíblicas y herramientas en la web.\n"
        f"Ingresa aquí: {current_app.config['APP_BASE_URL']}/auth/login\n"
    )
    mail.send(msg)


def send_password_reset_email(user, reset_url: str):
    msg = Message(
        subject="Recuperación de contraseña — Fe y Reflexión",
        recipients=[user.email],
    )
    msg.html = render_template(
        "email/reset_password.html",
        user=user,
        reset_url=reset_url,
        base_url=current_app.config["APP_BASE_URL"],
    )
    msg.body = (
        f"Hola {user.nombre},\n\n"
        "Recibimos una solicitud para restablecer tu contraseña.\n"
        f"Usa este enlace (válido por tiempo limitado): {reset_url}\n\n"
        "Si no fuiste tú, ignora este mensaje.\n"
    )
    mail.send(msg)


def send_support_to_developer(contact_email: str, asunto: str, descripcion: str, username: str | None):
    dev = current_app.config["DEVELOPER_EMAIL"]
    msg = Message(
        subject=f"[Soporte Fe y Reflexión] {asunto}",
        recipients=[dev],
        reply_to=contact_email or dev,
    )
    msg.html = render_template(
        "email/support_report.html",
        contact_email=contact_email,
        username=username,
        asunto=asunto,
        descripcion=descripcion,
    )
    msg.body = (
        f"Reporte de soporte\n\n"
        f"Contacto: {contact_email}\n"
        f"Usuario: {username or 'invitado'}\n"
        f"Asunto: {asunto}\n\n"
        f"{descripcion}\n"
    )
    mail.send(msg)
