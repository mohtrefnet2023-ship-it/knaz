app_name = "knaz_fleet"
app_title = "Knaz Fleet Operations ERP"
app_publisher = "Knaz"
app_description = "Fleet operations ERP custom app for car rental operations"
app_email = "knaz.rnt@gmail.com"
app_license = "MIT"

required_apps = ["erpnext"]

after_install = "knaz_fleet.install.after_install"
after_migrate = "knaz_fleet.install.after_install"

scheduler_events = {
    "daily": [
        "knaz_fleet.tasks.update_overdue_collections",
        "knaz_fleet.tasks.update_overdue_finance_installments",
        "knaz_fleet.tasks.create_document_expiry_alerts",
    ]
}

fixtures = []

# Lightweight Desk assets. The app is primarily standard Frappe DocTypes + Reports.
app_include_css = "/assets/knaz_fleet/css/knaz_fleet.css"
app_include_js = "/assets/knaz_fleet/js/knaz_fleet.js"
