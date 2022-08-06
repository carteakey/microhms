from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

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


class BookingSources(db.Model):
    __tablename__ = "booking_sources"
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
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"))
    payment_mode_id = db.Column(db.Integer, db.ForeignKey("payment_modes.id"))
    tpr = db.Column(db.Numeric(10, 2))
    npa = db.Column(db.Numeric(10, 2))

    db = SQLAlchemy()

    @validates("invoice_num", "booking_id")
    def convert_upper(self, key, value):
        return value.upper()

    def __init__(
        self,
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
    ):
        self.invoice_num = invoice_num
        self.invoice_date = invoice_date
        self.booking_id = booking_id
        self.booking_date = booking_date
        self.payee = payee
        self.guest = guest
        self.guest_details = guest_details
        self.gstin = gstin
        self.arrive = arrive
        self.depart = depart
        self.nights = nights
        self.rooms = rooms
        self.category = category
        self.hotel_id = hotel_id
        self.payment_mode_id = payment_mode_id
        self.tpr = tpr
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
    sell_rate = db.Column(db.Numeric(10, 2))
    inclusion = db.Column(db.Numeric(10, 2))
    subtotal = db.Column(db.Numeric(10, 2))
    cgst = db.Column(db.Numeric(10, 2))
    sgst = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

    def __init__(
        self,
        invoice_id,
        charge_id,
        hsnsac,
        stay_date,
        sell_rate,
        inclusion,
        subtotal,
        cgst,
        sgst,
        total,
    ):
        self.invoice_id = invoice_id
        self.charge_id = charge_id
        self.hsnsac = hsnsac
        self.stay_date = stay_date
        self.sell_rate = sell_rate
        self.inclusion = inclusion
        self.subtotal = subtotal
        self.cgst = cgst
        self.sgst = sgst
        self.total = total

    def __repr__(self):
        return f"<id {self.id}>"


class Guests(db.Model):
    __tablename__ = "guests"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    mobile = db.Column(db.String())

    def __init__(self, first_name, last_name, email, mobile):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile = mobile

    def __repr__(self):
        return f"<id {self.id}>"


class Bookings(db.Model):

    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id", ondelete="CASCADE"))
    guests = db.Column(db.Integer)
    room = db.Column(db.String())
    checkin = db.Column(db.Date())
    checkout = db.Column(db.Date())
    tariff = db.Column(db.Numeric(10, 2))
    gst = db.Column(db.Numeric(10, 2))
    tariff_wo_gst = db.Column(db.Numeric(10, 2))
    booking_source_id = db.Column(db.Integer, db.ForeignKey("booking_sources.id"))
    operator = db.Column(db.String())
    and_register_serial_no = db.Column(db.Integer)
    checkin_time = db.Column(db.Time())
    payment_mode_id = db.Column(db.Integer, db.ForeignKey("payment_modes.id"))
    tpr = db.Column(db.Numeric(10, 2))
    npa = db.Column(db.Numeric(10, 2))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    hotel = db.relationship("Hotels", backref=db.backref("bookings", lazy="dynamic"))
    booking_source = db.relationship(
        "BookingSources", backref=db.backref("bookings", lazy="dynamic")
    )
    payment_mode = db.relationship(
        "PaymentModes", backref=db.backref("bookings", lazy="dynamic")
    )

    def __init__(
        self,
        guest_id,
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
        date_created,
    ):
        self.guest_id = guest_id
        self.guests = guests
        self.hotel_id = hotel_id
        self.room = room
        self.checkin = checkin
        self.checkout = checkout
        self.tariff = tariff
        self.gst = gst
        self.tariff_wo_gst = tariff_wo_gst
        self.booking_source_id = booking_source_id
        self.operator = operator
        self.and_register_serial_no = and_register_serial_no
        self.checkin_time = checkin_time
        self.payment_mode_id = payment_mode_id
        self.tpr = tpr
        self.npa = npa
        self.date_created = date_created

    def __repr__(self):
        return f"<id {self.id}>"


class Documents(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id", ondelete="CASCADE"))
    doc = db.Column(db.LargeBinary())

    doc_guest = relationship("Guests", backref="doc_guest")

    def __init__(self, guest_id, doc):
        self.guest_id = guest_id
        self.doc = doc

    def __repr__(self):
        return f"<id {self.id}>"


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, username, password, active):
        self.username = username
        self.password = generate_password_hash(password)
        self.active = active

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def create(name, password, active=True):
        rv = User(name, password, active)
        db.session.add(rv)
        db.session.commit()
        return rv

    def get_id(self):
        return self.id

    def has_role(self, role):
        return any(
            role == role_assignment.role.name and role_assignment.role.active
            for role_assignment in self.role_assignments
        )


# RBAC
# https://github.com/maxcountryman/flask-login/issues/421
class Role(db.Model):

    name = db.Column(db.VARCHAR(100), primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, name, active=True):
        self.name = name
        self.active = active

    @staticmethod
    def create(name, active=True):
        rv = Role(name, active)
        db.session.add(rv)
        db.session.commit()
        return rv

    @staticmethod
    def get(role_name):
        role = Role.query.filter(Role.name == role_name).first()
        return role


class RoleAssignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.VARCHAR(100), db.ForeignKey("role.name"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # Why was unique=True?

    # For ease of use, I have left lazy's as 'joined'. You shouldn't do this unless you mean to.
    role = db.relationship(
        "Role", backref=db.backref("role_assignments", lazy="joined"), lazy="joined"
    )
    user = db.relationship(
        "User", backref=db.backref("role_assignments", lazy="joined"), lazy="joined"
    )

    def __init__(self, role_name, user_id):
        self.role_name = role_name
        self.user_id = user_id

    @staticmethod
    def create(role_name, user_id):
        rv = RoleAssignment(role_name, user_id)
        db.session.add(rv)
        db.session.commit()
        return rv

    @staticmethod
    def get(id):
        rv = RoleAssignment.query.filter(RoleAssignment.id == id).first()
        return rv
