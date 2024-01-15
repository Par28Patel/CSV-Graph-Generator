
# importing the csv library to read the survey results, and numpy and maplotlibrary for plotting the data onto graphs
import csv
import matplotlib.pyplot as plt
import numpy as np

"""
This function reads the comma delmited csv file containing the google forms survey, 
and converts it into a list of dictionaries, containing the responses of each survey participant.
example output of return value is [{"Question": "Answer", "Question": "Answer"} , {"Question:" "Answer", "Question": "Answer}]

@param target_file: string containing source file of google form's csv
@return: a list of dictionaries, with each dictionary representing an individual response from a survey participant. 
key = question value = answer for each question in survey for each dictionary in the list.
"""
def csv_to_dict(target_file):

    # open target file containing survey results
    with open(target_file) as csv_file:   

        # data in each row is separated by commas, so each row is split into subarrays delmited by a comma ('contains the answer choice of each question')
        target_csv = list(csv.reader(csv_file, delimiter=','))

        # the first row holds an array containing all the questions of the survey
        column_names = target_csv[0]

        # holds the result
        results_list = []

        # starting range is 1 since we want to skip the first row which is just the column titles ('not part of responses')
        for i in range(1, len(target_csv)):
            # holds each response in key value pair {"question": answer}
            temp_dict = {}
            
            # go through all the columns (questions) and set that as the key in the dictionary, and the answer is the current row's sub-array (containing answer)
            for j in range(len(column_names)):
                temp_dict[column_names[j]] = target_csv[i][j]

            # add dictionary to outer list
            results_list.append(temp_dict)
    

    # free memory by closing file
    csv_file.close()

    return results_list


"""
calculates through the results list, and  
and finds the amount of times each answer choice was selected by all survery participants 
for the passed in question 

@param results_list: list of dictionaries with survey results
@param question: the question that we're using to find
 the different answer choices and the amount of times it was selected respectively 

@return: a 2D array, with the first subarray representing the 
possible answers to that question, and the second subarray containing the respective counts of each possible answer.
 e.g if male was selected 50 times, and female was selected 20 times, the output would be [['Male', 'Female'] , ['50', '20]] 
 (this is the format that matplot lib expects for rendering graphs)
"""

def find_unique_answers(results_list, question):

    # dict holding the key (answer choice,) and value (the frequency of that answer choice)
    unique_answers = {}

    for i in range(len(results_list)):
        # if a given answer choice does not exist, add it as a key and initalize to 1
        if results_list[i][question] not in unique_answers:
            unique_answers[results_list[i][question]] = 1
        else:
            # if it exists, increment it's count by 1 since we've encountered the same answer choice again
            unique_answers[results_list[i][question]] += 1

    # sort the dictionary by key, or in other words in alphabetical/numerical order (depending on the x axis labels)
    unique_answers = dict(sorted(unique_answers.items()))

    # first array is the keys (answer choice) second array is the values (answer count)
    return [list(unique_answers.keys()), list(unique_answers.values()) ]


"""
performs the same action as the function above,except it handles the question type where 
participants can select multiple options.
finds the amount of times each answer choice was selected by all survery participants. 
it splits the answer by the delimeter ';', and uses each answer choice as part of the count
for the passed in question 

@param results_list: list of dictionaries with survey results
@param question: the question that we're using to find
 the different answer choices and the amount of times it was selected respectively 

@return: a 2D array, with the first subarray representing the 
possible answers to that question, and the second subarray containing the respective counts of each possible answer.
 e.g if male was selected 50 times, and female was selected 20 times, the output would be [['Male', 'Female'] , ['50', '20]] 
 (this is the format that matplot lib expects for rendering graphs)
"""

