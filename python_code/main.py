import math
import random


# Write your code here
def print_list(input_list):
    for a in input_list:
        print(a, end=" ")
    print()


# Reverse Linked List with pair
class ReverseLinkedList:
    stack = []
    result = []

    def reverse_link_list(self):
        n = int(input())
        val_list = input().split(' ')
        index = 0
        while n > 0:
            a = int(val_list[index])
            index = index + 1
            if a % 2 == 0:
                self.stack.append(a)
            else:
                s = len(self.stack)
                while s > 0:
                    self.result.append(self.stack.pop())
                    s = s - 1
                self.result.append(a)
            n = n - 1

        s = len(self.stack)
        while s > 0:
            self.result.append(self.stack.pop())
            s = s - 1
        print_list(self.result)


# Write your code here
def print_list_new(input_list):
    for a in input_list:
        print(a)


def maximumBorders():
    test_case = int(input())
    result = []
    while test_case > 0:
        row_col = input().split(' ')
        row = int(row_col[0])
        Max = 0
        for i in range(0, row):
            print(" when  i = %d" % i)
            input_str = input()
            print(input_str)
            Max = max(list(input_str).count('#'), Max)

        result.append(Max)
        test_case = test_case - 1
    print_list_new(result)


def isPerfectSquare(x):
    if x >= 0:
        sr = math.sqrt(x)
        return (sr * sr) == float(x)
    return False


def isInteger(val):
    if val.isdigit():
        return True
    elif "." in val:
        str_list = val.split(".")
        if str_list[1] == "0":
            return True
    return False


def generate_abcd_value():
    try:
        A = random.randint(1, 5)
        B = random.randint(1, 5)
        C = random.randint(-5, 5)
        D = random.randint(-5, 5)
        X1 = (-B - 2)
        X2 = (-B - 1)
        # X3 = (-B + 1)
        X3 = 0
        X4 = (A + 1)
        X5 = (A + 2)

        Y1 = ((2 * A) + (2 * B) + 4)
        Y2 = (A + B + 1)
        # Y3 = (-A - B + 1)
        Y3 = -1 * A * B
        Y4 = (A + B + 1)
        Y5 = ((2 * A) + (2 * B) + 4)

        Disc = math.sqrt(((B - A) * (B - A)) + 4 * ((A * B) + C))
        Root_1 = (-(B - A) + Disc) / 2
        Root_2 = (-(B - A) - Disc) / 2

        Y_value = (D * D) + (B - A) * D - (A * B)

        if isInteger(str(Root_1)) and isInteger(str(Root_2)) and int(Root_1) < 30 and int(Root_2) < 30 and int(
                Root_1) != int(Root_2):
            if B - A != 0 and B - A > 0:
                if D != X1 and D != X2 and D != X3 and D != X4 and D != X5 and D != int(Root_1) and D != int(Root_2):
                    if C != Y1 and C != Y2 and C != Y3 and C != Y_value and Y_value < 30:
                        print(A, B, C, D)
                        generate_abcd_value()
                    else:
                        generate_abcd_value()
                else:
                    generate_abcd_value()
            else:
                generate_abcd_value()
        else:
            generate_abcd_value()
    except:
        generate_abcd_value()


def getLastDigit(number):
    return number % 10


def divisibleByTen(number_str):
    return "Yes" if int(number_str) % 10 == 0 else "No"


N = int(input())
data = [int(x) for x in input().split()]
temp_value = ""
for val in data:
    temp_value = temp_value + str(getLastDigit(val))
print(divisibleByTen(temp_value))
