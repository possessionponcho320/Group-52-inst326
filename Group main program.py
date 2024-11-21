import calendar

# Availability options
AVAILABILITY_OPTIONS = ["preferred", "available", "unavailable"]

class Caregiver:
    def __init__(self, name, phone, email, pay_rate, hours, is_paid):
        self.name = name
        self.phone = phone
        self.email = email
        self.pay_rate = pay_rate
        self.hours = hours
        self.is_paid = is_paid
        self.weekly_hours = []
        
        # Update pay_rate if is_paid is True
        if self.is_paid:
            self.pay_rate = 20
        
    # Getter for pay_rate
    def get_pay_rate(self):
        return self.pay_rate
   
    # Setter for pay_rate
    def set_pay_rate(self, value):
        self.pay_rate += value
        
    # Getter for hours
    def get_hours(self):
        return self.hours
    
    # Setter for hours
    def set_hours(self, value):
        self.hours += value
    
    
    # calculates weekly pay
    def get_weekly_pay(self, week):
        return self.weekly_hours[week - 1] * self.pay_rate
        
    
   


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
    def update_schedule(self, user):
        num_days = calendar.monthrange(self.year, self.month)[1]
        weekly_total = 0

        for day in range(1, num_days + 1):
            day_name = calendar.day_name[calendar.weekday(self.year, self.month, day)]
            print(f"\nAvailability for {day_name}, {self.month}/{day}/{self.year}:")
            
            # Get availability for the morning shift
            morning_shift = input("Morning shift (7:00AM - 1:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if morning_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["7:00AM - 1:00PM"] = morning_shift
            
            if morning_shift == "available" or morning_shift == "":
                user.set_hours(6)
                weekly_total += 6
                
            
            # Get availability for the afternoon shift
            afternoon_shift = input("Afternoon shift (1:00PM - 7:00PM): Enter 'preferred', 'available', or 'unavailable' (default is 'available'): ").strip().lower()
            if afternoon_shift in AVAILABILITY_OPTIONS:
                self.schedule[day]["1:00PM - 7:00PM"] = afternoon_shift
            
            if afternoon_shift == "available" or afternoon_shift == "":
                user.set_hours(6)
                weekly_total += 6
           
            if day_name == "Sunday":
                user.weekly_hours.append(weekly_total)
                weekly_total = 0  
       
        # Append remaining weekly total if the month ends mid-week
        if weekly_total > 0:
            user.weekly_hours.append(weekly_total)
            
   
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
        caregivers = [
                    Caregiver("Emily Martins", "123-456-7890", "emily@gmail.com", 0, 0, True),
                    Caregiver("Emma Martinez", "234-567-8901", "emma@gmail.com", 0, 0, True),
                    Caregiver("Abigail Garcia", "345-678-9012", "abigail@gmail.com", 0, 0, True),
                    Caregiver("Isabella Lopez", "456-789-0123", "isabella@gmail.com", 0, 0, True),
                    Caregiver("James Rodriguez", "567-890-1234", "james@gmail.com", 0, 0, False),
                    Caregiver("Benjamin Martinez", "678-901-2345", "benjamin@gmail.com", 0, 0, False),
                    Caregiver("Aiden Martins", "789-012-3456", "aiden@gmail.com", 0, 0, False),
                    Caregiver("Emma Smith", "890-123-4567", "emma.smith@gmail.com", 0, 0, False),
                    ]
    
        user = input("What is Your Name: ")
        
        index = None  # Initialize index to track the caregiver
        for i in range(len(caregivers)):
            if user == caregivers[i].name:
                user = caregivers[i]
                index = i
                break
        if index is not None:
            print("Welcome to the Care Availability Scheduler")
            program = 0
            while program != 1:
                user_options = input("What do you want to do? Press 1 to update or create a schedule. Press 2 to get your hours. Press 3 to get your pay rate. Press 4 to calculate weekly pay. Press any other to exit")
                if user_options == "1":
                    # Get user input for the year and month
                    year = int(input("Enter the year: "))
                    month = int(input("Enter the month (1-12): "))
                    schedule = CaregiverSchedule(user.name, year, month)
                    schedule.generate_month_schedule()
                    schedule.update_schedule(user)
                    schedule.display_care_schedule_as_html()
            
                elif user_options == "2":
                    print(f"You are working {user.hours} hours.")
                
                
                elif user_options == "3":
                     print(f"You are making ${user.pay_rate} an hour.")
                        
                elif user_options == "4":
                    week = input("What week do you want to calculate? ")
                    print(f"You are making ${user.get_weekly_pay(week)} on week {week}")
                else:
                    program = 1
                    
                
        else:
            print("You are not a member of the care team!")
            
        option = input("Do you want to reschedule or is there another user(yes/no): ")
        if option == "yes":
            continue
        else:
            break
            
