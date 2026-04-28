from flask import Flask, render_template, request, redirect, session
import psycopg2
import os
DATABASE_URL = "postgresql://tickets_bd_user:PsQaGIjyr5d2vstugfEgn4J1RrL1eK1n@dpg-d7o257hf9bms738rc220-a.oregon-postgres.render.com/tickets_bd"

app = Flask(__name__)
app.secret_key = "12345"

# 🔌 Conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        pwd = request.form["password"]
    
        if (user == "pao" and pwd == "lucas") or (user == "jhon" and pwd == "123"):
            session["user"] = user
            return redirect("/tickets")

    return render_template("login.html")


# LISTAR TICKETS
@app.route("/tickets")
def tickets():
    if "user" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()

    return render_template("tickets.html", tickets=data)


# CREAR TICKET
@app.route("/crear", methods=["POST"])
def crear():
    titulo = request.form["titulo"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (titulo, estado, mensaje) VALUES (%s, %s, %s)",
        (titulo, "Pendiente", "")
    )
    conn.commit()
    conn.close()

    return redirect("/tickets")


# CAMBIAR ESTADO
@app.route("/estado/<int:id>/<nuevo_estado>")
def cambiar_estado(id, nuevo_estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET estado=%s WHERE id=%s",
        (nuevo_estado, id)
    )
    conn.commit()
    conn.close()

    return redirect("/tickets")


# GUARDAR MENSAJE
@app.route("/mensaje/<int:id>", methods=["POST"])
def guardar_mensaje(id):
    mensaje = request.form["mensaje"]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET mensaje=%s WHERE id=%s",
        (mensaje, id)
    )
    conn.commit()
    conn.close()

    return redirect("/tickets")


# ELIMINAR TICKET
@app.route("/eliminar/<int:id>")
def eliminar_ticket(id):
    if "user" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tickets WHERE id=%s",
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect("/tickets")


# RUN APP
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)