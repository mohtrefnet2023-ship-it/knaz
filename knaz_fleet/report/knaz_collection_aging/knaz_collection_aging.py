import frappe


def execute(filters=None):
    filters = filters or {}
    conditions = ["status not in ('Collected', 'Closed')"]
    values = {}
    if filters.get("customer"):
        conditions.append("customer = %(customer)s")
        values["customer"] = filters["customer"]
    columns = [
        {"label": "ملف التحصيل", "fieldname": "name", "fieldtype": "Link", "options": "Knaz Collection Case", "width": 160},
        {"label": "العميل", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "المتبقي", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 120},
        {"label": "أيام التأخير", "fieldname": "delay_days", "fieldtype": "Int", "width": 100},
        {"label": "الحالة", "fieldname": "status", "fieldtype": "Data", "width": 150},
    ]
    data = frappe.db.sql(f"""
        select name, customer, outstanding_amount, delay_days, status
        from `tabKnaz Collection Case`
        where {' and '.join(conditions)}
        order by delay_days desc
    """, values, as_dict=True)
    return columns, data
