def showOutput(data):
    try:
        file = open("output.txt","a")
        file.writelines(str(data))
        file.write("\n")
        file.close()
    except:
        return "Not able to write in output.txt file"

# Problem-1 word break problem
# By recursion
def wordBreakUsingRecusion(wordList, word):
    print(word)
    if word == '':
        print(word)
        return True
    else:

        return any([word[:i] in wordList and wordBreakUsingRecusion(wordList,word[i:]) for i in range(1,len(word)+1)])


def wordBreakUsingRecusionType2(wordList,word):
    showOutput("word : "+word)
    if word == "":
        return True
    for i in range(1,len(word)+1):
        showOutput("index : "+str(i))
        showOutput("break-1 :"+word[0:i])
        showOutput("break-2 :"+word[i:len(word)])
        booleanCase1 = word[0:i] in wordList
        booleanCase2 = wordBreakUsingRecusionType2(wordList,word[i:len(word)])
        if booleanCase1 and booleanCase2:
            showOutput("Case-True :"+word)
            return True
    showOutput("Outside Rec : "+word)
    return False



inputString = "ilikegoogle"
print(inputString[15:])
dictString = ["i","google","like"]
print(wordBreakUsingRecusionType2(dictString,"ilikegoogle"))




