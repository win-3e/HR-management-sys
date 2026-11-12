from datetime import datetime
class Leave():
    def __init__(self,employee_manager):
        self.leave_request= {}
        self.counter = 1
        self.employee_manager = employee_manager
    #create request ID
    def create_request_id(self):
        request_id = f"L{self.counter:04d}"
        self.counter += 1
        return request_id
    def request_leave(self, emp_id : str, leave_type, start , end , reason , status= "Pending"):
        #check employee exits
        if not self.employee_manager.find_employee(emp_id):
            raise ValueError("Employee does not exits!")
        #validate required infomation 
        if not all([emp_id, leave_type and leave_type.strip(), reason and reason.strip()]):
            raise ValueError("Required field cannot be empty!.")
        if status != "Pending":
            raise ValueError("New request must be Pending.")
        #validate date
        try:
            start_date = datetime.strptime(start , "%Y-%m-%d").date()
            end_date = datetime.strptime(end , "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format.Use YYYY-MM-DD.")
        if start_date < datetime.today().date():
            raise ValueError("Start date cannot be in the past.")
        if end_date < start_date:
            raise ValueError("End date cannot be before start date.")
        # check over lapping request 
        for request in self.leave_request.values():
            if request["emp_id"] != emp_id:
                continue
            if request["status"] not in ["Pending", "Approved"]:
                continue

            old_start = datetime.strptime(request["start"], "%Y-%m-%d").date()
            old_end = datetime.strptime(request["end"], "%Y-%m-%d").date()

            if start_date <= old_end and end_date >= old_start:
                raise ValueError("Overlapping leave request.")
