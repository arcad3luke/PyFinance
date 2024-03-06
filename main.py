import json
import math
import csv

def hourly():
    rate = float(input("Enter Wage: "))
    hours = float(input("Enter hours worked: "))
    shift_diff = float(input("Enter shift differential or 0 if none: "))
    overtime = input("Do you earn overtime? (Y/N) ")
    if overtime.upper() == 'Y':
        ot_rate = float(input("Enter OT rate: "))
        overtime_hours = float(input("Enter OT hours: "))
        weekly_pay = (rate * hours) + (shift_diff * hours) + (ot_rate * overtime_hours)
    else:
        weekly_pay = (rate * hours) + (shift_diff * hours)
    annual_gross = weekly_pay * 52
    confirm = input("Based on your responses: your weekly pay is: " + str(weekly_pay) +
                    ", and your yearly gross pay is: " + str(annual_gross) + ". Is this correct? (y/n)")
    if confirm == "n":
        return hourly()
    else:
        print("Great! Let's continue!")
        return annual_gross, weekly_pay

def federal_tax(weekly_pay):
    try:
        with open('federal_rates.json', 'r') as file:
            rates = json.load(file)
    except FileNotFoundError:
        print("Error: 'federal_rates.json' not found.")
        return
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON from 'federal_rates.json'. Make sure it contains valid JSON data.")
        return

    for rate, limits in rates.items():
        lower_limit = float(limits["lower_limit"])
        upper_limit = float(limits["upper_limit"]) if limits["upper_limit"] is not None else math.inf

        if lower_limit <= weekly_pay <= upper_limit:
            weekly_pay -= weekly_pay * (float(rate.strip('%')) / 100)

    return weekly_pay

def state_tax(weekly_pay, user_state):
    try:
        with open('state_rates.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            state_index = headers.index('State')  # Find the index of the 'State' column

            for row in reader:
                state = row[state_index]

                if user_state.lower() == state.lower():  # Check if the entered state matches the current row
                    rates = row[1:11]
                    brackets = row[11:21]

                    for rate, bracket in zip(rates, zip(brackets, brackets[1:])):
                        state_rate = float(rate.strip('%')) / 100
                        state_lower_limit = float(bracket[0].replace('$', '').replace(',', ''))
                        state_upper_limit = float(bracket[1].replace('$', '').replace(',', '')) if bracket[1] != ">" else math.inf

                        if state_lower_limit <= weekly_pay <= state_upper_limit:
                            weekly_pay -= weekly_pay * state_rate

                    break  # Stop iterating once the state is found

    except FileNotFoundError:
        print("Error: 'state_rates.csv' not found.")
        return

    return weekly_pay

def calculate_deductions(weekly_pay):
    pre_tax_deductions = float(input("Enter total pre-tax deductions: "))
    post_tax_deductions = float(input("Enter total post-tax deductions: "))
    weekly_pay -= pre_tax_deductions
    weekly_pay -= post_tax_deductions

    return weekly_pay

def calculate_401k_contribution(weekly_pay):
    percentage_cut = float(input("Enter 401k contribution percentage (0-100): "))
    if 0 <= percentage_cut <= 100:
        weekly_pay -= weekly_pay * (percentage_cut / 100)
    else:
        print("Invalid percentage. 401k contribution not applied.")

    return weekly_pay

def main():
    type_of_pay = input("Do you get paid hourly or salary? (Enter hourly or salary)")
    if type_of_pay == "hourly":
        user_state = input("Enter your state name: ")
        annual_gross, weekly_pay = hourly()
        weekly_pay = federal_tax(weekly_pay)
        weekly_pay = state_tax(weekly_pay, user_state)
        weekly_pay = calculate_deductions(weekly_pay)
        weekly_pay = calculate_401k_contribution(weekly_pay)

        net_pay = weekly_pay
        print(f"NET PAY: {net_pay}")

    else:
        pass

if __name__ == '__main__':
    main()
