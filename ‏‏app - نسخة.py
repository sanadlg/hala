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
@app.route('/')
def home():
    return render_template('home.html')

# 🚀 تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True, port=8080)
