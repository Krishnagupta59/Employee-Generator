import csv
import logging
import configparser
from faker import Faker

#Set up logging
config = configparser.ConfigParser()
config.read('config.ini')

#Initialize logger
logging.basicConfig(filename=config['EmployeeGenerator']['log_file'], level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

#Create an Employee Class
class Employee:
    def __init__(self, first_name, last_name, employee_id, manager_name, join_date, dob, age, salary, department_name):
        self.first_name = first_name
        self.last_name =last_name
        self.employee_id = employee_id
        self.manager_name = manager_name
        self.join_date = join_date
        self.dob = dob
        self.age = age
        self.salary = salary
        self.department_name = department_name

# Generate Employee Data
fake = Faker()
employees = []
for _ in range(100):
    employee = Employee(
        fake.first_name(),
        fake.last_name(),
        fake.unique.random_number(),
        fake.name(),
        fake.date_of_birth(tzinfo=None, minimum_age=22, maximum_age=65),
        fake.date_of_birth(tzinfo=None, minimum_age=22, maximum_age=65),
        fake.random_int(min=22, max=65),
        fake.random_int(min=30000, max=150000),
        fake.job()
    )
    employees.append(employee)

try:
    #Write data to CSV
    with open(config['EmployeeGenerator']['output_file'], mode='w', newline='') as csv_file:
        fieldnames = ['First Name', 'Last Name', 'Employee ID', 'Manager Name', 'Join Date', 'Date of Birth',
                      'Age', 'Salary', 'Department Name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for employee in employees:
            writer.writerow({
                'First Name': employee.first_name,
                'Last Name': employee.last_name,
                'Employee ID': employee.employee_id,
                'Manager Name': employee.manager_name,
                'Join Date': employee.join_date,
                'Date of Birth': employee.dob,
                'Age': employee.age,
                'Salary': employee.salary,
                'Department Name': employee.department_name,
            })
    #Logging Success Message
    logging.info("Employee data saved to employee.csv")
except Exception as e:
    # Exception Handling
    logging.error(f'An error occured: {str(e)}', exc_info=True)
