import os

from flask import Flask, abort, render_template, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secretkey123")


items = []

ADMIN_PASSWORD = "admin123"
LANGUAGES = {"ar", "en"}

TRANSLATIONS = {
    "ar": {
        "default_title": "منصة المفقودات",
        "brand": "مفقودات المطار",
        "brand_subtitle": "Airport Lost & Found",
        "nav_report": "إبلاغ",
        "nav_search": "بحث",
        "nav_admin": "إدارة",
        "language_label": "English",
        "footer_brand": "منصة مفقودات المطار",
        "footer_note": "خدمة رقمية لتنظيم البلاغات واستعادة الممتلكات",
        "home_title": "منصة مفقودات المطار",
        "hero_eyebrow": "مركز خدمات المسافرين",
        "hero_heading": "استعادة المفقودات داخل المطار أصبحت أوضح وأسرع.",
        "hero_text": "منصة منظمة لتسجيل البلاغات، متابعة حالة المفقودات، ومساعدة فريق الإدارة على تحديث النتائج باحترافية.",
        "hero_report": "تسجيل بلاغ مفقود",
        "hero_track": "تتبع بلاغ",
        "hero_caption": "مكتب مفقودات حديث داخل صالة المطار",
        "ticket_report": "رقم البلاغ",
        "ticket_review": "قيد المراجعة",
        "card_report_title": "إبلاغ عن مفقود",
        "card_report_text": "أدخل بيانات الغرض ومعلومات التواصل لتوليد رقم بلاغ.",
        "card_search_title": "البحث برقم البلاغ",
        "card_search_text": "تابع حالة البلاغ ومعرفة هل تم العثور على الغرض.",
        "card_admin_title": "لوحة الإدارة",
        "card_admin_text": "تحديث حالة المفقودات والاستلام من صفحة رسمية مرتبة.",
        "trust_1": "استقبال البلاغات",
        "trust_2": "متابعة الحالة",
        "trust_3": "تحديث إداري فوري",
        "trust_4": "واجهة ثنائية اللغة",
        "metric_reports": "بلاغات منظمة",
        "metric_tracking": "متابعة واضحة",
        "metric_staff": "لوحة موظفين",
        "workflow_title": "كيف تعمل المنصة؟",
        "workflow_text": "رحلة مختصرة ومنظمة من لحظة تسجيل البلاغ حتى تحديث حالة الاستلام.",
        "step_1_title": "سجل البلاغ",
        "step_1_text": "أدخل بيانات الغرض والوصف التفصيلي ليتم إنشاء رقم بلاغ.",
        "step_2_title": "تابع الحالة",
        "step_2_text": "استخدم رقم البلاغ لمعرفة آخر تحديث مسجل على الطلب.",
        "step_3_title": "تحديث إداري",
        "step_3_text": "يقوم الموظف بتحديث حالة العثور والاستلام من لوحة الإدارة.",
        "report_title": "تسجيل بلاغ مفقود",
        "report_eyebrow": "بلاغ جديد",
        "report_heading": "تسجيل غرض مفقود",
        "report_text": "اكتب وصفاً واضحاً يساعد فريق المطار على مطابقة البلاغ مع الأغراض التي يتم العثور عليها.",
        "name_label": "اسم صاحب البلاغ",
        "name_placeholder": "مثال: أحمد محمد",
        "item_label": "اسم الغرض",
        "item_placeholder": "مثال: حقيبة سفر، سماعات، جواز",
        "description_label": "الوصف",
        "description_placeholder": "اذكر اللون، العلامة التجارية، مكان الفقدان التقريبي، وأي تفاصيل مميزة",
        "submit_report": "إرسال البلاغ",
        "back": "رجوع",
        "tip_title": "نصيحة سريعة",
        "tip_text": "كلما كان الوصف أدق زادت فرصة المطابقة، خصوصاً رقم الرحلة أو البوابة أو منطقة الانتظار.",
        "search_title": "البحث عن بلاغ",
        "search_eyebrow": "متابعة البلاغ",
        "search_heading": "البحث عن مفقود",
        "search_text": "أدخل رقم البلاغ الذي حصلت عليه بعد التسجيل لمعرفة آخر حالة مسجلة.",
        "report_success": "تم تسجيل البلاغ بنجاح. رقم البلاغ الخاص بك:",
        "report_id_label": "رقم البلاغ",
        "report_id_placeholder": "مثال: 73926",
        "search_button": "بحث",
        "details_title": "تفاصيل البلاغ",
        "field_id": "رقم البلاغ",
        "field_name": "الاسم",
        "field_item": "الغرض",
        "field_date": "تاريخ البلاغ",
        "field_description": "الوصف",
        "field_status": "حالة العثور",
        "field_claim": "حالة الاستلام",
        "not_found": "لم يتم العثور على بلاغ بهذا الرقم. تأكد من الرقم وحاول مرة أخرى.",
        "keep_id_title": "احتفظ برقم البلاغ",
        "keep_id_text": "سيتم استخدام الرقم للمتابعة مع مكتب المفقودات داخل المطار أو عبر المنصة.",
        "login_title": "تسجيل دخول الإدارة",
        "login_eyebrow": "دخول مصرح",
        "login_heading": "لوحة إدارة المفقودات",
        "login_text": "هذه الصفحة مخصصة لموظفي إدارة المفقودات لتحديث حالة البلاغات.",
        "password_label": "كلمة المرور",
        "login_button": "تسجيل الدخول",
        "login_error": "كلمة المرور غير صحيحة",
        "admin_title": "لوحة الإدارة",
        "admin_eyebrow": "لوحة التحكم",
        "admin_heading": "إدارة بلاغات المفقودات",
        "admin_text": "راجع البلاغات المسجلة وحدّث حالة العثور والاستلام مباشرة.",
        "logout": "تسجيل الخروج",
        "table_id": "رقم البلاغ",
        "table_name": "الاسم",
        "table_item": "الغرض",
        "table_description": "الوصف",
        "table_date": "التاريخ",
        "table_status": "حالة العثور",
        "table_claim": "حالة الاستلام",
        "status_missing": "مفقود",
        "status_found": "تم العثور عليه",
        "claim_unclaimed": "لم يتم الاستلام",
        "claim_claimed": "تم الاستلام",
        "empty_state": "لا توجد بلاغات مسجلة حالياً.",
    },
    "en": {
        "default_title": "Lost and Found Platform",
        "brand": "Airport Lost & Found",
        "brand_subtitle": "Passenger Services",
        "nav_report": "Report",
        "nav_search": "Search",
        "nav_admin": "Admin",
        "language_label": "العربية",
        "footer_brand": "Airport Lost & Found Platform",
        "footer_note": "A digital service for organized reports and property recovery",
        "home_title": "Airport Lost & Found",
        "hero_eyebrow": "Passenger Services Center",
        "hero_heading": "Recovering lost items at the airport is now clearer and faster.",
        "hero_text": "A professional platform for submitting reports, tracking item status, and helping staff update results with confidence.",
        "hero_report": "Report Lost Item",
        "hero_track": "Track Report",
        "hero_caption": "Modern lost-and-found desk inside an airport terminal",
        "ticket_report": "Report ID",
        "ticket_review": "Under Review",
        "card_report_title": "Report an Item",
        "card_report_text": "Enter item details and contact information to generate a report number.",
        "card_search_title": "Search by Report ID",
        "card_search_text": "Track the report status and check whether the item has been found.",
        "card_admin_title": "Admin Panel",
        "card_admin_text": "Update item and claim statuses from a clean official dashboard.",
        "trust_1": "Report Intake",
        "trust_2": "Status Tracking",
        "trust_3": "Live Admin Updates",
        "trust_4": "Bilingual Interface",
        "metric_reports": "Structured Reports",
        "metric_tracking": "Clear Tracking",
        "metric_staff": "Staff Dashboard",
        "workflow_title": "How the platform works",
        "workflow_text": "A short organized journey from submitting a report to updating the claim status.",
        "step_1_title": "Submit the report",
        "step_1_text": "Enter item details and a useful description to generate a report number.",
        "step_2_title": "Track the status",
        "step_2_text": "Use the report ID to view the latest recorded update.",
        "step_3_title": "Staff update",
        "step_3_text": "Authorized staff update found and claim statuses from the admin panel.",
        "report_title": "Report Lost Item",
        "report_eyebrow": "New Report",
        "report_heading": "Register a Lost Item",
        "report_text": "Write a clear description to help airport staff match your report with recovered items.",
        "name_label": "Reporter Name",
        "name_placeholder": "Example: Ahmed Mohammed",
        "item_label": "Item Name",
        "item_placeholder": "Example: suitcase, headphones, passport",
        "description_label": "Description",
        "description_placeholder": "Include color, brand, approximate location, and any unique details",
        "submit_report": "Submit Report",
        "back": "Back",
        "tip_title": "Quick Tip",
        "tip_text": "A more precise description improves matching, especially flight number, gate, or waiting area.",
        "search_title": "Search Report",
        "search_eyebrow": "Report Tracking",
        "search_heading": "Search for a Lost Item",
        "search_text": "Enter the report number you received after submission to see the latest recorded status.",
        "report_success": "Your report was submitted successfully. Your report ID:",
        "report_id_label": "Report ID",
        "report_id_placeholder": "Example: 73926",
        "search_button": "Search",
        "details_title": "Report Details",
        "field_id": "Report ID",
        "field_name": "Name",
        "field_item": "Item",
        "field_date": "Report Date",
        "field_description": "Description",
        "field_status": "Found Status",
        "field_claim": "Claim Status",
        "not_found": "No report was found with this number. Check the ID and try again.",
        "keep_id_title": "Keep Your Report ID",
        "keep_id_text": "You will use it to follow up with the airport lost-and-found office or through the platform.",
        "login_title": "Admin Login",
        "login_eyebrow": "Authorized Access",
        "login_heading": "Lost and Found Admin Panel",
        "login_text": "This page is for lost-and-found staff to update report statuses.",
        "password_label": "Password",
        "login_button": "Login",
        "login_error": "Incorrect password",
        "admin_title": "Admin Panel",
        "admin_eyebrow": "Control Panel",
        "admin_heading": "Manage Lost Item Reports",
        "admin_text": "Review submitted reports and update found and claim statuses directly.",
        "logout": "Logout",
        "table_id": "Report ID",
        "table_name": "Name",
        "table_item": "Item",
        "table_description": "Description",
        "table_date": "Date",
        "table_status": "Found Status",
        "table_claim": "Claim Status",
        "status_missing": "Missing",
        "status_found": "Found",
        "claim_unclaimed": "Unclaimed",
        "claim_claimed": "Claimed",
        "empty_state": "No reports have been submitted yet.",
    },
}


