import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    description TEXT,
                    category TEXT,
                    type TEXT CHECK(type IN ('Income', 'Expense')),
                    amount REAL)''')
    conn.commit()
    conn.close()

# --- Add Transaction ---
def add_transaction():
    if not (date.get() and desc.get() and category.get() and t_type.get() and amount.get()):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    try:
        amt = float(amount.get())
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")
        return

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("INSERT INTO transactions (date, description, category, type, amount) VALUES (?, ?, ?, ?, ?)",
              (date.get(), desc.get(), category.get(), t_type.get(), amt))
    conn.commit()
    conn.close()
    load_transactions()
    clear_form()

# --- Load Transactions ---
def load_transactions():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    rows = c.fetchall()
    total_income = total_expense = 0

    for row in rows:
        tree.insert('', 'end', values=row[1:])
        if row[4] == 'Income':
            total_income += row[5]
        else:
            total_expense += row[5]

    balance.set(f"Balance: ${total_income - total_expense:.2f}")
    conn.close()

# --- Filter Transactions by Date ---
def filter_transactions():
    start = start_date.get()
    end = end_date.get()
    if not start or not end:
        messagebox.showwarning("Input Error", "Please enter both start and end dates.")
        return

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT * FROM transactions WHERE date BETWEEN ? AND ?", (start, end))
    rows = c.fetchall()
    total_income = total_expense = 0

    for row in rows:
        tree.insert('', 'end', values=row[1:])
        if row[4] == 'Income':
            total_income += row[5]
        else:
            total_expense += row[5]

    balance.set(f"Balance: ${total_income - total_expense:.2f}")
    conn.close()

# --- Export to CSV ---
def export_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if not filename:
        return
    rows = []
    for child in tree.get_children():
        rows.append(tree.item(child)['values'])

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Description', 'Category', 'Type', 'Amount'])
        for row in rows:
            writer.writerow(row)
    messagebox.showinfo("Export", "Filtered data exported successfully!")

# --- Show Charts ---
def show_chart():
    conn = sqlite3.connect("finance.db")
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = c.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Chart", "No expense data available to plot.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.clf()
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.set_title("Expense Breakdown")
    plt.tight_layout()

    top = tk.Toplevel(root)
    top.title("Chart")
    chart = FigureCanvasTkAgg(fig, top)
    chart.get_tk_widget().pack()
    chart.draw()

# --- Clear Form ---
def clear_form():
    date.set("")
    desc.set("")
    category.set("")
    t_type.set("Expense")
    amount.set("")

# --- Main App ---
init_db()

root = tk.Tk()
root.title("Finance Tracker")
root.geometry("800x750")
root.configure(bg="#1e1e2f")  # Dark background

# --- Variables ---
date = tk.StringVar()
desc = tk.StringVar()
category = tk.StringVar()
t_type = tk.StringVar(value="Expense")
amount = tk.StringVar()
balance = tk.StringVar()
start_date = tk.StringVar()
end_date = tk.StringVar()

# --- Entry Form ---
form_frame = tk.LabelFrame(root, text="Add New Transaction", padx=20, pady=10, bg="#2a2a40", fg="white")
form_frame.pack(pady=15, padx=10, fill="x")

for i, (label, var) in enumerate(zip(["Date (YYYY-MM-DD)", "Description", "Category", "Type", "Amount"],
                                     [date, desc, category, t_type, amount])):
    tk.Label(form_frame, text=label, bg="#2a2a40", fg="white", anchor="w").grid(row=i, column=0, sticky='w', pady=2)
    entry = tk.Entry(form_frame, textvariable=var, width=50, bg="#3c3c5c", fg="white", insertbackground="white")
    entry.grid(row=i, column=1, pady=2)

add_btn = tk.Button(form_frame, text="Add Transaction", command=add_transaction, bg="#4CAF50", fg="white", width=20)
add_btn.grid(row=5, column=0, columnspan=2, pady=10)

# --- Filter Section ---
filter_frame = tk.LabelFrame(root, text="Filter by Date", padx=20, pady=10, bg="#2a2a40", fg="white")
filter_frame.pack(pady=10, padx=10, fill="x")

tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):", bg="#2a2a40", fg="white").grid(row=0, column=0, sticky="w")
tk.Entry(filter_frame, textvariable=start_date, bg="#3c3c5c", fg="white", insertbackground="white").grid(row=0, column=1, padx=5)
tk.Label(filter_frame, text="End Date (YYYY-MM-DD):", bg="#2a2a40", fg="white").grid(row=0, column=2, sticky="w")
tk.Entry(filter_frame, textvariable=end_date, bg="#3c3c5c", fg="white", insertbackground="white").grid(row=0, column=3, padx=5)
tk.Button(filter_frame, text="Filter Transactions", command=filter_transactions, bg="#6c63ff", fg="white").grid(row=0, column=4, padx=10)

# --- Transaction List ---
list_frame = tk.LabelFrame(root, text="Transactions", padx=10, pady=5, bg="#2a2a40", fg="white")
list_frame.pack(padx=10, pady=10, fill="both", expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#1e1e2f", fieldbackground="#1e1e2f", foreground="white", rowheight=25)
style.configure("Treeview.Heading", background="#3c3c5c", foreground="white", font=("Arial", 10, "bold"))

cols = ["Date", "Description", "Category", "Type", "Amount"]
tree = ttk.Treeview(list_frame, columns=cols, show='headings', height=10)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor='center', width=100)
tree.pack(fill="both", expand=True)

# --- Dashboard & Actions ---
dashboard = tk.Frame(root, bg="#1e1e2f")
dashboard.pack(pady=10)

balance_label = tk.Label(dashboard, textvariable=balance, font=("Arial", 16, "bold"), fg="#17a2b8", bg="#1e1e2f")
balance_label.pack(pady=5)

btn_frame = tk.Frame(dashboard, bg="#1e1e2f")
btn_frame.pack(pady=5)

chart_btn = tk.Button(btn_frame, text="Show Expense Chart", command=show_chart, bg="#17a2b8", fg="white", width=20)
chart_btn.grid(row=0, column=0, padx=10)

export_btn = tk.Button(btn_frame, text="Export to CSV", command=export_csv, bg="#ffc107", fg="#1e1e2f", width=20)
export_btn.grid(row=0, column=1, padx=10)

# --- Load data ---
load_transactions()

root.mainloop()
