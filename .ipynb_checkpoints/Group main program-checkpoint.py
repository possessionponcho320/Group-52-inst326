import calendar

# Availability options
AVAILABILITY_OPTIONS = ["preferred", "available", "unavailable"]


class CaregiverSchedule:
    def __init__(self, name, year, month):
        self.name = name
        self.year = year
        self.month = month
        self.schedule = {}

    # Create the default availability schedule for the month (all shifts "available")
    def generate_month_schedule(self):
        
        # Get the number of days in the specified month
        num_days = calendar.monthrange(self.year, self.month)[1]
        
        for day in range(1, num_days + 1):  # 7 days a week (Mon-Sun)
            self.schedule[day] = {
                "7:00AM - 1:00PM": "available",
                "1:00PM - 7:00PM": "available"
            }

    # Function to update the schedule based on user input
    def update_schedule(self):
        day_names = list(calendar.day_name)  # ['Monday', 'Tuesday', ...]

        for day in range(1, 8):
            print(f"\nAvailability for {day_names[day - 1]}")
            
            # Get availability for the morning shift
            morning_shift = input("Morning shift (7:00AM - 1:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if morning_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["7:00AM - 1:00PM"] = morning_shift
            
            # Get availability for the afternoon shift
            afternoon_shift = input("Afternoon shift (1:00PM - 7:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if afternoon_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["1:00PM - 7:00PM"] = afternoon_shift
   
    # Function to display the schedule as an HTML calendar
    def display_care_schedule_as_html(self):
        # Create the HTML structure
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
        
        # Get the first weekday of the month and the total days
        first_weekday, num_days = calendar.monthrange(self.year, self.month)

        # Fill in the days of the month
        current_day = 1
        for week in range((num_days + first_weekday) // 7 + 1):
            html_schedule += "<tr>"
            for day in range(7):
                if (week == 0 and day < first_weekday) or current_day > num_days:
                    html_schedule += "<td></td>"  # Empty cell for days outside the month
                else:
                    # Add the day and the assigned shifts
                    shifts_for_day = self.schedule.get(current_day, {})
                    morning_shift = shifts_for_day.get("7:00AM - 1:00PM", "N/A")
                    afternoon_shift = shifts_for_day.get("1:00PM - 7:00PM", "N/A")

                    html_schedule += f"<td>{current_day}<br><b>AM:</b> {morning_shift}<br><b>PM:</b> {afternoon_shift}</td>"
                    current_day += 1
            html_schedule += "</tr>"

        # Close the table and HTML
        html_schedule += """
            </table>
        </body>
        </html>
        """
        
        # Write the HTML content to a file
        with open(f"care_schedule_{self.year}_{self.month}_{self.name}.html", "w") as file:
            file.write(html_schedule)

        print(f"HTML care schedule for {calendar.month_name[self.month]} {self.year} generated successfully!")
        
if __name__ == "__main__":
    while True:
        names = ["Emily Martins", "Emma Martinez", 
             "Abigail Garcia", "Isabella Lopez", "James Rodriguez", 
             "Benjamin Martinez", "Aiden Martins", "Emma Smith",
             "Benjamin Thomas", "Jackson Taylor"] 
    
        user = input("What is Your Name: ")
        if user in names:
            print("Welcome to the Care Availability Scheduler")
        
            # Get user input for the year and month
            year = int(input("Enter the year: "))
            month = int(input("Enter the month (1-12): "))
            schedule = CaregiverSchedule(user, year, month)
            schedule.generate_month_schedule()
            schedule.update_schedule()
            schedule.display_care_schedule_as_html()
        else:
            print("You are not a member of the care team!")
            
        option = input("Do you want to reschedule or is there another user(yes/no): ")
        if option == "yes":
            continue
        else:
            break
            
    