import sys
def showOutput(data):
    try:
        file = open("output.txt","a")
        file.write("========== Output ================\n")
        file.write(str(data))
        file.write("\n\n")
        file.close()
    except:
        return "Not able to write in output.txt file"

if __name__ == '__main__':
    function_name_and_args = sys.argv[1]
    for index in range(len(function_name_and_args)):
        try:
            exec(function_name_and_args[index])
        except:
            globals()[function_name_and_args[index]] = str(
                function_name_and_args[index])
    eval(function_name_and_args)
