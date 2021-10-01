class Employee:
    increment = 1.5

    def __init__(self, fname, lname, salary):
        self.fname = fname
        self.lname = lname
        self.salary = salary

    def salaryIncrement(self):
        self.salary = self.salary * self.increment

    # here we are adding decorator for classmate
    @classmethod
    def increaseIncrement(cls, increment):
        cls.increment = increment

    # alternative constructor
    @classmethod
    def addEmplyDetails(cls, empString):
        fname, lname, salary = empString.split("-")
        return cls(fname, lname, salary)

    # staticmethod we can call this methods without any object(independent function)
    @staticmethod
    def isOpen(day):
        if day == "sunday" or day == "Saturday":
            return "office close"
        else:
            return "office open"


# inheritance
class Programmer(Employee):
    def __init__(self, fname, lname, salary, pro, exp):
        super().__init__(fname, lname, salary)
        self.pro = pro
        self.exp = exp

    def salaryIncrement(self):
        self.salary = self.salary * self.increment + 0.2

    # Dunder methods

    def __add__(self, other):
        return self.salary + other.salary

    def __repr__(self):
        return "Programer({},{},{})".format(self.fname, self.lname, self.salary)

    def __str__(self):
        return "The name : " + self.fname


class Car:
    wheel = 4

    def __init__(self):
        self.brand = "BMW"
        self.avg = 20

