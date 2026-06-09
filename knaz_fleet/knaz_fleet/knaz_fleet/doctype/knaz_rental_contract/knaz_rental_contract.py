import frappe
from frappe import _
from frappe.model.document import Document
from knaz_fleet.utils import validate_date_order, ensure_gt_zero, ensure_positive

BLOCKED_STATUSES = ["In Workshop", "Under Maintenance", "Accident", "Insurance Claim", "Sold", "Inactive"]


class KnazRentalContract(Document):
    def validate(self):
        validate_date_order(self.start_date, self.end_date, "تاريخ نهاية العقد يجب أن يكون بعد تاريخ البداية")
        ensure_gt_zero(self.total_amount, "إجمالي العقد")
        ensure_positive(self.daily_rate, "السعر اليومي")
        ensure_positive(self.paid_amount, "المدفوع")
        self.outstanding_amount = max(float(self.total_amount or 0) - float(self.paid_amount or 0), 0)
        if self.docstatus == 0 and self.vehicle:
            status = frappe.db.get_value("Knaz Vehicle", self.vehicle, "current_status")
            if status in BLOCKED_STATUSES:
                frappe.throw(_("لا يمكن إنشاء عقد لسيارة حالتها {0}").format(status))

    def on_submit(self):
        if self.vehicle:
            frappe.db.set_value("Knaz Vehicle", self.vehicle, {
                "current_status": "Rented",
                "current_customer": self.customer,
                "current_contract": self.name,
            })
        self.status = "Active"
        self.db_update()

    def on_cancel(self):
        if self.vehicle:
            frappe.db.set_value("Knaz Vehicle", self.vehicle, {
                "current_status": "Available",
                "current_customer": None,
                "current_contract": None,
            })
        self.status = "Cancelled"
        self.db_update()
