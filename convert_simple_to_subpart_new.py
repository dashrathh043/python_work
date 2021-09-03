import json
import os
import random
import pathlib


def combining_writing_json_txt_file_to_different_file(List_simple_cts, InputFile, OutputFile, final_ct_name,
                                                      main_question):
    file_25_matrix = open(InputFile, "r")
    Lines_25_matrix = file_25_matrix.readlines()
    Map_25_matrix_init = {"Config_type": "", "Image_info": "", "Answer": "", "Answer_check_type": "",
                          "Answer_lower_limit": "", "Answer_upper_limit": "", \
                          "Answer_type": "", "No_of_answer_box": "", "Question": "", "Hint": "", "Solution": ""}
    Map_25_matrix = Map_25_matrix_init

    answer_lower_limit = []
    answer_upper_limit = []
    Individual_part = ""
    Id_no = 100

    for line in Lines_25_matrix:
        if len(line.split(" : ")) == 2:
            Lhs = line.split(" : ")[0]
            Rhs = line.split(" : ")[1]
            Map_25_matrix[Lhs] = Rhs.rstrip("\n")

        elif line[4:9:] == "-----":
            simple_ct = Map_25_matrix
            Id = str(Id_no)
            answer_lower_limit.append(simple_ct["Answer_lower_limit"])
            answer_upper_limit.append(simple_ct["Answer_upper_limit"])
            Q_Id = simple_ct["Question"]
            S_Id = simple_ct["Solution"]
            Answer_type_Id = simple_ct["Answer_type"]
            No_of_answer_box_Id = simple_ct["No_of_answer_box"]
            Answer_check_type_Id = simple_ct["Answer_check_type"]
            Answer_Id = simple_ct["Answer"]
            Hint_Id = simple_ct["Hint"]
            Individual_part += "Question_sub_parts_id_" + Id + " : " + Q_Id + "\nSolution_sub_parts_id_" + Id + " : " + S_Id + "\nAnswer_type_sub_parts_id_" + Id + " : " + Answer_type_Id + "\nNo_of_answer_box_id_" + Id + " : " + No_of_answer_box_Id + "\nAnswer_check_type_sub_parts_id_" + Id + " : " + Answer_check_type_Id + "\nAnswer_sub_parts_id_" + Id + " : " + Answer_Id + "\nHint_sub_parts_id_" + Id + " : " + Hint_Id + "\n"
            Id_no += 100

    file_25_matrix.close()
    if (Id_no - 100) == len(List_simple_cts) * 100:
        Answer_ll = max(answer_lower_limit)
        Answer_ul = max(answer_upper_limit)
        Subpart_ctname = final_ct_name
        Subpart_question = "Image_info : []\nQuestion : [" + main_question + "]\nConfig : []\nAnswer_check_type : 6\nAnswer_lower_limit : " + str(
            Answer_ll) + "\nAnswer_upper_limit : " + str(
            Answer_ul) + "\n" + Individual_part + "Concepts_used : [[" + Subpart_ctname + ",0]]\nConfig_type : [" + Subpart_ctname + "]\nQuestion_type : [\"subpart_qt\"]\nQid : " + str(
            random.randint(101, 999))
        subpart_25_matrix = open(OutputFile, "w")
        subpart_25_matrix.write(str(Subpart_question))
        subpart_25_matrix.close()

    else:
        raise Exception("Sorry, there's some problem in generation of one or more cts")


def replace_backslash(json_data):
    return json_data.replace("\\", "\\\\\\\\")


def write_json_data_into_file(json_data, file1):
    if len(json_data.strip()) == 0:
        return []
    else:
        json_object = json.loads(json_data)
        json_list = json_object["ct_list_output"]
        f1 = open(file1, "w")
        for i in range(len(json_list)):
            if i > 0:
                f1.write("\n")
            dict_data = json_list[i]
            for key in dict_data:
                f1.write(key + " : " + dict_data[key] + "\n")
            f1.write("\n")
            f1.write("\n")
            f1.write("----------------------\n")
        f1.close()
        return len(json_list)


