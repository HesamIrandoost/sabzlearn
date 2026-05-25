# run.py - در ریشه پروژه قرار بده
import os
import subprocess
import sys
import webbrowser
from threading import Timer

def run_command(command):
    """اجرای دستور در ترمینال"""
    process = subprocess.Popen(command, shell=True)
    process.wait()

def open_browser():
    """باز کردن مرورگر بعد از 2 ثانیه"""
    Timer(2, lambda: webbrowser.open('http://127.0.0.1:8000')).start()

def main():
    print("=" * 50)
    print("   سبزلرن - آکادمی برنامه‌نویسی")
    print("=" * 50)
    
    # چک کردن پایتون
    if sys.version_info < (3, 8):
        print("❌ پایتون 3.8 یا بالاتر نیاز است!")
        sys.exit(1)
    
    # ایجاد محیط مجازی
    if not os.path.exists("venv"):
        print("📦 ایجاد محیط مجازی...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # فعالسازی محیط مجازی
    if sys.platform == "win32":
        activate_script = "venv\\Scripts\\activate"
        python_path = "venv\\Scripts\\python"
    else:
        activate_script = "venv/bin/activate"
        python_path = "venv/bin/python"
    
    # نصب پیش‌نیازها
    if not os.path.exists("installed.txt"):
        print("📥 نصب کتابخانه‌ها...")
        subprocess.run([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        with open("installed.txt", "w") as f:
            f.write("installed")
    
    # مایگریشن
    print("🔄 بروزرسانی دیتابیس...")
    subprocess.run([python_path, "manage.py", "makemigrations"])
    subprocess.run([python_path, "manage.py", "migrate"])
    
    # استاتیک فایل
    print("📁 جمع‌آوری فایل‌های استاتیک...")
    subprocess.run([python_path, "manage.py", "collectstatic", "--noinput"])
    
    # اجرای سرور
    print("\n" + "=" * 50)
    print("✅ سرور در حال اجراست...")
    print("🌐 آدرس: http://127.0.0.1:8000")
    print("🛑 برای خروج Ctrl+C رو بزن")
    print("=" * 50 + "\n")
    
    open_browser()
    subprocess.run([python_path, "manage.py", "runserver"])

if __name__ == "__main__":
    main()
