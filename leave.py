from datetime import date, datetime


class Leave:
    def __init__(self, employee_manager):
        if employee_manager is None:
            raise ValueError("An employee manager is required.")

        self.leave_request = {}
        self.counter = 1
        self.employee_manager = employee_manager

    def create_request_id(self):
        request_id = f"L{self.counter:04d}"
        self.counter += 1
        return request_id

    def _get_request(self, request_id):
        if not isinstance(request_id, str) or not request_id.strip():
            raise ValueError("Request ID cannot be empty.")

        request_id = request_id.strip().upper()
        request = self.leave_request.get(request_id)

        if request is None:
            raise ValueError(f"Leave request {request_id} was not found.")

        return request_id, request

    def request_leave(
        self,
        emp_id,
        leave_type,
        start,
        end,
        reason,
        status="Pending",
    ):
        if not isinstance(emp_id, str) or not emp_id.strip():
            raise ValueError("Employee ID cannot be empty.")

        emp_id = emp_id.strip()

        if not self.employee_manager.find_employee(emp_id):
            raise ValueError(f"Employee {emp_id} does not exist.")

        if not isinstance(leave_type, str) or not leave_type.strip():
            raise ValueError("Leave type cannot be empty.")

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Reason cannot be empty.")

        # Requests must start as pending; only an evaluator changes the status.
        if not isinstance(status, str) or status.strip().casefold() != "pending":
            raise ValueError("A new leave request must have Pending status.")

        if not isinstance(start, str) or not isinstance(end, str):
            raise ValueError("Start and end dates must use YYYY-MM-DD format.")

        try:
            start_date = datetime.strptime(start.strip(), "%Y-%m-%d").date()
            end_date = datetime.strptime(end.strip(), "%Y-%m-%d").date()
        except ValueError as error:
            raise ValueError("Invalid date. Use YYYY-MM-DD.") from error

        if start_date < date.today():
            raise ValueError("Start date cannot be in the past.")

        if end_date < start_date:
            raise ValueError("End date cannot be before start date.")

        # Prevent overlapping requests that are still pending or already approved.
        for existing in self.leave_request.values():
            if existing["emp_id"] != emp_id:
                continue

            if existing["status"] not in {"Pending", "Approved"}:
                continue

            old_start = date.fromisoformat(existing["start"])
            old_end = date.fromisoformat(existing["end"])

            if start_date <= old_end and end_date >= old_start:
                raise ValueError("This request overlaps another pending or approved leave.")

        request_id = self.create_request_id()

        self.leave_request[request_id] = {
            "emp_id": emp_id,
            "leave_type": leave_type.strip(),
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "reason": reason.strip(),
            "status": "Pending",
            "comment": None,
        }

        return request_id

    def view_request(self, request_id):
        request_id, request = self._get_request(request_id)
        return {"request_id": request_id, **request.copy()}

    def evaluate_request(self, request_id, decision):
        request_id, request = self._get_request(request_id)

        if request["status"] != "Pending":
            raise ValueError("Only pending requests can be evaluated.")

        if not isinstance(decision, str) or not decision.strip():
            raise ValueError("Decision must be approve or reject.")

        decisions = {
            "approve": "Approved",
            "approved": "Approved",
            "reject": "Rejected",
            "rejected": "Rejected",
        }

        decision = decision.strip().casefold()

        if decision not in decisions:
            raise ValueError("Decision must be approve or reject.")

        request["status"] = decisions[decision]
        return {"request_id": request_id, **request.copy()}

    def add_comment(self, request_id, comment):
        request_id, request = self._get_request(request_id)

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