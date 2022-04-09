"""
Flask App
"""
import os
from time import time
from random import randint
from dotenv import load_dotenv
from flask_wtf import CSRFProtect

# Flask
from flask import (
    Flask,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
    jsonify,
)
from flask.logging import create_logger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4

# Load Environment Variables
load_dotenv()

# Config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "Lux"
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
# Loggger
log = create_logger(app)

# Bootstrap
Bootstrap4(app)

# DB
db = SQLAlchemy(app)

csrf = CSRFProtect(app)

from models import (
    InvoiceHeaders,
    PaymentModes,
    db,
    Hotels,
    Config,
    ChargeTypes,
    InvoiceLines,
)

migrate = Migrate(app, db, compare_type=True)

# Custom
from util import get_totals, calc_gst
from forms import InvoiceForm, PrintInvoiceForm


def clear_session():
    """
    clear session variables
    """
    session.pop("booking_id", None)
    session.pop("_flashes", None)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html", error=e), 404


def gen_invoice(invoice_id):

    invoice_dict = {}

    config = db.session.query(Config).filter(Config.id == 1).first().__dict__

    headers = (
        db.session.query(InvoiceHeaders)
        .filter(InvoiceHeaders.id == invoice_id)
        .first()
        .__dict__
    )

    hotel = db.session.query(Hotels).filter(Hotels.id == headers["hotel_id"]).first()

    payment_mode = (
        db.session.query(PaymentModes)
        .filter(PaymentModes.id == headers["payment_mode_id"])
        .first()
    )

    headers["hotel"] = hotel.name
    headers["hotel_address"] = hotel.address
    headers["payment_mode"] = payment_mode.name

    invoice_dict.update(config)
    invoice_dict.update(headers)

    lines = []
    count = 1

    for line in (
        db.session.query(InvoiceLines)
        .filter(InvoiceLines.invoice_id == headers["id"])
        .all()
    ):

        data_line = line.__dict__
        data_line["no"] = count

        charge = (
            db.session.query(ChargeTypes)
            .filter(ChargeTypes.id == data_line["charge_id"])
            .first()
        )
        data_line["particulars"] = charge.name

        lines.append(data_line)
        count += 1

    log.debug(lines)
    invoice_dict["lines"] = lines

    totals = get_totals(lines)
    invoice_dict.update(totals)

    return render_template("invoice.html", **invoice_dict)


# Routes
@app.route("/", methods=["GET", "POST"])
def homepage():
    """
    homepage route
    """
    return render_template("homepage.html")


@app.route("/invoice", methods=["GET", "POST"])
def invoice():
    form = PrintInvoiceForm()

    page = request.args.get("page", 1, type=int)

    result = db.session.execute(
        '''SELECT ih.id AS "id", ih.invoice_num AS "Invoice Num", ih.invoice_date AS "Invoice Date" from public.invoice_headers ih order by 1 desc LIMIT 20'''
    ).fetchall()

    # pagination = InvoiceHeaders.query.order_by(InvoiceHeaders.id.desc()).paginate(
    #     page, per_page=20
    # )
    # invoices = pagination.items


    invoices = []
    for row in result:
        row_dict = {}
        row_dict["id"] = row[0]
        row_dict["invoice_num"] = row[1]
        row_dict["invoice_date"] = row[2]
        invoices.append(row_dict)

    titles = [
        ("id", "#"),
        ("invoice_num", "Invoice Num"),
        ("invoice_date", "Invoice Date"),
    ]

    log.debug(invoices)

   
    return render_template(
        "invoice_print.html",
        form=form,
        titles=titles,
        invoices=invoices,
        InvoiceHeaders=InvoiceHeaders,
    )


@app.route("/invoice_form", methods=["GET", "POST"])
def invoice_form():
    form = InvoiceForm()
    log.debug(request.form)
    log.debug(form.errors)

    if request.method == "POST":
        log.debug("POST")
        if request.form["button"] == "Add Row":
            form.lines._add_entry()
        elif request.form["button"] == "Delete Row":
            form.lines.pop_entry()

        elif form.validate_on_submit():
            log.debug("validation complete")
            hotel = form.hotel.data
            invoice_num = form.invoice_num.data
            invoice_date = form.invoice_date.data
            booking_id = form.booking_id.data
            booking_date = form.booking_date.data
            payee = form.payee.data
            guest = form.guest.data
            guest_details = form.guest_details.data
            arrive = form.arrive.data
            depart = form.depart.data
            nights = form.nights.data
            rooms = form.rooms.data
            hotel_id = request.form["hotel"]
            payment_mode_id = request.form["payment_mode"]
            tpr = form.tpr.data
            npa = form.npa.data

            headers = InvoiceHeaders(
                invoice_num,
                invoice_date,
                booking_id,
                booking_date,
                payee,
                guest,
                guest_details,
                arrive,
                depart,
                nights,
                rooms,
                hotel_id,
                payment_mode_id,
                tpr,
                npa,
            )

            db.session.add(headers)
            db.session.flush()
            count = 0
            for line in form.lines:

                charge_id = request.form["lines-" + str(count) + "-particulars"]
                hsnsac = line.hsnsac.data
                stay_date = line.stay_date.data
                sell_rate = line.sell_rate.data
                inclusion = line.inclusion.data
                subtotal = line.subtotal.data
                cgst = line.cgst.data
                sgst = line.sgst.data
                total = line.total.data

                invoice_line = InvoiceLines(
                    headers.id,
                    charge_id,
                    hsnsac,
                    stay_date,
                    sell_rate,
                    inclusion,
                    subtotal,
                    cgst,
                    sgst,
                    total,
                )
                db.session.add(invoice_line)
                db.session.flush()
                count += 1
            db.session.commit()
            clear_session()
            flash("Data added Succesfully!", "success")
            return redirect(url_for("homepage"))

    else:
        form.lines._add_entry()

    log.debug(form.errors)

    return render_template("invoice_form.html", form=form)


@app.route("/get_hsn")
def get_hsn():
    charge = request.args.get("charge", "01")
    res = db.session.query(ChargeTypes).filter(ChargeTypes.id == charge).first()
    return jsonify(res.hsnsac)


@app.route("/get_gst")
def get_gst():
    price = request.args.get("price", "01")
    return jsonify(calc_gst(float(price)))


@app.route("/printinvoice", methods=["POST"])
def printinvoice():
    """
    generate invoice data and pass to invoice.html
    """
    invoice_num = request.form["invoice_num"]

    headers = (
        db.session.query(InvoiceHeaders)
        .filter(InvoiceHeaders.invoice_num == invoice_num)
        .first_or_404(
            description="There is no invoice with number: {}".format(invoice_num)
        )
        .__dict__
    )

    return gen_invoice(headers["id"])


@app.route("/messages/<int:invoice_id>/delete", methods=["POST"])
def delete_invoice(invoice_id):
    db.session.query(InvoiceLines).filter(
        InvoiceLines.invoice_id == invoice_id
    ).delete()
    db.session.query(InvoiceHeaders).filter(InvoiceHeaders.id == invoice_id).delete()
    db.session.commit()
    flash("Invoice Deleted Succesfully!", "success")
    return redirect(url_for("homepage"))


@app.route("/messages/<invoice_id>/print", methods=["GET", "POST"])
def print_invoice(invoice_id):
    return gen_invoice(invoice_id)

if __name__ == "__main__":
    app.run(debug=True)
