import frappe


def execute(filters=None):
    columns = [
        {"label": "الحالة", "fieldname": "status", "fieldtype": "Data", "width": 180},
        {"label": "العدد", "fieldname": "count", "fieldtype": "Int", "width": 120},
    ]
    data = frappe.db.sql("""
        select current_status as status, count(*) as count
        from `tabKnaz Vehicle`
        group by current_status
        order by count desc
    """, as_dict=True)
    return columns, data
