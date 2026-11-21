
from department import Department 
from position import Position


class DepartmentManager:
    def __init__(self):
        self.departments = {} 
        self.positions = {}
        
    def create_department(self, name, description, active=True):
        if name in self.departments:
            print(f"Department {name} already exist.")
            return None
        dept = Department(name, description, active)
        self.departments[name] = dept
        return dept 
    
    def view_department(self):
        if not self.departments:
            print("No departments.")
        else:
            for dept in self.departments.values():
                if dept.active == True:
                    status = "Active"
                else:
                    status = "Inactive"
            
                print(f"Department: {dept.name} | {status} | {dept.description}")

    
    def update_department(self, old_name, new_name=None, new_description=None):
        if old_name not in self.departments:
            print(f"Department {old_name} not found.")
            return False

        dept = self.departments[old_name]

        if new_description is not None:
            dept.description = new_description

        
        if new_name and new_name != old_name:
            if new_name in self.departments:
                print(f"Cannot rename: {new_name} already exist.")
                return False
            dept.name = new_name
            self.departments[new_name] = self.departments.pop(old_name)

        return True
    
    def find_department(self, name):
        if name in self.departments:
            return self.departments[name].name
        return None
    
    def deactivate_department(self, dept_name):
        if dept_name in self.departments:
            self.departments[dept_name].active = False
            return True
        print(f"Department {dept_name} not found.")
        return False
    
    def create_position(self, name, description, active=True):
        if name in self.positions:
            print(f"Position {name} already exist.")
            return None
        pos = Position(name, description, active)
        self.positions[name] = pos
        return pos

    def view_position(self):
        if not self.positions:
            print("No positions.")
            return
        for pos in self.positions.values():
            if pos.active==True:
                status="Active"
            else:
                status = "Inactive"
                
            print(f"Position: {pos.name} | {status} | {pos.description}")
            

    def update_position(self, old_name, new_name=None, new_description=None):
        if old_name not in self.positions:
            print(f"Position {old_name} not found.")
            return False

        pos = self.positions[old_name]

        if new_description is not None:
            pos.description = new_description

       
        if new_name and new_name != old_name:
            if new_name in self.positions:
                print(f"Cannot rename: {new_name} already exist.")
                return False
            pos.name = new_name
            self.positions[new_name] = self.positions.pop(old_name)

        return True

    def deactivate_position(self, position_name):
        if position_name in self.positions:
            self.positions[position_name].active = False
            return True
        print(f"Position {position_name} not found.")
        return False

    def find_position(self, name):
        if name in self.positions:
            return self.positions[name].name
        return None