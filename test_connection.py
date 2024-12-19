import pyodbc

# اطلاعات اتصال به SQL Server
server = 'DESKTOP-IVK08VE\\SQLEXPRESS'  # نام سرور یا localhost\SQLEXPRESS
database = 'my_database'  # نام پایگاه داده
username = 'rah'  # نام کاربری
password = '123'  # رمز عبور

# ساخت رشته اتصال
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# اتصال به SQL Server
try:
    connection = pyodbc.connect(connection_string)
    print("اتصال به SQL Server موفقیت‌آمیز بود!")

    # ایجاد یک cursor برای اجرای دستورات SQL
    cursor = connection.cursor()

    # اجرای یک دستور SQL ساده
    cursor.execute("SELECT 1")  # دستور ساده برای تست اتصال
    result = cursor.fetchone()
    
    # نمایش نتیجه
    print("نتیجه تست اتصال:", result)

except pyodbc.Error as e:
    print(f"اتصال به SQL Server شکست خورد: {e}")
