import re
import math
from spellchecker import SpellChecker
from fuzzywuzzy import fuzz
from num2words import num2words
from sympy import simplify
from latex2sympy2 import latex2sympy


# input = [str1,str2]
# output = str1+str2(Concatenation by new line)
def combine_all_string(input_string_list):
    final_output = ""
    for index in range(len(input_string_list)):
        if len(input_string_list[index]) > 0:
            final_output = final_output + input_string_list[index] + "<br>"
    return final_output


# input = [string(Find the value of latex(2+3).),string(Divide the value latex(10/5))]
# output = [string(Find the value of .),string(Divide the value)]
def fetch_only_string(input_string):
    final_string = re.sub(",", " ", input_string)
    latex_string_list = get_all_string_by_break_string_from_given_string('latex', final_string)
    for index in range(0, len(latex_string_list)):
        final_string = final_string.replace(latex_string_list[index], " ")
    return get_all_string_by_break_string_from_given_string('string', final_string)


# input = [string(Find the value of latex(2+3).),string(Divide the value latex(10/5))]
# output = [latex(2+3),latex(10/5)]
def fetch_only_latex_string(input_string):
    final_latex_string = []
    latex_string_list = get_all_string_by_break_string_from_given_string('latex', input_string)
    for index in range(0, len(latex_string_list)):
        final_latex_string.append(re.sub(r"\s|~|\\quad|\\qquad|\\", "", latex_string_list[index]))
    return final_latex_string


def get_error_msg(input_string):
    input_string = input_string.strip()
    if input_string is None:
        final_question_error_msg = "No Error<br>"
    elif len(input_string) == 0:
        final_question_error_msg = "No Error<br>"
    else:
        final_question_error_msg = input_string
    return final_question_error_msg


def get_latex_string_utility(index, input_string):
    open_count = 0
    final_output = ""
    while index < len(input_string):
        if input_string[index] != '(' and input_string[index] != ')':
            final_output = final_output + input_string[index]
            index = index + 1
        elif input_string[index] == '(':
            final_output = final_output + input_string[index]
            open_count = open_count + 1
            index = index + 1
        elif input_string[index] == ')':
            final_output = final_output + input_string[index]
            open_count = open_count - 1
            index = index + 1
            if open_count == 0:
                break
    return final_output, index


def get_all_string_by_break_string_from_given_string(break_string, input_string):
    final_latex_list = []
    pattern_of_latex = re.compile(break_string)
    obj_list = pattern_of_latex.finditer(input_string)
    for latex_val in obj_list:
        latex_string, latex_end_index = get_latex_string_utility(latex_val.start(), input_string)
        final_latex_list.append(latex_string)
    return final_latex_list


def check_input_string_have_both_frac_and_dfrac(input_string):
    after_space_removed_str = re.sub(r"\s|~|\\quad|\\qquad|\\", "", input_string)
    pattern_for_frac = re.compile(
        r'\bfrac\b\{[A-Za-z0-9+-]+\}\{[A-Za-z0-9+-]+\}|\bfrac\b\{\([A-Za-z0-9+-]+\)\}\{\([A-Za-z0-9+-]+\)\}|\bfrac\b\{[A-Za-z0-9+-]+\}\{\([A-Za-z0-9+-]+\)\}|\bfrac\b\{[A-Za-z0-9+-]+\}\{\([A-Za-z0-9+-]+\)\}')
    pattern_for_dfrac = re.compile(
        r'\bdfrac\b\{[A-Za-z0-9+-]+\}\{[A-Za-z0-9+-]+\}|\bdfrac\b\{\([A-Za-z0-9+-]+\)\}\{\([A-Za-z0-9+-]+\)\}|\bdfrac\b\{[A-Za-z0-9+-]+\}\{\([A-Za-z0-9+-]+\)\}|\bdfrac\b\{[A-Za-z0-9+-]+\}\{\([A-Za-z0-9+-]+\)\}')
    frac_list = pattern_for_frac.findall(after_space_removed_str)
    dfrac_list = pattern_for_dfrac.findall(after_space_removed_str)
    final_list = []
    if len(frac_list) > 0 and len(dfrac_list) > 0:
        final_list.append(str(frac_list) + ":" + str(dfrac_list))
    if len(final_list) > 0:
        finalOutput = "<p>frac and dfrac both used</p><br>" + '[%s]' % ', '.join(
            map(str, final_list)) + ""
    else:
        finalOutput = ""
    return finalOutput