def fetch_data_from_file(file):
    f1 = open(file, "r")
    line = f1.readline()
    final_str = ""
    while line:
        final_str += line
        line = f1.readline()
    return final_str


def convert_simple_ct_to_subpart_ct(json_data, subpart_ct_name):
    try:
        current_path = pathlib.Path(__file__).parent.resolve()
        file1 = os.path.join(current_path, "simple_ct_input.txt")
        file2 = os.path.join(current_path, "subpart_ct_output.txt")
        final_json_data = replace_backslash(json_data)
        json_object = json.loads(final_json_data)
        ct_list = json_object["ct_list"]
        main_question = json_object["main_question"]
        write_json_data_into_file(final_json_data, file1)
        combining_writing_json_txt_file_to_different_file(ct_list, file1, file2, subpart_ct_name, main_question)
        return fetch_data_from_file(file2)
    except:
        return "Error"
    finally:
         os.remove(file1)
         os.remove(file2)


json_data = """ {
	"main_question":"",
	"ct_list_output": [{
			"Answer": "[[\\frac{\\pi}{6}]]",
			"Answer_lower_limit": "0",
			"Answer_upper_limit": "0",
			"Answer_type": "[answer_types([[string(),type(algebra_form),placeholder(string(Enter answer in terms of latex(\\pi))),unit()]])]",
			"Question": "[string(),string(The function latex(f) given by latex(f(x)) latex(=) latex(tan^{-1}(3~sin~x+3\\sqrt{3}~cos~x)),  latex(x>0) is always increasing in latex((0, \\alpha)) in first quadrant. Find the value of latex(\\alpha). )]",
			"Hint": "[string(Use Differentiation for trigonometric functions.)]",
			"Solution": "[,string(We have),string(latex(f(x)) latex(=) latex(tan^{-1}(3~sin~x+ 3\\sqrt{3} ~ cos~ x))),string(latex(f^{\\prime}(x)) latex(=) latex(\\frac{1}{1+(3~sin ~x+3\\sqrt{3} ~ cos ~ x)^{2}} \\times (3 ~ cos~x - 3\\sqrt{3} sin~x))), string(latex(f^{\\prime}(x)) latex(=) latex(\\frac{3 ~ cos~x - 3\\sqrt{3} sin~x}{1+(3~sin ~x+3\\sqrt{3} ~ cos ~ x)^{2}})), string(Since latex(1+(3 ~ sin~x + 3\\sqrt{3} ~ cos~x)^{2}>0) in first quadrant) ,string(latex(\\therefore f^{\\prime}(x)>0) if latex(3 ~ cos~x - 3\\sqrt{3}~ sin~x>0)),string(latex(\\Rightarrow f^{\\prime}(x)>0) if latex(3 ~ cos~x > 3\\sqrt{3}~ sin~x)), string(latex(\\Rightarrow f^{\\prime}(x)>0) if latex(cot~x > \\sqrt{3})), string(i.e latex(cot~x>\\sqrt{3} \\Rightarrow tan~x< \\frac{1}{\\sqrt{3}} \\Rightarrow 0<x<\\frac{\\pi}{6})), string(Thus latex(f^{\\prime}(x)>0) in latex((0,\\frac{\\pi}{6}))), string(Hence, latex(f(x)) is increasing latex((0,\\frac{\\pi}{6}))),string(latex(\\therefore) latex(\\alpha) latex(=) latex(\\frac{\\pi}{6})),]"
		},
		{
			"Answer": "[[72]]",
			"Answer_lower_limit": "0",
			"Answer_upper_limit": "0",
			"Answer_type": "[answer_types([[string(),type(continuous(string( ),input(string(),type(s_textbox)),string(latex(m^{3})),input(string(),type())))]])]",
			"No_of_answer_box": "1",
			"Image_info": "[]",
			"Question": "[string(),string(An open topped box is to be constructed by removing equal squares from each corner of a latex(7) metre by latex(15) metre rectangular sheet of aluminium and folding up the sides. Find the volume of the largest such box. )]",
			"Hint": "[string(Volume of a box latex(=) length latex(\\times) width latex(\\times) height.)]",
			"Solution": "[,string(Let latex(x) metre be the length of a side of the removed squares.),string(latex(\\therefore) length of the box latex(=) latex(15-2x) and breadth of the box latex(=) latex(7-2x)),string(If latex(V(x)) is the volume of the box, then), string(latex(V(x)) latex(=) latex(x \\times (7-2x) \\times (15-2x)) ), string(latex(V(x)) latex(=) latex(4x^{3}- 44 x^{2} + 105x)) ,string(latex(V^{\\prime}(x)) latex(=) latex(12x^{2} - 88x+ 105)),string(latex(V^{\\prime\\prime}(x)) latex(=) latex(24x - 88)), string(Now latex(V^{\\prime}(x)) latex(=) latex(0) gives latex(x) latex(=) latex(\\frac{3}{2}~,~\\frac{35}{6})), string(latex(V^{\\prime\\prime}(\\frac{3}{2})) latex(=) latex(24 \\times \\frac{3}{2}  - 88<0)), string(latex(V^{\\prime\\prime}(\\frac{3}{2})) latex(=) latex(-52<0)), string(latex(\\therefore) latex(x = \\frac{3}{2}) is the point of maxima.),string(Hence the largest volume of the box is given by), string(latex(V(\\frac{3}{2})) latex(=) latex(4 \\times (\\frac{3}{2} )^{3} - 44 \\times (\\frac{3}{2} )^{2} + 105 \\times \\frac{3}{2})), string(latex(V(\\frac{3}{2})) latex(=) latex(72 ~ m^{3}) ),]"
		}

	]
} """
print(convert_simple_ct_to_subpart_ct(json_data, "subpart_ct_final"))
{
            "Answer": ["[[\\frac{\\pi}{6}]]","[[72]]"],
            "Answer_lower_limit": "0",
            "Answer_upper_limit": "0",
            "Answer_type": "[answer_types([[string(),type(algebra_form),placeholder(string(Enter answer in terms of latex(\\pi))),unit()]])]",
            "Question": "[string(),string(The function latex(f) given by latex(f(x)) latex(=) latex(tan^{-1}(3~sin~x+3\\sqrt{3}~cos~x)),  latex(x>0) is always increasing in latex((0, \\alpha)) in first quadrant. Find the value of latex(\\alpha). )]",
            "Hint": "[string(Use Differentiation for trigonometric functions.)]",
            "Solution": "[,string(We have),string(latex(f(x)) latex(=) latex(tan^{-1}(3~sin~x+ 3\\sqrt{3} ~ cos~ x))),string(latex(f^{\\prime}(x)) latex(=) latex(\\frac{1}{1+(3~sin ~x+3\\sqrt{3} ~ cos ~ x)^{2}} \\times (3 ~ cos~x - 3\\sqrt{3} sin~x))), string(latex(f^{\\prime}(x)) latex(=) latex(\\frac{3 ~ cos~x - 3\\sqrt{3} sin~x}{1+(3~sin ~x+3\\sqrt{3} ~ cos ~ x)^{2}})), string(Since latex(1+(3 ~ sin~x + 3\\sqrt{3} ~ cos~x)^{2}>0) in first quadrant) ,string(latex(\\therefore f^{\\prime}(x)>0) if latex(3 ~ cos~x - 3\\sqrt{3}~ sin~x>0)),string(latex(\\Rightarrow f^{\\prime}(x)>0) if latex(3 ~ cos~x > 3\\sqrt{3}~ sin~x)), string(latex(\\Rightarrow f^{\\prime}(x)>0) if latex(cot~x > \\sqrt{3})), string(i.e latex(cot~x>\\sqrt{3} \\Rightarrow tan~x< \\frac{1}{\\sqrt{3}} \\Rightarrow 0<x<\\frac{\\pi}{6})), string(Thus latex(f^{\\prime}(x)>0) in latex((0,\\frac{\\pi}{6}))), string(Hence, latex(f(x)) is increasing latex((0,\\frac{\\pi}{6}))),string(latex(\\therefore) latex(\\alpha) latex(=) latex(\\frac{\\pi}{6})),]"
        },

