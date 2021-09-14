import re
'''
Let’s assume you want to match any six-letter word inside the following target string
target_string = "Jessa loves Python and pandas"
If you use a match() method to match any six-letter word inside the string you will get None because it returns a match only if the pattern is located
at the beginning of the string. And as we can see the six-letter word is not present at the start.
So to match the regex pattern anywhere in the string you need to use either search() or findall() method of a RE module
'''
def all_one():
    target_string = "dea loves Python and pandas"
    pattern = r"\w{6}"
    # match method()
    result = re.match(pattern, target_string)
    print(result)
    # search()method
    result = re.search(pattern, target_string)
    print(result.group())
    # findall()method
    result = re.findall(pattern, target_string)
    print(result)

def match_last():
    target_string = "Emma is a 1234 basketball player who was born on June 17, 1993 1994"
    # Match at the end
    result = re.search(r"\d{4}$", target_string)
    print(result)
    print("Match num:", result.group())

def understanding_match_object():
    string = "Deepa and shila"
    ## Match five-letter word
    result = re.match(r"\b\w{5}\b", string)
    # printing entire match object
    print(result)
    # Extract Matching value
    print(result.group())
    # Start index of a match
    print("start index is :", result.start())
    # End index of a match
    print("End index:", result.end())
    # Start and end index of a match
    position = result.span()
    print(position)
    # Use span to retrieve the matching string
    print(string[position[0]:position[1]])

# string starts with letter 'ch1' ends with letter 'ch2'
def starts_ends_with(ch1,ch2,str1):
    res = re.match(r'^('+ch1+').*('+ch2+')$', str1,re.IGNORECASE)
    if res:
        print(res.group())
    else:
        print('None')
'''
some common regex matching operations such as
Match any character
Match number
Match digits
match special characters
'''
def some_common_regex():
    string = "Deepali 21 25"
    # match any character
    print(re.match(r'.', string))
    # match all digit
    print(re.findall(r"\d", string))
    # match all numbers
    # + indicate 1 or more occurence of \d
    print(re.findall(r"\d+", string))
    # match all special characters and symbol
    str2 = "Deep@li $$$$@%^"
    print(re.findall(r"\W", str2))

starts_ends_with('d','h',"Dashrath")