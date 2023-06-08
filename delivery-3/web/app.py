#!/usr/bin/python3
from logging.config import dictConfig

import psycopg
import json
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


@app.route("/products", methods=("GET",))
@app.route("/products/<page>", methods=("GET",))
def products_index(page=0):
    """Show all the products, ordered by name."""

    page = int(page)

    if page < 0:
        return redirect(url_for("products_index"))

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            query = """
                SELECT *
                FROM product
                ORDER BY name ASC
                OFFSET %(page)s
                LIMIT 10;
            """

            products = cur.execute(
                query,
                {"page": page * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            if cur.rowcount == 0:
                return redirect(url_for("products_index"))

            cur.execute(
                query,
                {"page": (page + 1) * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            last = True if cur.rowcount == 0 else False

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(products)

    return render_template(
        "products/index.html", products=products, page=page, last=last
    )


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
        elif not price.isnumeric():
            error += "Price is required to be numeric. "

        if not ean:
            ean = None
        elif not ean.isnumeric():
            error += "EAN is required to be numeric. "

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
                        {
                            "sku": sku,
                            "name": name,
                            "description": description,
                            "price": price,
                            "ean": ean,
                        },
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
        elif not price.isnumeric():
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


@app.route("/suppliers", methods=("GET",))
@app.route("/suppliers/<page>", methods=("GET",))
def suppliers_index(page=0):
    """Show all the suppliers, ordered by TIN."""

    page = int(page)

    if page < 0:
        return redirect(url_for("suppliers_index"))

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            query = """
                SELECT *
                FROM supplier
                ORDER BY TIN ASC
                OFFSET %(page)s
                LIMIT 10;
            """

            suppliers = cur.execute(
                query,
                {"page": page * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            if cur.rowcount == 0:
                return redirect(url_for("suppliers_index"))

            cur.execute(
                query,
                {"page": (page + 1) * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            last = True if cur.rowcount == 0 else False

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(suppliers)

    return render_template(
        "suppliers/index.html", suppliers=suppliers, page=page, last=last
    )


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
                        {
                            "tin": tin,
                            "name": name,
                            "sku": sku,
                            "address": address,
                            "date": date,
                        },
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


@app.route("/", methods=("GET",))
@app.route("/customers", methods=("GET",))
@app.route("/customers/<page>", methods=("GET",))
def customers_index(page=0):
    """Show all the customers, ordered by name."""

    page = int(page)

    if page < 0:
        return redirect(url_for("customers_index"))

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            query = """
                SELECT *
                FROM customer
                ORDER BY name ASC
                OFFSET %(page)s
                LIMIT 10;
            """

            customers = cur.execute(
                query,
                {"page": page * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            if cur.rowcount == 0:
                return redirect(url_for("customers_index"))

            cur.execute(
                query,
                {"page": (page + 1) * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            last = True if cur.rowcount == 0 else False

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(customers)

    return render_template(
        "customers/index.html", customers=customers, page=page, last=last
    )


@app.route("/customers/create", methods=("GET", "POST"))
def customer_create():
    """Create a customer."""

    if request.method == "POST":
        cust_no = request.form["cust_no"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        error = ""

        if not cust_no:
            error += "Customer number is required. "
        elif not cust_no.isnumeric():
            error += "Customer number is required to be numeric. "

        if not name:
            error += "Name is required. "

        if not email:
            error += "Email is required. "

        if not phone:
            phone = None

        if not address:
            address = None

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO customer(cust_no, name, email, phone, address)
                        VALUES
                            (
                            %(cust_no)s,
                            %(name)s,
                            %(email)s,
                            %(phone)s,
                            %(address)s
                            );
                        """,
                        {
                            "cust_no": cust_no,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "address": address,
                        },
                    )
                conn.commit()
            return redirect(url_for("customers_index"))

    return render_template("customers/create.html")


@app.route("/customers/<cust_no>/delete", methods=("POST",))
def customer_delete(cust_no):
    """Delete the customer."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                DELETE FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
        conn.commit()
    return redirect(url_for("customers_index"))


@app.route("/orders", methods=("GET",))
@app.route("/orders/<page>", methods=("GET",))
def orders_index(page=0):
    """Show all the orders, most recent first."""

    page = int(page)

    if page < 0:
        return redirect(url_for("orders_index"))

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            query = """
                    SELECT
                        o.order_no,
                        o.cust_no,
                        o.date,
                        p.cust_no AS paid_by
                    FROM orders o
                    LEFT JOIN pay p USING (order_no)
                    ORDER BY date DESC
                    OFFSET %(page)s
                    LIMIT 10;
            """

            orders = cur.execute(
                query,
                {"page": page * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            if cur.rowcount == 0:
                return redirect(url_for("orders_index"))

            cur.execute(
                query,
                {"page": (page + 1) * 10},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

            last = True if cur.rowcount == 0 else False

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(orders)

    return render_template(
        "orders/index.html",
        orders=orders,
        page=page,
        last=last,
    )


@app.route("/orders/view/<order_no>", methods=("GET",))
def order_view(order_no):
    """Show the order."""

    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            order = cur.execute(
                """
                SELECT
                    o.order_no,
                    o.cust_no,
                    o.date,
                    p.cust_no AS paid_by
                FROM orders o
                LEFT JOIN pay p USING (order_no)
                WHERE o.order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchone()

            products = cur.execute(
                """
                SELECT *
                FROM contains
                WHERE order_no = %(order_no)s;
                """,
                {"order_no": order_no},
            ).fetchall()

            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify({"order": order, "products": products})

    return render_template("orders/view.html", order=order, products=products)


@app.route(
    "/orders/<order_no>/pay",
    methods=(
        "GET",
        "POST",
    ),
)
def order_pay(order_no):
    """Pay the order."""

    if request.method == "POST":
        paid_by = request.form["paid_by"]

        error = ""

        if not paid_by:
            error += "Order number is required. "
        elif not paid_by.isnumeric():
            error += "Order number is required to be numeric. "

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO pay(order_no, cust_no)
                        VALUES
                            (
                            %(order_no)s,
                            %(paid_by)s
                            );
                        """,
                        {"order_no": order_no, "paid_by": paid_by},
                    )

                    log.debug(f"Found {cur.rowcount} rows.")

                conn.commit()

            return redirect(url_for("order_view", order_no=order_no))

    return render_template("orders/pay.html", order_no=order_no)


@app.route("/orders/create", methods=("GET", "POST"))
def order_create():
    """Create a order."""

    if request.method == "POST":
        order_no = request.form["order_no"]
        cust_no = request.form["cust_no"]
        date = request.form["date"]
        products = json.loads(request.form["products"])

        error = ""

        if not order_no:
            error += "Order number is required. "
        elif not order_no.isnumeric():
            error += "Order number is required to be numeric. "

        if not cust_no:
            error += "Customer number is required. "
        elif not cust_no.isnumeric():
            error += "Customer number is required to be numeric. "

        if not date:
            error += "Date is required. "

        if not products or len(products) == 0:
            error += "Products are required. "
        else:
            for product in products:
                if not product["sku"] or not product["qty"]:
                    error += "Products are required. "
                    break

        if error != "":
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO orders(order_no, cust_no, date)
                        VALUES
                            (
                            %(order_no)s,
                            %(cust_no)s,
                            %(date)s
                            );
                        """,
                        {"order_no": order_no, "cust_no": cust_no, "date": date},
                    )

                    for product in products:
                        cur.execute(
                            """
                            INSERT INTO contains(order_no, SKU, qty)
                            VALUES
                                (
                                %(order_no)s,
                                %(SKU)s,
                                %(qty)s
                                );
                            """,
                            {
                                "order_no": order_no,
                                "SKU": product["sku"],
                                "qty": product["qty"],
                            },
                        )

                conn.commit()
            return redirect(url_for("orders_index"))

    return render_template("orders/create.html")


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