def call_tester_to_check_font_issue_in_string(input_string):
    Line_start_with = "<p> Font issue:<p><br>"
    result_string_1 = check_input_string_have_both_frac_and_dfrac(input_string)
    final_output = combine_all_string([result_string_1])
    return final_output


def call_tester_to_check_latex_issue_in_string_utility(input_string):
    final_list = []
    string_list = fetch_only_string(input_string)
    issue_list = ["=", "^", "+", "-", "*"]
    for index in range(0, len(string_list)):
        text_inside_string = string_list[index][len("string("):-len(")")]
        current_output = []
        if len(text_inside_string) > 0:
            word_list = re.split(r"[\s]", text_inside_string)
            for word in word_list:
                if len(word) > 0:
                    for issue_str in issue_list:
                        if issue_str in word:
                            current_output.append(word)
                        elif word.isdigit():
                            current_output.append(word)
                        elif '\\' in word:
                            current_output.append(word)
                        elif 'x' in word and any(map(str.isdigit, word)):
                            current_output.append(word)
                        elif 'X' in word and any(map(str.isdigit, word)):
                            current_output.append(word)
                        elif 'X' == word:
                            current_output.append(word)
                        elif 'x' == word:
                            current_output.append(word)
                    if len(current_output) > 0:
                        final_list.append(current_output[0])
                        current_output = []
    if len(final_list) > 0:
        finalOutput = "<p>Latex issue</p><br>" + '[%s]' % ', '.join(
            map(str, final_list)) + ""
    else:
        finalOutput = ""
    return finalOutput


def call_tester_to_check_latex_issue_in_string(input_string):
    try:
        return call_tester_to_check_latex_issue_in_string_utility(input_string)
    except Exception:
        return "<p>Something Error in call_tester_to_check_latex_issue_in_string<br></p>"


# checking pi handler
def call_tester_to_check_pi_handler_is_used_in_final_answer_if_pi_used_in_question(question_string, final_answer):
    question_check = False
    answer_check = False
    if '\\pi' in question_string:
        question_check = True
        if 'pi_handler' in final_answer:
            answer_check = True
    if question_check == True and answer_check == True:
        return "pi_handler methods used"
    elif question_check == True and answer_check == False:
        return "pi_handler methods not used in final_answer"
    else:
        return ""


def call_tester_to_check_possible_convert_frac_value_to_lowest_term(input_string):
    after_space_removed_str = re.sub(r"\s|~|\\quad|\\qquad|\\", "", input_string)
    pattern_of_frac = re.compile(r'\bdfrac\b{[-+]?\d+}{[-+]?\d+}|\bfrac\b{[-+]?\d+}{[-+]?\d+}')
    frac_list = pattern_of_frac.findall(after_space_removed_str)
    final_list = []
    for frac_index in range(0, len(frac_list)):
        pat = r"{[-+]?\d+}"
        curly_paren = re.compile(pat)
        frac_num_and_dem_list = curly_paren.findall(frac_list[frac_index])
        numerator_value = frac_num_and_dem_list[0][1:-len('}')]
        denomator_value = frac_num_and_dem_list[1][1:-len('}')]
        gcd = math.gcd(int(numerator_value), int(denomator_value))
        if gcd > 1:
            final_list.append(frac_list[frac_index])
    if len(final_list) > 0:
        finalOutput = "<p>Lowest term issue</p><br>" + '[%s]' % ', '.join(
            map(str, final_list)) + ""
    else:
        finalOutput = ""
    return finalOutput


