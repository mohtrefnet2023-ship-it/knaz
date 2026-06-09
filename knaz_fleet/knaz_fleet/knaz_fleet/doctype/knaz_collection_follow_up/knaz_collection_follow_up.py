import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today


class KnazCollectionFollowUp(Document):
    def validate(self):
        if self.next_follow_up_date and getdate(self.next_follow_up_date) < getdate(today()):
            frappe.throw(_("تاريخ المتابعة القادمة لا يجب أن يكون في الماضي"))
        if self.result == "Promise to Pay" and not self.promise_date:
            frappe.throw(_("تاريخ وعد السداد إلزامي"))

    def after_insert(self):
        if self.result == "Promise to Pay":
            frappe.db.set_value("Knaz Collection Case", self.collection_case, {
                "status": "Promise to Pay",
                "promise_date": self.promise_date,
                "promise_amount": self.promised_amount,
            })
        elif self.result == "Escalate":
            frappe.db.set_value("Knaz Collection Case", self.collection_case, "status", "Escalated")
