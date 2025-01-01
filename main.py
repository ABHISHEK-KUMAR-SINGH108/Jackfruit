import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from datetime import datetime

class RestaurantBookingSystem:
    def __init__(self, root):  
        self.root = root
        self.root.title("Restaurant Booking System")
        self.root.geometry("1000x900")

        # Navigation Bar
        self.nav_frame = ttk.Frame(self.root)
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_restaurants = ttk.Button(self.nav_frame, text="Restaurants", command=self.show_restaurants)
        self.btn_restaurants.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_booking = ttk.Button(self.nav_frame, text="Booking", command=self.show_booking)
        self.btn_booking.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_user_management = ttk.Button(self.nav_frame, text="User Management", command=self.show_user_management)
        self.btn_user_management.pack(side=tk.LEFT, padx=5, pady=5)

        #Frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.show_restaurants()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_restaurants(self):
        self.clear_content_frame()

        # Restaurant
        lbl_title = ttk.Label(self.content_frame, text="Restaurants", font=("Arial", 16))
        lbl_title.pack(pady=10)

        filter_frame = ttk.Frame(self.content_frame)
        filter_frame.pack(fill=tk.X, pady=5)

        lbl_cuisine = ttk.Label(filter_frame, text="Cuisine Type:")
        lbl_cuisine.pack(side=tk.LEFT, padx=5)

        cb_cuisine = ttk.Combobox(filter_frame, values=["All", "Italian", "Chinese", "Indian", "Japanese"])
        cb_cuisine.pack(side=tk.LEFT, padx=5)
        cb_cuisine.set("All")

        lbl_rating = ttk.Label(filter_frame, text="Rating:")
        lbl_rating.pack(side=tk.LEFT, padx=5)

        cb_rating = ttk.Combobox(filter_frame, values=["All", "1", "2", "3", "4", "5"])
        cb_rating.pack(side=tk.LEFT, padx=5)
        cb_rating.set("All")

        btn_filter = ttk.Button(filter_frame, text="Filter", command=lambda: self.filter_restaurants(cb_cuisine.get(), cb_rating.get()))
        btn_filter.pack(side=tk.LEFT, padx=5)

        restaurant_list = ttk.Treeview(self.content_frame, columns=("Name", "Cuisine", "Rating"), show="headings")
        restaurant_list.heading("Name", text="Name")
        restaurant_list.heading("Cuisine", text="Cuisine")
        restaurant_list.heading("Rating", text="Rating")
        restaurant_list.pack(fill=tk.BOTH, expand=True, pady=10)

        self.restaurant_list = restaurant_list
        self.load_restaurants()

    def load_restaurants(self):
        self.restaurant_list.delete(*self.restaurant_list.get_children())
        with open('restaurants.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.restaurant_list.insert("", "end", values=(row['name'], row['cuisine_type'], row['rating']))

    def filter_restaurants(self, cuisine, rating):
        self.restaurant_list.delete(*self.restaurant_list.get_children())
        with open('restaurants.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (cuisine == "All" or row['cuisine_type'] == cuisine) and \
                   (rating == "All" or float(row['rating']) >= float(rating)):
                    self.restaurant_list.insert("", "end", values=(row['name'], row['cuisine_type'], row['rating']))

    def show_booking(self):
        self.clear_content_frame()

        lbl_title = ttk.Label(self.content_frame, text="Booking", font=("Arial", 16))
        lbl_title.pack(pady=10)

        lbl_name = ttk.Label(self.content_frame, text="Name:")
        lbl_name.pack(pady=5)
        entry_name = ttk.Entry(self.content_frame)
        entry_name.pack(pady=5)

        lbl_restaurant = ttk.Label(self.content_frame, text="Restaurant:")
        lbl_restaurant.pack(pady=5)
        cb_restaurant = ttk.Combobox(self.content_frame, values=self.get_restaurant_names())
        cb_restaurant.pack(pady=5)

        lbl_date = ttk.Label(self.content_frame, text="Date (YYYY-MM-DD):")
        lbl_date.pack(pady=5)
        entry_date = ttk.Entry(self.content_frame)
        entry_date.pack(pady=5)

        lbl_time = ttk.Label(self.content_frame, text="Time (HH:MM):")
        lbl_time.pack(pady=5)
        entry_time = ttk.Entry(self.content_frame)
        entry_time.pack(pady=5)

        lbl_party_size = ttk.Label(self.content_frame, text="Party Size:")
        lbl_party_size.pack(pady=5)
        entry_party_size = ttk.Entry(self.content_frame)
        entry_party_size.pack(pady=5)

        lbl_table = ttk.Label(self.content_frame, text="Table Selection:")
        lbl_table.pack(pady=5)
        cb_table = ttk.Combobox(self.content_frame, values=["Table 1", "Table 2", "Table 3"])
        cb_table.pack(pady=5)

        btn_confirm = ttk.Button(self.content_frame, text="Confirm Booking", command=lambda: self.confirm_booking(entry_name.get(), cb_restaurant.get(), entry_date.get(), entry_time.get(), entry_party_size.get(), cb_table.get()))
        btn_confirm.pack(pady=10)

        btn_cancel = ttk.Button(self.content_frame, text="Cancel Booking", command=self.show_cancel_booking)
        btn_cancel.pack(pady=10)

    def get_restaurant_names(self):
        restaurant_names = []
        with open('restaurants.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                restaurant_names.append(row['name'])
        return restaurant_names

    def confirm_booking(self, name, restaurant, date, time, party_size, table):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time, '%H:%M')
        except ValueError:
            messagebox.showerror("Invalid Format", "Please enter the date in YYYY-MM-DD format and time in HH:MM format.")
            return

        with open('bookings.csv', 'a', newline='') as csvfile:
            fieldnames = ['booking_id', 'user_id', 'restaurant_id', 'table_id', 'date', 'time', 'party_size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'booking_id': 'B001',  # This should be dynamically generated
                'user_id': name,  # Use the entered name as user_id
                'restaurant_id': self.get_restaurant_id(restaurant),  # Use the selected restaurant
                'table_id': table,
                'date': date,
                'time': time,
                'party_size': party_size
            })
        messagebox.showinfo("Booking Confirmed", "Your booking has been confirmed!")

    def get_restaurant_id(self, restaurant_name):
        with open('restaurants.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['name'] == restaurant_name:
                    return row['restaurant_id']
        return None

    def show_cancel_booking(self):
        self.clear_content_frame()

        lbl_title = ttk.Label(self.content_frame, text="Cancel Booking", font=("Arial", 16))
        lbl_title.pack(pady=10)

        lbl_booking_id = ttk.Label(self.content_frame, text="Booking ID:")
        lbl_booking_id.pack(pady=5)
        entry_booking_id = ttk.Entry(self.content_frame)
        entry_booking_id.pack(pady=5)

        btn_cancel = ttk.Button(self.content_frame, text="Cancel Booking", command=lambda: self.cancel_booking(entry_booking_id.get()))
        btn_cancel.pack(pady=10)

    def cancel_booking(self, booking_id):
        bookings = []
        with open('bookings.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['booking_id'] != booking_id:
                    bookings.append(row)

        with open('bookings.csv', 'w', newline='') as csvfile:
            fieldnames = ['booking_id', 'user_id', 'restaurant_id', 'table_id', 'date', 'time', 'party_size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bookings)

        messagebox.showinfo("Booking Cancelled", "Your booking has been cancelled.")

    def show_user_management(self):
        self.clear_content_frame()

        lbl_title = ttk.Label(self.content_frame, text="User Management", font=("Arial", 16))
        lbl_title.pack(pady=10)

        lbl_current_bookings = ttk.Label(self.content_frame, text="Current Bookings:")
        lbl_current_bookings.pack(pady=5)
        current_bookings_list = ttk.Treeview(self.content_frame, columns=("Booking ID", "Restaurant", "Date", "Time"), show="headings")
        current_bookings_list.heading("Booking ID", text="Booking ID")
        current_bookings_list.heading("Restaurant", text="Restaurant")
        current_bookings_list.heading("Date", text="Date")
        current_bookings_list.heading("Time", text="Time")
        current_bookings_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # Load data from bookings.csv and users.csv
        with open('bookings.csv', newline='') as bookings_file, open('users.csv', newline='') as users_file:
            bookings_reader = csv.DictReader(bookings_file)
            users_reader = csv.DictReader(users_file)
            users = {row['user_id']: row for row in users_reader}
            for booking in bookings_reader:
                user = users.get(booking['user_id'])
                if user:
                    current_bookings_list.insert("", "end", values=(booking['booking_id'], booking['restaurant_id'], booking['date'], booking['time']))

        lbl_booking_history = ttk.Label(self.content_frame, text="Booking History:")
        lbl_booking_history.pack(pady=5)
        booking_history_list = ttk.Treeview(self.content_frame, columns=("Booking ID", "Restaurant", "Date", "Time"), show="headings")
        booking_history_list.heading("Booking ID", text="Booking ID")
        booking_history_list.heading("Restaurant", text="Restaurant")
        booking_history_list.heading("Date", text="Date")
        booking_history_list.heading("Time", text="Time")
        booking_history_list.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_cancel = ttk.Button(self.content_frame, text="Cancel Booking", command=self.show_cancel_booking)
        btn_cancel.pack(pady=10)

        btn_remove = ttk.Button(self.content_frame, text="Remove Booking", command=self.show_remove_booking)
        btn_remove.pack(pady=10)

    def show_remove_booking(self):
        self.clear_content_frame()

        lbl_title = ttk.Label(self.content_frame, text="Remove Booking", font=("Arial", 16))
        lbl_title.pack(pady=10)

        lbl_booking_id = ttk.Label(self.content_frame, text="Booking ID:")
        lbl_booking_id.pack(pady=5)
        entry_booking_id = ttk.Entry(self.content_frame)
        entry_booking_id.pack(pady=5)

        btn_remove = ttk.Button(self.content_frame, text="Remove Booking", command=lambda: self.remove_booking(entry_booking_id.get()))
        btn_remove.pack(pady=10)

    def remove_booking(self, booking_id):
        bookings = []
        with open('bookings.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['booking_id'] != booking_id:
                    bookings.append(row)

        with open('bookings.csv', 'w', newline='') as csvfile:
            fieldnames = ['booking_id', 'user_id', 'restaurant_id', 'table_id', 'date', 'time', 'party_size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bookings)

        messagebox.showinfo("Booking Removed", "The booking has been removed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantBookingSystem(root)
    root.mainloop()