# input_string = [string(1x+5)]
# output = Error_msg for 1x
def call_tester_to_check_if_any_expression_with_one_coefficient(input_string):
    final_list = []
    input_string = input_string.replace("\\", "\\\\")
    while re.search("\\b1[a-z]\\b", input_string):
        X = re.search("\\b1[a-z]\\b", input_string)
        final_list.append(input_string[X.start():X.end()])
        char = X.group().replace("1", "")
        pos = X.start()
        input_string = input_string[:pos] + char + input_string[pos + 2:]
    if len(final_list) > 0:
        finalOutput = "<p>1 coefficient issue</p><br>" + '[%s]' % ', '.join(
            map(str, final_list)) + ""
    else:
        finalOutput = ""
    return finalOutput


def check_algebra_answer_type_should_be_in_last(input_string):
    check = True
    listOfAllAnswerType = ["textbox", "checkbox", "type(fraction)", "exponential", "improper_fraction", "standard_form",
                           "objective_answer_types", "input_list"]
    algebraAnswerType = "algebra_form"
    ansIndexList = []
    for ansType in listOfAllAnswerType:
        tempIndexList = []
        allIndexOfAnsType = re.finditer(ansType, input_string)
        for indexOneByOne in allIndexOfAnsType:
            tempIndexList.append(indexOneByOne.start())
        if len(tempIndexList) > 0:
            ansIndexList.append(max(tempIndexList))

    algebraAnswerTypePointer = re.finditer(algebraAnswerType, input_string)
    tempIndexList = []
    for indexOneByOne in algebraAnswerTypePointer:
        tempIndexList.append(indexOneByOne.start())
    if len(tempIndexList) > 0:
        minIndex = min(tempIndexList)
    else:
        minIndex = -1
    for indexValue in ansIndexList:
        if indexValue > minIndex:
            check = False
    if check is False and minIndex != -1:
        final_output = "<p> Algebra answer type should be in the last </p><br>"
    else:
        final_output = ""

    return final_output


# input = "23.00 -23.001 1.00 23.00"
# output = [23.00,1.00,23.00]
def find_decimal_end_with_dot_zero(input_string):
    reObject = re.compile(r"\d+[.][0-9]+|-\d+[.][0-9]+")
    allDecimalList = reObject.findall(input_string)
    finalDecimalList = []
    for decimal in allDecimalList:
        splDecimal = decimal.split(".")
        if len(splDecimal[1].replace("0", "")) == 0:
            finalDecimalList.append(decimal)
    if len(finalDecimalList) > 0:
        OutputStr = "<p>Remove zero (.0) from below decimal value:</p><br>" + str(finalDecimalList) + "<br>"
    else:
        OutputStr = ""
    return OutputStr


def check_spelling_mistake_in_string(input_string):
    suggested_correct_words_str = ""
    only_fetched_string_list = fetch_only_string(input_string)
    only_fetched_string = " "
    only_fetched_string = only_fetched_string.join(only_fetched_string_list)
    only_fetched_string_without_symbols = re.sub("[^a-zA-Z]+", " ", only_fetched_string)
    only_fetched_string_without_symbols_list = [str(word) for word in only_fetched_string_without_symbols.split()]
    spell_checker = SpellChecker()
    for words in range(0, len(only_fetched_string_without_symbols_list)):
        if only_fetched_string_without_symbols_list[words] not in spell_checker.candidates(
                only_fetched_string_without_symbols_list[words]):
            if len(only_fetched_string_without_symbols_list[words]) >= 3:
                suggested_correct_words_str = suggested_correct_words_str + f'{only_fetched_string_without_symbols_list[words]} : {spell_checker.candidates(only_fetched_string_without_symbols_list[words])}' + "<br>"
    if len(suggested_correct_words_str) > 0:
        finalOutput = "<p> Spelling Error </p><br>" + suggested_correct_words_str
    else:
        finalOutput = ""
    return finalOutput


# input = [string(latex(5+-4))]
def check_if_two_or_more_operator_are_consecutive(input_string):
    reObject = re.compile("[0-9]+[-][+][0-9]+|[0-9]+[+][-][0-9]+|[0-9]+[*][-][0-9]+|[0-9]+[-][*][0-9]+")
    mixOperatorList = reObject.findall(input_string)
    if len(mixOperatorList) > 0:
        finalOutput = "<p> Mixed operator Error </p><br>" + '[%s]' % ', '.join(map(str, mixOperatorList)) + ""
    else:
        finalOutput = ""
    return finalOutput


