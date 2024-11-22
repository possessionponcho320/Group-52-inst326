import calendar

# Availability options
AVAILABILITY_OPTIONS = ["preferred", "available", "unavailable"]

class Caregiver:
    def __init__(self, name, phone, email, is_paid):
        self.name = name
        self.phone = phone
        self.email = email
        self._pay_rate = 20 if is_paid else 0
        self._hours = 0
        self._is_paid = is_paid
        self.weekly_hours = []
    
    # Getter for pay_rate
    def get_pay_rate(self):
        return self._pay_rate
   
    # Setter for pay_rate
    def set_pay_rate(self, value):
        self._pay_rate = value
        
    # Getter for hours
    def get_hours(self):
        return self._hours
    
    # Setter for hours
    def set_hours(self, value):
        if self._is_paid:  # Only allow hours to accumulate for paid caregivers
            self._hours += value
    
    # Calculates weekly pay
    def get_weekly_pay(self, week):
        if week < 1 or week > len(self.weekly_hours):
            return 0  # Return 0 for invalid week
        return self.weekly_hours[week - 1] * self._pay_rate

    # Calculate monthly pay
    def get_monthly_pay(self):
        return self._hours * self._pay_rate


class CaregiverSchedule:
    def __init__(self, name, year, month):
        self.name = name
        self.year = year
        self.month = month
        self.schedule = {}

    # Create the default availability schedule for the month (all shifts "available")
    def generate_month_schedule(self):
        num_days = calendar.monthrange(self.year, self.month)[1]
        for day in range(1, num_days + 1):
            self.schedule[day] = {
                "7:00AM - 1:00PM": "available",
                "1:00PM - 7:00PM": "available"
            }

    # Function to update the schedule based on user input
    def update_schedule(self, caregiver):
        num_days = calendar.monthrange(self.year, self.month)[1]
        weekly_total = 0

        for day in range(1, num_days + 1):
            day_name = calendar.day_name[calendar.weekday(self.year, self.month, day)]
            print(f"\nAvailability for {day_name}, {self.month}/{day}/{self.year}:")

            # Get availability for the morning shift
            morning_shift = input("Morning shift (7:00AM - 1:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if morning_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["7:00AM - 1:00PM"] = morning_shift
                if morning_shift in ["available", "preferred"]:
                    caregiver.set_hours(6)
                    weekly_total += 6
            
            # Get availability for the afternoon shift
            afternoon_shift = input("Afternoon shift (1:00PM - 7:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if afternoon_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["1:00PM - 7:00PM"] = afternoon_shift
                if afternoon_shift in ["available", "preferred"]:
                    caregiver.set_hours(6)
                    weekly_total += 6
            
            # Append weekly total on Sundays
            if day_name == "Sunday":
                caregiver.weekly_hours.append(weekly_total)
                weekly_total = 0

        # Append remaining weekly total for partial weeks
        if weekly_total > 0:
            caregiver.weekly_hours.append(weekly_total)

    # Function to display the schedule as an HTML calendar
    def display_care_schedule_as_html(self):
        html_schedule = f"""
        <html>
        <head>
            <title>{self.name}'s Care Schedule for {calendar.month_name[self.month]} {self.year}</title>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 10px;
                    text-align: center;
                }}
                td {{
                    height: 100px;
                    vertical-align: top;
                }}
            </style>
        </head>
        <body>
            <h1>{self.name}'s Care Schedule for {calendar.month_name[self.month]} {self.year}</h1>
            <table>
                <tr>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    <th>Sat</th>
                    <th>Sun</th>
                </tr>
        """

        first_weekday, num_days = calendar.monthrange(self.year, self.month)
        current_day = 1
        for week in range((num_days + first_weekday) // 7 + 1):
            html_schedule += "<tr>"
            for day in range(7):
                if (week == 0 and day < first_weekday) or current_day > num_days:
                    html_schedule += "<td></td>"
                else:
                    shifts = self.schedule.get(current_day, {})
                    morning_shift = shifts.get("7:00AM - 1:00PM", "N/A")
                    afternoon_shift = shifts.get("1:00PM - 7:00PM", "N/A")
                    html_schedule += f"<td>{current_day}<br><b>AM:</b> {morning_shift}<br><b>PM:</b> {afternoon_shift}</td>"
                    current_day += 1
            html_schedule += "</tr>"

        html_schedule += """
            </table>
        </body>
        </html>
        """
        with open(f"care_schedule_{self.year}_{self.month}_{self.name}.html", "w") as file:
            file.write(html_schedule)
        print(f"HTML care schedule for {calendar.month_name[self.month]} {self.year} generated successfully!")


def generate_pay_report(caregivers, year, month):
    html_report = f"""
    <html>
    <head>
        <title>Pay Report for {calendar.month_name[month]} {year}</title>
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid black;
                padding: 10px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Caregiver Pay Report for {calendar.month_name[month]} {year}</h1>
        <table>
            <tr>
                <th>Caregiver</th>
                <th>Monthly Pay</th>
                <th>Weekly Pay (Week 1)</th>
                <th>Weekly Pay (Week 2)</th>
                <th>Weekly Pay (Week 3)</th>
                <th>Weekly Pay (Week 4)</th>
                <th>Weekly Pay (Week 5)</th>
            </tr>
    """
    for caregiver in caregivers:
        monthly_pay = caregiver.get_monthly_pay()
        weekly_pays = (caregiver.weekly_hours + [0] * 5)[:5]
        html_report += f"""
            <tr>
                <td>{caregiver.name}</td>
                <td>${monthly_pay:.2f}</td>
                <td>${weekly_pays[0] * caregiver.get_pay_rate():.2f}</td>
                <td>${weekly_pays[1] * caregiver.get_pay_rate():.2f}</td>
                <td>${weekly_pays[2] * caregiver.get_pay_rate():.2f}</td>
                <td>${weekly_pays[3] * caregiver.get_pay_rate():.2f}</td>
                <td>${weekly_pays[4] * caregiver.get_pay_rate():.2f}</td>
            </tr>
        """
    html_report += """
        </table>
    </body>
    </html>
    """
    with open(f"caregiver_pay_report_{year}_{month}.html", "w") as file:
        file.write(html_report)
    print(f"Pay report for {calendar.month_name[month]} {year} generated successfully!")

if __name__ == "__main__":
    caregivers = [
        Caregiver("Emily Martins", "123-456-7890", "emily@gmail.com", True),
        Caregiver("Emma Martinez", "234-567-8901", "emma@gmail.com", True),
        Caregiver("Abigail Garcia", "345-678-9012", "abigail@gmail.com", True),
        Caregiver("Isabella Lopez", "456-789-0123", "isabella@gmail.com", True),
        Caregiver("James Rodriguez", "567-890-1234", "james@gmail.com", False),
        Caregiver("Benjamin Martinez", "678-901-2345", "benjamin@gmail.com", False),
        Caregiver("Aiden Martins", "789-012-3456", "aiden@gmail.com", False),
        Caregiver("Emma Smith", "890-123-4567", "emma.smith@gmail.com", False),
    ]
    
    while True:
        user_name = input("What is Your Name: ")
        user = next((cg for cg in caregivers if cg.name == user_name), None)
        
        if user:
            print("Welcome to the Care Availability Scheduler")
            while True:
                user_option = input("Select an option: 1-Update/Create Schedule, 2-View Hours, 3-View Pay Rate, 4-Weekly Pay, 5-Monthly Pay, 6-Generate Pay Report, 0-Exit: ")
                if user_option == "1":
                    year = int(input("Enter the year: "))
                    month = int(input("Enter the month (1-12): "))
                    schedule = CaregiverSchedule(user.name, year, month)
                    schedule.generate_month_schedule()
                    schedule.update_schedule(user)
                    schedule.display_care_schedule_as_html()
                elif user_option == "2":
                    print(f"You are working {user.get_hours()} hours.")
                elif user_option == "3":
                    print(f"You are making ${user.get_pay_rate()} an hour.")
                elif user_option == "4":
                    week = int(input("What week do you want to calculate? "))
                    print(f"You are making ${user.get_weekly_pay(week)} for week {week}.")
                elif user_option == "5":
                    print(f"You are making ${user.get_monthly_pay()} this month.")
                elif user_option == "6":
                    year = int(input("Enter the year: "))
                    month = int(input("Enter the month (1-12): "))
                    generate_pay_report(caregivers, year, month)
                elif user_option == "0":
                    break
                else:
                    print("Invalid option. Try again.")
        else:
            print("You are not a member of the care team.")
        
        if input("Do you want to continue? (yes/no): ").lower() != "yes":
            print("Goodbye!")
            break