def find_unique_answers_checklist(results_list, question):
    unique_answers = {}
    for i in range(len(results_list)):

        # split the answer values on ; since each answer choice is delimited by a ;
        #  (since multiple answers are stored in string)

        # rest of function is same as find_unique_answers_checklist
        option_choice = results_list[i][question].split(";")

        for j in range(len(option_choice)):
            if option_choice[j] not in unique_answers:
                unique_answers[option_choice[j]] = 1
            else:
                unique_answers[option_choice[j]] += 1

    unique_answers = dict(sorted(unique_answers.items()))
    return [list(unique_answers.keys()), list(unique_answers.values()) ]


"""
Calculates a specific metric, which the amount of students who 
voted a specific number answer to the question "is chatgpt harmful or helpful"  by faculty in university

@param results_list: list of dictionaries with survey results
@param number1: the number answer that the student voted for
 the different answer choices and the amount of times it was selected respectively 

@param number2: the alternate number answer  choice we're searching for 
 the different answer choices and the amount of times it was selected respectively 

@return: a 2D array, with the first subarray representing the 
faculty, and the second one representing the respective counts of each faculty
 e.g if science was selected 50 times, and arts was selected 20 times, 
 the output would be [['science', 'art'] , ['50', '20]]
"""

def find_harms_vs_major(results_list, number1, number2):
    unique_answers = {}
    for i in range(len(results_list)):
        # if the current question is the one regarding the harms and helps of chatgpt and it's value is one of the 2 target numbers, then its the data we want to capture
        if results_list[i]["In the long run, do you think the use of ChatGPT will be helpful or harmful to society?"] == number1 or results_list[i]["In the long run, do you think the use of ChatGPT will be helpful or harmful to society?"] == number2:
            # if its a unique answer choice, initalize it in the dict otherwise, just increment the existing key.
            if results_list[i]["What faculty are you in?"] not in unique_answers:
                unique_answers[results_list[i]["What faculty are you in?"]] = 1
            else:
                 unique_answers[results_list[i]["What faculty are you in?"]] += 1

    # sort the dictionary 
    unique_answers = dict(sorted(unique_answers.items()))
    return [list(unique_answers.keys()), list(unique_answers.values()) ]

"""
Adds labels to the bar graph in matplot lib
@param labels: label array that contains the values to print on the graph 
@return: None (void function)
"""
def set_bar_labels(labels,count):
    for i,v in enumerate(labels):
        # matplotlib print text function, (center it for good formatting)
        plt.text(i, count[i], count[i], ha = 'center')


"""
Generates a bar graph of the given survey data using the matplotlib library
@param results_list: 2d array containings the data in the x and y axis of the graph (labels, and then the count of each data label)
@title: graph title
@param xlabel: title for the x axis
@param ylabel: title for the y axis
@return: None (void function)
"""

def generate_bar_graph(results_list, title, x_label, ylabel):
    
    # pass x axis and y axis data to plot
    plt.bar(np.array(results_list[0]),np.array(results_list[1]))
    #sets title x and y axis lables
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(ylabel)

    # call function to append the count above each respective bar
    set_bar_labels(results_list[0],results_list[1])

    # display graph
    plt.show() 


"""
Generates a pie  raph of the given survey data using the matplotlib library
@param results_list: 2d array containings the data in the x and y axis of the graph (labels, and then the count of each data label)
@title: graph title
@return: None (void function)
"""

def generate_pie_graph(results_list, title):
    # pass the y values to the pie graph
    current_pie = np.array(results_list[1])
    # settings to allow percentage sign of each slice on pie, and other visual  properties like angle, and labels
    plt.pie(current_pie, labels = results_list[0], autopct='%1.1f%%', startangle=90)
    plt.title(title)

    # display pie graph
    plt.show()  