def getIndexOfElementInList(element, element_list):
    try:
        return element_list.index(element)
    except:
        return -1


def check_none_of_these_option_should_in_last(input_string):
    tempOutput = []
    if input_string.find("objective_answer_types") > -1 and input_string.find(
            "None of these") > -1 or input_string.find("objective_answer_types") > -1 and input_string.find(
        "None of These") > -1 or input_string.find("objective_answer_types") > -1 and input_string.find(
        "None of the above") > -1:
        objectiveAnswerTypeList = get_all_string_by_break_string_from_given_string('objective_answer_types',
                                                                                   input_string)
        for objAnsType in objectiveAnswerTypeList:
            optionList = get_all_string_by_break_string_from_given_string('string', objAnsType)
            finalOptionList = optionList[1::2]
            indexList = [getIndexOfElementInList("string(None of these)", finalOptionList),
                         getIndexOfElementInList("string(None of These)", finalOptionList),
                         getIndexOfElementInList("string(None of the above)", finalOptionList)]
            finalIndex = [x for x in indexList if x > 0] or None
            if len(finalOptionList) - 1 != finalIndex[0]:
                tempOutput.append(finalOptionList[finalIndex[0]])
    if len(tempOutput) > 0:
        finalOutput = "<p> None of These option should be in the last</p><br>" + '[%s]' % ', '.join(
            map(str, tempOutput)) + ""
    else:
        finalOutput = ""
    return finalOutput


# All cases not handled here.
# input = [string(latex(1 \\times \\frac{-1}{2})),string(latex(1 \\times \\frac{1}{2}))]
# ouput = [1 \\times \\frac{-1}{2} ]

# Handled case are
# 1) p + \\frac{-1}{2} where p be any value postive or negative like : -2 or 2
# 2) p \\times \\frac{-1}{2}
# 3) p - \\frac{-1}{2}
def check_possible_consecutive_sign(input_string):
    frac_list = []
    input_string = re.sub(r"dfrac", "frac", input_string)
    after_space_removed_str = re.sub(r"\s|~|\\quad|\\qquad|\\", "", input_string)
    # pattern_of_frac = re.compile(r'(?:\d+[+-]{2,}\d{0,}|\d+[\]{2,}times[\]{2,}(?:frac|dfrac){[+-]+\d+}{[+-]?\d+})')
    pattern_of_frac = re.compile(
        r'(-?\d+?timesfrac\{-\d+\}\{[-+]?\d+\}|-?\d+?\+frac\{-\d+\}\{[-+]?\d+\}|-?\d+?\-frac\{-\d+\}\{[-+]?\d+\})')
    frac_list = pattern_of_frac.findall(after_space_removed_str)
    if len(frac_list) > 0:
        finalOutput = "<p> Mixed operator Error </p><br>" + '[%s]' % ', '.join(map(str, frac_list)) + "<br>"
    else:
        finalOutput = ""
    return finalOutput


# input = [string(latex(1^{nd})),string(latex(1^{pqr} 2^{rd} )),string(latex(1^{st})),]
# output = [1^{nd},2^{rd}]
def check_format_of_ordinal_number(input_string):
    reObject = re.compile("\d+\^\{[a-z][a-z]\}")
    latex_list = reObject.findall(input_string)
    wrong_strings = []
    for lat in latex_list:
        st = lat.rpartition('^')
        if st is not None:
            expected_ordinals = num2words(int(st[0]), to="ordinal_num")
            expected_ordinals = expected_ordinals[-2] + expected_ordinals[-1]
            given_ordinals = st[-1][-3] + st[-1][-2]
            if expected_ordinals not in given_ordinals:
                wrong_strings.append(st[0] + st[1] + st[2])
            st = None
    if len(wrong_strings) > 0:
        finalOutput = "<p> Wrong power number </p><br>" + '[%s]' % ', '.join(map(str, wrong_strings)) + ""
    else:
        finalOutput = ""
    return finalOutput


