import frappe
from frappe.model.document import Document


class KnazInsuranceClaimFollowUp(Document):
    def after_insert(self):
        frappe.db.set_value("Knaz Insurance Claim", self.insurance_claim, "last_follow_up_date", self.follow_up_date)
