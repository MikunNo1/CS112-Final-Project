import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database_program import add_outage, init_db, add_user, authenticate_user,add_complaint,get_substations,get_open_outages,get_technician,assign_work_order,get_technician_work_orders ,mark_work_order_complete

init_db()


class LoginApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Login Form")
        self.geometry("1500x800")
        self.config(bg="#121010")
        self.resizable(False, False)

        #variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)
        self.remember_me = tk.BooleanVar()
        self.current_user = None
        #frames as a parent container for other widgets 
        self.container= tk.Frame(self)
        self.container.pack(fill="both", expand=True)#fits the screen when maximized

        #widgets
        self.show_login_screen()#this replaces all the widget code that used to be here
    def show_login_screen(self):
        self.clear_container()
 
        tk.Label(self.container, text="Login", font=("Arial", 19, "bold"), fg="grey").pack(pady=10)
 
        tk.Label(self.container, text="Username", fg="grey").pack(anchor='w', padx=30)
        tk.Entry(self.container, textvariable=self.username, width=30).pack(pady=2)
 
        tk.Label(self.container, text="password", fg='grey').pack(anchor='w', padx=30)
        self.password_entry = tk.Entry(self.container, textvariable=self.password, show="*", width=30)
        self.password_entry.pack(pady=2)
 
        toogle_button = tk.Checkbutton(
            self.container, text='show password', variable=self.show_password,
            fg='grey', command=self.toggle_password
        )
        toogle_button.pack(anchor='w', pady=30, padx=30)
 
        remember_me_button = tk.Checkbutton(
            self.container, text='remember me', variable=self.remember_me, fg='grey'
        )
        remember_me_button.pack(anchor='w', padx=30)
 
        tk.Button(
            self.container, text='Login', command=self.login, width=25, bg="#899289", fg='grey'
        ).pack(pady=8)
        tk.Button(
            self.container, text='Register', command=self.register, width=25, bg="#7f8b80", fg='grey'
        ).pack()

    # methods (these only run later, when triggered)
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
       
        self.clear_container()
        role = self.current_user["role"]

        if role == "admin":
            self.render_admin_screen()
        elif role == "engineer":
            self.render_engineer_screen()
        elif role == "technician":
            self.render_technician_screen()
        elif role == "customer_service":
            self.render_customer_service_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():## loop through everything currently inside the box
            widget.destroy() 

    def render_customer_service_screen(self):
        complaint_text=tk.StringVar()
        outage_id=tk.StringVar()

        tk.Label(
            self.container,
            text="Customer Service Support",
            font=("Arial", 16, "bold"),
            fg="grey"
        ).pack(pady=10)
        #u need to call  self.contaner to make sure the label is inside the frame and not outside of it
        tk.Label(self.container, text="complaint", fg='grey').pack(anchor='w', padx=30)
        tk.Entry(self.container, textvariable=complaint_text, width=30).pack(pady=5)

        tk.Label(self.container, text="outage_id", fg='grey').pack(anchor='w', padx=30)   
        tk.Entry(self.container, textvariable=outage_id, width=15).pack(pady=5) 

        def submit_complaint():
            complaint = complaint_text.get().strip()
            outage = outage_id.get().strip()
            if not complaint :
                messagebox.showerror("Error", "Complaint cannot be empty.")
                return
            outage_value= outage if outage else None  # Convert empty string to None for optional field
                
            # Here you would call a function to save the complaint to the database
            if add_complaint(complaint, outage_value, self.current_user["user_id"]):
                messagebox.showinfo("Success", "Complaint submitted successfully!")
            else:
                messagebox.showerror("Error", "Failed to submit complaint. Please try again.")

        tk.Button(
                self.container, text="Submit Complaint", command=submit_complaint,bg="#545454",  fg="grey",width=25
            ).pack(pady=15)

        tk.Button(
                self.container, text="Logout", command=self.show_login_screen, bg="#545454",  fg="grey", width=25
            ).pack(pady=15)

    def render_engineer_screen(self):
        substations=get_substations()  # Fetch substations from the database

        display_list = [f'{s[1]}({s[2]})' for s in substations]  # Format: "Substation Name (Location)"
        substation_map = {f'{s[1]}({s[2]})': s[0] for s in substations}  # Map display name to substation_id
        selected_substation = tk.StringVar()

        description_text = tk.StringVar()

        tk.Label(self.container, text="Log New Outage", font=("Arial", 14, "bold"), fg="grey").pack(pady=10)
        tk.Label(self.container, text="Select Substation", fg='grey').pack(anchor='w', padx=30)
        dropdown=ttk.Combobox(
            self.container,
            textvariable=selected_substation,
            values=display_list,
            state="readonly",
            width=30,
        )
        dropdown.pack(pady=5)
        tk.Label(self.container, text="Description", fg='grey').pack(anchor='w', padx=30)
        description_entry=tk.Entry(self.container, textvariable=description_text, width=30)
        description_entry.pack(pady=5)

        def handle_submit():
            display_val= selected_substation.get()
            description=description_text.get().strip()
            if not display_val or not description:
                messagebox.showerror("Error", "All fields are required.")
                return
            sub_id=substation_map[display_val]  # Get the corresponding substation_id
            if add_outage(sub_id, self.current_user["user_id"], description):
                messagebox.showinfo("Success", "Outage logged successfully!")
                description_entry.delete(0, tk.END)  # Clear the description field
            else:
                messagebox.showerror("Error", "Failed to log outage. Please try again.")

        tk.Button(
            self.container, text="Submit Outage", command=handle_submit, bg="#545454", fg="grey", width=25
    ).pack(pady=15)

        tk.Button(self.container, text="Logout", command=self.show_login_screen, bg="#545454", fg="grey", width=25).pack(pady=5)
           
        
        

    

    def render_admin_screen(self):
        self.clear_container()
        open_outages =get_open_outages()
        technician = get_technician()

        outage_map = {f"Outage #{o[0]} - {o[1]}" : o[0] for o in open_outages}
        tech_map = {f"{t[1]} (ID : {t[0]})" : t[0] for t in technician}

        selected_outage = tk.StringVar()
        selected_tech = tk.StringVar()
        scheduled_date = tk.StringVar()#kinda communicates user input to our code,thats what tk.StringVar does

        tk.Label(self.container, text="Admin: Assign Work Orders", font=("Arial",14,"bold"), fg="grey").pack(pady=10)

        #dropdown for selecting outages
        tk.Label(self.container,text='Admin: Select Open Outage',fg='grey').pack(anchor='w',padx=30)
        outage_dropdown = ttk.Combobox(
            self.container, textvariable=selected_outage, values =list(outage_map.keys()), state="readonly", width=35
        )
        outage_dropdown.pack(pady=5)

        tk.Label(self.container, text='Assign Technician', fg='grey').pack(anchor='w', padx=30)
        tech_dropdown = ttk.Combobox(
                self.container, textvariable=selected_tech, values=list(tech_map.keys()), state="readonly", width=35
            )
        tech_dropdown.pack(pady=5)
        
        tk.Label(self.container, text="Scheduled Date (YYYY-MM-DD)", fg='grey').pack(anchor='w', padx=30)
        date_entry = tk.Entry(self.container, textvariable=scheduled_date, width=35)
        date_entry.pack(pady=5)

        def handle_assign():
            outage_str = selected_outage.get()
            tech_str = selected_tech.get()
            date_val = scheduled_date.get().strip()

            if not outage_str or not tech_str or not date_val:
                messagebox.showerror("Error", "All fields are required.")
                return
            #drop down for select tech
            outage_id = outage_map[outage_str]
            tech_id=tech_map[tech_str]

            if assign_work_order(outage_id, tech_id, date_val):
                messagebox.showinfo("Success", "Work order assigned successfully!")
                self.route_dashboard()  # Refresh view to update open outages
            else:
                messagebox.showerror("Error", "Failed to assign work order.")


    # Action Buttons
        tk.Button(self.container, text="Assign Work Order", command=handle_assign, bg="#545454", fg="grey", width=25).pack(pady=10)
        tk.Button(self.container, text="Logout", command=self.show_login_screen, bg="#545454", fg="grey", width=25).pack(pady=5)
   

    def render_technician_screen(self):
        self.clear_container()

        #handle user_id extraction regardless of it its a tuple or dict
        user_id = self.current_user["user_id"] if isinstance(self.current_user, dict) else self.current_user[0]

        #
        work_orders= get_technician_work_orders(user_id) 
        order_map = {f"WO #{w[0]} - Outage #{w[1]}-{w[3]}": w[0] for w in work_orders}
        selected_order = tk.StringVar()

        tk.Label(self.container, text="Technician Workspace", font=("Arial", 14, "bold"), fg="grey").pack(pady=10)
        tk.Label(self.container, text="Assigned Work Orders", fg="grey").pack(anchor='w', padx=30)

        order_dropdown = ttk.Combobox(
            self.container, textvariable = selected_order, values=list(order_map.keys()), state="readonly" ,width=40
        )
        order_dropdown.pack(pady=5)

        def handle_complete():
            order_str = selected_order.get()
            if not order_str:
                messagebox.showerror("Error", "Please select a work order.")
                return
            work_order_id = order_map[order_str]
            if mark_work_order_complete(work_order_id):
                messagebox.showinfo("Success", "Work order marked complete!")
                self.render_technician_screen()  # refresh to remove the completed one from view context
            else:
                messagebox.showerror("Error", "Failed to update work order.")

        tk.Button(
            self.container, text="Mark Complete", command=handle_complete, bg="#545454", fg="grey", width=25
        ).pack(pady=15)

        tk.Button(
            self.container, text="Logout", command=self.show_login_screen, bg="#545454", fg="grey", width=25
        ).pack(pady=15)    




   
        









                     
#when everything else is done lets maximize the screen and run the app      
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()


