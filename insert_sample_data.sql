insert
	into
	public.charges (id,
	name,
	hsnsac)
values (2,
'Room Rent',
'996311');

insert
	into
	public.charges (id,
	name,
	hsnsac)
values (3,
'Food & Beverages',
'996331');

insert
	into
	public.charges (id,
	name,
	hsnsac)
values (4,
'Laundry',
'9997');

insert
	into
	public.charges (id,
	name,
	hsnsac)
values (1,
'Taxi',
'996412');

insert
	into
	public.config (id,
	company_name,
	address,
	email,
	phone)
values (1,
'Company ABC',
'Limgrave',
'hotelabc@abchotel.com',
'1234-567-89');

insert
	into
	public.hotels (
	name,
	address)
values (
'Hotel ABC',
'Limgrave');

insert
	into
	public.payment_modes(name)
values ('Credit Card');

insert
	into
	public.payment_modes(name)
values ('Debit Card');

insert
	into
	public.payment_modes(name)
values ('Cash');

-- public.invoices_v source

CREATE OR REPLACE VIEW public.invoices_v
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
  GROUP BY ih.id, ih.invoice_num, ih.invoice_date, ih.booking_id, ih.booking_date, h.name, ih.payee, ih.guest, ih.guest_details;