# check lowest term like : \\frac{12(a+b)}{24}
def find_lowest_term_isuue(input_string):
    after_space_removed_str = re.sub(r"\s|~|\\quad|\\qquad|\\", "", input_string)
    pattern_of_frac = re.compile(
        r'(?:frac|dfrac){[-+]?\d+[(]?\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[)]?}{[-+]?\d+[(]?\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[)]?}')
    frac_list = pattern_of_frac.findall(after_space_removed_str)
    final_list = []
    for frac_index in range(0, len(frac_list)):
        pat = r"{[+-]?\d+[(]?\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[-+]*\d*[a-z A-Z]*[)]?}"
        curly_paren = re.compile(pat)
        frac_num_and_dem_list = curly_paren.findall(frac_list[frac_index])
        numerator_value = frac_num_and_dem_list[0][1:-len('}')].split('(')[0]
        denomator_value = frac_num_and_dem_list[1][1:-len('}')].split('(')[0]

        isInt = True
        try:
            int(numerator_value)
            int(denomator_value)
        except ValueError:
            isInt = False
        if isInt:
            numerator_value = int(numerator_value)
            denomator_value = int(denomator_value)
            gcd = math.gcd(abs(int(numerator_value)), abs(int(denomator_value)))
            if gcd != 1:
                final_list.append(frac_list[frac_index])
    if len(final_list) > 0:
        finalOutput = "<p> Lowest term issue </p><br>" + '[%s]' % ', '.join(map(str, final_list)) + ""
    else:
        finalOutput = ""
    return finalOutput


def get_string_match_percentage(Str_A, Str_B):
    ratio = fuzz.ratio(Str_A.lower(), Str_B.lower())
    return ratio


def match_last_two_steps_of_solution_steps(string):
    try:
        lst = get_all_string_by_break_string_from_given_string('string', string)
        if len(lst) > 2:
            without_string_list1 = lst[-2][len("string("):-len(")")]
            without_string_list1 = re.sub("latex", "", without_string_list1)
            without_string_list1 = re.sub(r"\s", "", without_string_list1)
            without_string_list2 = lst[-1][len("string("):-len(")")]
            without_string_list2 = re.sub("latex", "", without_string_list2)
            without_string_list2 = re.sub(r"\s", "", without_string_list2)
            percentage = get_string_match_percentage(without_string_list1.strip(), without_string_list2.strip())
            if percentage >= 90:
                finalOutput = "<p> Last two solution steps are same.</p><br>"
            else:
                finalOutput = ""
        return finalOutput
    except:
        return ""


def check_two_string_is_equal(str1, str2):
    str1 = str1.strip()
    str1 = str1[len("string("):-len(")")]
    str1 = re.sub(r"\s", "", str1)

    str2 = str2.strip()
    str2 = str2[len("string("):-len(")")]
    str2 = re.sub(r"\s", "", str2)
    if str1 == str2:
        return True
    return False


def check_objective_answer_type_have_duplicate_option(input_string):
    tempOutput = []
    objectiveAnswerTypeList = get_all_string_by_break_string_from_given_string('objective_answer_types', input_string)
    for objAnsType in objectiveAnswerTypeList:
        # optionList = get_all_string_by_break_string_from_given_string('string', objAnsType)
        optionList = fetch_only_string(objAnsType)
        finalOptionList = optionList[1::2]
        for ithIndex in range(0, len(finalOptionList)):
            jthIndex = ithIndex + 1
            while jthIndex < len(finalOptionList):
                str1 = finalOptionList[ithIndex][len("string("):-len(")")].strip()
                str2 = finalOptionList[jthIndex][len("string("):-len(")")].strip()
                if len(str1) > 0 and len(str2) > 0 and check_two_string_is_equal(str1, str2):
                    tempOutput.append(finalOptionList[ithIndex] + ":" + finalOptionList[jthIndex] + "")
                jthIndex = jthIndex + 1
    if len(tempOutput) > 0:
        finalOutput = "<p> Duplicate option</p><br>" + '[%s]' % ', '.join(
            map(str, tempOutput)) + ""
    else:
        finalOutput = ""
    return finalOutput


