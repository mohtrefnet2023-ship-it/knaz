import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today
from knaz_fleet.utils import ensure_gt_zero, ensure_positive


class KnazFinanceInstallment(Document):
    def validate(self):
        ensure_gt_zero(self.installment_amount, "قيمة القسط")
        ensure_positive(self.paid_amount, "المدفوع")
        if float(self.paid_amount or 0) > float(self.installment_amount or 0):
            frappe.throw(_("المدفوع لا يمكن أن يتجاوز قيمة القسط"))
        self.outstanding_amount = max(float(self.installment_amount or 0) - float(self.paid_amount or 0), 0)
        if self.outstanding_amount == 0:
            self.status = "Paid"
        elif self.paid_amount:
            self.status = "Partially Paid"
        elif self.due_date and getdate(self.due_date) < getdate(today()):
            self.status = "Overdue"

    def on_update(self):
        if self.finance_contract:
            total_paid = frappe.db.sql("""
                select coalesce(sum(paid_amount), 0)
                from `tabKnaz Finance Installment`
                where finance_contract=%s and docstatus < 2
            """, self.finance_contract)[0][0]
            contract_total = frappe.db.get_value("Knaz Vehicle Finance Contract", self.finance_contract, "total_finance_amount") or 0
            frappe.db.set_value("Knaz Vehicle Finance Contract", self.finance_contract, {
                "paid_amount": total_paid,
                "outstanding_amount": max(float(contract_total or 0) - float(total_paid or 0), 0),
            })
