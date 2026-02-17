from flask import Flask, render_template, request, redirect, session,flash
from models import create_tables, create_user, get_user, get_user_by_id, update_subscription_type, user_exists
import requests
from flask import abort


app = Flask(__name__)

# Configuración de la clave secreta para sesiones
app.secret_key = "clave_secreta_para_sesiones"

@app.route("/")
def index():
    return redirect("/login")

# Creamos las tablas de la base de datos
create_tables()

@app.route("/registro", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # VALIDACIONES
        if not username or not password:
            message = "❌ Todos los campos son obligatorios."

        elif len(username) < 4:
            message = "❌ El usuario debe tener mínimo 4 caracteres."

        elif len(password) < 6:
            message = "❌ La contraseña debe tener mínimo 6 caracteres."

        elif user_exists(username):   # función que valida si existe
            message = "❌ El usuario ya existe."

        else:
            create_user(username, password)
            message = "✅ Usuario registrado correctamente."

    return render_template("registro.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():   
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username, password)

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["subscription_type"] = user[2]
            return redirect("/home")
        else:
            flash("Usuario o contraseña incorrectos ❌", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()  # Limpiamos la sesión para cerrar la sesión del usuario
    return redirect("/login")

@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/login")
    
    return render_template(
        "home.html", 
        username=session["username"], 
        subscription_type=session["subscription_type"]
    )

@app.route("/catalog")
def catalog():
    if "user_id" not in session:
        return redirect("/login")

    response = requests.get("https://api.tvmaze.com/shows")
    shows = response.json()[:12]

    # Marcamos contenido FREE / PREMIUM
    for index, show in enumerate(shows):
        show["access"] = "FREE" if index < 4 else "PREMIUM"

    return render_template(
        "catalog.html",
        shows=shows,
        subscription_type=session["subscription_type"]
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    user = get_user_by_id(session["user_id"])

    if request.method == "POST":
        new_subscription_type = request.form["subscription_type"]
        update_subscription_type(session["user_id"], new_subscription_type)
        session["subscription_type"] = new_subscription_type  # Actualizamos la suscripción en la sesión
        
    user = get_user_by_id(session["user_id"])  # Obtenemos la información actualizada del usuario

    return render_template("profile.html", username=user[1], subscription_type=user[2])

@app.route("/watch/<int:show_id>")
def watch(show_id):
    if "user_id" not in session:
        return redirect("/login")

    response = requests.get("https://api.tvmaze.com/shows")
    shows = response.json()

    show = next((s for s in shows if s["id"] == show_id), None)

    if not show:
        abort(404)

    index = shows.index(show)
    access = "FREE" if index < 4 else "PREMIUM"

    if access == "PREMIUM" and session["subscription_type"] != "PREMIUM":
        return render_template("blocked.html", show=show)

    youtube_videos = {
        0: "f_Y5YeYrqUk",  
        1: "HQXmfAGOe0Y",
        2: "tUQ_ZXjzkiQ",
        3: "nPL9wWWuFqA",
        4: "WkL7cpG2UhE",  
        5: "aDrsItJ_HU4",
        6: "Liucv1Hte4c",
        7: "sefQqCMusJI",
        8: "R1C8ygebkng",  
        9: "2-4xKNZ_gaA",
        10: "VwOPA2upeCA",
        11: "W057R9MNRw4"
    }
    video_url = youtube_videos.get(index)
    

    return render_template("watch.html", show=show, video_url=video_url)


    
if __name__ == "__main__":
    app.run(debug=True)
