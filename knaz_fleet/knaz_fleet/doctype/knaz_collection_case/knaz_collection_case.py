import frappe
from frappe import _
from frappe.model.document import Document
from knaz_fleet.utils import ensure_gt_zero, ensure_positive, days_overdue


class KnazCollectionCase(Document):
    def validate(self):
        ensure_gt_zero(self.due_amount, "المبلغ المستحق")
        ensure_positive(self.paid_amount, "المدفوع")
        if float(self.paid_amount or 0) > float(self.due_amount or 0) and not frappe.has_permission("Knaz Collection Case", "submit"):
            frappe.throw(_("المدفوع لا يمكن أن يكون أكبر من المستحق"))
        self.outstanding_amount = max(float(self.due_amount or 0) - float(self.paid_amount or 0), 0)
        self.delay_days = days_overdue(self.due_date)
        if self.outstanding_amount == 0 and self.status not in ["Collected", "Closed"]:
            self.status = "Collected"
        if self.status == "Legal" and not self.escalation_reason:
            frappe.throw(_("سبب التصعيد إلزامي عند التحويل للقانوني"))
