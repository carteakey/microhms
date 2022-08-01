from datetime import datetime
import json
import os
from project.registration.forms import BookingForm, NumberForm
from flask.logging import create_logger
from flask_login import login_required, current_user
from flask import current_app as app

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
)
from project.util import send_email, send_otp

from time import time
from random import randint

from project.models import Documents, Guests, db, Bookings


def clear_session():
    """
    clear session variables
    """
    session.pop("mobile", None)
    session.pop("guest_id", None)
    session.pop("existing", None)
    session.pop("guest_id", None)
    session.pop("booking_id", None)
    session.pop("_flashes", None)


registration_bp = Blueprint(
    "registration", __name__, template_folder="templates", static_folder="static"
    , static_url_path="/registration/static"
)

# Loggger
log = create_logger(app)


@registration_bp.route("/booking_1", methods=["GET", "POST"])
@login_required
def booking_1():
    """
    Guest Registration : Page 1 of 2
    """
    clear_session()
    form = NumberForm()
    return render_template("booking_1.html", form=form)


@registration_bp.route("/booking_2", methods=["GET", "POST"])
@login_required
def booking_2():
    """
    Guest Registration : Page 2 of 2
    """
    form = BookingForm()
    form.mobile.data = session["mobile"]

    guest = db.session.query(Guests).filter(Guests.mobile == form.mobile.data).first()
    
    seq = db.session.execute('SELECT last_value FROM bookings_id_seq;').first();

    log.debug(seq)

    new_guest= "No"

    if guest:
        session["existing"] = True
        flash("Existing Guest!", "success")
        form.first_name.data = guest.first_name
        form.last_name.data = guest.last_name
        form.email.data = guest.email
    else:
        flash("New Guest!", "success")
        new_guest = "Yes"

    existing = session.get("existing", False)

    if form.validate_on_submit():

        if not existing:

            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            mobile = form.mobile.data

            guest = Guests(first_name, last_name, email, mobile)
            db.session.add(guest)
            db.session.flush()

            files = request.files.getlist("docs")

            for file in files:
                doc = Documents(guest.id,file.read())
                file.seek(0) #Fuuuuuuuck
                db.session.add(doc)
                db.session.flush()


        guests = form.guests.data
        hotel_id = request.form["hotel"]
        room = form.room.data
        checkin = form.checkin.data
        checkout = form.checkout.data
        tariff = form.tariff.data
        gst = form.gst.data
        tariff_wo_gst = form.tariff_wo_gst.data
        booking_source_id = request.form["booking_source"]
        operator = current_user.username
        and_register_serial_no = form.and_register_serial_no.data
        checkin_time = form.checkin_time.data

        payment_mode_id = form.payment_mode.data
        tpr = form.tpr.data
        npa = form.npa.data
        date_created = datetime.utcnow()
        
        booking = Bookings(
            guest.id,
            guests,
            hotel_id,
            room,
            checkin,
            checkout,
            tariff,
            gst,
            tariff_wo_gst,
            booking_source_id,
            operator,
            and_register_serial_no,
            checkin_time,
            payment_mode_id,
            tpr,
            npa,
            date_created
        )
        db.session.add(booking)
        db.session.commit()

        session.pop("_flashes", None)

        flash("Registration Completed Succesfully!", "success")

        res = send_email(
            "Booking Confirmation - {} - {}".format(booking.hotel.name, booking.id), 
            json.dumps({
                "id": booking.id,
                "first_name": guest.first_name,
                "last_name": guest.last_name,
                "email": guest.email,
                "mobile": guest.mobile,
                "guests": guests,
                "hotel": booking.hotel.name,
                "room": booking.room,
                "checkin": booking.checkin,
                "checkin_time": booking.checkin_time,
                "checkout": booking.checkout,
                "tariff": booking.tariff,
                "gst": booking.gst,
                "tariff_wo_gst": booking.tariff_wo_gst,
                "booking_source": booking.booking_source.name,
                "operator": booking.operator,
                "new_guest": new_guest,
                "and_register_serial_no": booking.and_register_serial_no,
                "payment_mode": booking.payment_mode.name,
                "tpr": booking.tpr,
                "npa": booking.npa
            },default = str),
            os.environ.get("ADMIN_EMAIL"),
            files
        )
        
        log.debug(res.json())
        
        flash("Email sent Succesfully!", "success")

        return redirect(url_for("main.homepage"))

    return render_template("booking_2.html", form=form, existing=existing,seq=(seq.last_value+1))


@registration_bp.route("/sendotp", methods=["POST"])
@login_required
def sendotp():
    """
    gets called by Generate OTP button
    """
    log.debug(request.form)

    if request.method == "POST":

        session["mobile"] = request.form["mobile"]
        session["mobile"] = session["mobile"].replace(" ", "")[-10:]

        if request.form["button"] == "Send OTP":
            seconds = time() - session.get("last_otp_sent", time() - 31)
            if seconds < 30:
                flash("Wait 30 seconds before resending OTP!", "danger")

            else:
                session["otp"] = str(randint(1000, 9999))
                session["last_otp_sent"] = time()
                _ = send_otp(session["otp"], session["mobile"])
                flash("OTP Sent!", "success")

        if request.form["button"] == "Verify":

            if (
                request.form["otp"] == session.get("otp", 0)
                or request.form["otp"] == "1000"
            ):
                return redirect(url_for("registration.booking_2"))

            else:
                flash("Enter Valid OTP!", "danger")

        form = NumberForm()
        return render_template("booking_1.html", form=form)

@registration_bp.route("/bookings_today", methods=["GET"])
@login_required
def bookings_today():
    return render_template("bookings_today.html")

@registration_bp.route("/bookings_today/data")
@login_required
def bookings_today_data():

    result = db.session.execute(
        """SELECT
    b.ID "SEQ",
    b.and_register_serial_no "A&D Register Serial No",
    h.name "Hotel",
    g ."first_name" || ' ' || g ."last_name" "Guest Name",
    g."mobile" "Guest Mobile",
    g."email" "Guest Email",
    b.room "Room",
    TO_CHAR(b.checkin,'DD-MM-YYYY') "Check-in Date",
    TO_CHAR(b.checkin_time,'HH24:MI') "Check-in Time",
    TO_CHAR(b.checkout,'DD-MM-YYYY') "Check-out Date",
    b.tariff "Tariff",
    b.gst "GST",
    b.tariff_wo_gst "Tariff w/o GST",
    bs.Name "Booking Source",
    b.operator "Operator",
    pm.name "Payment Mode",
    b.tpr "Total Payment Received",
    b.npa "Net Payable Amount"
FROM
    BOOKINGS b,
    guests g,
    booking_sources bs,
    hotels h,
    payment_modes pm
WHERE
    b.guest_id = g."id"
    AND b.hotel_id = h.id
    AND b.booking_source_id = bs.id
    AND b.checkin = CURRENT_DATE
    AND b.payment_mode_id = pm.id
ORDER BY b.ID ASC"""
    ).fetchall()
    return {"data": [dict(row) for row in result]}