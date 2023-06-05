#!/usr/bin/python3
from logging.config import dictConfig

import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool


# postgres://{user}:{password}@{hostname}:{port}/{database-name}
DATABASE_URL = "postgres://db:db@postgres/db"

pool = ConnectionPool(conninfo=DATABASE_URL)
# the pool starts connecting immediately.

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
log = app.logger


@app.route("/", methods=("GET",))
@app.route("/products", methods=("GET",))
def products_index():
    """Show all the products, ordered by name."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            products = cur.execute(
                """
                SELECT *
                FROM product
                ORDER BY name ASC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(products)

    return render_template("products/index.html", products=products)


@app.route("/products/create", methods=("GET", "POST"))
def product_create():
    """Create a product."""

    if request.method == "POST":
        sku = request.form["sku"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        ean = request.form["ean"]

        error = ""

        if not sku:
            error += "SKU is required. "

        if not name:
            error += "Name is required. "

        if not price:
            error += "Price is required. "
            if not price.isnumeric():
                error += "Price is required to be numeric. "
        
        if not ean:
            ean = None

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO product(SKU, name, description, price, ean)
                        VALUES
                            (
                            %(sku)s,
                            %(name)s,
                            %(description)s,
                            %(price)s,
                            %(ean)s
                            );
                        """,
                        {"sku": sku, "name": name, "description": description, "price": price, "ean": ean},
                    )
                conn.commit()
            return redirect(url_for("products_index"))

    return render_template("products/create.html")

    
@app.route("/products/<sku>/update", methods=("GET", "POST"))
def product_update(sku):
    """Update the product price and description."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                SELECT *
                FROM product
                WHERE SKU = %(sku)s;
                """,
                {"sku": sku},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

    if request.method == "POST":
        price = request.form["price"]
        description = request.form["description"]

        error = ""

        if not price:
            error += "Price is required. "
            if not price.isnumeric():
                error += "Price is required to be numeric. "

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        UPDATE product
                        SET
                            price = %(price)s,
                            description = %(description)s
                        WHERE SKU = %(sku)s;
                        """,
                        {"sku": sku, "price": price, "description": description},
                    )
                conn.commit()
            return redirect(url_for("products_index"))

    return render_template("products/update.html", product=product)


@app.route("/products/<sku>/delete", methods=("POST",))
def product_delete(sku):
    """Delete the product."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %(sku)s;
                """,
                {"sku": sku},
            )
        conn.commit()
    return redirect(url_for("products_index"))


@app.route("/", methods=("GET",))
@app.route("/suppliers", methods=("GET",))
def suppliers_index():
    """Show all the suppliers, ordered by TIN."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            suppliers = cur.execute(
                """
                SELECT *
                FROM supplier
                ORDER BY TIN ASC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(suppliers)

    return render_template("suppliers/index.html", suppliers=suppliers)


@app.route("/suppliers/create", methods=("GET", "POST"))
def supplier_create():
    """Create a supplier."""

    if request.method == "POST":
        tin = request.form["tin"]
        name = request.form["name"]
        address = request.form["address"]
        sku = request.form["sku"]
        date = request.form["date"]

        error = ""

        if not tin:
            error += "TIN is required. "
        
        if not name:
            name = None

        if not address:
            address = None

        if not sku:
            sku = None
        
        if not date:
            date = None

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO supplier(TIN, name, address, sku, date)
                        VALUES
                            (
                            %(tin)s,
                            %(name)s,
                            %(address)s,
                            %(sku)s,
                            %(date)s
                            );
                        """,
                        {"tin": tin, "name": name, "sku": sku, "address": address, "date": date},
                    )
                conn.commit()
            return redirect(url_for("suppliers_index"))

    return render_template("suppliers/create.html")


@app.route("/suppliers/<tin>/delete", methods=("POST",))
def supplier_delete(tin):
    """Delete the supplier."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                DELETE FROM supplier
                WHERE TIN = %(tin)s;
                """,
                {"tin": tin},
            )
        conn.commit()
    return redirect(url_for("suppliers_index"))


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
