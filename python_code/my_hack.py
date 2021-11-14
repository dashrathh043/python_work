

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Company:
    def __init__(self, cname, name, age):
        Person.__init__(self, name, age)
        self.cname = cname


companyTypeList = []
n = 5
for i in range(0, n):
    com = Company("Amazon", "Ram", 12)
    companyTypeList.append(com)

print(companyTypeList)
