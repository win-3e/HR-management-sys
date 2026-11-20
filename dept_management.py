
import Department from department


class DepartmentManager:
    def __init__(self):
        self.departments = {} 
        self.positions = {}
        
    def create_department(self, name, description, active=True):
        if name in self.departments:
            print(f"Department '{name}' already exists.")
            return None
        dept = Department(name, description, active)
        self.departments[name] = dept
        return dept    