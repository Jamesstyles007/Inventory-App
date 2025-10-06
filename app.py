from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, ProductMovement, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


# ---------------- Authentication ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for("signup"))

        # Create new user
        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        login_user(user)  # Auto login after sign-up
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------------- Home ----------------
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# ---------------- Products ----------------
@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    if request.method == "POST":
        pid = request.form["product_id"]
        name = request.form["name"]
        desc = request.form.get("description", "")
        db.session.add(Product(product_id=pid, name=name, description=desc))
        db.session.commit()
        return redirect(url_for("products"))

    products = Product.query.all()
    return render_template("products.html", products=products)

@app.route("/products/edit/<pid>", methods=["GET", "POST"])
@login_required
def edit_product(pid):
    product = Product.query.get_or_404(pid)
    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form.get("description", "")
        db.session.commit()
        return redirect(url_for("products"))
    return render_template("edit_product.html", product=product)

@app.route("/products/delete/<pid>")
@login_required
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products"))


# ---------------- Movements ----------------
@app.route("/movements", methods=["GET", "POST"])
@login_required
def movements():
    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form["product_id"]
        from_loc = request.form.get("from_location") or None
        to_loc = request.form.get("to_location") or None
        qty = int(request.form["qty"])
        db.session.add(ProductMovement(product_id=product_id,
                                       from_location=from_loc,
                                       to_location=to_loc,
                                       qty=qty))
        db.session.commit()
        return redirect(url_for("movements"))

    movements = ProductMovement.query.all()
    return render_template("movements.html", movements=movements, products=products)

@app.route("/movements/delete/<mid>")
@login_required
def delete_movement(mid):
    movement = ProductMovement.query.get_or_404(mid)
    db.session.delete(movement)
    db.session.commit()
    return redirect(url_for("movements"))


# ---------------- Add Stock ----------------
@app.route("/add_stock", methods=["GET", "POST"])
@login_required
def add_stock():
    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form["product_id"]
        location = request.form["location"]
        qty = int(request.form["qty"])
        db.session.add(ProductMovement(product_id=product_id,
                                       from_location=None,
                                       to_location=location,
                                       qty=qty))
        db.session.commit()
        return redirect(url_for("add_stock"))

    return render_template("add_stock.html", products=products)


# ---------------- Report ----------------
@app.route("/report")
@login_required
def report():
    movements = ProductMovement.query.all()
    balance = {}
    for m in movements:
        if m.to_location:
            balance[(m.product_id, m.to_location)] = balance.get((m.product_id, m.to_location), 0) + m.qty
        if m.from_location:
            balance[(m.product_id, m.from_location)] = balance.get((m.product_id, m.from_location), 0) - m.qty

    totals = {}
    for (product, location), qty in balance.items():
        totals[product] = totals.get(product, 0) + qty

    return render_template("report.html", report=balance, totals=totals, movements=movements)


if __name__ == "__main__":
    app.run(debug=True)
