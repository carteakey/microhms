from project.models import ChargeTypes, PaymentModes, Hotels
from flask_wtf import FlaskForm, Form
from wtforms.widgets import NumberInput


from wtforms import (
    StringField,
    SelectField,
    FieldList,
    FormField,
    DecimalField,
    DateField,
    IntegerField,
)

from wtforms.validators import InputRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from datetime import datetime

class InvoiceLines(Form):
    def __init__(self, *args, **kwargs):
        kwargs["csrf_enabled"] = False
        super(InvoiceLines, self).__init__(*args, **kwargs)

    particulars = QuerySelectField(
        query_factory=lambda: ChargeTypes.query, get_label="name"
    )
    hsnsac = StringField("HSN/SAC", validators=[InputRequired()])
    stay_date = DateField(
        "Stay Date", default=datetime.today, validators=[InputRequired()]
    )
    sell_rate = DecimalField("Sell Rate", places=2, validators=[InputRequired()])
    inclusion = DecimalField("Inclusion", places=2, validators=[InputRequired()])
    subtotal = DecimalField("Sub Total", places=2, validators=[InputRequired()])
    cgst = DecimalField("CGST", places=2, validators=[InputRequired()])
    sgst = DecimalField("SGST", places=2, validators=[InputRequired()])
    total = DecimalField("Total", places=2, validators=[InputRequired()])


class InvoiceForm(FlaskForm):
    invoice_num = StringField("Invoice#", validators=[InputRequired()])
    invoice_date = DateField(
        "Invoice Date", default=datetime.today, validators=[InputRequired()]
    )
    booking_id = StringField("Booking ID")
    booking_date = DateField(
        "Booking Date", default=datetime.today, validators=[InputRequired()]
    )
    payee = StringField("Payee", validators=[InputRequired()])
    guest = StringField("Guest Name", validators=[InputRequired()])
    guest_details = StringField("Guest Details")
    gstin = StringField("GSTIN")

    arrive = DateField(
        "Arrival Date", default=datetime.today, validators=[InputRequired()]
    )
    depart = DateField(
        "Departure Date", default=datetime.today, validators=[InputRequired()]
    )

    rooms = IntegerField("No of Rooms", widget=NumberInput(min=1, max=100))
    nights = IntegerField("Room Nights", widget=NumberInput(min=1, max=100))
    category = SelectField("Category", choices=["B2B", "B2C"])

    hotel = QuerySelectField(
        "Hotel", query_factory=lambda: Hotels.query, get_label="name"
    )

    payment_mode = QuerySelectField(
        query_factory=lambda: PaymentModes.query, get_label="name"
    )

    lines = FieldList(FormField(InvoiceLines))

    tpr = DecimalField("Total Payment Received", places=2, validators=[InputRequired()])
    npa = DecimalField("Net Payable Amount", places=2, validators=[InputRequired()])


class PrintInvoiceForm(FlaskForm):
    invoice_num = StringField("Invoice#", validators=[InputRequired()])
