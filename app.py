from flask import Flask, render_template, request, redirect, url_for
from models import db, Product, ProductMovement

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- Home ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- Products ----------------
@app.route("/products", methods=["GET", "POST"])
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
def edit_product(pid):
    product = Product.query.get_or_404(pid)
    if request.method == "POST":
        product.name = request.form["name"]
        product.description = request.form.get("description", "")
        db.session.commit()
        return redirect(url_for("products"))
    return render_template("edit_product.html", product=product)


@app.route("/products/delete/<pid>")
def delete_product(pid):
    product = Product.query.get_or_404(pid)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products"))


# ---------------- Movements ----------------
@app.route("/movements", methods=["GET", "POST"])
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
def delete_movement(mid):
    movement = ProductMovement.query.get_or_404(mid)
    db.session.delete(movement)
    db.session.commit()
    return redirect(url_for("movements"))


# ---------------- Add Stock Directly ----------------
@app.route("/add_stock", methods=["GET", "POST"])
def add_stock():
    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form["product_id"]
        location = request.form["location"]
        qty = int(request.form["qty"])

        # Create a ProductMovement with only "to_location"
        db.session.add(ProductMovement(product_id=product_id,
                                       from_location=None,
                                       to_location=location,
                                       qty=qty))
        db.session.commit()
        return redirect(url_for("add_stock"))

    return render_template("add_stock.html", products=products)


# ---------------- Report ----------------
@app.route("/report")
def report():
    movements = ProductMovement.query.all()
    balance = {}

    for m in movements:
        if m.to_location:
            balance[(m.product_id, m.to_location)] = balance.get((m.product_id, m.to_location), 0) + m.qty
        if m.from_location:
            balance[(m.product_id, m.from_location)] = balance.get((m.product_id, m.from_location), 0) - m.qty

    # also calculate total per product
    totals = {}
    for (product, location), qty in balance.items():
        totals[product] = totals.get(product, 0) + qty

    return render_template("report.html", report=balance, totals=totals)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
