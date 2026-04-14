import os

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from app import db
from app.emails import send_password_reset_email, send_support_to_developer, send_welcome_email
from app.forms import (
    ChangePasswordForm,
    ForgotPasswordForm,
    GeminiReflectionForm,
    LoginForm,
    ProfileForm,
    RegistrationForm,
    ResetPasswordForm,
    SupportForm,
)
from app.gemini_service import generar_reflexion_biblica
from app.image_generator import crear_tarjeta_reflexion
from app.models import CuratedReflection, GeneratedReflection, SupportReport, User

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="fe-reflexion-recovery")


@main_bp.route("/")
def index():
    reflexiones = CuratedReflection.query.order_by(CuratedReflection.orden.asc(), CuratedReflection.id.asc()).limit(6).all()
    return render_template("index.html", reflexiones=reflexiones)


@main_bp.route("/reflexiones")
@login_required
def reflexiones():
    curated = CuratedReflection.query.order_by(CuratedReflection.orden.asc(), CuratedReflection.id.asc()).all()
    generadas = (
        GeneratedReflection.query.filter_by(user_id=current_user.id)
        .order_by(GeneratedReflection.created_at.desc())
        .limit(24)
        .all()
    )
    form = GeminiReflectionForm()
    return render_template("reflexiones.html", curated=curated, generadas=generadas, form=form)


@main_bp.route("/reflexiones/generar", methods=["POST"])
@login_required
def generar_reflexion_imagen():
    form = GeminiReflectionForm()
    if not form.validate_on_submit():
        for err in form.errors.values():
            flash(err[0], "danger")
        return redirect(url_for("main.reflexiones"))
    tema = (form.tema.data or "").strip() or None
    try:
        data = generar_reflexion_biblica(tema)
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("main.reflexiones"))

    out_dir = os.path.join(current_app.static_folder, "generated")
    try:
        rel_path = crear_tarjeta_reflexion(
            cita=data["cita_corta"],
            referencia=data["referencia"],
            reflexion=data["reflexion"],
            output_dir=out_dir,
        )
    except Exception as e:
        flash(f"No se pudo crear la imagen: {e}", "danger")
        return redirect(url_for("main.reflexiones"))

    peticion = tema or "(tema libre)"
    gr = GeneratedReflection(
        user_id=current_user.id,
        tema_o_peticion=peticion,
        texto_gemini=data["reflexion"],
        referencia_sugerida=data["referencia"],
        archivo_relativo=rel_path,
    )
    db.session.add(gr)
    db.session.commit()
    flash("Reflexión generada. Puedes descargar la imagen abajo.", "success")
    return redirect(url_for("main.reflexiones"))


@main_bp.route("/descargas/<int:reflection_id>")
@login_required
def descargar_reflexion(reflection_id: int):
    gr = GeneratedReflection.query.get_or_404(reflection_id)
    if gr.user_id != current_user.id:
        abort(403)
    folder = os.path.dirname(os.path.join(current_app.static_folder, gr.archivo_relativo))
    fname = os.path.basename(gr.archivo_relativo)
    return send_from_directory(folder, fname, as_attachment=True, download_name=f"reflexion_{reflection_id}.png")


@main_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    profile_form = ProfileForm(
        prefix="pf",
        original_username=current_user.username,
        original_email=current_user.email,
        obj=current_user,
    )
    pwd_form = ChangePasswordForm(prefix="pwd")
    if request.method == "POST":
        if "pf-save_profile" in request.form and profile_form.validate():
            current_user.nombre = profile_form.nombre.data.strip()
            current_user.apellido = profile_form.apellido.data.strip()
            current_user.username = profile_form.username.data.strip()
            current_user.email = profile_form.email.data.strip().lower()
            db.session.commit()
            flash("Perfil actualizado.", "success")
            return redirect(url_for("main.perfil"))
        if "pwd-change_password" in request.form and pwd_form.validate():
            if not current_user.check_password(pwd_form.current_password.data):
                flash("La contraseña actual no es correcta.", "danger")
            else:
                current_user.set_password(pwd_form.password.data)
                db.session.commit()
                flash("Contraseña actualizada.", "success")
                return redirect(url_for("main.perfil"))
    return render_template("perfil.html", profile_form=profile_form, pwd_form=pwd_form)


@main_bp.route("/soporte", methods=["GET", "POST"])
def soporte():
    form = SupportForm()
    if current_user.is_authenticated and request.method == "GET":
        form.contact_email.data = current_user.email
    if request.method == "POST" and form.validate_on_submit():
        email_contacto = form.contact_email.data.strip().lower()
        try:
            send_support_to_developer(
                contact_email=email_contacto,
                asunto=form.asunto.data.strip(),
                descripcion=form.descripcion.data.strip(),
                username=current_user.username if current_user.is_authenticated else None,
            )
        except Exception as e:
            flash(f"No se pudo enviar el reporte por correo: {e}", "danger")
            return render_template("soporte.html", form=form)
        rep = SupportReport(
            user_id=current_user.id if current_user.is_authenticated else None,
            contacto_email=email_contacto,
            asunto=form.asunto.data.strip(),
            descripcion=form.descripcion.data.strip(),
        )
        db.session.add(rep)
        db.session.commit()
        flash("Gracias. Tu mensaje fue enviado al equipo de soporte.", "success")
        return redirect(url_for("main.soporte"))
    return render_template("soporte.html", form=form)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("main.reflexiones"))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(
            nombre=form.nombre.data.strip(),
            apellido=form.apellido.data.strip(),
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
        )
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        try:
            send_welcome_email(u)
        except Exception as e:
            flash(f"Cuenta creada, pero el correo de bienvenida no se pudo enviar: {e}", "warning")
        flash("Cuenta creada. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("registro.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.reflexiones"))
    form = LoginForm()
    if form.validate_on_submit():
        ident = form.username.data.strip()
        user = User.query.filter((User.username == ident) | (User.email == ident.lower())).first()
        if user is None or not user.check_password(form.password.data):
            flash("Usuario o contraseña incorrectos.", "danger")
        elif not user.is_active:
            flash("Cuenta desactivada.", "danger")
        else:
            login_user(user, remember=form.remember.data)
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("main.reflexiones"))
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("main.index"))


@auth_bp.route("/recuperar", methods=["GET", "POST"])
def recuperar():
    if current_user.is_authenticated:
        return redirect(url_for("main.reflexiones"))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Ese correo no se encuentra registrado.", "danger")
            return render_template("recuperar.html", form=form)
        token = _serializer().dumps({"uid": user.id})
        reset_url = url_for("auth.restablecer", token=token, _external=True)
        try:
            send_password_reset_email(user, reset_url)
        except Exception as e:
            flash(f"No se pudo enviar el correo: {e}", "danger")
            return render_template("recuperar.html", form=form)
        flash("Revisa tu bandeja de entrada para continuar.", "success")
        return redirect(url_for("auth.login"))
    return render_template("recuperar.html", form=form)


@auth_bp.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.reflexiones"))
    try:
        data = _serializer().loads(token, max_age=60 * 60 * 24)
    except SignatureExpired:
        flash("El enlace expiró. Solicita uno nuevo.", "danger")
        return redirect(url_for("auth.recuperar"))
    except BadSignature:
        flash("Enlace no válido.", "danger")
        return redirect(url_for("auth.recuperar"))
    user = User.query.get(data.get("uid"))
    if not user:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("auth.login"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Contraseña actualizada. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("restablecer.html", form=form)
