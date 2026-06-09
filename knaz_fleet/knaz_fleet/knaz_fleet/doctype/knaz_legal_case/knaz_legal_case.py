import frappe
from frappe import _
from frappe.model.document import Document
from knaz_fleet.utils import ensure_positive


class KnazLegalCase(Document):
    def validate(self):
        if not (self.customer or self.collection_case or self.insurance_claim or self.rental_contract):
            frappe.throw(_("يجب ربط القضية بعميل أو عقد أو تحصيل أو مطالبة"))
        ensure_positive(self.claimed_amount, "المبلغ المطالب به")
        ensure_positive(self.collected_amount, "المبلغ المحصل")
        if self.status == "Closed" and not (self.judgment_summary or self.remarks):
            frappe.throw(_("ملخص الإغلاق أو الحكم إلزامي عند إغلاق القضية"))
