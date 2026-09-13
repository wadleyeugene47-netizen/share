from flask import Flask, request, redirect, url_for, session, render_template_string, flash, send_file

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

PRODUCT = {
    "name": "TreatSpin™ Interactive Treat Ball",
    "price": 19.99,
    "description": "A fun treat-dispensing toy that keeps your pet curious, active, and rewarded."
}

# ---------------- LOGIN PAGE ----------------

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | TreatSpin</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f8f5;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .login-box {
            width: 400px;
            max-width: 90%;
            background: white;
            padding: 40px;
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,.10);
            text-align: center;
        }

        .logo {
            font-size: 27px;
            font-weight: bold;
            color: #17221c;
        }

        .logo span {
            color: #63a995;
        }

        .paw {
            font-size: 45px;
            margin-top: 25px;
        }

        h1 {
            color: #17221c;
        }

        .description {
            color: #777;
        }

        label {
            display: block;
            text-align: left;
            margin-top: 20px;
            margin-bottom: 7px;
            font-weight: bold;
            font-size: 14px;
        }

        input {
            width: 100%;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 15px;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 15px;
            background: #17221c;
            color: white;
            border: none;
            border-radius: 11px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            opacity: .9;
        }

        .demo {
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>

<body>

<div class="login-box">

    <div class="logo">
        Treat<span>Spin</span>™
    </div>

    <div class="paw">🐾</div>

    <h1>Welcome Back</h1>

    <p class="description">
        Sign in to shop smarter for your best friend.
    </p>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <p>{{ messages[0] }}</p>
        {% endif %}
    {% endwith %}

    <form method="POST">

        <label>Email</label>

        <input
            type="email"
            name="email"
            placeholder="you@example.com"
            required
        >

        <label>Password</label>

        <input
            type="password"
            name="password"
            placeholder="••••••••"
            required
        >

        <button type="submit">
            Sign In
        </button>

    </form>

    <p class="demo">
        Demo website: any email and password will work.
    </p>

</div>

</body>
</html>
"""


# ---------------- STORE PAGE ----------------

STORE_PAGE = """
<!DOCTYPE html>
<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{{ product.name }}</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #17221c;
    background: #f8faf6;
}


/* HEADER */

