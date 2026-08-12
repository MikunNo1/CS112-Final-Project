
import tkinter as tk
from tkinter import messagebox
from database_program import init_db, add_user, authenticate_user

init_db()


class LoginApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Login Form")
        self.geometry("350x400")
        self.config(bg="#f0f0f0")
        self.resizable(False, False)

        # --- state variables ---
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)
        self.remember_me = tk.BooleanVar()
        self.current_user = None

        # --- widgets (all widget creation lives here in __init__) ---
        tk.Label(self, text="Login", font=("Arial", 19, "bold"), fg="blue").pack(pady=10)

        tk.Label(self, text="Username", fg="white").pack(anchor='w', padx=30)
        tk.Entry(self, textvariable=self.username, width=30).pack(pady=2)

        tk.Label(self, text="password", fg='blue').pack(anchor='w', padx=30)
        self.password_entry = tk.Entry(self, textvariable=self.password, show="*", width=30)
        self.password_entry.pack(pady=2)

        toogle_button = tk.Checkbutton(
            self, text='show password', variable=self.show_password,
            fg='blue', command=self.toggle_password
        )
        toogle_button.pack(anchor='w', pady=30, padx=30)

        remember_me_button = tk.Checkbutton(
            self, text='remember me', variable=self.remember_me, fg='blue'
        )
        remember_me_button.pack(anchor='w', padx=30)

        tk.Button(
            self, text='Login', command=self.login, width=25, bg='#4caf50', fg='blue'
        ).pack(pady=8)
        tk.Button(
            self, text='Register', command=self.register, width=25, bg='#4caf50', fg='blue'
        ).pack()

    # --- methods (these only run later, when triggered) ---
    def login(self):
        user_input = self.username.get()
        user_password = self.password.get()
        auth = authenticate_user(user_input, user_password)

        if auth:
            user_id, role = auth
            self.current_user = {
                "user_id": user_id,
                "username": user_input,
                "role": role
            }
            self.route_dashboard()
        else:
            messagebox.showerror("unsuccessful", "invalid username or password")

    def register(self):
        user_input = self.username.get()
        user_password = self.password.get()
        # since we are just recording new data there's no need to unpack
        if add_user(user_input, user_password):
            messagebox.showinfo("success", "succesful _registration")
        else:
            messagebox.showinfo("unsuccess", "username alread exist")

    def toggle_password(self):
        if self.show_password.get():  # if the checkbox is ticked, show the password
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def route_dashboard(self):
        # placeholder for now — we'll build this out next
        messagebox.showinfo("Logged in", f"Welcome, role: {self.current_user['role']}")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
