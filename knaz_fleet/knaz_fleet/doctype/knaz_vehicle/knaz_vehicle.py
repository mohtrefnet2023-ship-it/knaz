import frappe
from frappe import _
from frappe.model.document import Document


class KnazVehicle(Document):
    def validate(self):
        if not self.plate_no:
            frappe.throw(_("رقم اللوحة إلزامي"))
        if not self.chassis_no:
            frappe.throw(_("رقم الهيكل إلزامي"))
        if (self.odometer or 0) < 0:
            frappe.throw(_("قراءة العداد لا يمكن أن تكون سالبة"))
        old = self.get_doc_before_save()
        if old and self.odometer is not None and old.odometer is not None and float(self.odometer or 0) < float(old.odometer or 0):
            frappe.throw(_("قراءة العداد الجديدة لا يجب أن تكون أقل من القراءة السابقة"))
        if self.current_status == "Sold" and self.current_contract:
            frappe.throw(_("لا يمكن بيع سيارة لديها عقد نشط"))

    def after_insert(self):
        self.create_status_log(None, self.current_status, "Initial Status")

    def on_update(self):
        old = self.get_doc_before_save()
        if old and old.current_status != self.current_status:
            self.create_status_log(old.current_status, self.current_status, "Status Changed")

    def create_status_log(self, old_status, new_status, reason=None):
        log = frappe.new_doc("Knaz Vehicle Status Log")
        log.vehicle = self.name
        log.old_status = old_status
        log.new_status = new_status
        log.changed_by_user = frappe.session.user
        log.change_date = frappe.utils.now_datetime()
        log.reason = reason
        log.insert(ignore_permissions=True)
