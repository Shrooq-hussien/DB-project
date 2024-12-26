import tkinter as tk
import os
from tkinter import filedialog
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Tk, Label, Button, messagebox,Toplevel
from tkcalendar import Calendar

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sh@851018#op-", 
            database="Duckdb"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def send_email(to_email, subject, body):
    try:
        sender_email = "shrooqhussien2@gmail.com"
        sender_password = "tvyzegsagwkatjjs"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email: {e}")

class ServiceApp:
    def sign_in(self):
     
      email = self.email_entry.get()
      name = self.name_entry.get()
      phone = self.phone_entry.get()

      if not email or not name or not phone:
        messagebox.showerror("Input Error", "All fields are required.")
        return

      try:
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
        user = cursor.fetchone()

        if user:
            self.current_user = user
            messagebox.showinfo("Welcome Back", f"Welcome, {user[1]}!")
        else:
            cursor.execute("INSERT INTO User (Name, Email, PhoneNumber) VALUES (%s, %s, %s)", (name, email, phone))
            self.db_connection.commit()
            cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
            self.current_user = cursor.fetchone()
            messagebox.showinfo("Registration Successful", "Your account has been created!")

        self.category_page()
      except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


    def __init__(self, root):
        self.root = root
        self.root.title("DuckTour Service Management")
        self.root.geometry("1000x800")
        self.root.configure(bg="#fffff0")  

        self.db_connection = connect_to_database()
        icon = tk.PhotoImage(file="logo.png") 
        self.root.iconphoto(False, icon)
        
        self.current_user = None
        self.current_admin =None
        self.selected_date =None

        self.logo = PhotoImage(file="logo.png")  
        self.login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def branding(self):
      tk.Label(self.root, text="DuckTour", font=("Freestyle Script", 72, "bold"), fg="#004c99",bg="#fffff0").pack(pady=10)

      image = Image.open("logo.png")  
      image = image.resize((200, 200))  
      self.logo = ImageTk.PhotoImage(image)

      logo_label = tk.Label(self.root,bg="#fffff0", image=self.logo)
      logo_label.place(relx=1.0, rely=1.0, anchor="se")  


    def login_page(self):
      self.clear_window()
      self.branding()

      tk.Label(self.root, text="Welcome to DuckTour Service Management App", font=("Aref Ruqaa", 16), fg="#960f05",bg="#fffff0").pack(pady=3)
          
      tk.Label(self.root, text="Name:", font=("Gabriola", 24),bg="#fffff0").pack()
      self.name_entry = tk.Entry(self.root, width=30)
      self.name_entry.pack()

      tk.Label(self.root, text="Email:", font=("Gabriola", 24),bg="#fffff0").pack()
      self.email_entry = tk.Entry(self.root, width=30)
      self.email_entry.pack()

      

      tk.Label(self.root, text="Phone Number:", font=("Gabriola", 24),bg="#fffff0").pack()
      self.phone_entry = tk.Entry(self.root, width=30)
      self.phone_entry.pack()

      tk.Button(self.root, text="Sign In", command=self.sign_in, bg="#004c99", fg="white", font=("Lucida Calligraphy", 16)).pack(pady=10)
      tk.Button(self.root, text="Service Provider Login", command=self.admin_page, bg="#008000", fg="white", font=("Lucida Calligraphy", 16)).pack(pady=5)


    def category_page(self):
        self.clear_window()
        self.branding()

        tk.Label(self.root, text="xx Select a Category xx", font=("Gabriola", 36),fg="#960f05",bg="#fffff0").pack(pady=3)
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM Category")
            categories = cursor.fetchall()

            for category in categories:
                tk.Button(self.root, text=category[1],font=("Lucida Calligraphy",20),bg="#637caf", fg="white" ,command=lambda c=category[0]: self.service_list_page(c)).pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

        tk.Button(self.root, text="Logout", font=("Gabriola", 16),bg="#960f05",fg="white", command=self.login_page).pack(pady=30)

    def service_list_page(self, category_id):
        self.clear_window()
        self.branding()

        filters_frame = tk.Frame(self.root, bg="#fffff0")
        filters_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(filters_frame, bg="#fffff0", text="Filters", font=("Gabriola", 24)).pack(pady=10)

        tk.Label(filters_frame, bg="#fffff0", text="Capacity (>=)", font=("Helvetica", 12)).pack(pady=5)
        self.capacity_slider = tk.Scale(filters_frame, from_=0, to=100, orient="horizontal", length=200, bg="#fffff0")
        self.capacity_slider.pack()

        tk.Label(filters_frame, bg="#fffff0", text="Price (<=)", font=("Helvetica", 12)).pack(pady=5)
        self.price_slider = tk.Scale(filters_frame, from_=0, to=1000, orient="horizontal", length=200, bg="#fffff0")
        self.price_slider.pack()

        tk.Button(filters_frame, text="Apply Filters", command=lambda: self.display_services(category_id),
              bg="#004c99", fg="white", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(filters_frame, text="Back", command=self.category_page, bg="#808080", fg="white", font=("Helvetica", 12)).pack(pady=10)

        self.services_frame = tk.Frame(self.root, bg="#fffff0")
        self.services_frame.pack(side="left", fill="both", padx=150, pady=90)
        tk.Label(self.services_frame, bg="#fffff0", text="Available Services", font=("Gabriola", 16)).pack(pady=10)

        self.display_services(category_id)


    def display_services(self, category_id):
        for widget in self.services_frame.winfo_children():
            widget.destroy()

        capacity_filter = self.capacity_slider.get()
        price_filter = self.price_slider.get()

        query = "SELECT * FROM Service WHERE CategoryID = %s"
        params = [category_id]

        if capacity_filter > 0:
           query += " AND Capacity >= %s"
           params.append(capacity_filter)

        if price_filter > 0:
           query += " AND Price <= %s"
           params.append(price_filter)

        try:
           cursor = self.db_connection.cursor()
           cursor.execute(query, tuple(params))
           services = cursor.fetchall()

           for service in services:
            tk.Button(self.services_frame, text=service[1], 
                      command=lambda s=service: self.confirm_service_page(s),
                      font=("Monotype Corsiva", 24), bg="#960f05", fg="white").pack(pady=10, padx=20, fill="x")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



    def confirm_service_page(self, service):
        self.clear_window()
        self.branding()

        tk.Label(self.root,bg="#fffff0", text=f"Confirm Booking for {service[1]}", font=("Gabriola", 24, "bold"), fg="#004c99").pack(pady=10)

       

        try:
           image_path = os.path.join(os.getcwd(), service[5])  
           print(f"Loading image: {image_path}")  
           service_image = Image.open(image_path)
           service_image = service_image.resize((200, 200), Image.Resampling.LANCZOS)
           service_photo = ImageTk.PhotoImage(service_image)
           image_label = tk.Label(self.root,bg="#fffff0", image=service_photo)
           image_label.image = service_photo  
           image_label.pack(pady=10)
        except Exception as e:
              print(f"Failed to load image: {service[5]} - Error: {e}")
              tk.Label(self.root,bg="#fffff0", text="Image not available", font=("Helvetica", 12), fg="red").pack(pady=10)

        details_frame = tk.Frame(self.root,bg="#fffff0")
        details_frame.pack(pady=10)

        tk.Label(details_frame,bg="#fffff0", text=f"Location: {service[4]}", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(details_frame, bg="#fffff0",text=f"Price: ${service[3]:.2f}", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5)

        tk.Label(self.root,bg="#fffff0", text="Number of People:", font=("Helvetica", 12)).pack(pady=5)
        self.people_entry = tk.Entry(self.root, width=10)
        self.people_entry.pack()
        

        tk.Button(self.root, text="Choose date", command=self.open_calendar,
                bg="#004c99", fg="white", font=("Helvetica", 12)).pack(padx=10)
        tk.Button(self.root, text="Confirm", command=lambda: self.confirm_booking(service),
              bg="#004c99", fg="white", font=("Helvetica", 12)).pack(padx=10)

        tk.Button(self.root, text="Back", command=lambda: self.service_list_page(service[2]),
              bg="#808080", fg="white", font=("Helvetica", 12)).pack(pady=10)
        
    def open_calendar(self):
        calendar_window = Toplevel(self.root)
        calendar_window.title("Date")

        cal = Calendar(calendar_window, date_pattern="yyyy-mm-dd") 
        cal.pack(pady=20)

        confirm_button = Button(calendar_window, text="Confirm Date", 
                                 command=lambda: self.date(cal, calendar_window))
        confirm_button.pack(pady=10)
    def date(self,cal,calendar_window):
        self.selected_date = cal.get_date()
        calendar_window.destroy()
        

    def confirm_booking(self, service):
        try:
            people_count = int(self.people_entry.get())
            total_price = people_count * service[3]

            cursor = self.db_connection.cursor()
            cursor.execute("INSERT INTO Transaction (UserID, ServiceID, TransactionDate,TicketDate ,NumberOfPeople,TotalAmount ) "
                           "VALUES (%s, %s, NOW(),%s, %s, %s)",
                           (self.current_user[0], service[0],self.selected_date , people_count,total_price))
            self.db_connection.commit()

            send_email(self.current_user[2], "Booking Confirmation",
                       f"Thank you for booking {service[1]}!\n\nLocation: {service[4]}\nTotal Price: {total_price}\n  Date: {self.selected_date}")
            messagebox.showinfo("Success", "Your ticket has been sent to your email.")
            self.category_page()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of people.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



    def admin_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Service Provider Login", font=("Gabriola", 24, "bold")).pack(pady=20)
        
        tk.Label(self.root,bg="#fffff0", text="National ID:", font=("Gabriola", 16)).pack(pady=5)
        self.national_id_entry = tk.Entry(self.root, width=30)
        self.national_id_entry.pack(pady=5)
      

        tk.Label(self.root,bg="#fffff0", text="Name:", font=("Gabriola", 16)).pack()
        self.admin_name_entry = tk.Entry(self.root, width=30)
        self.admin_name_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="Phone Number:", font=("Gabriola", 16)).pack()
        self.admin_phone_entry = tk.Entry(self.root, width=30)
        self.admin_phone_entry.pack()
        tk.Label(self.root,bg="#fffff0", text="Email:", font=("Gabriola", 16)).pack()
        self.admin_mail_entry = tk.Entry(self.root, width=30)
        self.admin_mail_entry.pack()

        tk.Button(self.root, text="Login", command=self.admin_login, font=("Gabriola", 16), bg="#004c99", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.login_page, font=("Gabriola", 12), bg="grey", fg="white").pack(pady=20)
        
    def admin_login(self):
    
        national_id = self.national_id_entry.get()
        name = self.admin_name_entry.get()
        phone = self.admin_phone_entry.get()
        mail = self.admin_mail_entry.get()

        if not (national_id and name and phone and mail):
           messagebox.showerror("Error", "All fields are required!")
           return
        self.current_admin=national_id
        try:
           cursor = self.db_connection.cursor()
           cursor.execute("SELECT * FROM Admin WHERE NationalID = %s", (national_id,))
           admin = cursor.fetchone()

           if admin:
              self.national_id = national_id  
              messagebox.showinfo("Welcome", f"Welcome back, {name}!")
              self.service_provider_page()
           else:
              cursor.execute("INSERT INTO Admin (NationalID, Name, PhoneNumber,Email) VALUES (%s, %s, %s,%s)",
                           (national_id, name, phone,mail))
              self.db_connection.commit()
              self.national_id = national_id  
              messagebox.showinfo("Registered", f"Hello {name}, your account has been created!")
              self.service_provider_page()
        except Exception as e:
           messagebox.showerror("Error", f"Failed to log in: {e}")
        


    def service_provider_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Service Provider Panel", font=("Gabriola", 24, "bold")).pack(pady=20)

        tk.Button(self.root, text="Add Service", command=self.add_service_page, font=("Helvetica", 12), bg="#004c99", fg="white").pack(pady=10)
        tk.Button(self.root, text="Delete Service", command=self.remove_service_page, font=("Helvetica", 12), bg="#ff0000", fg="white").pack(pady=10)
        tk.Button(self.root, text="Edit Service", command=self.edit_service_page, font=("Helvetica", 12), bg="#004c99", fg="white").pack(pady=10)
        tk.Button(self.root, text="Transactions", command=self.transactions_page, font=("Helvetica", 12), bg="#004c99", fg="white").pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.admin_page, font=("Gabriola", 12), bg="#808080", fg="white").pack(pady=20)

    def add_service_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Add New Service", font=("Gabriola", 24, "bold")).pack(pady=20)

        tk.Label(self.root,bg="#fffff0", text="Name:", font=("Helvetica", 16)).pack()
        self.service_name_entry = tk.Entry(self.root, width=30)
        self.service_name_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="Category Name:", font=("Gabriola", 16)).pack()
        self.category_name_entry = tk.Entry(self.root, width=30)
        self.category_name_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="Price Per Individual:", font=("Gabriola", 16)).pack()
        self.price_entry = tk.Entry(self.root, width=30)
        self.price_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="Capacity:", font=("Gabriola", 16)).pack()
        self.capacity_entry = tk.Entry(self.root, width=30)
        self.capacity_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="Location:", font=("Gabriola", 16)).pack()
        self.location_entry = tk.Entry(self.root, width=30)
        self.location_entry.pack()
        tk.Label(self.root, bg="#fffff0", text="Service Image:", font=("Gabriola", 12)).pack()
        self.image_path_label = tk.Label(self.root, bg="#fffff0", text="No image selected", font=("Gabriola", 12))
        self.image_path_label.pack()

        self.image_path = None 
        def upload_image():
            self.image_path = filedialog.askopenfilename(
            title="Select Service Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
             )
            if self.image_path:
               self.image_path_label.config(text=os.path.basename(self.image_path))  

        tk.Button(self.root, text="Upload Image", command=upload_image, bg="#004c99", fg="white", font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self.root, text="Add Service", command=self.add_service, bg="#004c99", fg="white", font=("Helvetica", 12)).pack(pady=10)
    
        tk.Button(self.root, text="Back", command=self.service_provider_page, bg="#808080", fg="white", font=("Helvetica", 12)).pack(pady=10)

        
    def add_service(self):
        try:
           name = self.service_name_entry.get()
           category_name = self.category_name_entry.get()
           price = float(self.price_entry.get())
           capacity = int(self.capacity_entry.get())
           location = self.location_entry.get()
           owner=self.current_admin

           if not (name and category_name and location and self.image_path):
              messagebox.showwarning("Warning", "All fields, including the image, are required!")
              return

           cursor = self.db_connection.cursor()
           cursor.execute("SELECT CategoryID FROM Category WHERE Name = %s", (category_name,))
           category = cursor.fetchone()

           if category:
              category_id = category[0]
           else:
              cursor.execute("INSERT INTO Category (Name) VALUES (%s)", (category_name,))
              category_id = cursor.lastrowid
              self.db_connection.commit()

           image_folder = os.path.join(os.getcwd(), "images")
           os.makedirs(image_folder, exist_ok=True)
           saved_image_path = os.path.join(image_folder, os.path.basename(self.image_path))

           if not os.path.exists(saved_image_path):
                  os.rename(self.image_path, saved_image_path)

           cursor.execute(
            "INSERT INTO Service (Name, CategoryID, Price,  Location, ImagePath,OwnerID,Capacity) VALUES (%s, %s, %s, %s, %s, %s,%s)",
            (name, category_id, price,  location, saved_image_path,owner,capacity)
        )
           service_id = cursor.lastrowid
           self.db_connection.commit()

           messagebox.showinfo("Success", f"Service added successfully! Your Service ID is {service_id}.")
           self.service_provider_page()

        except ValueError:
             messagebox.showerror("Input Error", "Price and Capacity must be valid numbers.")
        except Exception as e:
             messagebox.showerror("Error", f"Failed to add service: {e}")       

    def remove_service_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Delete Service", font=("Gabriola", 24, "bold")).pack(pady=20)

        tk.Label(self.root,bg="#fffff0", text="Service ID:", font=("Gabriola", 16)).pack()
        self.service_id_entry = tk.Entry(self.root, width=30)
        self.service_id_entry.pack()

        tk.Button(self.root, text="Delete Service", command=self.remove_service, font=("Helvetica", 16), bg="#ff0000", fg="white").pack(pady=20)
        tk.Button(self.root, text="Back", command=self.service_provider_page, font=("Gabriola", 12), bg="#808080", fg="white").pack(pady=10)

    def remove_service(self):
        try:
            service_id = int(self.service_id_entry.get())
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM Transaction WHERE ServiceID = %s ", (service_id,))
            self.db_connection.commit()
            cursor.execute("DELETE FROM Service WHERE ServiceID = %s AND OwnerID = %s", (service_id, self.current_admin))
            self.db_connection.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Service deleted successfully!")
            else:
                messagebox.showerror("Error", "Service not found or you do not own this service.")
        except Exception as e:
            self.db_connection.rollback()
            messagebox.showerror("Error", f"Failed to delete service: {e}")

    def transactions_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Transactions for Your Services", font=("Gabriola", 24, "bold")).pack(pady=20)

        frame = tk.Frame(self.root,bg="#fffff0")
        frame.pack(pady=10)

        headers = ["Transaction ID", "Service Name", "User Name", "Transaction Date","Ticket Date", "Number of People", "Total Amount"]
        for idx, header in enumerate(headers):
         tk.Label(frame,bg="#fffff0", text=header, font=("Gabriola", 16, "bold"),  borderwidth=1, relief="solid").grid(row=0, column=idx, padx=5, pady=5)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT ServiceID, Name FROM Service WHERE OwnerID = %s", (self.current_admin,))
            services = cursor.fetchall()

            if not services:
               tk.Label(self.root,bg="#fffff0", text="No transactions available for your services.", font=("Gabriola", 16)).pack(pady=20)
               tk.Button(self.root, text="Back", command=self.service_provider_page, font=("Gabriola", 12), bg="#808080", fg="white").pack(pady=10)
               return

            service_ids = [service[0] for service in services]
            service_map = {service[0]: service[1] for service in services}

            cursor.execute(f"""
SELECT t.TransactionID, t.ServiceID, u.Name, t.TransactionDate, t.TicketDate, t.NumberOfPeople, t.TotalAmount
FROM `Transaction` t
JOIN `User` u ON t.UserID = u.UserID
WHERE t.ServiceID IN ({','.join(['%s'] * len(service_ids))})
""", service_ids)

            transactions = cursor.fetchall()

            for row_idx, row in enumerate(transactions, start=1):
              transaction_id, service_id, user_name, transaction_date, ticket_date, num_people, total_amount = row
              values = [
              transaction_id, 
              service_map[service_id], 
              user_name, 
              transaction_date, 
              ticket_date, 
              num_people, 
              total_amount
                ]
    
              for col_idx, value in enumerate(values):
                   tk.Label(frame,bg="#fffff0", text=value, font=("Gabriola", 14), borderwidth=1, relief="solid").grid(row=row_idx, column=col_idx, padx=5, pady=5)

        except Exception as e:
             messagebox.showerror("Error", f"Failed to fetch transactions: {e}")

        tk.Button(self.root, text="Back", command=self.service_provider_page, font=("Gabriola", 12), bg="#808080", fg="white").pack(pady=10)

    def edit_service_page(self):
        self.clear_window()
        self.branding()
        tk.Label(self.root,bg="#fffff0", text="Edit Service Details", font=("Gabriola", 24, "bold")).pack(pady=20)

        tk.Label(self.root,bg="#fffff0", text="Service ID:", font=("Gabriola", 16)).pack()
        self.edit_service_id_entry = tk.Entry(self.root, width=30)
        self.edit_service_id_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="New Price:", font=("Gabriola", 16)).pack()
        self.edit_price_entry = tk.Entry(self.root, width=30)
        self.edit_price_entry.pack()

        tk.Label(self.root,bg="#fffff0", text="New Location:", font=("Gabriola", 16)).pack()
        self.edit_location_entry = tk.Entry(self.root, width=30)
        self.edit_location_entry.pack()
        tk.Label(self.root, bg="#fffff0", text="Service Image:", font=("Gabriola", 12)).pack()
        self.image_path_label = tk.Label(self.root, bg="#fffff0", text="No image selected", font=("Gabriola", 12))
        self.image_path_label.pack()
        self.image_path = None 
        def upload_image():
            self.image_path = filedialog.askopenfilename(
            title="Select Service Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
             )
            if self.image_path:
               self.image_path_label.config(text=os.path.basename(self.image_path))  

        tk.Button(self.root, text="Upload Image", command=upload_image, bg="#004c99", fg="white", font=("Helvetica", 12)).pack(pady=10)

        tk.Button(self.root, text="Edit Service", command=self.edit_service, font=("Gabriola", 16), bg="#004c99", fg="white").pack(pady=20)
        tk.Button(self.root, text="Back", command=self.service_provider_page, font=("Gabriola", 12), bg="#808080", fg="white").pack(pady=10)

    def edit_service(self):
        try:
            image_folder = os.path.join(os.getcwd(), "images")
            os.makedirs(image_folder, exist_ok=True)

            saved_image_path = None
            if self.image_path :
                saved_image_path = os.path.join(image_folder, os.path.basename(self.image_path))
                if not os.path.exists(saved_image_path) and os.path.exists(self.image_path):
                    os.rename(self.image_path, saved_image_path)

            service_id = int(self.edit_service_id_entry.get())
            new_price = float(self.edit_price_entry.get()) if self.edit_price_entry.get() else None
            new_location = self.edit_location_entry.get() if self.edit_location_entry.get() else None

            if not (new_price or new_location or saved_image_path):
               messagebox.showerror("Error", "At least one field (Price, Location, or Image) must be updated.")
               return

            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM Service WHERE ServiceID = %s AND OwnerID = %s", (service_id, self.national_id))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Service not found or you do not own this service.")
                return

            update_queries = []
            update_values = []

            if new_price is not None:
               update_queries.append("Price = %s")
               update_values.append(new_price)
            if new_location:
               update_queries.append("Location = %s")
               update_values.append(new_location)
            if saved_image_path:
               update_queries.append("ImagePath = %s")
               update_values.append(saved_image_path)

            if update_queries:
               update_values.append(service_id)
               query = f"UPDATE Service SET {', '.join(update_queries)} WHERE ServiceID = %s"
               cursor.execute(query, update_values)

            self.db_connection.commit()
            messagebox.showinfo("Success", "Service updated successfully!")
            self.service_provider_page()

        except Exception as e:
              self.db_connection.rollback()
              messagebox.showerror("Error", f"Failed to update service: {e}")


root = tk.Tk()
app = ServiceApp(root)
root.mainloop()
