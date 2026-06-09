from frappe.model.document import Document


class KnazVehicleProfitabilitySnapshot(Document):
    def validate(self):
        self.net_profit = (self.rental_revenue or 0) + (self.insurance_received or 0) - (self.maintenance_cost or 0) - (self.spare_parts_cost or 0) - (self.finance_cost or 0) - (self.other_expenses or 0)
        if self.net_profit > 0:
            self.profitability_status = "Profitable"
        elif self.net_profit < 0:
            self.profitability_status = "Loss"
        else:
            self.profitability_status = "Neutral"
