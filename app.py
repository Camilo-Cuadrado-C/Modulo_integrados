# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'hola'

bcrypt = Bcrypt(app)

#  Conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="bd_arte_en_papel",
        user="soporte",
        password="soporte"
    )

#  Página principal (registro)
@app.route("/")
def home():
    return render_template("usuario.html")

#  Registrar usuario
@app.route("/registrar", methods=["POST"])
def registrar():
    usuario = request.form["usuario"]
    correo = request.form["correo"]
    contraseña = request.form["password"]

    conexion = get_db_connection()
    cursor = conexion.cursor()

    #  Validar si el correo ya existe
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        flash("El correo ya está registrado", "error")
        cursor.close()
        conexion.close()
        return redirect(url_for("home"))

    #  Encriptar contraseña
    contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    cursor.execute(
        "INSERT INTO usuarios (usuario, correo, contraseña) VALUES (%s, %s, %s)",
        (usuario, correo, contraseña_hash)
    )

    conexion.commit()
    cursor.close()
    conexion.close()

    flash("Usuario registrado correctamente", "success")
    return redirect(url_for("home"))


#  Ver usuarios registrados
@app.route("/usuarios")
def usuarios():
    conexion = get_db_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, usuario, correo, fecha_registro FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("registro.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)
