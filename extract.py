import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


def calculate_score(position, ctr, impressions):
    pos_score = max(0, 30 - position) / 22 * 40
    imp_score = min(impressions, 10000) / 10000 * 35
    ctr_gap = max(0, 5 - ctr)
    ctr_score = (ctr_gap / 5) * 25
    total = pos_score + imp_score + ctr_score
    return min(round(total), 100)


def analyze_page(position, ctr, impressions):
    score = calculate_score(position, ctr, impressions)

    if position <= 12 and ctr < 3:
        return f"""Opportunity Score: {score}/100

نوع فرصت:
Quick Win

اولویت:
فوری ⭐⭐⭐⭐⭐

تحلیل:
این صفحه در آستانه ورود به صفحه اول گوگل است
اما نرخ کلیک پایین باعث از دست رفتن ترافیک شده است.

مشکل اصلی:
CTR پایین نسبت به Position

اقدامات پیشنهادی:
1- بازنویسی Title
2- بهبود Meta Description
3- افزودن FAQ
4- استفاده از عدد در Title
5- لینک‌سازی داخلی هدفمند

اثر مورد انتظار:
20% تا 50% افزایش کلیک

زمان اثر:
2 تا 6 هفته"""

    elif position <= 15:
        return f"""Opportunity Score: {score}/100

نوع فرصت:
CTR Problem

اولویت:
بالا

تحلیل:
رتبه مناسب است اما نرخ کلیک ضعیف است.

مشکل اصلی:
Snippet ضعیف یا Title غیر جذاب

اقدامات پیشنهادی:
1- بازنویسی Title
2- تست A/B عنوان
3- استفاده از کلمات جذاب
4- اضافه کردن سال یا عدد

اثر مورد انتظار:
15% تا 35% افزایش CTR

زمان اثر:
2 تا 4 هفته"""

    elif position <= 20:
        return f"""Opportunity Score: {score}/100

نوع فرصت:
Content Gap

اولویت:
متوسط

تحلیل:
صفحه برای رقابت با Top 10 نیاز به توسعه محتوا دارد.

مشکل اصلی:
کمبود عمق محتوا

اقدامات پیشنهادی:
1- افزایش طول محتوا
2- افزودن H2 های جدید
3- پاسخ کامل‌تر به Intent
4- لینک‌سازی داخلی

اثر مورد انتظار:
10% تا 25% رشد رتبه

زمان اثر:
1 تا 3 ماه"""

    else:
        return f"""Opportunity Score: {score}/100

نوع فرصت:
Authority Gap

اولویت:
متوسط تا پایین

تحلیل:
صفحه برای رقابت نیاز به سیگنال‌های قدرت دارد.

مشکل اصلی:
ضعف در اعتبار صفحه نسبت به رقبا

اقدامات پیشنهادی:
1- دریافت بک‌لینک
2- تقویت لینک داخلی
3- بهبود EEAT
4- بروزرسانی محتوا

اثر مورد انتظار:
10% تا 20% رشد

زمان اثر:
2 تا 4 ماه"""


class GSCApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GSC SEO Opportunity Analyzer | BY M.Hossein Rahimloo")
        self.root.geometry("1150x650")
        self.data = None

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Upload CSV", command=self.load_csv, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Export Excel", command=self.export_excel, width=20).pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(root, text="No file loaded")
        self.label.pack()

        columns = ("URL", "Clicks", "Impressions", "CTR", "Position")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_click)
        version_label = tk.Label(root, text="v1.0.1", fg="gray", font=("Arial", 8))
        version_label.pack(side=tk.BOTTOM, anchor=tk.E, padx=10, pady=5)

    def load_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".csv"):
            messagebox.showerror(
                "فرمت اشتباه",
                "فایل انتخابی CSV نیست.\nلطفاً فایل خروجی Google Search Console را با فرمت CSV وارد کنید."
            )
            return

        # try different encodings because GSC files vary
        df = None
        for enc in ("utf-8-sig", "utf-8", "cp1256", "latin-1"):
            try:
                df = pd.read_csv(file_path, encoding=enc)
                break
            except (UnicodeDecodeError, Exception):
                continue

        if df is None:
            messagebox.showerror(
                "خطای خواندن فایل",
                "فایل قابل خواندن نیست.\nممکن است فایل خراب باشد یا encoding آن پشتیبانی نشود."
            )
            return

        if df.empty:
            messagebox.showwarning("فایل خالی", "فایل CSV هیچ داده‌ای ندارد.")
            return

        df.columns = [c.strip() for c in df.columns]

        required = ["Top pages", "Clicks", "Impressions", "CTR", "Position"]
        missing = [col for col in required if col not in df.columns]
        if missing:
            messagebox.showerror(
                "ستون‌های مفقود",
                f"این ستون‌ها در فایل پیدا نشدند:\n{', '.join(missing)}\n\n"
                f"ستون‌های موجود در فایل:\n{', '.join(df.columns.tolist())}"
            )
            return

        try:
            df["CTR"] = df["CTR"].astype(str).str.replace("%", "").str.strip().astype(float)
            if df["CTR"].max() <= 1:
                df["CTR"] = df["CTR"] * 100
        except Exception:
            messagebox.showerror("خطای CTR", "مقادیر ستون CTR قابل پردازش نیستند.\nمطمئن شوید فایل خروجی مستقیم Google Search Console است.")
            return

        try:
            df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
            df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce")
            df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce")
        except Exception:
            messagebox.showerror("خطای داده", "تبدیل مقادیر عددی با مشکل روبرو شد.")
            return

        nan_count = df[["Position", "Impressions", "Clicks", "CTR"]].isna().any(axis=1).sum()
        if nan_count > 0:
            df = df.dropna(subset=["Position", "Impressions", "Clicks", "CTR"])

        bad_rows = df[(df["Impressions"] < 0) | (df["Clicks"] < 0) | (df["Position"] <= 0)]
        if not bad_rows.empty:
            df = df.drop(bad_rows.index)

        df = df[
            (df["Position"] >= 8) &
            (df["Position"] <= 30) &
            (df["Impressions"] >= 10) &
            (df["CTR"] <= 5)
        ]

        if df.empty:
            messagebox.showinfo(
                "نتیجه‌ای پیدا نشد",
                "هیچ صفحه‌ای با شرایط تحلیل پیدا نشد.\n\n"
                "دلایل احتمالی:\n"
                "- بازه زمانی انتخابی در GSC خیلی کوتاه است\n"
                "- سایت جدید است و داده کافی ندارد\n"
                "- فیلترهای اعمال شده در GSC نتایج را محدود کرده‌اند\n\n"
                "پیشنهاد: بازه زمانی را به ۳ ماه یا بیشتر تغییر دهید."
            )
            return

        df = df.sort_values("Impressions", ascending=False).head(50)
        self.data = df

        self.tree.delete(*self.tree.get_children())

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(
                row["Top pages"],
                int(row["Clicks"]),
                int(row["Impressions"]),
                f"{round(row['CTR'], 2)}%",
                round(row["Position"], 2)
            ))

        self.label.config(text=f"Loaded: {len(df)} rows")

    def on_click(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")

        try:
            url = values[0]
            clicks = float(values[1])
            impressions = float(values[2])
            ctr = float(values[3].replace("%", ""))
            position = float(values[4])
        except (ValueError, IndexError):
            messagebox.showerror("خطا", "اطلاعات این ردیف قابل پردازش نیست.")
            return

        analysis = analyze_page(position, ctr, impressions)
        messagebox.showinfo(f"SEO Analysis\n{url}", analysis)

    def export_excel(self):
        if self.data is None or self.data.empty:
            messagebox.showwarning("داده‌ای وجود ندارد", "ابتدا یک فایل CSV بارگذاری کنید.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if not file_path:
            return

        try:
            self.data.to_excel(file_path, index=False)
            messagebox.showinfo("موفق", "فایل Excel با موفقیت ذخیره شد.")
        except PermissionError:
            messagebox.showerror(
                "خطای دسترسی",
                "فایل در جای دیگری باز است.\nلطفاً آن را ببندید و دوباره امتحان کنید."
            )
        except Exception as e:
            messagebox.showerror("خطا", f"ذخیره‌سازی با مشکل روبرو شد:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GSCApp(root)
    root.mainloop()
