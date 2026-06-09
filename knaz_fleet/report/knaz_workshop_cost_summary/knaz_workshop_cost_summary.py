import frappe


def execute(filters=None):
    columns = [
        {"label": "أمر الصيانة", "fieldname": "name", "fieldtype": "Link", "options": "Knaz Workshop Order", "width": 160},
        {"label": "السيارة", "fieldname": "vehicle", "fieldtype": "Link", "options": "Knaz Vehicle", "width": 160},
        {"label": "الحالة", "fieldname": "status", "fieldtype": "Data", "width": 130},
        {"label": "تكلفة القطع", "fieldname": "parts_cost", "fieldtype": "Currency", "width": 120},
        {"label": "العمالة", "fieldname": "labor_cost", "fieldtype": "Currency", "width": 120},
        {"label": "خارجي", "fieldname": "external_workshop_cost", "fieldtype": "Currency", "width": 120},
        {"label": "الإجمالي", "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
    ]
    data = frappe.db.sql("""
        select name, vehicle, status, parts_cost, labor_cost, external_workshop_cost, total_cost
        from `tabKnaz Workshop Order`
        order by modified desc
    """, as_dict=True)
    return columns, data