header {
    height: 75px;
    padding: 0 7%;
    background: white;

    display: flex;
    justify-content: space-between;
    align-items: center;

    border-bottom: 1px solid #e5ebe6;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

.logo span {
    color: #63a995;
}

nav {
    display: flex;
    gap: 25px;
    align-items: center;

    color: #59645e;
    font-size: 14px;
}

.logout {
    padding: 9px 14px;
    border: 1px solid #ddd;
    border-radius: 10px;
}


/* MAIN */

main {
    max-width: 1150px;
    margin: auto;
    padding: 50px 25px;
}


/* HERO */

.hero {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 70px;

    align-items: center;

    min-height: 550px;
}


/* PRODUCT IMAGE */

.product-image {

    position: relative;

    text-align: center;

}

.product-image::before {

    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    border-radius: 50%;

    background: #dcefe7;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%);

    z-index: -1;
}

.product-image img {

    width: 100%;
    max-width: 500px;

    border-radius: 25px;

    mix-blend-mode: multiply;

}


/* BADGE */

.badge {

    position: absolute;

    right: 5%;
    top: 5%;

    width: 80px;
    height: 80px;

    border-radius: 50%;

    background: #17221c;

    color: white;

    display: flex;

    justify-content: center;
    align-items: center;

    text-align: center;

    font-size: 10px;

    font-weight: bold;

    transform: rotate(8deg);
}


/* TEXT */

.eyebrow {

    color: #5c9e89;

    font-size: 12px;

    letter-spacing: 2px;

    font-weight: bold;
}

h1 {

    font-size: 55px;

    line-height: 1.05;

    letter-spacing: -2px;

    margin: 15px 0;
}

h1 em {

    font-family: Georgia, serif;

}

.description {

    font-size: 18px;

    line-height: 1.7;

    color: #69756e;
}

.rating {

    margin:
        25px 0;

    font-size: 17px;
}

.rating span {

    color: #777;

    font-size: 13px;

}


/* PRICE */

.price {

    font-size: 35px;

    font-weight: bold;

}

.old-price {

    margin-left: 10px;

    color: #999;

    text-decoration: line-through;
}


/* BUTTON */

.buy-button {

    margin-top: 25px;

    width: 260px;

    padding: 16px;

    background: #17221c;

    color: white;

    border: none;

    border-radius: 12px;

    font-size: 15px;

    font-weight: bold;

    cursor: pointer;
}


/* FEATURES */

.features {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 20px;

    margin-top: 60px;
}

.feature {

    background: white;

    border: 1px solid #e5ebe6;

    padding: 30px;

    border-radius: 18px;
}

.feature-icon {

    font-size: 30px;
}

.feature h3 {

    margin:
        12px 0 8px;
}

.feature p {

    color: #737e78;

    line-height: 1.6;

    font-size: 14px;
}


/* MESSAGE */

.message {

    text-align: center;

    background: #e5f4ed;

    color: #286d59;

    padding: 12px;
}


/* MOBILE */

@media(max-width: 800px) {

    nav a:not(.logout) {
        display: none;
    }

    .hero {

        grid-template-columns: 1fr;

        gap: 30px;
    }

    h1 {

        font-size: 43px;
    }

    .product-image::before {

        width: 290px;
        height: 290px;
    }

    .features {

        grid-template-columns: 1fr;
    }

}

</style>

</head>


<body>


<header>

    <div class="logo">
        Treat<span>Spin</span>™
    </div>

    <nav>

        <a href="#features">
            Features
        </a>

        <span>
            Hi, {{ user }}
        </span>

        <a class="logout" href="/logout">
            Log out
        </a>

    </nav>

</header>


{% with messages = get_flashed_messages() %}

    {% if messages %}

        <div class="message">
            {{ messages[0] }}
        </div>

    {% endif %}

{% endwith %}


<main>


<section class="hero">


<!-- PRODUCT IMAGE -->

<div class="product-image">

    <img
        src="/product.jpg"
        alt="TreatSpin Interactive Treat Ball"
    >

    <div class="badge">

        BEST<br>
        SELLER

    </div>

</div>


<!-- PRODUCT INFORMATION -->

<div>

    <div class="eyebrow">

        SMART PLAY • HAPPY PETS

    </div>


    <h1>

        Turn treat time into
        <em>play time.</em>

    </h1>


    <p class="description">

        {{ product.description }}

    </p>


    <div class="rating">

        ⭐⭐⭐⭐⭐

        <span>
            4.9/5 · 1,200+ happy pet parents
        </span>

    </div>


    <div>

        <span class="price">

            ${{ "%.2f"|format(product.price) }}

        </span>

        <span class="old-price">

            $29.99

        </span>

    </div>


    <form method="POST" action="/buy">

        <button class="buy-button">

            Add to Cart →

        </button>

    </form>


    <p>

        ✓ Free shipping
        ·
        ✓ 30-day returns
        ·
        ✓ Secure checkout

    </p>


</div>


</section>


<!-- FEATURES -->

<section id="features" class="features">


<div class="feature">

    <div class="feature-icon">
        🧠
    </div>

    <h3>
        Mental Stimulation
    </h3>

    <p>

        Turn snacks into a rewarding puzzle
        that keeps pets engaged.

    </p>

</div>


<div class="feature">

    <div class="feature-icon">
        🏃
    </div>

    <h3>
        Active Play
    </h3>

    <p>

        Rolling movement encourages pets
        to chase, paw and explore.

    </p>

</div>


<div class="feature">

    <div class="feature-icon">
        🧼
    </div>

    <h3>
        Easy To Clean
    </h3>

    <p>

        Simple design makes refilling
        and cleaning quick and easy.

    </p>

</div>


</section>


</main>

</body>

</html>
"""


# ---------------- LOGIN ----------------

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

    return render_template_string(LOGIN_PAGE)


# ---------------- HOME ----------------

@app.route("/")
def home():

    if not session.get("logged_in"):

        return redirect(url_for("login"))

    return render_template_string(
        STORE_PAGE,
        product=PRODUCT,
        user=session["user"]
    )


# ---------------- ADD TO CART ----------------

@app.route("/buy", methods=["POST"])
def buy():

    if not session.get("logged_in"):

        return redirect(url_for("login"))

    flash("✅ Product added to your cart!")

    return redirect(url_for("home"))


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- PRODUCT IMAGE ----------------

@app.route("/product.jpg")
def product_image():

    return send_file(
        "product.jpg",
        mimetype="image/jpeg"
    )


# ---------------- START SERVER ----------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )