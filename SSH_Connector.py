# app_exact_updated.py
# UI matching your mockup exactly (with green box removed & buttons aligned)
# Run: python app_exact_updated.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import threading

# paramiko is optional — detect at runtime and show helpful message if missing
try:
    import paramiko
except Exception:
    paramiko = None

# ---------------- PLACEHOLDER HELPERS ----------------
def set_placeholder(entry: tk.Entry, placeholder: str, is_password=False):
    entry.placeholder = placeholder
    entry.insert(0, placeholder)
    entry.is_password_field = is_password
    entry.bind("<FocusIn>", lambda e: _clear_placeholder(entry))
    entry.bind("<FocusOut>", lambda e: _add_placeholder(entry))

def _clear_placeholder(entry):
    if entry.get() == entry.placeholder:
        entry.delete(0, "end")
        if entry.is_password_field:
            entry.config(show="*")

def _add_placeholder(entry):
    if not entry.get():
        if entry.is_password_field:
            entry.config(show="")
        entry.insert(0, entry.placeholder)

# ---------------- MAIN APP ----------------
class ExactApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Config Limit Application")
        self.configure(bg="#e6e6e6")
        self.geometry("420x500")
        self.resizable(False, False)

        # Fonts matching your mockup
        heading_font = ("Arial", 16, "bold")
        sub_font = ("Courier", 10)
        desc_font = ("Courier", 8)
        label_font = ("Courier", 10, "bold")
        entry_font = ("Courier", 10)

        # -------- OUTER PANEL --------
        panel = tk.Frame(self, bg="#e6e6e6", bd=1, relief="flat")
        panel.place(x=12, y=12, width=396, height=476)

        # -------- TITLE --------
        title_label = tk.Label(panel, text="HPE MSA", font=heading_font, bg="#e6e6e6", anchor="w")
        title_label.place(x=20, y=12)

        # Subtitle
        subtitle_label = tk.Label(panel, text="Config Limit Application", font=sub_font, bg="#e6e6e6")
        subtitle_label.place(x=20, y=40)

        # Divider strip
        divider = tk.Frame(panel, bg="#e6e6e6", height=14)
        divider.place(x=10, y=80, width=396)

        # -------- DESCRIPTION BOX --------
        desc_bg = tk.Frame(panel, bg="#e6e6e6")
        desc_bg.place(x=10, y=80, width=356, height=80)

        desc_text = (
            "HPE MSA Config Limits is a lightweight desktop\n"
            "tool designed to connect to an HPE MSA storage\n"
            "array via SSH and display or validate\n"
            "configuration limits."
        )

        desc_label = tk.Label(desc_bg, text=desc_text, font=desc_font, bg="#e6e6e6", justify="left")
        desc_label.place(x=8, y=8)

        # -------- SOFTWARE VERSION BOX --------
        version_bg = tk.Frame(panel, bg="#e6e6e6")
        version_bg.place(x=10, y=170, width=200, height=32)

        version_label = tk.Label(version_bg, text="Software Version:  v1.0",
                                 font=("Courier", 8), bg="#e6e6e6")
        version_label.place(x=8, y=6)

        # -------- CREDENTIALS SECTION --------
        cred_bg = tk.Frame(panel, bg="#e9e9e9", bd=1, relief="flat")
        cred_bg.place(x=20, y=240, width=356, height=160)

        lbl_x = 24
        val_x = 170
        row_y = 36
        gap  = 32

        # ARRAY IP
        tk.Label(cred_bg, text="ARRAY IP", font=label_font, bg="#e6e9e9").place(x=lbl_x, y=row_y)
        self.ip_entry = tk.Entry(cred_bg, width=22, font=entry_font, bd=1, relief="flat")
        self.ip_entry.place(x=val_x, y=row_y - 4)
        set_placeholder(self.ip_entry, "Enter Array IP")

        # USERNAME
        tk.Label(cred_bg, text="USERNAME", font=label_font, bg="#e6e9e9").place(x=lbl_x, y=row_y + gap)
        self.username_entry = tk.Entry(cred_bg, width=22, font=entry_font, bd=1, relief="flat")
        self.username_entry.place(x=val_x, y=row_y + gap - 4)
        set_placeholder(self.username_entry, "Enter Username")

        # PASSWORD
        tk.Label(cred_bg, text="PASSWORD", font=label_font, bg="#e6e9e9").place(x=lbl_x, y=row_y + 2*gap)
        self.pw_entry = tk.Entry(cred_bg, width=22, font=entry_font, bd=1, relief="flat", show="")
        self.pw_entry.place(x=val_x, y=row_y + 2*gap - 4)
        set_placeholder(self.pw_entry, "Enter Password", True)

        # ---- PASSWORD TOGGLE BUTTON ----
        self.show_pw = False  # track state

        def toggle_password():
            if self.show_pw:
                self.pw_entry.config(show="*")    # hide password
                toggle_btn.config(text="👁")      # eye icon
                self.show_pw = False
            else:
                self.pw_entry.config(show="")     # show password
                toggle_btn.config(text="👁‍🗨")    # crossed-eye icon
                self.show_pw = True

        # small toggle button beside password field
        toggle_btn = tk.Button(
            cred_bg,
            text="👁",          # eye icon
            font=("Arial", 9),
            relief="flat",
            bg="#e9e9e9",
            activebackground="#e9e9e9",
            command=toggle_password
        )
        toggle_btn.place(x=328, y=row_y + 2*gap - 6)

        # -------- BUTTONS (CENTERED PERFECTLY) --------
        btn_frame = tk.Frame(cred_bg, bg="#e6e6e6")
        btn_frame.place(x=150, y=135, width=356)

        btn_login = tk.Button(btn_frame, text="Login",
                              bg="#3b73c7", fg="white",
                              activebackground="#2e5fa3",
                              font=("Arial", 10, "bold"),
                              bd=0, relief="raised",
                              command=self._on_login)

        btn_close = tk.Button(btn_frame, text="Close",
                              bg="#3b73c7", fg="white",
                              activebackground="#2e5fa3",
                              font=("Arial", 10, "bold"),
                              bd=0, relief="raised",
                              command=self._on_close)

        # store for later (disable/enable) - no layout change
        self.btn_login = btn_login
        self.btn_close = btn_close

        # Center the pair
        btn_login.pack(side="left", padx=(90, 10))
        btn_close.pack(side="left", padx=10)

        # -------- FOOTER --------
        footer = tk.Label(panel, text="In development by RishuRaj - 2025",
                          font=("Courier", 6), bg="#e6e6e6")
        footer.place(x=20, y=450)

        # Keyboard shortcuts
        self.bind("<Return>", lambda e: self._on_login())
        self.bind("<Escape>", lambda e: self._on_close())

        # keep references for use in methods
        self._cred_bg = cred_bg

    # ---------------- BUTTON ACTIONS ----------------
    def _on_login(self):
        ip = self.ip_entry.get().strip()
        username = self.username_entry.get().strip()
        pw = self.pw_entry.get().strip()

        # handle placeholders
        if ip == "Enter Array IP" or ip == "Enter Array IP": ip = ""
        if username == "Enter Username" or username == "ENTER USERNAME": username = ""
        if pw == "ENTER PASSWORD" or pw == "Enter Password": pw = ""

        port = 22   # Default SSH port

        missing = []
        if not ip: missing.append("Array IP")
        if not username: missing.append("Username")
        if not pw: missing.append("Password")

        if missing:
            messagebox.showerror("Missing Information", "Please enter: " + ", ".join(missing))
            return

        # Disable UI controls while connecting
        self._set_controls_state("disabled")

        # Show modal loading dialog
        loading = self._show_loading_modal("Connecting", f"Connecting to {ip}:{port} ...")

        # Start background thread to attempt SSH connection
        t = threading.Thread(target=self._connect_thread,
                             args=(ip, username, pw, port, loading),
                             daemon=True)
        t.start()

    # ---------------- helpers for SSH + UI ----------------
    def _set_controls_state(self, state):
        # disable/enable inputs & buttons
        widgets = [self.ip_entry, self.username_entry, self.pw_entry, getattr(self, "btn_login", None), getattr(self, "btn_close", None)]
        for w in widgets:
            if w is None:
                continue
            try:
                w.config(state=state)
            except Exception:
                try:
                    if state == "disabled":
                        w.config(state="disabled")
                    else:
                        w.config(state="normal")
                except Exception:
                    pass

    def _show_loading_modal(self, title, message):
        # create a modal Toplevel with an indeterminate progress bar
        top = tk.Toplevel(self)
        top.title(title)
        top.geometry("300x100")
        top.resizable(False, False)
        top.transient(self)
        top.grab_set()

        lbl = tk.Label(top, text=message, font=("Segoe UI", 10))
        lbl.pack(pady=(12, 6))

        pb = ttk.Progressbar(top, mode="indeterminate")
        pb.pack(fill="x", padx=20, pady=(4, 12))
        pb.start(10)  # speed of animation

        # center modal relative to main window
        self._center_window(top, 300, 100)
        return {"top": top, "progress": pb}

    def _connect_thread(self, ip, username, pw, port, loading):
        # background SSH connect (uses paramiko). On finish, schedule UI update via self.after()
        result = {"success": False, "message": "", "output": ""}
        if paramiko is None:
            result["message"] = "Paramiko not installed. Install with: pip install paramiko"
            self.after(0, lambda: self._connect_finished(result, loading))
            return

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port=port, username=username, password=pw, timeout=10)
            # run a simple command to verify shell (non-interactive)
            stdin, stdout, stderr = client.exec_command("echo Connected")
            out = stdout.read().decode(errors="ignore").strip()
            err = stderr.read().decode(errors="ignore").strip()
            result["success"] = True
            result["message"] = "Connected successfully."
            result["output"] = out or err
            client.close()
        except Exception as e:
            result["message"] = f"Connection failed: {e}"
        finally:
            # ensure UI updated on main thread
            self.after(0, lambda: self._connect_finished(result, loading))

    def _connect_finished(self, result, loading):
        # close loading modal
        try:
            loading["progress"].stop()
            loading["top"].grab_release()
            loading["top"].destroy()
        except Exception:
            pass

        # re-enable controls
        self._set_controls_state("normal")

        if result.get("success"):
            messagebox.showinfo("SSH Connected", f"{result.get('message')}\n\nOutput: {result.get('output')}")
            # TODO: navigate to next page or show connection details
        else:
            messagebox.showerror("SSH Error", result.get("message"))

    def _center_window(self, w, width, height):
        # center window 'w' relative to this root (self)
        self.update_idletasks()
        sx = self.winfo_x()
        sy = self.winfo_y()
        sw = self.winfo_width()
        sh = self.winfo_height()
        x = sx + (sw - width)//2
        y = sy + (sh - height)//2
        w.geometry(f"{width}x{height}+{x}+{y}")

    def _on_close(self):
        self.quit()
        self.destroy()
        sys.exit(0)


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = ExactApp()
    app.mainloop()
