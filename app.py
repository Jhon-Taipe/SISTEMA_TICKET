from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "12345"

# Crear BD simple
def init_db():
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY, titulo TEXT, estado TEXT, mensaje TEXT)''')

    conn.commit()
    conn.close()

init_db()

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["usuario"]
        pwd = request.form["password"]

        if user == "admin" and pwd == "123":
            session["user"] = user
            return redirect("/tickets")
    return render_template("login.html")

# LISTAR TICKETS
@app.route("/tickets")
def tickets():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tickets")
    data = c.fetchall()
    conn.close()

    return render_template("tickets.html", tickets=data)

# CREAR TICKET
@app.route("/crear", methods=["POST"])
def crear():
    titulo = request.form["titulo"]

    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("INSERT INTO tickets (titulo, estado, mensaje) VALUES (?, ?, ?)", (titulo, "Pendiente", ""))
    conn.commit()
    conn.close()

    return redirect("/tickets")

# CAMBIAR ESTADO
@app.route("/estado/<int:id>/<nuevo_estado>")
def cambiar_estado(id, nuevo_estado):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("UPDATE tickets SET estado=? WHERE id=?", (nuevo_estado, id))
    conn.commit()
    conn.close()
    return redirect("/tickets")

@app.route("/mensaje/<int:id>", methods=["POST"])
def guardar_mensaje(id):
    mensaje = request.form["mensaje"]

    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("UPDATE tickets SET mensaje=? WHERE id=?", (mensaje, id))
    conn.commit()
    conn.close()    

    return redirect("/tickets")

app.run(debug=True)