import frappe


@frappe.whitelist()
def get_dashboard_summary():
    return {
        "vehicles": _count_by_status("Knaz Vehicle", "current_status"),
        "workshop_orders": _count_by_status("Knaz Workshop Order", "status"),
        "technician_requests": _count_by_status("Knaz Technician Request", "status"),
        "collections": _collection_summary(),
        "insurance_claims": _count_by_status("Knaz Insurance Claim", "status"),
        "legal_cases": _count_by_status("Knaz Legal Case", "status"),
        "finance_installments": _count_by_status("Knaz Finance Installment", "status"),
    }


def _count_by_status(doctype, fieldname):
    if not frappe.db.table_exists(doctype):
        return {}
    rows = frappe.db.sql(f"""select {fieldname}, count(*) from `tab{doctype}` group by {fieldname}""", as_list=True)
    return {row[0] or "Not Set": row[1] for row in rows}


def _collection_summary():
    if not frappe.db.table_exists("Knaz Collection Case"):
        return {"outstanding_total": 0, "open_count": 0}
    row = frappe.db.sql("""
        select coalesce(sum(outstanding_amount), 0), count(*)
        from `tabKnaz Collection Case`
        where status not in ('Collected', 'Closed')
    """, as_list=True)[0]
    return {"outstanding_total": row[0], "open_count": row[1]}
