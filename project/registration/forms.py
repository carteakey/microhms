from flask_wtf import FlaskForm
from sqlalchemy import extract
from wtforms.widgets import NumberInput

from wtforms import (
    StringField,
    DateField,
    SelectField,
    IntegerField,
    MultipleFileField,
    TimeField,
)

from wtforms.validators import InputRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField

from project.models import BookingSources, Bookings, Hotels, PaymentModes

from project.models import db


class NumberForm(FlaskForm):

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    otp = IntegerField("OTP", widget=NumberInput(min=0, max=9999))


class GuestForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])

    last_name = StringField("Last Name", validators=[InputRequired()])

    email = StringField("Email", validators=[Email(), InputRequired()])

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    docs = MultipleFileField("Guest ID", validators=[InputRequired()])


class BookingForm(FlaskForm):

    and_register_serial_no = IntegerField(
        "A&D Register Serial #", validators=[InputRequired()]
    )

    hotel = QuerySelectField(
        "Hotel", query_factory=lambda: Hotels.query, get_label="name"
    )

    guests = IntegerField("Guests")

    room = StringField("Room No.", validators=[InputRequired()])

    tariff = IntegerField("Tariff (incl. GST)", validators=[InputRequired()])
    gst = IntegerField("GST", validators=[InputRequired()])
    tariff_wo_gst = IntegerField("Tariff (excl. GST)", validators=[InputRequired()])

    checkin = DateField("Check-in Date", validators=[InputRequired()])
    checkin_time = TimeField("Check-in Time", validators=[InputRequired()])
    checkout = DateField("Check-out Date", validators=[InputRequired()])

    booking_source = QuerySelectField(
        "Booking Source", query_factory=lambda: BookingSources.query, get_label="name"
    )

    payment_mode = QuerySelectField(
        query_factory=lambda: PaymentModes.query, get_label="name"
    )
    tpr = IntegerField("Total Payment Received", validators=[InputRequired()])
    npa = IntegerField("Net Payable Amount", validators=[InputRequired()])


class BookingsToday(FlaskForm):
    pass


def get_booking_months():
    try: 
        rows = db.session.execute(
            "SELECT DISTINCT TO_CHAR(checkout, 'MON-YY') AS month FROM bookings ORDER BY TO_CHAR(checkout, 'MON-YY')"
        )
    except:
        return []
    
    return [row.month for row in rows]


class BookingsMonthly(FlaskForm):
    month = SelectField(
        "Month",
        choices=get_booking_months(),
    )
