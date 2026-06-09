# تثبيت التطبيق على Frappe Cloud

## 1) رفع التطبيق إلى GitHub
1. فك ضغط الملف.
2. أنشئ مستودع GitHub جديد باسم `knaz_fleet`.
3. ارفع **محتويات مجلد التطبيق** بحيث يظهر `pyproject.toml` في جذر المستودع.
4. أنشئ فرعًا باسم `version-15` أو استخدم `main` إذا كان Bench v15.

## 2) تجهيز Frappe Cloud
- استخدم Private Bench Group لأن تثبيت custom apps يتطلب التحكم في التطبيقات داخل Bench Group.
- أنشئ Site عليه ERPNext v15.

## 3) إضافة التطبيق للـ Bench Group
1. افتح Bench Group.
2. Apps.
3. Add App.
4. أدخل رابط GitHub للمستودع.
5. اختر الفرع المتوافق مع Frappe v15.
6. نفّذ Deploy / Update للـ Bench Group.

## 4) تثبيت التطبيق على الـ Site
1. افتح Site.
2. Apps.
3. Install App.
4. اختر `knaz_fleet`.
5. انتظر اكتمال التثبيت.

## 5) بعد التثبيت
- ادخل إلى Desk وابحث عن Module: `Knaz Fleet`.
- أنشئ مستخدمين واربطهم بالأدوار التي تبدأ بـ `Knaz`.
- أنشئ سيارات، عقود، أوامر صيانة، وملفات تحصيل للتجربة.

## 6) عند فشل التثبيت
- افتح Deploy Logs في Frappe Cloud.
- تأكد أن `pyproject.toml` يحتوي على `[tool.bench.frappe-dependencies]`.
- تأكد أن الموقع مثبت عليه ERPNext وليس Frappe فقط.
- تأكد أن إصدار Bench هو Frappe v15.
