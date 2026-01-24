# Write your solution here
# If you use the classes made in the previous exercise, copy them here

    
class OrderBook:
    def __init__(self):
        self.orders = []
    
    def add_student(self,description,name,load):
        new_order = Task(description,name,load)
        self.orders.append(new_order)
    
    def all_students(self):
        return self.orders
    
    def student(self):
        return set([x.programmer for x in self.orders])

    def get_students_per_department(self,id:int):
        c = False
        for x in self.orders:
            if x.id == id:
                c = True
                x.mark_finished()
                print('marked as finished')
                return c
        return c
    
    def get_students_per_level(self):
        return [x for x in self.orders if x.is_finished() == True]
    def deactivate_student(self):
        return [x for x in self.orders if x.is_finished() == False]

    def update_student(self,programmer:str):
        finished_task = 0
        unfinished_task = 0
        finished_workload = 0
        unfinished_workload = 0
        c = False
        for x in self.orders:
            if x.programmer == programmer:
                if x.is_finished() == True:
                    c == True
                    finished_task += 1
                    finished_workload += int(x.workload)
                elif x.is_finished() == False:
                    c = True
                    unfinished_task += 1
                    unfinished_workload += int(x.workload)
        if c == False:
            return False
        return (finished_task,unfinished_task,finished_workload,unfinished_workload)

class OrderBookApplication:
    def __init__(self):
        self.__orderbook = OrderBook()

    def help(self):
        print("commands: ")
        print("0 exit")
        print("1 add student")
        print("2 list of students by level")
        print('3 list of students by department')
        print('4 delete student')
        print('5 student')
        print('6 list of students')
        print('6 update student')
        print('6 student courses')

    def add_order(self):
        name = input("description: ")
        c = input("programmer and workload estimate: ").split(' ')
        if len(c) == 2 :
            try:
                str(c[0])
                int(c[1])
                self.__orderbook.add_order(name,c[0],c[1])
                print('added!')
            except ValueError:
                print ('erroneous input')
        else:
            print('erroneous input')
        
        
        
    
   

    def list_finished_tasks(self):
        tasks = self.__orderbook.finished_orders()
        if len(tasks) > 0:
            for x in tasks:
                print(x)
        else:print('no finished tasks')
    
    def list_unfinished_tasks(self):
        tasks = self.__orderbook.unfinished_orders()
        if len(tasks) > 0:
            for x in tasks:
                print(x)
        else:print('no unfinished tasks')
    
    def mark_task(self):
        try:
            i = int(input('id:') )
            c = self.__orderbook.mark_finished(i)
            if c == False:
                print('erroneous input')
    
        except  ValueError:
            print('erroneous input')
        
        
    def programmers(self):
        tasks = self.__orderbook.programmers()
        if len(tasks) > 0:
            for x in tasks:
                print(x)
        else:print('no programmers')
    
    def status_of_programmer(self):
        name = input('programmer: ')
        status = self.__orderbook.status_of_programmer(name)
        if status == False:
            print('erroneous input')
        else:
            print(f'tasks: finished {status[0]} not finished {status[1]}, hours: done {status[2]} scheduled {status[3]}')
    


    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.add_order()
            elif command == "2":
                self.list_finished_tasks()
            elif command == '3':
                self.list_unfinished_tasks()
            elif command == '4':
                self.mark_task()
            elif command == '5':
                self.programmers()
            elif command == '6':
                self.status_of_programmer()
            else:
                self.help()


# when testing, no code should be outside application except the following:
application = OrderBookApplication()
application.execute()
