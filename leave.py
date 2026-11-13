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
    def request_leave(self, emp_id : str, leave_type, start , end , reason ):
        # Validate the employee ID before looking it up.
        if not isinstance(emp_id, str) or not emp_id.strip():
            raise ValueError("Employee ID cannot be empty.")
        emp_id = emp_id.strip()
        if not self.employee_manager.find_employee(emp_id):
            raise ValueError("Employee does not exist.")

        if not isinstance(leave_type, str) or not leave_type.strip():
            raise ValueError("Leave type cannot be empty.")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Reason cannot be empty.")
        leave_type = leave_type.strip()
        reason = reason.strip()

        if not isinstance(start, str) or not isinstance(end, str):
            raise ValueError("Start and end dates must be strings in YYYY-MM-DD format.")

        try:
            start_date = datetime.strptime(start.strip(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date. Use YYYY-MM-DD.")

        if start_date < datetime.today().date():
            raise ValueError("Start date cannot be in the past.")
        if end_date < start_date:
            raise ValueError("End date cannot be before start date.")

        # Reject an overlapping pending or approved request for this employee.
        for request in self.leave_request.values():
            if request["emp_id"] != emp_id:
                continue
            if request["status"] not in ["Pending", "Approved"]:
                continue
            old_start = datetime.strptime(request["start"], "%Y-%m-%d").date()
            old_end = datetime.strptime(request["end"], "%Y-%m-%d").date()
            if start_date <= old_end and end_date >= old_start:
                raise ValueError("Overlapping leave request.")

        request_id = self.create_request_id()
        self.leave_request[request_id] = {
            "emp_id": emp_id,
            "leave_type": leave_type,
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "reason": reason,
            "status": "Pending",
            "comment": None
        }
        return request_id
    def view_request(self, request_id: str):
        if not isinstance(request_id, str ) or not request_id.strip():
            raise ValueError("Request ID cannot be empty.")
        request_id = request_id.strip().upper()
        request = self.leave_request.get(request_id)
        if request is None:
            raise ValueError("Leave request not found.")
        return {"request_id": request_id, **request.copy()}
    def evaluate_request(self, request_id, decision):
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID cannot be empty.")

        request_id = request_id.strip().upper()
        request = self.leave_request.get(request_id)
        if request is None:
            raise ValueError("Leave request not found.")
        if request["status"] != "Pending":
            raise ValueError("Only pending requests can be evaluated.")

        if not isinstance(decision, str) or not decision.strip():
            raise ValueError("Pass a decision: approve or reject.")

        decision = decision.strip().lower()

        decisions = {
            "approve": "Approved",
            "approved": "Approved",
            "reject": "Rejected",
            "rejected": "Rejected",
        }
        if decision not in decisions:
            raise ValueError("Decision must be approve or reject.")

        request["status"] = decisions[decision]
        return {"request_id": request_id, **request.copy()}

    def add_comment(self, request_id, comment):
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID cannot be empty.")

        request_id = request_id.strip().upper()
        request = self.leave_request.get(request_id)
        if request is None:
            raise ValueError("Leave request not found.")
        if not isinstance(comment, str) or not comment.strip():
            raise ValueError("Comment cannot be empty.")
        request["comment"] = comment.strip()
        return {"request_id": request_id, **request.copy()}
    def get_leave_summary(self):
        return {
            request_id: request.copy()
            for request_id, request in self.leave_request.items()
        }

    def get_pending_leave(self):
        return {
            request_id: request.copy()
            for request_id, request in self.leave_request.items()
            if request["status"] == "Pending"
        }

