from db import *
import re

class Poll:
    def __init__(self, id: int, activation: int, title: str, options: list) -> None:
        self.id = id
        self.activation = activation
        self.title = title
        self.options = options
        
    def participate(self, num: int) -> str:
        answer = self.options[num-1]
        return answer

class User:
    def __init__(self, id:int, email: str, password: str, cp: list, pp: list) -> None:
        self.id = id
        self.email = email
        self.password = password
        self.created_polls = cp
        self.participated_polls = pp

class Session:
    def __init__(self, user: User, system: 'System') -> None:
        self.user = user
        self.system = system
        
    def createPoll(self, title: str, num: int) -> None:
        if system.polls != []:
            idd = system.polls.index(system.polls[-1]) + 1
        else:
            idd = 0
        options = []
        for i in range(num):
            options.append(input(f"Option {i+1}: "))
        poll = Poll(idd, 1, title, options)
        print("Created")
        system.polls.append(poll)
        self.user.created_polls.append(str(poll.id))
        addPoll(poll, self.user)
        
    def showPolls(self) -> None:
        for i in system.polls:
            if i.activation == 1:
                activation = "Active"
            else:
                activation = "DeActive"   
            print(f"{i.id}. {i.title} ({activation})")
                
    def participate(self, poll: Poll) -> None:
        if poll.activation == 1:
            for j in poll.options:
                print(f"{poll.options.index(j)+1}. {j}")
            num = int(input("Which option would u choose: "))
            if num > len(poll.options)+1:
                print("Sry this option doesn't exist")
            else:
                participate(poll.id, num, self.user)
                self.user.participated_polls.append(str(poll.id))
                print("Submitted")
        else:
            print("Sry this poll is deactivated")
            
    def deletePoll(self, poll: Poll) -> None:
        if str(poll.id) in self.user.created_polls:
            self.user.created_polls.pop(self.user.created_polls.index(str(poll.id)))
            delPoll(self.user, poll.id)
            print("Deleted")
        else:
            print("This poll isn't created by you")
            
    def actPoll(self, poll: Poll) -> None:
        if str(poll.id) in self.user.created_polls:
            activation = actiPoll(poll.id)
            poll.activation = activation
            if activation == 1:
                print("Poll activated")
            else:
                print("Poll deactivated")
        else:
            print("This poll isn't created by you")
            
    def showPollReaults(self, poll: Poll) -> None:
        results = getPollResults(poll.id)
        res_list = list(results.items())
        print(poll.title)
        for i in res_list:
            print(i[0] + " --> " + i[1] + " votes")

class System:
    def __init__(self):
        self.polls: list[Poll] = getPolls()
        self.users: list[User] = getUsers()
        
    def runCLI(self):
        login = self.loginOrSignup()
        if login == True:
            while True:
                print("1. Create a new poll")
                print("2. List of polls")
                print("3. Participate in a poll")
                print("4. Delete your poll")
                print("5. Activate or deactivate your poll")
                print("6. Poll results")
                print("7. Exit")
                code = int(input())
                if code == 1:
                    title = input("Enter ur poll title: ")
                    num = int(input("Number of options: "))
                    self.s.createPoll(title, num)
                elif code == 2:
                    self.s.showPolls()
                elif code == 3:
                    pollid = int(input("Enter poll id: "))
                    for i in self.polls:
                        if i.id == pollid:
                            flag = True
                            for p in self.s.user.participated_polls:
                                if p == str(i.id):
                                    flag = False
                                    print("Sry you have participated in this poll")
                            if flag == True:
                                self.s.participate(i)
                            break
                    else:
                        print("No poll found")
                elif code == 4:
                    pollid = int(input("Enter your poll id: "))
                    for i in self.polls:
                        if i.id == pollid:
                            self.s.deletePoll(i)
                            break
                    else:
                        print("No poll found")
                elif code == 5:
                    pollid = int(input("Enter your poll id: "))
                    for i in self.polls:
                        if i.id == pollid:
                            self.s.actPoll(i)
                            break
                    else:
                        print("No poll found")
                elif code == 6:
                    pollid = int(input("Enter your poll id: "))
                    for i in self.polls:
                        if i.id == pollid:
                            self.s.showPollReaults(i)
                            break
                    else:
                        print("No poll found")
                else:
                    break
    
    def loginOrSignup(self):
        print("1. Login")
        print("2. Signup")
        option = int(input("Enter your option: "))
        if option == 1:
            email = input("Email: ")
            password = input("Password: ")
            for u in self.users:
                if u.email == email and u.password == password:
                    self.s = Session(u, self)
                    return True
            else:
                print("Wrong email or password")
        elif option == 2:
            while True:
                email = input("Email: ")
                if self.checkEmail(email) == True:
                    break
                else:
                    print("Wrong email")
            while True:
                password = input("Password: ")
                if self.checkPassword(password) == True:
                    break
                else:
                    print("Pick up a stronger password")
            while True:
                repassword = input("Retype password: ")
                if repassword == password:
                    break
                else:
                    print("passwords do not match")
            if self.users != []:
                user = User(self.users.index(self.users[-1])+1, email, password, "", "")
            else:
                user = User(0, email, password, "", "")
            self.users.append(user)
            addUser(user)
            self.s = Session(user, self)
            return True
    
    def checkEmail(self, email) -> bool:
        regex = '^[A-Za-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            return True
        else:
            return False
        
    def checkPassword(self, password) -> bool:
        regex  = '^(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if re.search(regex, password):
            return True
        else:
            return False

if __name__ == "__main__":
    system = System()
    system.runCLI()