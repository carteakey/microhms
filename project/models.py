from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship,validates
from flask_login import UserMixin

db = SQLAlchemy()

class Config(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String())
    address = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())
    hsnsac = db.Column(db.String())
    pan = db.Column(db.String())
    gstin = db.Column(db.String())
    acs = db.Column(db.String())

class ChargeTypes(db.Model):
    __tablename__ = "charges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    hsnsac = db.Column(db.String())

class PaymentModes(db.Model):
    __tablename__ = "payment_modes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

class Hotels(db.Model):
    __tablename__ = "hotels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())

class InvoiceHeaders(db.Model):
    __tablename__ = "invoice_headers"
    id = db.Column(db.Integer, primary_key=True)
    invoice_num = db.Column(db.String())
    invoice_date = db.Column(db.Date())
    booking_id = db.Column(db.String())
    booking_date = db.Column(db.Date())
    payee = db.Column(db.String())
    guest = db.Column(db.String())
    guest_details = db.Column(db.String())
    gstin = db.Column(db.String())
    arrive = db.Column(db.Date()) 
    depart = db.Column(db.Date())
    nights = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    category = db.Column(db.String())
    hotel_id = db.Column(db.Integer,db.ForeignKey("hotels.id"))
    payment_mode_id = db.Column(db.Integer,db.ForeignKey("payment_modes.id"))
    tpr = db.Column(db.Numeric(10,2))
    npa = db.Column(db.Numeric(10,2))

    hotel = relationship("Hotels", backref="hotels")
    payment = relationship("PaymentModes", backref="payment_modes")
    db = SQLAlchemy()

    @validates('invoice_num', 'booking_id')
    def convert_upper(self, key, value):
        return value.upper()

    def __init__(
        self, 
        invoice_num ,
        invoice_date ,
        booking_id ,
        booking_date, 
        payee ,
        guest,
        guest_details,
        gstin ,
        arrive,
        depart ,
        nights ,
        rooms ,
        category, 
        hotel_id ,
        payment_mode_id,  
        tpr ,
        npa  
    ):
        self.invoice_num = invoice_num
        self.invoice_date = invoice_date
        self.booking_id = booking_id
        self.booking_date = booking_date
        self.payee = payee
        self.guest= guest
        self.guest_details= guest_details
        self.gstin = gstin
        self.arrive= arrive
        self.depart = depart
        self.nights = nights
        self.rooms = rooms
        self.category = category
        self.hotel_id = hotel_id
        self.payment_mode_id  = payment_mode_id
        self.tpr  = tpr
        self.npa = npa

    def __repr__(self):
        return f"<id {self.id}>"

class InvoiceLines(db.Model):
    __tablename__ = "invoice_lines"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoice_headers.id"))
    charge_id = db.Column(db.Integer, db.ForeignKey("charges.id"))
    hsnsac = db.Column(db.String())
    stay_date = db.Column(db.Date())
    sell_rate = db.Column(db.Numeric(10,2))
    inclusion = db.Column(db.Numeric(10,2))
    subtotal = db.Column(db.Numeric(10,2))
    cgst = db.Column(db.Numeric(10,2))
    sgst = db.Column(db.Numeric(10,2))
    total = db.Column(db.Numeric(10,2))

    invoice = relationship("InvoiceHeaders", backref="invoice_headers")
    charge = relationship("ChargeTypes", backref="charges")

    def __init__(
        self, 
        invoice_id ,
        charge_id ,
        hsnsac ,
        stay_date, 
        sell_rate ,
        inclusion ,
        subtotal ,
        cgst,
        sgst,
        total 
    ):
        self.invoice_id = invoice_id
        self.charge_id = charge_id
        self.hsnsac = hsnsac
        self.stay_date = stay_date
        self.sell_rate = sell_rate
        self.inclusion= inclusion
        self.subtotal = subtotal
        self.cgst= cgst
        self.sgst = sgst
        self.total = total

    def __repr__(self):
        return f"<id {self.id}>"


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