def get_locale():
    return session.get("lang", "ar") if session.get("lang") in LANGUAGES else "ar"


def set_current_language(lang="ar"):
    if lang not in LANGUAGES:
        abort(404)
    session["lang"] = lang
    return lang


def localized_status(value):
    t = TRANSLATIONS[get_locale()]
    return t["status_found"] if value == "Found" else t["status_missing"]


def localized_claim(value):
    t = TRANSLATIONS[get_locale()]
    return t["claim_claimed"] if value == "Claimed" else t["claim_unclaimed"]

@app.context_processor
def inject_datetime():
    lang = get_locale()
    other_lang = "en" if lang == "ar" else "ar"
    return dict(
        datetime=datetime,
        TRANSLATIONS=TRANSLATIONS,
        current_lang=lang,
        html_dir="rtl" if lang == "ar" else "ltr",
        other_lang=other_lang,
        t=TRANSLATIONS[lang],
        localized_status=localized_status,
        localized_claim=localized_claim,
    )


@app.route('/')
@app.route('/<lang>')
def index(lang="ar"):
    set_current_language(lang)
    return render_template('index.html')

@app.route('/add_lost', methods=['GET', 'POST'])
def add_lost():
    if request.method == 'POST':
        name = request.form['name']
        item_name = request.form['item_name']
        description = request.form['description']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Missing"
        claim_status = "Unclaimed"
        report_id = random.randint(10000, 99999)

        item = {
            'id': report_id,
            'name': name,
            'item_name': item_name,
            'description': description,
            'date': date,
            'status': status,
            'claim_status': claim_status
        }
        items.append(item)
        return render_template('search.html', report_id=report_id, searched=False)
    return render_template('add_lost.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    found_item = None
    searched = False
    if request.method == 'POST':
        searched = True
        report_id = request.form['report_id']
        for item in items:
            if str(item['id']) == report_id:
                found_item = item
                break
    return render_template('search.html', item=found_item, searched=searched)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return render_template('login.html', error=TRANSLATIONS[get_locale()]["login_error"])
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin_panel.html', items=items)

@app.route('/update_status/<int:item_id>', methods=['POST'])
def update_status(item_id):
    for item in items:
        if item['id'] == item_id:
            item['status'] = request.form['status']
    return redirect(url_for('admin_panel'))

@app.route('/update_claim/<int:item_id>', methods=['POST'])
def update_claim(item_id):
    for item in items:
        if item['id'] == item_id:
            item['claim_status'] = request.form['claim_status']
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
