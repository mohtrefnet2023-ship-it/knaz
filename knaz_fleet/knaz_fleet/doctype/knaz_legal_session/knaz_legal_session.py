import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, today


class KnazLegalSession(Document):
    def validate(self):
        if getdate(self.session_date) < getdate(today()) and self.is_new():
            frappe.throw(_("تاريخ الجلسة الجديدة لا يجب أن يكون في الماضي"))

    def after_insert(self):
        if self.legal_case:
            frappe.db.set_value("Knaz Legal Case", self.legal_case, "next_session_date", self.session_date)
