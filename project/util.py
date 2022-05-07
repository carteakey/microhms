"""
Utility Functions
"""
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
    if price < 1000:
        return 0
    elif 1000 <= price <= 2499:
        return 0.06 * price
    elif 2500 <= price <= 7499:
        return 0.09 * price
    elif price >= 7500:
        return 0.14 * price
