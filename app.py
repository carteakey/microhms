import os
import io
from dotenv import load_dotenv
from flask_wtf import CSRFProtect

# Flask
from flask import (
    Flask,
    render_template,
    request,
    flash,
    send_file,
    redirect,
    url_for,
    jsonify,
)

from weasyprint import HTML

from flask.logging import create_logger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5

# Load Environment Variables
load_dotenv()

# Config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024
app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "Zephyr"
app.config["BOOTSTRAP_SERVE_LOCAL"] = True
# Loggger
log = create_logger(app)

# Bootstrap
Bootstrap5(app)

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
from forms.billing import InvoiceForm, PrintInvoiceForm

this_folder = os.path.dirname(os.path.abspath(__file__))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html", error=e), 404

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
        "Select * from invoices_v order by 1 desc LIMIT 20"
    ).fetchall()

    pagination = InvoiceHeaders.query.order_by(InvoiceHeaders.id.desc()).paginate(
        page, per_page=20
    )

    invoices = []
    for row in result:
        row_dict = {}
        row_dict["id"] = row[0]
        row_dict["invoice_num"] = row[1]
        row_dict["invoice_date"] = row[2]
        row_dict["booking_id"] = row[3]
        row_dict["booking_date"] = row[4]
        row_dict["hotel"] = row[5]
        row_dict["payee"] = row[6]
        row_dict["guest"] = row[7]
        row_dict["guest_details"] = row[8]
        row_dict["total"] = row[9]
        invoices.append(row_dict)

    titles = [
        ("id", "#"),
        ("invoice_num", "Invoice Num"),
        ("invoice_date", "Invoice Date"),
        ("booking_id", "Booking ID"),
        ("booking_date", "Booking Date"),
        ("hotel", "Hotel"),
        ("payee", "Payee"),
        ("guest", "Guest"),
        ("guest_details", "Guest Details"),
        ("total", "Total"),
    ]

    log.debug(invoices)

    # invoices = pagination.items

    return render_template(
        "billing/invoice_print.html",
        form=form,
        titles=titles,
        invoices=invoices,
        InvoiceHeaders=InvoiceHeaders,
    )


@app.route("/invoice_form/", defaults={"invoice_id": None}, methods=["GET", "POST"])
@app.route("/invoice_form/<int:invoice_id>", methods=["GET", "POST"])
def invoice_form(invoice_id):
    form = InvoiceForm()
    log.debug(request.form)
    log.debug(form.errors)

    if request.method == "GET":
        if invoice_id is not None:
            header = (
                db.session.query(InvoiceHeaders)
                .filter(InvoiceHeaders.id == invoice_id)
                .first_or_404()
            )
            form.invoice_num.data = header.invoice_num
            form.invoice_date.data = header.invoice_date
            form.booking_id.data = header.booking_id
            form.booking_date.data = header.booking_date
            form.payee.data = header.payee
            form.guest.data = header.guest
            form.guest_details.data = header.guest_details
            form.gstin.data = header.gstin
            form.arrive.data = header.arrive
            form.depart.data = header.depart
            form.nights.data = header.nights
            form.rooms.data = header.rooms
            form.category.data = header.category
            form.hotel.data = header.hotel_id
            form.tpr.data = header.tpr
            form.npa.data = header.npa

            lines = (
                db.session.query(InvoiceLines)
                .filter(InvoiceLines.invoice_id == invoice_id)
            )

    if request.method == "POST":
        log.debug("POST")
        if request.form["button"] == "Add Line":
            form.lines._add_entry()
        elif request.form["button"] == "Delete Line":
            form.lines.pop_entry()

        elif form.validate_on_submit():
            log.debug(form.lines)
            log.debug("validation complete")
            invoice_num = form.invoice_num.data
            invoice_date = form.invoice_date.data
            booking_id = form.booking_id.data
            booking_date = form.booking_date.data
            payee = form.payee.data
            guest = form.guest.data
            guest_details = form.guest_details.data
            gstin = form.gstin.data
            arrive = form.arrive.data
            depart = form.depart.data
            nights = form.nights.data
            rooms = form.rooms.data
            category = form.category.data
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
                gstin,
                arrive,
                depart,
                nights,
                rooms,
                category,
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
            flash("Entry added.", "success")
            return redirect(url_for("homepage"))

    else:
        form.lines._add_entry()

    log.debug(form.errors)

    return render_template("billing/invoice_form.html", form=form)


@app.route("/get_hsn/<int:charge_id>")
def get_hsn(charge_id=0):
    res = db.session.query(ChargeTypes).filter(ChargeTypes.id == charge_id).first()

    if res is not None:
        return jsonify(float(res.hsnsac))
    else:
        return jsonify(-1)


@app.route("/get_gst/<float:price>")
def get_gst(price=0):
    return jsonify(calc_gst(price))


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

    return save_invoice(headers["id"])


@app.route("/messages/<int:invoice_id>/delete", methods=["POST"])
def delete_invoice(invoice_id):
    db.session.query(InvoiceLines).filter(
        InvoiceLines.invoice_id == invoice_id
    ).delete()
    db.session.query(InvoiceHeaders).filter(InvoiceHeaders.id == invoice_id).delete()
    db.session.commit()
    flash("Invoice Deleted Succesfully!", "success")
    return redirect(url_for("homepage"))


@app.route("/messages/<invoice_id>/save", methods=["GET", "POST"])
def save_invoice(invoice_id):

    invoice_dict = gen_invoice(invoice_id)

    file = "Invoice " + invoice_dict["invoice_num"].replace("/", "-") + ".pdf"

    html_out = render_template("billing/invoice.html", **invoice_dict)

    HTML(string=html_out).write_pdf(file, stylesheets=["./static/css/styles.css"])

    return_data = io.BytesIO()
    with open(file, "rb") as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    os.remove(file)

    return send_file(return_data, mimetype="application/pdf", attachment_filename=file)


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

    headers["image_path"] = "file://" + os.path.join(this_folder, "static", "logo.png")
    headers["sign"] = "file://" + os.path.join(this_folder, "static", "stamp_g.jpg")

    headers["hotel"] = hotel.name
    headers["hotel_address"] = hotel.address
    headers["payment_mode"] = payment_mode.name
    headers["guest_gstin"] = headers["gstin"]
    headers.pop("gstin")

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

    return invoice_dict


if __name__ == "__main__":
    app.run(debug=True)