# main method that renders all the graphs
if __name__ == "__main__":

    
    # call function to read csv results from file and store list of dictionaries in variable
    results_list = csv_to_dict('./surveyresults.csv')

    # fetches the arrays and finds the amount of times each answer choice was selected by all survery participants for all the given questions in individual 2d arrays
    gender_results = find_unique_answers(results_list, "Gender")
    age_results = find_unique_answers(results_list, "Age")
    studies_year_results = find_unique_answers(results_list, "What is your year of studies?")
    faculty_results = find_unique_answers(results_list, "What faculty are you in?")
    support_chat_gpt = find_unique_answers(results_list, "Do you support the use of ChatGPT?")
    long_run_chat_gpt = find_unique_answers(results_list, "In the long run, do you think the use of ChatGPT will be helpful or harmful to society?")
    post_secondary_goal = find_unique_answers(results_list, "What is you Post Secondary academic goal?")
    chatgpt_often = find_unique_answers(results_list, "How often do you use ChatGPT?")
    chatgpt_benefits = find_unique_answers(results_list, "Do you think ChatGPT is academically beneficial?")
    chatgpt_circumstance = find_unique_answers_checklist(results_list, "In what circumstances should ChatGPT be used? (select all that apply)")
    controversy_graph = find_unique_answers_checklist(results_list,  "With the controversy surrounding the use of ChatGPT, there is a lot of blame being thrown around. In your opinion, who/what is to blame for the ethical/moral issues?")
    how_often_used = find_unique_answers(results_list, "How often do you think the use of ChatGPT in the academic/professional world is ethical?")
    voted5_vs_major = find_harms_vs_major(results_list, "4", "5")
    voted1_vs_major = find_harms_vs_major(results_list , "1" , "2")


    # generates the bar graph by passing in the collected data from the above 2darrays, and renders either a pie/bar graph depending on the 
    # situation using matplotlib library from the created function
    generate_bar_graph(gender_results, "Survey Participants' answer to 'Gender'" , "Gender Types" , "Count")
    generate_pie_graph(age_results, "Survey Participants' Answer to 'Age'")
    generate_bar_graph(studies_year_results, "Survey Participants' Answer to 'What is your Year of Study?'" , "Year of Study" , "Count" )
    generate_bar_graph(faculty_results, "Survey Participants' Answer to 'What faculty are you in?", "Types of Faculty" , "Count")
    generate_pie_graph(support_chat_gpt, "Survey Participants' Answer to 'Do you support the use of ChatGPT?'")
    generate_bar_graph(long_run_chat_gpt, "Survey Participants' Answer to \n 'In the long run, do you think the use of ChatGPT will be helpful or harmful to society?'", "Agreement Scale (1 being low 5 being high)", "Count")
    generate_bar_graph(post_secondary_goal, "Survey Participants' Answer to 'What is you Post Secondary academic goal?" , "Types of Academic Goals" , "Count")
    generate_pie_graph(chatgpt_often, "Survey Participants' Answer to 'How often do you use ChatGPT'")
    generate_bar_graph(chatgpt_benefits, "Survey Participants' Answer to 'Do you think ChatGPT is academically beneficial?", "Agreement Scale (1 being not benefical 5 being very benefical", "Count")
    generate_bar_graph(chatgpt_circumstance, "Survey Participants' Answer to 'In what circumstances should ChatGPT be used? (select all that apply)" , "Circumstance Type" , "Count")
    generate_bar_graph(controversy_graph, "Survey Participants' Answer to \n 'With the controversy surrounding the use of ChatGPT, there is a lot of blame being thrown around. \n In your opinion, who/what is to blame for the ethical/moral issues?'" , "Blame types" , "Count")
    generate_pie_graph(how_often_used, "Survey Participants' Answer to 'How often do you think the use of ChatGPT in the academic/professional world is ethical?'")
    generate_bar_graph(long_run_chat_gpt, "Survey Participants' Answer to 'In the long run, do you think the use of ChatGPT will be helpful or harmful to society?'" , "Agreement Scale (1 being not helpful 5 being helpful)", "Count")
    generate_pie_graph(voted5_vs_major, "Faculty of Students who selected 4 or 5 to the question 'do you think the use of ChatGPT will be helpful or harmful to society?'" )
    generate_pie_graph(voted1_vs_major, "Faculty of Students who selected 1 or 2 to the question 'do you think the use of ChatGPT will be helpful or harmful to society?'")
    