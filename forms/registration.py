from flask_wtf import FlaskForm
from wtforms.widgets import NumberInput

from wtforms import (
    StringField,
    SelectField,
    MultipleFileField,
    DateField,
    IntegerField,
)

from wtforms.validators import InputRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import datetime

class NumberForm(FlaskForm):

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    otp = IntegerField("OTP", widget=NumberInput(min=0, max=9999))


class PaymentsForm(FlaskForm):

    payment_mode = SelectField(
        "Payment Mode",
        choices=["PayTM", "EDC", "Credit Card", "Debit Card", "Wallet/UPI", "Cheque"],
        validators=[InputRequired()],
    )

    tpr = IntegerField("Total Payment Received")
    npa = IntegerField("Net Payable Amount")


class BookingForm(FlaskForm):

    first_name = StringField("First Name", validators=[InputRequired()])

    last_name = StringField("Last Name", validators=[InputRequired()])

    email = StringField("Email", validators=[Email(), InputRequired()])

    mobile = IntegerField("Mobile", validators=[InputRequired()])

    docs = MultipleFileField("Guest Docs")

    hotel = SelectField(
        "Hotel", choices=["VIZIMA PALACE", "VIZIMA CROSSROADS", "HOTEL VIZIMA 62"]
    )

    guests = IntegerField("Guests")

    room = StringField("Room No.", validators=[InputRequired()])

    tariff = IntegerField("Tariff")

    checkin = DateField("Check-in Date", validators=[InputRequired()])
    checkout = DateField("Check-in Date", validators=[InputRequired()])

    source = SelectField(
        "Booking Source",
        choices=[
            "Walk-In",
            "OYO",
            "TREEBO",
            "FABHOTELS",
            "BreviStay",
            "Go-Ibibo",
            "MakeMyTrip",
            "Mi-Stay",
            "Booking.com",
            "Expedia",
            "Agoda",
            "Airbnb",
            "PAYTM",
            "BAG2BAG",
            "OTA",
            "Others",
        ],
    )
    operator = SelectField(
        "Operator",
        choices=["VINAY", "SAGAR", "NEERAJ", "VIKASH", "LADOO", "AMIT", "KALUA", "ALI"],
    )
