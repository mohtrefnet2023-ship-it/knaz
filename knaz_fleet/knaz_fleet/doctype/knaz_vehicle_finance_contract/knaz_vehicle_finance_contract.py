import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months
from knaz_fleet.utils import validate_date_order, ensure_gt_zero, ensure_positive


class KnazVehicleFinanceContract(Document):
    def validate(self):
        validate_date_order(self.start_date, self.end_date, "تاريخ نهاية التمويل يجب أن يكون بعد تاريخ البداية")
        ensure_gt_zero(self.total_finance_amount, "مبلغ التمويل")
        ensure_gt_zero(self.installment_amount, "قيمة القسط")
        ensure_gt_zero(self.number_of_installments, "عدد الأقساط")
        ensure_positive(self.down_payment, "الدفعة المقدمة")
        self.outstanding_amount = max(float(self.total_finance_amount or 0) - float(self.down_payment or 0) - float(self.paid_amount or 0), 0)

    def on_submit(self):
        existing = frappe.db.count("Knaz Finance Installment", {"finance_contract": self.name})
        if not existing:
            for i in range(1, int(self.number_of_installments or 0) + 1):
                inst = frappe.new_doc("Knaz Finance Installment")
                inst.finance_contract = self.name
                inst.vehicle = self.vehicle
                inst.installment_no = i
                inst.due_date = add_months(self.start_date, i - 1)
                inst.installment_amount = self.installment_amount
                inst.paid_amount = 0
                inst.outstanding_amount = self.installment_amount
                inst.status = "Upcoming"
                inst.insert(ignore_permissions=True)
        frappe.db.set_value("Knaz Vehicle", self.vehicle, "finance_contract", self.name)
