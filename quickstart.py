from project import create_app
from project.models import db, User, Role, RoleAssignment

app = create_app()

with app.app_context():
    #Create a user, role, and role assignment
    user = User.create('admin', 'admin@123', True)
    role = Role.create('admin')
    RoleAssignment.create(role.name, user.id)

    #Insert sample data
    #Charges
    db.session.execute(
        "INSERT INTO charges (name,hsnsac) VALUES ('Room Rent','996311') , ('Food & Beverages','996331'), ('Laundry','9997'), ('Taxi','996412')"
    )
    #Config
    db.session.execute(
        "INSERT INTO config (company_name,address,email,phone) VALUES ('Hotel ABC', '123 Main St, New York, NY 10001','abc@hotel.com', '123-456-7890')"
    )
    #Payment Modes
    db.session.execute(
        "INSERT INTO payment_modes (name) VALUES ('Cash'), ('Credit Card'), ('Debit Card'), ('Paypal'), ('Other')"
    )
    #Booking Sources
    db.session.execute(
        "INSERT INTO booking_sources (name) VALUES ('Walk-in'), ('Online'), ('Phone'), ('Other')"
    )
    #Hotels
    db.session.execute(
        "INSERT INTO hotels (name,address) VALUES ('Hotel ABC', '123 Main St, New York, NY 10001')"
    )
    db.session.execute(
    '''CREATE OR REPLACE VIEW public.invoices_v
        AS SELECT ih.id AS "ID",
        ih.invoice_num AS "Invoice Num",
        ih.invoice_date AS "Invoice Date",
        ih.booking_id AS "Booking ID",
        ih.booking_date AS "Booking Date",
        h.name AS "Hotel",
        ih.payee AS "Payee",
        ih.guest AS "Guest",
        ih.guest_details AS "Guest Details",
        sum(il.total) AS "Total"
        FROM invoice_headers ih,
            invoice_lines il,
            hotels h,
            payment_modes p
        WHERE ih.id = il.invoice_id AND ih.hotel_id = h.id AND ih.payment_mode_id = p.id
        GROUP BY ih.id, ih.invoice_num, ih.invoice_date, ih.booking_id, ih.booking_date, h.name, ih.payee, ih.guest, ih.guest_details;'''
    )

    db.session.commit()
    print("Sample data inserted")
    print("You can now login with admin/admin@123")
    print("You can now create a new user with admin/admin@123")
    