# latex_expression_1 = "\\frac{20}{10}\\pi"
# latex_expression_2 = "2\\pi"
def mathematically_two_latex_string_is_equal(latex_expression_1, latex_expression_2):
    try:
        latex_expression_1 = latex_expression_1[len("latex("):-len(")")]
        latex_expression_2 = latex_expression_2[len("latex("):-len(")")]
        latex_expression_1 = re.sub("dfrac", "frac", latex_expression_1)
        latex_expression_2 = re.sub("dfrac", "frac", latex_expression_2)
        sympy_expression_1 = latex2sympy(latex_expression_1)
        sympy_expression_2 = latex2sympy(latex_expression_2)
        if simplify(sympy_expression_1 - sympy_expression_2) == 0:
            return True
        return False
    except:
        return ""


def check_objective_answer_type_have_duplicate_option_mathematically(input_string):
    tempOutput = []
    objectiveAnswerTypeList = get_all_string_by_break_string_from_given_string('objective_answer_types', input_string)
    for objAnsType in objectiveAnswerTypeList:
        optionList = get_all_string_by_break_string_from_given_string('latex', objAnsType)
        # finalOptionList = optionList[1::2]
        finalOptionList = optionList
        for ithIndex in range(0, len(finalOptionList)):
            jthIndex = ithIndex + 1
            while jthIndex < len(finalOptionList):
                try:
                    if mathematically_two_latex_string_is_equal(finalOptionList[ithIndex], finalOptionList[jthIndex]):
                        tempOutput.append(finalOptionList[ithIndex] + ":" + finalOptionList[jthIndex] + "")
                    jthIndex = jthIndex + 1
                except:
                    return ""
    if len(tempOutput) > 0:
        finalOutput = "<p>Mathematically duplicate option</p><br>" + '[%s]' % ', '.join(
            map(str, tempOutput)) + ""
    else:
        finalOutput = ""
    return finalOutput


# check duplicate option in dropdown option
def convert_string_to_char_list(string):
    list = []
    for i in string:
        list.append(i)
    return list


def check_two_string_equal_exactly(str1, str2):
    char_list_1 = convert_string_to_char_list(str2)
    char_list_2 = convert_string_to_char_list(str1)
    ct_len_1 = len(char_list_1)
    line_len_1 = len(char_list_2)
    for i in range(0, line_len_1, 1):
        if i < ct_len_1:
            if char_list_1[i] != char_list_2[i]:
                return False
        else:
            if char_list_2[i].isdigit() or char_list_2[i].isalpha():
                return False
    return True


def check_dropdown_answer_type_have_duplicate_option(input_string):
    if input_string.find("input_list(list(") > 0:
        string_list = fetch_only_string(input_string)
        tempOutput = []
        for i in range(0, len(string_list) - 1):
            for j in range(i + 1, len(string_list)):
                if check_two_string_equal_exactly(string_list[i], string_list[j]):
                    tempOutput.append(string_list[i])

        if len(tempOutput) > 0:
            return "<p>Duplicate option in dropdown answer type</p><br>" + '[%s]' % ', '.join(
                map(str, tempOutput)) + ""
        else:
            return ""
    else:
        return ""


# check format of question string
def call_tester_to_check_format_of_question_string(question_string):
    result_string_1 = call_tester_to_check_latex_issue_in_string(question_string)
    result_string_2 = call_tester_to_check_possible_convert_frac_value_to_lowest_term(question_string)
    result_string_3 = call_tester_to_check_if_any_expression_with_one_coefficient(question_string)
    result_string_4 = call_tester_to_check_font_issue_in_string(question_string)
    result_string_5 = find_decimal_end_with_dot_zero(question_string)
    result_string_6 = check_spelling_mistake_in_string(question_string)
    result_string_7 = check_if_two_or_more_operator_are_consecutive(question_string)
    result_string_8 = check_possible_consecutive_sign(question_string)
    result_string_9 = check_format_of_ordinal_number(question_string)
    result_string_10 = find_lowest_term_isuue(question_string)
    final_output = combine_all_string(
        [result_string_1, result_string_2, result_string_3, result_string_4, result_string_5, result_string_6,
         result_string_7, result_string_8, result_string_9, result_string_10])
    return final_output


