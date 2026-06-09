# Knaz Fleet Operations ERP

تطبيق Frappe / ERPNext مخصص لإدارة عمليات شركة تأجير سيارات: السيارات، العقود، الورشة، طلبات الفنيين، التحصيل، الحوادث، مطالبات التأمين، القضايا، التمويل، والتقارير.

## الحالة
هذه نسخة **Cloud-ready MVP** قابلة للرفع إلى GitHub وتجربتها على Frappe Cloud Private Bench. ليست بديلاً عن اختبار إنتاجي كامل، لكنها تحتوي على بنية تطبيق حقيقية وDocTypes وValidation Rules وتقارير أساسية.

## المتطلبات
- Frappe v15
- ERPNext v15 مثبت على الموقع
- Frappe Cloud Private Bench عند التثبيت على `.frappe.cloud`

## أهم المحتويات
- DocTypes مخصصة ببادئة `Knaz` لتجنب التعارض مع DocTypes الأصلية في ERPNext.
- أدوار وصلاحيات أولية.
- قواعد تحقق أساسية في Controllers.
- تقارير Script Reports.
- Scheduled Jobs للتأخير والتنبيهات.
- API مختصر للوحة التحكم.

## التشغيل المحلي للمطور
```bash
bench get-app https://github.com/YOUR_ORG/knaz_fleet.git --branch version-15
bench --site YOUR_SITE install-app knaz_fleet
bench --site YOUR_SITE migrate
bench build
bench restart
```

## ملاحظات مهمة
- يجب رفع محتويات هذا المجلد كـ Git repository، بحيث يكون `pyproject.toml` في جذر المستودع.
- إذا كان Bench على Frappe Cloud بإصدار Frappe مختلف عن v15، يجب تعديل `[tool.bench.frappe-dependencies]` في `pyproject.toml`.
- يفضّل إنشاء بيانات تجريبية للسيارات والعملاء والقطع بعد التثبيت من داخل Desk.
