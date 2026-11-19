

class Payroll:
    def __init__(self, employee_manager , attendance_manager):
        self.payrolls = {}
        self.employee_manager = employee_manager
        self.attendance_manager = attendance_manager
    def calculate_allowance(self,emp_id):
        base_salary = self.employee_manager.get_salary(emp_id)
        return base_salary* 0.15
    def calculate_deduction(self, emp_id, emp_absence):
        base_salary = self.employee_manager.get_salary(emp_id)
        return (base_salary/ 30 )* emp_absence
    def calculate_salary(self, emp_id):
        base_salary = self.employee_manager.get_salary(emp_id)
        records = self.attendance_manager.get_attendance(emp_id)

        if isinstance(records, dict):
            records = records.values()

        absent_days = sum(1 for record in records
                            if record.get("status", "").casefold()== "absent")
        allowance = self.calculate_allowance(emp_id)
        deduction = self.calculate_deduction(emp_id, absent_days)
        return base_salary + allowance - deduction