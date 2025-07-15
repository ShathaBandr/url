import pyperclip
import pyshorteners
from tkinter import *
from tkinter import ttk, messagebox
import webbrowser
import validators
import threading

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("مختصر الروابط")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f7fa")

        main_frame = Frame(self.root, bg="#f5f7fa")
        main_frame.pack(expand=True)

        title_frame = Frame(main_frame, bg="#4a6baf")
        title_frame.pack(fill=X, padx=10, pady=(10, 20))

        self.title_label = Label(title_frame,
                                 text="مختصر الروابط",
                                 font=("Helvetica", 20, "bold"),
                                 fg="white",
                                 bg="#4a6baf")
        self.title_label.pack(pady=15)

        input_frame = Frame(main_frame, bg="#f5f7fa")
        input_frame.pack(pady=(0, 20))

        Label(input_frame,
              text="أدخل الرابط الكامل هنا:",
              font=("Helvetica", 12),
              bg="#f5f7fa",
              anchor="e", justify="right").pack(anchor="e", pady=(0, 5))

        self.url_entry = ttk.Entry(input_frame,
                                   font=("Helvetica", 12),
                                   width=50,
                                   justify="right")
        self.url_entry.pack(pady=5, ipady=8)

        options_frame = Frame(main_frame, bg="#f5f7fa")
        options_frame.pack(pady=10)

        Label(options_frame,
              text="اختر خدمة الاختصار:",
              font=("Helvetica", 12),
              bg="#f5f7fa",
              anchor="e", justify="right").grid(row=0, column=0, padx=5, sticky="e")

        self.service_var = StringVar(value="tinyurl")
        services = [("TinyURL", "tinyurl"),
                    ("Is.gd", "isgd")]

        for i, (text, val) in enumerate(services):
            Radiobutton(options_frame,
                        text=text,
                        variable=self.service_var,
                        value=val,
                        bg="#f5f7fa",
                        font=("Helvetica", 10)).grid(row=0, column=i+1, padx=5)

        self.shorten_btn = ttk.Button(main_frame,
                                      text="اختصر الرابط",
                                      command=self.start_shortening,
                                      style="BlackText.TButton",
                                      )
        self.shorten_btn.pack(pady=15)

        self.progress = ttk.Progressbar(main_frame,
                                        orient=HORIZONTAL,
                                        length=300,
                                        mode='indeterminate')

        result_frame = Frame(main_frame, bg="#f5f7fa")
        result_frame.pack(pady=(20, 10))

        Label(result_frame,
              text="الرابط المختصر:",
              font=("Helvetica", 12),
              bg="#f5f7fa",
              anchor="e", justify="right").pack(anchor="e")

        self.result_entry = ttk.Entry(result_frame,
                                      font=("Helvetica", 12),
                                      width=50,
                                      state="readonly",
                                      justify="right")
        self.result_entry.pack(pady=5, ipady=8)

        btn_frame = Frame(main_frame, bg="#f5f7fa")
        btn_frame.pack(pady=15)

        self.copy_btn = ttk.Button(btn_frame,
                                   text="نسخ الرابط",
                                   command=self.copy_url,
                                   state=DISABLED)
        self.copy_btn.grid(row=0, column=0, padx=10)

        self.open_btn = ttk.Button(btn_frame,
                                   text="فتح الرابط",
                                   command=self.open_url,
                                   state=DISABLED)
        self.open_btn.grid(row=0, column=1, padx=10)

        self.status_var = StringVar()
        self.status_bar = Label(main_frame,
                                textvariable=self.status_var,
                                font=("Helvetica", 10),
                                fg="#666666",
                                bg="#f5f7fa",
                                anchor="e", justify="right")
        self.status_bar.pack(side=BOTTOM, fill=X, pady=(0, 10))

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("Accent.TButton",
                        font=("Helvetica", 12, "bold"),
                        background="#4a6baf",
                        foreground="white")
        style.map("Accent.TButton",
                  background=[("active", "#3a5a9f")])
        style.configure("TEntry", padding=10)

    def start_shortening(self):
        url = self.url_entry.get().strip()
        if not validators.url(url):
            messagebox.showerror("خطأ", "الرجاء إدخال رابط صحيح")
            return

        self.progress.pack()
        self.progress.start()
        self.shorten_btn.config(state=DISABLED)
        self.status_var.set("جاري اختصار الرابط...")

        threading.Thread(target=self.shorten_url, args=(url,), daemon=True).start()

    def shorten_url(self, url):
        try:
            service = self.service_var.get()
            shortener = pyshorteners.Shortener()
            if service == "tinyurl":
                short_url = shortener.tinyurl.short(url)
            elif service == "isgd":
                short_url = shortener.isgd.short(url)
            else:
                short_url = shortener.tinyurl.short(url)
            self.root.after(0, self.show_result, short_url)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def show_result(self, short_url):
        self.progress.stop()
        self.progress.pack_forget()
        self.result_entry.config(state=NORMAL)
        self.result_entry.delete(0, END)
        self.result_entry.insert(0, short_url)
        self.result_entry.config(state="readonly")
        self.copy_btn.config(state=NORMAL)
        self.open_btn.config(state=NORMAL)
        self.shorten_btn.config(state=NORMAL)
        self.status_var.set("تم اختصار الرابط بنجاح")

    def show_error(self, error_msg):
        self.progress.stop()
        self.progress.pack_forget()
        self.shorten_btn.config(state=NORMAL)
        messagebox.showerror("خطأ", f"فشل في اختصار الرابط:\n{error_msg}")
        self.status_var.set("حدث خطأ أثناء اختصار الرابط")

    def copy_url(self):
        short_url = self.result_entry.get()
        if short_url:
            pyperclip.copy(short_url)
            self.status_var.set("تم نسخ الرابط إلى الحافظة")
            messagebox.showinfo("تم النسخ", "تم نسخ الرابط المختصر بنجاح")

    def open_url(self):
        short_url = self.result_entry.get()
        if short_url:
            webbrowser.open(short_url)

if __name__ == "__main__":
    root = Tk()
    app = URLShortenerApp(root)
    root.mainloop()
