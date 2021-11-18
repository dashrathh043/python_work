def allSubsequenceOfString(input_str,output_str,result_list):
    #print("input : "+input_str)
    if len(input_str) == 0:
        if len(output_str)>0:
            result_list.append(output_str)
        return
    allSubsequenceOfString(input_str[1:], output_str,result_list)
    allSubsequenceOfString(input_str[1:], output_str + input_str[0],result_list)



result_list = []
allSubsequenceOfString("ilikedog","",result_list)
Dict = ["i","like","am","boy","e","o","dog","cat","g"]
print(result_list.index("dog"))
