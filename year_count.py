import datetime

def days_remaining_in_year():
    today = datetime.date.today()
    end_of_year = datetime.date(today.year, 12, 31)
    remaining_days = (end_of_year - today).days
    return remaining_days

def current_week_of_month():
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    week_number = (today.day - 1) // 7 + 1
    return week_number

def current_quarter():
    today = datetime.date.today()
    return (today.month - 1) // 3 + 1

def main():
    print(f"Days remaining in the year: {days_remaining_in_year()}")
    print(f"Current week of the month: {current_week_of_month()}")
    print(f"Current quarter of the year: {current_quarter()}")

if __name__ == "__main__":
    main()