# check format of solution string
def call_tester_to_check_format_of_solution_string(solution_string):
    result_string_1 = call_tester_to_check_latex_issue_in_string(solution_string)
    result_string_2 = call_tester_to_check_possible_convert_frac_value_to_lowest_term(solution_string)
    result_string_3 = call_tester_to_check_if_any_expression_with_one_coefficient(solution_string)
    result_string_4 = call_tester_to_check_font_issue_in_string(solution_string)
    result_string_5 = find_decimal_end_with_dot_zero(solution_string)
    result_string_6 = check_spelling_mistake_in_string(solution_string)
    result_string_7 = check_if_two_or_more_operator_are_consecutive(solution_string)
    result_string_8 = check_possible_consecutive_sign(solution_string)
    result_string_9 = check_format_of_ordinal_number(solution_string)
    result_string_10 = find_lowest_term_isuue(solution_string)
    result_string_11 = match_last_two_steps_of_solution_steps(solution_string)
    final_output = combine_all_string(
        [result_string_1, result_string_2, result_string_3, result_string_4, result_string_5, result_string_6,
         result_string_7, result_string_8, result_string_9, result_string_10, result_string_11])
    return final_output


# check format of hint string
def call_tester_to_check_format_of_hint_string(hint_string):
    result_string_1 = call_tester_to_check_latex_issue_in_string(hint_string)
    result_string_2 = call_tester_to_check_possible_convert_frac_value_to_lowest_term(hint_string)
    result_string_3 = call_tester_to_check_if_any_expression_with_one_coefficient(hint_string)
    result_string_4 = call_tester_to_check_font_issue_in_string(hint_string)
    result_string_5 = find_decimal_end_with_dot_zero(hint_string)
    result_string_6 = check_spelling_mistake_in_string(hint_string)
    result_string_7 = check_if_two_or_more_operator_are_consecutive(hint_string)
    result_string_8 = check_possible_consecutive_sign(hint_string)
    result_string_9 = check_format_of_ordinal_number(hint_string)
    result_string_10 = find_lowest_term_isuue(hint_string)
    final_output = combine_all_string(
        [result_string_1, result_string_2, result_string_3, result_string_4, result_string_5, result_string_6,
         result_string_7, result_string_8, result_string_9, result_string_10])
    return final_output


# check format of answer type string
def call_tester_to_check_format_of_answer_type_string(answer_type_string):
    result_string_1 = call_tester_to_check_latex_issue_in_string(answer_type_string)
    result_string_2 = call_tester_to_check_possible_convert_frac_value_to_lowest_term(answer_type_string)
    result_string_3 = call_tester_to_check_if_any_expression_with_one_coefficient(answer_type_string)
    result_string_4 = check_algebra_answer_type_should_be_in_last(answer_type_string)
    result_string_5 = check_spelling_mistake_in_string(answer_type_string)
    result_string_6 = check_none_of_these_option_should_in_last(answer_type_string)
    result_string_7 = check_format_of_ordinal_number(answer_type_string)
    if answer_type_string.find("objective_answer_types") > -1 and answer_type_string.find("latex") > -1:
        result_string_8 = check_objective_answer_type_have_duplicate_option_mathematically(answer_type_string)
    else:
        result_string_8 = check_objective_answer_type_have_duplicate_option(answer_type_string)
    result_string_9 = check_dropdown_answer_type_have_duplicate_option(answer_type_string)
    final_output = combine_all_string(
        [result_string_1, result_string_2, result_string_3, result_string_4, result_string_5, result_string_6,
         result_string_7, result_string_8, result_string_9])
    return final_output


# check format of final answer
def call_tester_to_check_format_of_final_answer(input_string):
    result_string_1 = call_tester_to_check_possible_convert_frac_value_to_lowest_term(input_string)
    final_output = combine_all_string([result_string_1])
    return final_output


# check duplicate option in dropdown option
def convert_string_to_char_list(string):
    list = []
    for i in string:
        list.append(i)
    return list


