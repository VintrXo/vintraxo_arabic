# تثبيت ترجمة فينتراكسو على سيرفر آخر

الحزمة مستقلة باسم `vintraxo_arabic`. لا تحتاج إلى نقل قاعدة البيانات أو تشغيل وضع المطوّر،
ولا تثبّت تطبيق المطعم أو التعليم أو الرعاية الصحية؛ تترجم النصوص المستخدمة في التطبيقات الموجودة فقط.

## التثبيت من الملف المضغوط

1. فك الأرشيف في مجلد دائم باسم `vintraxo_arabic` مثل `/home/frappe/releases/vintraxo_arabic`.
2. استخدم حساب مالك البنش، وخذ نسخة احتياطية للموقع الهدف قبل تعديل تطبيقاته.
3. استبدل اسم الموقع والمسارات في الأوامر التالية:

```sh
cd /home/frappe/frappe-bench
bench --site your-site.example backup
bench get-app --soft-link /home/frappe/releases/vintraxo_arabic --skip-assets
bench --site your-site.example install-app vintraxo_arabic
bench --site your-site.example clear-cache
bench --site your-site.example execute vintraxo_arabic.translation_tools.validate_server_batches.run
```

المجلد الدائم يجب ألا يُحذف بعد التثبيت؛ البنش يشير إليه برابط رمزي.
لا تستخدم أمر جلب التطبيق إذا كان التطبيق موجودًا بالفعل. اتبع مسار التحديث أدناه.
حدد اللغة العربية للمستخدم ثم حدّث المتصفح باستخدام Ctrl+Shift+R.
لا يلزم `bench build` لهذه الحزمة لأنها لا تضيف ملفات واجهة مبنية.

## تحديث تثبيت موجود

خذ نسخة احتياطية للموقع واحتفظ بنسخة من مجلد التطبيق الحالي قبل استبدال ملفات الإصدار،
خصوصًا إذا كان السيرفر الهدف يحتوي تعديلات ترجمة محلية. ادمج هذه التعديلات قبل الاستبدال.
انقل الملفات إلى **مجلد التطبيق الفعلي** مع الحفاظ على مالكه وصلاحياته، ثم:

```sh
cd /home/frappe/frappe-bench
bench --site your-site.example migrate
bench --site your-site.example clear-cache
bench --site your-site.example execute vintraxo_arabic.translation_tools.validate_server_batches.run
```

أعد تشغيل خدمات البنش حسب طريقة تشغيل السيرفر إذا ظلت العمليات القديمة تعمل بعد التحديث،
ثم حدّث المتصفح. لا تُفعّل وضع المطوّر في الإنتاج من أجل الترجمة.

## التحقق والحدود

يجب أن يعرض التحقق ست دفعات و2898 ترجمة دون تعارض في القاموس الفعلي.
يوجد بالملف الكامل 26608 مفتاح مصدر فريد؛ فحص المتغيرات وHTML التفصيلي يغطي الدفعات الست المراجعة،
ولا يعني مراجعة لغوية لكل الترجمات القديمة.
تتضمن الحزمة ترجمة «قسم الفحوص التشخيصية» و«إعادة التأهيل والعلاج الطبيعي».
قد تتقدم ترجمة قاعدة البيانات أو إضافة ترجمة أخرى على بعض القيم؛ عندها يعرض الفحص التعارض.
لا يحذف التثبيت هذه الترجمات ولا يغيّر بيانات المستخدمين أو صلاحياتهم.

تم التحقق محليًا على Frappe 16.33.1 وERPNext 16.34.2. دعم Frappe 15 مسموح في التغليف،
لكن تثبيتًا جديدًا عليه لم يُختبر. استخدم إصدار Python المطلوب لإصدار Frappe عندك.
التفعيل على السيرفر الجديد يحتاج اختبارًا بعد التثبيت؛ لا توجد شهادة تثبيت جديد ضمن هذه الحزمة.

## التثبيت المباشر من GitHub

المستودع المستقل: https://github.com/VintrXo/vintraxo_arabic
المستودع خاص حاليًا؛ يحتاج السيرفر إلى حساب مخوّل أو مفتاح نشر للقراءة فقط.
لا تضع رمز الوصول في رابط المستودع أو ملف إعدادات داخل Git.

```sh
cd /home/frappe/frappe-bench
bench --site your-site.example backup
bench get-app https://github.com/VintrXo/vintraxo_arabic.git --branch main
bench --site your-site.example install-app vintraxo_arabic
bench --site your-site.example clear-cache
bench --site your-site.example execute vintraxo_arabic.translation_tools.validate_server_batches.run
```