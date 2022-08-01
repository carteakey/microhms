"""
Utility Functions
"""
import requests


def get_totals(lines):
    """
    return total values from line dict.
    """
    totals = {}
    totals["total_inclusion"] = sum([line["inclusion"] for line in lines])
    totals["total_subtotal"] = sum([line["subtotal"] for line in lines])
    totals["total_cgst"] = sum([line["cgst"] for line in lines])
    totals["total_sgst"] = sum([line["cgst"] for line in lines])
    totals["total_amount"] = sum([line["total"] for line in lines])
    totals["total_tax"] = totals["total_cgst"] + totals["total_sgst"]
    return totals


def calc_gst(price):
    """
    calculate gst values
    """
    if 0 <= price <= 7499:
        return 0.06 * price
    elif price >= 7500:
        return 0.14 * price

import http
import os


def send_otp(otp, mobile):
    """
    This function calls MSG91 API for OTP generation
    """
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = '{"OTP":"' + str(otp) + '"}'

    headers = {"content-type": "application/json"}

    template_id = os.environ["MSG91_TEMPLATE_ID"]

    authkey = os.environ["MSG91_AUTHKEY"]

    conn.request(
        "GET",
        f"/api/v5/otp?template_id={template_id}&mobile=%2091{mobile}&authkey={authkey}",
        payload,
        headers,
    )

    res = conn.getresponse()

    data = res.read()

    return data

def send_email(subject,variables,to,attachments=None):
    

    if attachments:
        files = []
        for attachment in attachments:
            files.append(("attachment", (attachment.filename, attachment.read(), attachment.content_type)))
            
    res = requests.post(
		"https://api.mailgun.net/v3/mg.vizima.in/messages",
		auth=("api", os.environ["MAILGUN_API_KEY"]),
        files = files,
		data={"from": "New Booking <bookings@"+os.environ["MAILGUN_DOMAIN"]+">",
			"to": to,
            "subject": subject,
			"template": "booking",
			"h:X-Mailgun-Variables": variables,
            })
    
    return res

