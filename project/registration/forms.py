from flask_wtf import FlaskForm
from wtforms.widgets import NumberInput

from wtforms import (
    StringField,
    DateField,
    IntegerField,
    MultipleFileField,
    TimeField
)

from wtforms.validators import InputRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField

from project.models import BookingSources, Hotels


class NumberForm(FlaskForm):

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    otp = IntegerField("OTP", widget=NumberInput(min=0, max=9999))


class BookingForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])

    last_name = StringField("Last Name", validators=[InputRequired()])

    email = StringField("Email", validators=[Email(), InputRequired()])

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    docs = MultipleFileField("Guest ID", validators=[InputRequired()])

    and_register_serial_no = IntegerField("AND Register Serial #", validators=[InputRequired()])

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
