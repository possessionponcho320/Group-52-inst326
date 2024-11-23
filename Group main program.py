import calendar

# Availability options
AVAILABILITY_OPTIONS = ["preferred", "available", "unavailable"]

class Caregiver:
    def __init__(self, name, phone, email, pay_rate):
        self._name = name
        self.phone = phone
        self.email = email
        self.pay_rate = pay_rate
        self.hours = 0

    def __str__(self):
        return f"{self._name} ({self.phone}, {self.email})"
    
    def get_name(self):
        return self._name

class CaregiverSchedule:
    def __init__(self, name, year, month):
        self.name = name
        self.year = year
        self.month = month
        self.schedule = {}

    def generate_month_schedule(self):
        """Create a default availability schedule for the month."""
        num_days = calendar.monthrange(self.year, self.month)[1]
        for day in range(1, num_days + 1):
            self.schedule[day] = {
                "7:00AM - 1:00PM": "available",
                "1:00PM - 7:00PM": "available"
            }

    def update_schedule(self):
        """Update the schedule with user input."""
        day_names = list(calendar.day_name)
        for day in range(1, 8):
            print(f"\nAvailability for {day_names[day - 1]}")
            
            morning_shift = input("Morning shift (7:00AM - 1:00PM): Enter 'preferred', 'available', or 'unavailable': ").strip().lower()
            if morning_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["7:00AM - 1:00PM"] = morning_shift
            
            afternoon_shift = input("Afternoon shift (1:00PM - 7:00PM): Enter 'preferred', 'available', or 'unavailable': ").strip().lower()
            if afternoon_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["1:00PM - 7:00PM"] = afternoon_shift

    def display_care_schedule_as_html(self):
        """Generate and save the schedule as an HTML file."""
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
                    shifts_for_day = self.schedule.get(current_day, {})
                    morning_shift = shifts_for_day.get("7:00AM - 1:00PM", "N/A")
                    afternoon_shift = shifts_for_day.get("1:00PM - 7:00PM", "N/A")
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

    def generate_pay_report_as_html(self, caregiver):
        """Generate and save a pay report as an HTML file."""
        shift_hours = 6  # 6 hours per shift
        caregiver.hours = 0
        for shifts in self.schedule.values():
            for shift in shifts.values():
                if shift in ["preferred", "available"]:
                    caregiver.hours += shift_hours


        weekly_hours = caregiver.hours / 4  # Assuming 4 weeks in a month and is working next month
        weekly_pay = weekly_hours * caregiver.pay_rate
        monthly_pay = caregiver.hours * caregiver.pay_rate

        html_report = f"""
        <html>
        <head>
            <title>Pay Report for {caregiver.get_name()}</title>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 50%;
                    margin: 20px auto;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 10px;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <h1 style="text-align: center;">Pay Report for {caregiver.get_name()}</h1>
            <table>
                <tr>
                    <th>Name</th>
                    <td>{caregiver.get_name()}</td>
                </tr>
                <tr>
                    <th>Phone</th>
                    <td>{caregiver.phone}</td>
                </tr>
                <tr>
                    <th>Email</th>
                    <td>{caregiver.email}</td>
                </tr>
                <tr>
                    <th>Pay Rate</th>
                    <td>${caregiver.pay_rate:.2f}/hour</td>
                </tr>
                <tr>
                    <th>Monthly Hours</th>
                    <td>{caregiver.hours:.2f}</td>
                </tr>
                <tr>
                    <th>Weekly Hours</th>
                    <td>{weekly_hours:.2f}</td>
                </tr>
            <tr>
                <th>Weekly Pay</th>
                <td>${weekly_pay:.2f}</td>
            </tr>
                <tr>
                    <th>Monthly Pay</th>
                    <td>${monthly_pay:.2f}</td>
                </tr>
                <tr>
                    <th>Total Hours</th>
                    <td>{caregiver.hours:.2f}</td>
                </tr>
            </table>
        </body>
        </html>
        """
        with open(f"pay_report_{self.year}_{self.month}_{caregiver.get_name()}.html", "w") as file:
            file.write(html_report)
        print(f"Pay report for {caregiver.get_name()} generated successfully!")
        
        
if __name__ == "__main__":
    caregivers = [
        Caregiver("Logan Kim", "353-383-2849", "logank@gmail.com", 20),
        Caregiver("Samantha Green", "353-792-7943", "samag@gmail.com", 20),
        Caregiver("Tony Martin", "373-804-1264", "tonymar@gmail.com", 20),
        Caregiver("Tim Stephens", "373-294-02953", "timstp@gmail.com", 20),
        Caregiver("Jenny Dawnson", "364-305-1068", "jennydawnson@gmail.com", 0),
        Caregiver("Peter Zhang", "353-805-1852", "pdzhng@gmail.com", 0),
        Caregiver("David Lee", "364-703-2692", "ddgsan@gmail.com", 0),
        Caregiver("Jerrica Lopez", "284-903-9233", "jrricalpz@gmail.com", 0)
    ]

    while True:
        user_name = input("What is Your Name: ").strip().lower()
        caregiver = next((c for c in caregivers if c.get_name().strip().lower() == user_name), None)
        if caregiver:
            print(f"Welcome to the Care Availability Scheduler, {caregiver.get_name()}")
            year = int(input("Enter the year: "))
            month = int(input("Enter the month (1-12): "))
            schedule = CaregiverSchedule(caregiver.get_name(), year, month)
            schedule.generate_month_schedule()
            schedule.update_schedule()
            schedule.display_care_schedule_as_html()
            schedule.generate_pay_report_as_html(caregiver)
        else:
            print("You are not a member of the care team!")
        
        option = input("Do you want to reschedule or add another user (yes/no): ").strip().lower()
        if option != "yes":
            print("Goodbye!")
            break
