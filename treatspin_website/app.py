
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

PRODUCT = {
    "name": "TreatSpin™ Interactive Treat Ball",
    "price": 19.99,
    "description": "A fun treat-dispensing toy that keeps your pet curious, active, and rewarded.",
    "features": [
        "Adjustable treat opening",
        "Rolling and interactive design",
        "Easy to clean",
        "Great for dogs and cats"
    ]
}

@app.route("/", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("home.html", product=PRODUCT, user=session.get("user"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if email and password:
            session["logged_in"] = True
            session["user"] = email.split("@")[0]
            return redirect(url_for("home"))
        flash("Please enter your email and password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/buy", methods=["POST"])
def buy():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    session["cart_count"] = session.get("cart_count", 0) + 1
    flash("Added to your cart!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
