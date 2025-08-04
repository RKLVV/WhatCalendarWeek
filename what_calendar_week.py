import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def get_week_dates(year, week):
    try:
        first_day = datetime.strptime(f'{year}-W{int(week)}-1', "%G-W%V-%u")
        return [(first_day + timedelta(days=i)) for i in range(7)]
    except ValueError:
        return []

def get_weeks_in_month(year, month):
    first_day = datetime(year, month, 1)
    last_day = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    current_day = first_day
    weeks = {}
    while current_day <= last_day:
        week_num = current_day.isocalendar()[1]
        if week_num not in weeks:
            weeks[week_num] = get_week_dates(current_day.isocalendar()[0], week_num)
        current_day += timedelta(days=1)
    return weeks

def display_calendar_grid(weeks):
    clear_calendar_grid()
    today = datetime.today().date()
    current_week = today.isocalendar()[1]
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for col, day in enumerate(days):
        label = tk.Label(calendar_frame, text=day, font=('Arial', 10, 'bold'),
                         borderwidth=1, relief="solid", width=8, bg=bg_color, fg="white")
        label.grid(row=0, column=col+1, padx=1, pady=1, sticky="nsew")

    for row, (week_num, dates) in enumerate(sorted(weeks.items()), start=1):
        week_label = tk.Label(calendar_frame, text=f"W{week_num}", font=('Arial', 10, 'bold'),
                              borderwidth=1, relief="solid", width=8, bg=bg_color, fg="white")
        week_label.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")
        for col, date in enumerate(dates):
            bg = "#dddddd" if week_num == current_week else "#bbbbbb"
            if date.date() == today:
                bg = "orange"
            date_label = tk.Label(calendar_frame, text=date.strftime('%d.%m'), font=('Arial', 9),
                                  borderwidth=1, relief="solid", width=8, bg=bg)
            date_label.grid(row=row, column=col+1, padx=1, pady=1, sticky="nsew")

def clear_calendar_grid():
    for widget in calendar_frame.winfo_children():
        widget.destroy()

def reset_to_today():
    today = datetime.today()
    selected_year.set(today.year)
    selected_month.set(today.strftime('%B'))

def show_selected_week():
    try:
        week = int(week_entry.get())
        year = selected_year.get()
        dates = get_week_dates(year, week)
        if dates:
            display_calendar_grid({week: dates})
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid week number.")

def update_calendar(*args):
    year = selected_year.get()
    month_name = selected_month.get()
    try:
        month = datetime.strptime(month_name, '%B').month
        weeks = get_weeks_in_month(year, month)
        display_calendar_grid(weeks)
    except ValueError:
        messagebox.showerror("Error", "Invalid month or year.")

# === UI Setup ===
bg_color = "#333333"
fg_color = "white"
entry_bg = "#444444"
button_bg = "#555555"

root = tk.Tk()
root.title("What Calendar Week")
root.configure(bg=bg_color)

# Left panel: Year and Month
left_frame = tk.Frame(root, bg=bg_color)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

selected_year = tk.IntVar(value=datetime.today().year)
selected_month = tk.StringVar(value=datetime.today().strftime('%B'))

tk.Label(left_frame, text="Year:", bg=bg_color, fg=fg_color).pack(anchor="w")
year_spin = tk.Spinbox(left_frame, from_=2000, to=2100, textvariable=selected_year, width=6,
                       bg=entry_bg, fg=fg_color, insertbackground=fg_color, relief="flat")
year_spin.pack(anchor="w", pady=2)

tk.Label(left_frame, text="Month:", bg=bg_color, fg=fg_color).pack(anchor="w")
month_combo = tk.OptionMenu(left_frame, selected_month, *[datetime(2000, m, 1).strftime('%B') for m in range(1, 13)])
month_combo.config(bg=entry_bg, fg=fg_color, activebackground=button_bg, activeforeground=fg_color)
month_combo["menu"].config(bg=entry_bg, fg=fg_color)
month_combo.pack(anchor="w", pady=2)

# Bind changes to update calendar
selected_year.trace_add("write", update_calendar)
selected_month.trace_add("write", update_calendar)

# Right panel: Week input and Today button
right_frame = tk.Frame(root, bg=bg_color)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

tk.Label(right_frame, text="Calendar Week:", bg=bg_color, fg=fg_color).pack(anchor="e")
week_entry = tk.Entry(right_frame, width=5, bg=entry_bg, fg=fg_color, insertbackground=fg_color, relief="flat")
week_entry.pack(anchor="e", pady=2)

tk.Button(right_frame, text="Show Week", command=show_selected_week,
          bg=button_bg, fg=fg_color, activebackground="#777777").pack(anchor="e", pady=2)
tk.Button(right_frame, text="Today", command=lambda: [reset_to_today(), update_calendar()],
          bg=button_bg, fg=fg_color, activebackground="#777777").pack(anchor="e", pady=2)

# Calendar grid
calendar_frame = tk.Frame(root, bg=bg_color)
calendar_frame.pack(pady=10)

# Initial display
update_calendar()

# Run the app
root.mainloop()
