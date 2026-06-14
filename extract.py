import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox


# =========================
# SCORE CALCULATION
# =========================
def calculate_score(position, ctr, impressions):

    pos_score = max(0, 30 - position) / 22 * 40
    imp_score = min(impressions, 10000) / 10000 * 35

    ctr_gap = max(0, 5 - ctr)
    ctr_score = (ctr_gap / 5) * 25

    total = pos_score + imp_score + ctr_score

    return min(round(total), 100)


# =========================
# SEO ANALYSIS ENGINE
# =========================
def analyze_page(position, ctr, impressions):

    score = calculate_score(position, ctr, impressions)

    # QUICK WIN
    if position <= 12 and ctr < 3:

        return f"""
Opportunity Score: {score}/100

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
2 تا 6 هفته
"""

    # CTR PROBLEM
    elif position <= 15:

        return f"""
Opportunity Score: {score}/100

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
2 تا 4 هفته
"""

    # CONTENT GAP
    elif position <= 20:

        return f"""
Opportunity Score: {score}/100

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
1 تا 3 ماه
"""

    # AUTHORITY GAP
    else:

        return f"""
Opportunity Score: {score}/100

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
2 تا 4 ماه
"""


# =========================
# MAIN APP CLASS
# =========================
class GSCApp:

    def __init__(self, root):

        self.root = root
        self.root.title("GSC SEO Opportunity Analyzer| BY M.Hossein Rahimloo")
        self.root.geometry("1150x650")

        self.data = None

        # Buttons
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Upload CSV", command=self.load_csv, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Export Excel", command=self.export_excel, width=20).pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(root, text="No file loaded")
        self.label.pack()

        # Table
        columns = ("URL", "Clicks", "Impressions", "CTR", "Position")

        self.tree = ttk.Treeview(root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Double click event
        self.tree.bind("<Double-1>", self.on_click)

    # =========================
    # LOAD CSV
    # =========================
    def load_csv(self):

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

        if not file_path:
            return

        try:
            df = pd.read_csv(file_path)

            df.columns = [c.strip() for c in df.columns]

            required = ["Top pages", "Clicks", "Impressions", "CTR", "Position"]

            for col in required:
                if col not in df.columns:
                    messagebox.showerror("Error", f"Missing column: {col}")
                    return

            # Clean CTR
            df["CTR"] = df["CTR"].astype(str).str.replace("%", "").astype(float)
            df["Position"] = pd.to_numeric(df["Position"], errors="coerce")
            df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce")
            df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce")

            # Filter
            df = df[
                (df["Position"] >= 8) &
                (df["Position"] <= 30) &
                (df["Impressions"] >= 100) &
                (df["CTR"] <= 5)
            ]

            df = df.sort_values("Impressions", ascending=False).head(50)

            self.data = df

            self.tree.delete(*self.tree.get_children())

            for _, row in df.iterrows():

                self.tree.insert("", "end", values=(
                    row["Top pages"],
                    int(row["Clicks"]),
                    int(row["Impressions"]),
                    f"{row['CTR']}%",
                    round(row["Position"], 2)
                ))

            self.label.config(text=f"Loaded: {len(df)} rows")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =========================
    # ANALYSIS POPUP
    # =========================
    def on_click(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected, "values")

        url = values[0]
        clicks = float(values[1])
        impressions = float(values[2])
        ctr = float(values[3].replace("%", ""))
        position = float(values[4])

        analysis = analyze_page(position, ctr, impressions)

        messagebox.showinfo(f"SEO Analysis\n{url}", analysis)

    # =========================
    # EXPORT
    # =========================
    def export_excel(self):

        if self.data is None or self.data.empty:
            messagebox.showwarning("Warning", "No data to export")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

        if not file_path:
            return

        try:
            self.data.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Export done successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = GSCApp(root)
    root.mainloop()