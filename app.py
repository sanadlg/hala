from flask import Flask, request, render_template, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ تعريف app
app = Flask(__name__)

# 🔐 إعداد الوصول إلى Google Sheets
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(credentials)

# فتح جداول البيانات
sheet = client.open("Employee and Chef Data")
employee_sheet = sheet.worksheet("Employees")
chef_sheet = sheet.worksheet("Chefs")
receipts_sheet = sheet.worksheet("Receipts")  
admins_sheet = sheet.worksheet("admins")
ma_sheet = sheet.worksheet("ma") 

# مثال لصفحة رئيسية
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        admin_password = request.form['admin_password']
        admins_data = admins_sheet.get_all_records()
        for admin in admins_data:
            if admin['اسم المشرف'] == admin_name and admin['كلمة المرور'] == admin_password:
                # جلب الشيفات المرتبطين بالمشرف
                chef_list = admin['الشيفات'].replace(",", ".").split(".")
                return render_template('admin_dashboard.html', admin_name=admin_name, chef_list=chef_list)
        return "❌ اسم المستخدم أو كلمة المرور غير صحيحة."
    return render_template('admin_login.html')
@app.route('/store_manager', methods=['GET', 'POST'])
def store_manager():
    if request.method == 'POST':
        manager_name = request.form['manager_name']
        manager_password = request.form['manager_password']
        admins_data = admins_sheet.get_all_records()
        for admin in admins_data:
            if admin['اسم المشرف'] == manager_name and admin['كلمة المرور'] == manager_password:
                records = receipts_sheet.get_all_records()
                pending_items = {}
                for record in records:
                    chef_name = record['اسم الشيف']
                    delivered_quantity = int(record['الكمية المسلّمة'])
                    received_quantity = int(record['الكمية المستلمة'])
                    if delivered_quantity > received_quantity:
                        if chef_name not in pending_items:
                            pending_items[chef_name] = []
                        pending_items[chef_name].append({
                            'الصنف': record['الصنف'],
                            'باقي': delivered_quantity - received_quantity
                        })
                return render_template('store_manager.html', pending_items=pending_items)
    return render_template('store_manager_form.html')
@app.route('/hours', methods=['GET', 'POST'])
def hours():
    if request.method == 'POST':
        fingerprint = request.form['fingerprint']
        records = employee_sheet.get_all_records()
        for record in records:
            if str(record['رقم البصمة']) == fingerprint:
                return render_template('hours.html', record=record)
        return "❌ رقم البصمة غير موجود."
    return render_template('hours_form.html')
@app.route('/')
def home():
    return render_template('home.html')

# 🚀 تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True, port=8080)
