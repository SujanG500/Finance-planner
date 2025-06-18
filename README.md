# Finance Tracker App 💰📊

## Overview
The **Finance Tracker** is a desktop application built with Python's Tkinter library that helps users track their personal income and expenses. The app stores transactions in an SQLite database, allows filtering by date, visualizes expense breakdowns with pie charts, and supports exporting data to CSV files. It features a modern dark-themed UI for an enhanced user experience.

---

## Features
- ➕ Add income and expense transactions with date, description, category, type, and amount  
- 📅 Filter transactions by date range  
- 📊 Visualize expenses by category using pie charts  
- 📁 Export filtered transactions to CSV for external use  
- 💾 Persistent data storage using SQLite database  
- 🌙 Dark mode UI with responsive design for ease of use  

---

## Installation

### Prerequisites
- Python 3.6 or higher  
- Required Python packages:
  - `tkinter` (usually included with Python)  
  - `matplotlib`  
  - `sqlite3` (standard Python library)  

### Steps
1. Clone or download the repository:
    ```bash
    git clone https://github.com/your-username/finance-tracker.git
    cd finance-tracker
    ```

2. Install required packages:
    ```bash
    pip install matplotlib
    ```

3. Run the application:
    ```bash
    python finance_tracker.py
    ```

---

## Usage

1. **Add New Transaction:**  
   Fill out the form with date (`YYYY-MM-DD`), description, category, type (`Income` or `Expense`), and amount. Click **Add Transaction** to save.

2. **View Transactions:**  
   All transactions are listed in the table with columns for Date, Description, Category, Type, and Amount.

3. **Filter Transactions:**  
   Enter start and end dates in the filter section to view transactions within that period.

4. **View Expense Chart:**  
   Click **Show Expense Chart** to open a pie chart displaying the breakdown of expenses by category.

5. **Export to CSV:**  
   Export the currently displayed transactions to a CSV file by clicking **Export to CSV**.

---

## Database

- The app uses a local SQLite database file named `finance.db`.
- The database contains a table `transactions` with columns:  
  `id`, `date`, `description`, `category`, `type` (Income or Expense), and `amount`.

---

## Screenshots

*(Add screenshots here if available)*

---

## Technologies Used

- Python 3  
- Tkinter (GUI)  
- SQLite (Database)  
- Matplotlib (Charts)  

---

## License

This project is licensed under the MIT License.

---

## Contribution

Feel free to fork the repo, submit issues, and create pull requests!

---

## Contact

For questions or feedback, reach out to:  
**Your Name** — your.email@example.com  

---

Enjoy managing your finances with ease! 💸✨
