import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime
from knaz_fleet.utils import ensure_positive


class KnazWorkshopOrder(Document):
    def validate(self):
        if not self.vehicle:
            frappe.throw(_("السيارة إلزامية"))
        vehicle_status = frappe.db.get_value("Knaz Vehicle", self.vehicle, "current_status")
        if vehicle_status in ["Sold", "Inactive"]:
            frappe.throw(_("لا يمكن فتح أمر صيانة لسيارة مباعة أو غير نشطة"))
        ensure_positive(self.labor_cost, "تكلفة العمالة")
        ensure_positive(self.external_workshop_cost, "تكلفة ورشة خارجية")
        ensure_positive(self.odometer, "قراءة العداد")
        self.parts_cost = 0
        for row in self.get("items") or []:
            if (row.qty or 0) <= 0:
                frappe.throw(_("كمية قطعة الغيار يجب أن تكون أكبر من صفر"))
            row.amount = float(row.qty or 0) * float(row.rate or 0)
            self.parts_cost += row.amount
        self.total_cost = float(self.parts_cost or 0) + float(self.labor_cost or 0) + float(self.external_workshop_cost or 0)
        if self.status == "Closed" and not self.closing_notes:
            frappe.throw(_("ملاحظات الإغلاق إلزامية عند إغلاق أمر الصيانة"))

    def after_insert(self):
        frappe.db.set_value("Knaz Vehicle", self.vehicle, "current_status", "In Workshop")

    def on_update(self):
        if self.status == "Closed" and not self.actual_exit_date:
            self.db_set("actual_exit_date", now_datetime(), update_modified=False)
            frappe.db.set_value("Knaz Vehicle", self.vehicle, "current_status", "Available")
