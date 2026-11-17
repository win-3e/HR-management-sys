class User:
    def __init__(self, emp_id, username, password, role, active = True):
        self.emp_id = emp_id
        self.username = username
        self.password = password
        self.role = role
        self.active = active 
    
class UserManagement:
    def __init__(self):
        self.users = {}

    def create_user(self):
        employee_id = input("Enter the employee's id: ")
        if employee_id in employee_id:
            pass
            user_input = input("Enter your username: ").strip()
            pass_input = input("Enter your password: ").strip()
            new_user = User(100, user_input, pass_input, "Admin")
        self.users[user_input] = pass_input

    def log_in(self):
       user_input = input("Enter your username: ").strip()
       pass_input = input("Enter your password: ").strip()
       if user_input in self.users and self.users.get(user_input) == pass_input:
            print(f"Login successful! welcome {user_input}")
       else:
            print("wrong username or password")
    
    def log_out(self):
        pass

    def assign_role(self):
        pass
    
    def check_role(self):
        pass

    def deactivate_user(self, emp_id):
        pass

system = UserManagement()
system.create_user()
dict = system.users
print(dict)