def check_two_string_equal_exactly(str1, str2):
    str1 = re.sub("\s", "", str1)
    str2 = re.sub("\s", "", str2)
    char_str2 = convert_string_to_char_list(str2)
    char_str1 = convert_string_to_char_list(str1)
    str_len_1 = len(char_str1)
    str_len_2 = len(char_str2)
    if str_len_1 != str_len_2:
        return False
    else:
        for i in range(0, str_len_1):
            if char_str1[i] != char_str2[i]:
                return False
    return True


def check_dropdown_answer_type_have_duplicate_option(input_string):
    if input_string.find("input_list(list(") > 0:
        format_string_list = get_all_string_by_break_string_from_given_string("list", input_string)
        for dropdownanswertype in format_string_list:
            string_list = fetch_only_string(dropdownanswertype)
            tempOutput = []
            for i in range(0, len(string_list) - 1):
                for j in range(i + 1, len(string_list)):
                    if check_two_string_equal_exactly(string_list[i], string_list[j]):
                        tempOutput.append(string_list[i])
        if len(tempOutput) > 0:
            return "<p>Duplicate option in dropdown answer type</p><br>" + '[%s]' % ', '.join(
                map(str, tempOutput)) + ""
        else:
            return ""
    else:
        return ""


def call_testers(question_string, solution_string, hint_string, answer_type_string, final_answer, secondary_answer_type,
                 secondary_answer):
    question_error_msg = get_error_msg(call_tester_to_check_format_of_question_string(question_string))
    solution_error_msg = get_error_msg(call_tester_to_check_format_of_solution_string(solution_string))
    hint_error_msg = get_error_msg(call_tester_to_check_format_of_hint_string(hint_string))
    answer_type_string_error_msg = get_error_msg(call_tester_to_check_format_of_answer_type_string(answer_type_string))
    final_answer_error_msg = get_error_msg(call_tester_to_check_format_of_final_answer(final_answer))
    final_output_string = "<p><b> Question Error:</b></p>" + question_error_msg + "<p><b> Solution Error:</b></p>" + solution_error_msg + "<p><b> Hint Error:</b></p>" + hint_error_msg + "<p><b> Answer type Error:</b></p>" + answer_type_string_error_msg + "<p><b> Final answer Error:</b></p>" + final_answer_error_msg
    return final_output_string


#print(check_dropdown_answer_type_have_duplicate_option(
    #"[answer_types([[string(),type(continuous(input_list(list(string(....),string(1.1),string(**@@#&&1),string(11)))))]])]"))

# questio = " [,string(Let latex(x) metre be the length of a side of the removed squares.),string(latex(\\therefore) length of the box = latex(30-2x) and breadth of the box = latex(16-2x)),string(If latex(V(x)) is the volume of the box, then), string(latex(V(x)) = latex(x \\times (16-2x) \\times (30-2x)) ), string(latex(V(x)) = latex(4x^{3}- 92 x^{2} + 480x)) ,string(latex(V^{\\prime}(x)) = latex(12x^{2} - 184x+ 480)),string(latex(V^{\\prime\\prime}(x)) = latex(24x - 184)), string(Now latex(V^{\\prime}(x)) = latex(0) gives latex(x) = latex(\\frac{10}{3}~,~12)), string(latex(V^{\\prime\\prime}(\\frac{10}{3})) = latex(24 \\times \\frac{10}{3}  - 184<0)), string(latex(V^{\\prime\\prime}(\\frac{10}{3})) = latex(-104<0)), string(latex(\\therefore) latex(x = \\frac{10}{3}) is the point of maxima.),string(Hence the largest volume of the box is given by), string(latex(V(\\frac{10}{3})) = latex(4 \\times (\\frac{10}{3} )^{3} - 92 \\times (\\frac{10}{3} )^{2} + 480 \\times \\frac{10}{3})), string(latex(V(\\frac{10}{3})) = latex(\\frac{19600}{27} ~ m^{3}) ),]"
# questio = "[string(latex(1 \\times \\frac{-1}{2})),string(latex(1 \\times \\frac{1}{2}))]"
# questio = "[string(latex(1 - \\left( \\frac{-1}{2} \\right))latex(-3 \\times \\dfrac{1}{2})latex(3 \\times \\dfrac{-1}{2}))]"
# print(check_possible_consecutive_sign(questio))
