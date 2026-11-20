

class Payroll:
    def __init__(self, employee_manager, attendance_manager):
        if employee_manager is None:
            raise ValueError("An employee manager is required.")
        if attendance_manager is None:
            raise ValueError("An attendance manager is required.")

        self.payrolls = {}
        self.employee_manager = employee_manager
        self.attendance_manager = attendance_manager

    def _validate_employee_id(self, emp_id):
        if not isinstance(emp_id, str) or not emp_id.strip():
            raise ValueError("Employee ID cannot be empty.")

        emp_id = emp_id.strip()

        if not self.employee_manager.find_employee(emp_id):
            raise ValueError(f"Employee {emp_id} does not exist.")

        return emp_id

    def _get_base_salary(self, emp_id):
        emp_id = self._validate_employee_id(emp_id)
        salary = self.employee_manager.get_salary(emp_id)

        if not isinstance(salary, (int, float)) or isinstance(salary, bool):
            raise ValueError("Employee salary must be a number.")
        if salary < 0:
            raise ValueError("Employee salary cannot be negative.")

        return salary

    def calculate_allowance(self, emp_id):
        base_salary = self._get_base_salary(emp_id)
        return base_salary * 0.15

    def calculate_deduction(self, emp_id, emp_absence):
        if not isinstance(emp_absence, int) or isinstance(emp_absence, bool):
            raise ValueError("Absent days must be a whole number.")
        if emp_absence < 0:
            raise ValueError("Absent days cannot be negative.")

        base_salary = self._get_base_salary(emp_id)
        return (base_salary / 30) * emp_absence

    def _get_absent_days(self, emp_id):
        emp_id = self._validate_employee_id(emp_id)
        records = self.attendance_manager.get_attendance(emp_id)

        if records is None:
            return 0

        if isinstance(records, dict):
            records = records.values()

        try:
            records = list(records)
        except TypeError as error:
            raise ValueError("Attendance records must be a list or dictionary.") from error

        absent_days = 0

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each attendance record must be a dictionary.")

            status = record.get("status")
            if not isinstance(status, str):
                raise ValueError("Each attendance record needs a text status.")

            if status.casefold() == "absent":
                absent_days += 1

        return absent_days

    def calculate_salary(self, emp_id):
        emp_id = self._validate_employee_id(emp_id)
        base_salary = self._get_base_salary(emp_id)
        absent_days = self._get_absent_days(emp_id)

        allowance = self.calculate_allowance(emp_id)
        deduction = self.calculate_deduction(emp_id, absent_days)

        return base_salary + allowance - deduction

    def save_payroll(self, emp_id, emp_absence):
        emp_id = self._validate_employee_id(emp_id)
        base_salary = self._get_base_salary(emp_id)
        allowance = self.calculate_allowance(emp_id)
        deduction = self.calculate_deduction(emp_id, emp_absence)
        net_salary = base_salary + allowance - deduction

        record = {
            "base_salary": base_salary,
            "allowance": allowance,
            "deduction": deduction,
            "absence_days": emp_absence,
            "net_salary": net_salary,
        }

        self.payrolls.setdefault(emp_id, []).append(record)
        return record.copy()

    def view_salary(self, emp_id):
        emp_id = self._validate_employee_id(emp_id)
        return [record.copy() for record in self.payrolls.get(emp_id, [])]

    def get_payroll_summary(self):
        records = [
            record
            for employee_history in self.payrolls.values()
            for record in employee_history
        ]

        return {
            "total_base_salary": sum(record["base_salary"] for record in records),
            "total_allowance": sum(record["allowance"] for record in records),
            "total_deduction": sum(record["deduction"] for record in records),
            "total_net_salary": sum(record["net_salary"] for record in records),
        }