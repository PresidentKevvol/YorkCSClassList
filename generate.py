# a python script to generate an html file of course skill tree
# from a formatted list of courses and dependancies

import sys # for command line arguments
import re # for regex
import json # for reading json

# the template for the div element in a generated html page
# with the prereq html attribute in the div, the JS in the webpage will generate the arrows
# pointing from a prerequsite to it's dependent, as well as the animation
# so for now we need only worry about the placement of each 'box' representing a course
div_template = \
"""
<div class="classBox {dept} {year_level}" id="{dept}{code}" style="left: {x}em; top: {y}em;" prereq="{prereqs}">
    <span class="course-code-full">{dept_upper} {code} ({credit:.2f})</span><br>
    <span class="course-name" style="font-size:{name_font_size};">{name}</span>
    <div class="course-description" hidden="hidden">{full_description}</div>
</div>
"""

# represents a course in York University
# including the prerequsites
class Course:
    def __init__(self, dept, code, credit, name, prereqs, desc):
        self.dept = dept # department name such as 'EECS', 'MATH'
        self.code = code # course code such as '2031', as a str not an int, because there are courses with letters in their course code
        self.credit = credit # the credit count of the course, usually 3.00, as a number not str, this is so the course can be read from database easier this way
        self.name = name # the common name of the course, such as 'Software Tools'
        self.prereqs = prereqs # the list of prerequsites, should be formatted as list of 2-tuples, e.g. [('eecs', '1022'), ('math', '1310')]
        self.desc = desc

    def generate_div_element(self, x, y):
        # joining the list such as [('eecs', '1022'), ('math', '1019'), ('math', '1310')] into 'eecs1022 math1019 math1310'
        prereqs = " ".join([(i[0] + i[1]) for i in self.prereqs])
        # font size of the course name (we need to shrink it if too long)
        name_font_size = "0.9em" if len(self.name) > 60 else "1.0em"
        # the year level of the course
        year_level = "yl-" + self.code[0]
        # returning a formatted html text of div element
        return div_template.format(
            dept = self.dept,
            year_level = year_level,
            code = self.code,
            x = x,
            y = y,
            prereqs = prereqs,
            credit = self.credit,
            name_font_size = name_font_size,
            name = self.name,
            dept_upper = self.dept.upper(),
            full_description=self.desc)

    # method to get the code tuple of the course
    def get_code_tuple(self):
        return (self.dept, self.code)

# a sample dict of courses for test generation
# it have a very relational database like schema
sample_courses_list = {}
sample_courses_list[('eecs', '1001')] = Course('eecs', '1001', 1.0, 'Research Directions in Computing', [], "An introduction to research directions within the department and more broadly within the field. Students will attend lectures and other events organised by the department. Note: This course is expected to be completed in the first-year of study.")
sample_courses_list[('eecs', '1012')] = Course('eecs', '1012', 3.0, 'Introduction to Computing: A Net-centric Approach', [], "The objectives of 1012 are threefold: providing a first exposure to event-driven programming, teaching students a set of computing skills (including reasoning about algorithms, tracing programs, test-driven development, unit testing), and providing an introduction to computing within a mobile, net-centric context. It uses problem-based approach to expose the underlying concepts and an experiential laboratory to implement them. A mature mobile software infrastructure (such as HTML, CSS, and JavaScript) is used so that students can pick up key programming concepts (such as variables and control flow) within a client-server context without being bogged down in complex or abstract constructs. Laboratory exercises expose students to a range of real-world problems with a view of motivating computational thinking and grounding the material covered in lecture.")
sample_courses_list[('eecs', '1015')] = Course('eecs', '1015', 3.0, 'Introduction to Computer Science and Programming', [], "This course is an introduction to the concepts and tools of computer science as students learn a procedural subset of the Python programming language. Python has a variety of libraries in different domains allowing for the solution of interesting problems which has made it a popular language in industry and the academy. Students do hands-on work to design, write, debug and test computer programs that solve problems computationally. Students study variables, assignments, expressions (arithmetic, relational and logical) and sequencing of statements to implement solutions for computational problems, in Python. They document programs with comments and preconditions. They analyze the type correctness of programs via a type checker. They use an Integrated Development Environment (IDE) to develop, unit-test and debug programs given a problem specification. They apply conditionals (including nested conditionals) to implement algorithms to solve computational problems. They code functions to develop modular programming solutions for computational problems. They apply Python loops (including nested loops) to implement algorithms to solve computational problems. They apply data structures, including tuples, sets, lists and dictionaries, to implement algorithms to solve computational problems. They code simple recursive functions to implement algorithms to solve computational problems. ")
sample_courses_list[('eecs', '1022')] = Course('eecs', '1022', 3.0, 'Programming for Mobile Computing', [('eecs', '1012'), ('eecs', '1015')], "Provides a first exposure to object-oriented programming and enhances student understanding of key computing skills such as reasoning about algorithms, designing user interfaces, and working with software tools. It uses problem-based approach to expose the underlying concepts and an experiential laboratory to implement them. A mature mobile software infrastructure (such as Java and the Android programming environment) is used to expose and provide context to the underlying ideas. Laboratory exercises expose students to a range of real-world problems with a view of motivating computational thinking and grounding the material covered in lectures.")
sample_courses_list[('math', '1019')] = Course('math', '1019', 3.0, 'Discrete Mathematics for Computer Science', [], "Introduction to abstraction. Use and development of precise formulations of mathematical ideas. Informal introduction to logic; introduction to naïve set theory; induction; relations and functions; big O-notation; recursive definitions, recurrence relations and their solutions; graphs and trees. ")
sample_courses_list[('math', '1300')] = Course('math', '1300', 3.0, 'Differential Calculus with Applications', [], "Limits, derivatives with applications, antiderivatives, fundamental theorem of calculus, beginnings of integral calculus. ")
sample_courses_list[('math', '1310')] = Course('math', '1310', 3.0, 'Integral Calculus with Applications', [('math', '1300')], "Transcendental functions, differential equations, techniques of integration, improper integrals, infinite series. ")

sample_courses_list[('eecs', '2001')] = Course('eecs', '2001', 3.0, 'Introduction to the Theory of Computation', [('eecs', '1022')], "Introduction to the theory of computing, including automata theory, formal languages and Turing machines; theoretical models and their applications in various fields of computer science. The emphasis is on practical applications of the theory and concepts rather than formal rigour. ")
sample_courses_list[('eecs', '2011')] = Course('eecs', '2011', 3.0, 'Fundamentals of Data Structures', [('eecs', '2030'), ('math', '1019')], "A study of fundamental data structures and their use in the efficient implementation of algorithms. Topics include abstract data types, lists, stacks, queues, trees and graphs. The course discusses the fundamental data structures commonly used in the design of algorithms. Abstract operations on data structures are specified using pre and post conditions and/or system invariants. Trade-offs between a number of different implementations of each abstract data types (ADT) are analyzed. Each algorithm operating on data structures is proved correct using loop invariants or induction. Both formal and informal proofs are introduced though most of the reasoning is done informally. Data structures are coded and unit tested in an object-oriented language. Selecting the appropriate ADT and a suitable implementation depending on the application is covered. ")
# as you can see, this is the exact reason why we use a HashMap instead of a list
# the order of the elements matter, as otherwise the placement of the boxes will be awkward, however...
# 2011 < 2030, but EECS2030 is a prerequsite of EECS2011!
# if we simply sort the courses by course code, EECS2011 will come before EECS2030
# therefore, we will need something else to determine the intrinsic order of the courses
sample_courses_list[('eecs', '2021')] = Course('eecs', '2021', 4.0, 'Computer Organization', [('eecs', '1022')], "Introduction to computer organization and instruction set architecture, covering assembly language, machine language and encoding, addressing modes, single/multicycle datapaths (including functional units and controls), pipelining, memory segments and memory hierarchy.")
sample_courses_list[('eecs', '2030')] = Course('eecs', '2030', 3.0, 'Advanced Object Oriented Programming', [('eecs', '1022')], "This course continues the separation of concern theme introduced in LE/EECS 1020 3.00 and LE/EECS1021 3.00. While 1020 and 1021 focuses on the client concern, this course focuses on the concern of the implementer. Hence, rather than using an API (Application Programming Interface) to build an application, the student is asked to implement a given API. Topics include implementing classes (non-utilities, delegation within the class definition, documentation and API generation, implementing contracts), aggregations (implementing aggregates versus compositions and implementing collections), inheritance hierarchies (attribute visibility, overriding methods, abstract classes versus interfaces, inner classes); applications of aggregation and inheritance in concurrent programming and event-driven programming; recursion; searching and sorting including quick and merge sorts); stacks and queues; linked lists; binary trees. ")
sample_courses_list[('eecs', '2031')] = Course('eecs', '2031', 3.0, 'Software Tools', [('eecs', '1022')], 'Tools commonly used in the software development process: the C language; shell programming; filters and pipes; version control systems and "make"; debugging and testing.')
sample_courses_list[('math', '1090')] = Course('math', '1090', 3.0, 'Introduction to Logic for Computer Science', [('math', '1019')], "The syntax and semantics of propositional and predicate logic. Applications to program specification and verification. Optional topics include set theory and induction using the formal logical language of the first part of the course. ")

# now a course list dict is basically a HashMap/dict representation of a Directed Acyclic Graph (DAG)
# (OS: I would surely hope the courses form a DAG, otherwise we will have circular dependancy in our school's courses? what the hell?)
# with each element being a node/vertex, and each containing an adjacency list, albeit pointing backwards/upstream
# the 'intrinsic order of courses' is basically a topological order of the DAG!
# therefore, here we will use a DFS algorithm to find the topological order just like how we learnt in EECS3101. (Praise Prof. Andy! "\o/")

def topological_sort(courses):
    # to keep track of which node we visited
    visited = {}
    for key in courses:
        visited[key] = False
    # a stack to store the result
    stack = []

    # now loop through each course
    for key in courses:
        # apply DFS
        if visited[key] == False:
            topological_sort_util(courses, key, visited, stack)

    # for the result
    res = []

    # now in the original algorithm the stack at the end of the algorithm will be in reverse order
    # but since our graph started out in reverse order in the first place, the stack here will be in the right order
    # i.e. early year courses first
    for key in stack:
        res.append((key, courses[key]))

    return res

# the recursive function for the DFS
def topological_sort_util(courses, key, visited, stack):
    # mark node as visited
    visited[key] = True
    # for each course node this course is pointed to
    for prereq in courses[key].prereqs:
        if visited[prereq] == False: # if it has not been visited
            topological_sort_util(courses, prereq, visited, stack) # DFS down to it
    # finally append this course to the stack
    stack.append(key)

# reference for topological ordering of DAG: https://www.geeksforgeeks.org/topological-sorting/

# a function taking in a dict/HashMap of courses and generate a str of many html elements
# representing the courses, with inline CSS styles defining their position on the page included
# the column count represent how many boxes should exist in a row at max
# it is optional argument and default is 6
def generate(courses, box_width, box_height, horizontal_gap, vertical_gap, col_count=6):
    # perform a topological sorting of the courses DAG
    sorted = topological_sort(courses)
    # the result string (html)
    res = ""
    # now we know the intrinsic order of the courses, we just need to put them in the right position on the screen
    # still, we need to keep track of what rows we are on so if A is a prereq of B, A and B cannot be in the same row
    current_row = 0
    current_col = 0
    current_col_courses = []
    for key, course in sorted:
        # first make sure we didn't go out of column limit
        if current_col >= col_count:
            # reset to next column
            current_col = 0
            current_row += 1
            current_col_courses = []
        # now if this current course have a prerequsite, but it's already on the current column
        # immediately reset to the next column to make sure this current course is below its prerequsites on the page
        for prereq in course.prereqs: # if any of it's prereq
            if prereq in current_col_courses: # is on the current row
                # reset to next column
                current_col = 0
                current_row += 1
                current_col_courses = []

        # calculate x and y values
        x = current_col * (box_width + horizontal_gap)
        y = current_row * (box_height + vertical_gap)
        # convert with the x and y values
        elem_text = course.generate_div_element(x, y)
        # append the formatted html text to the result str
        res += (elem_text)
        # record the courses on the current row
        current_col_courses.append(key)
        # add 1 to the column for the next box
        current_col += 1

    return res

# an alternative generation algorithm for a more asthetically pleasing result
# precondition: there is not a chain of length more than 2 in a same year
# i.e. EECS2030 -> EECS2011 is ok, but there can't be a chain like BBBB3113 -> BBBB3021 -> BBBB3491
def generate_2(courses, box_width, box_height, horizontal_gap, vertical_gap, base_margin_horizontal, base_margin_vertical, col_count=6):
    # first seperate the courses into years
    years_list = {}
    for key in courses:
        year = int(key[1][0]) # as always, the first character of a course's number is its year level
        if year not in years_list: # if this year level has not been recorded, add it
            # the two lists represent first and second semester
            # i.e. since EECS2011 have prerequsite EECS2030, one can only take 2011 after 2030
            # thus, it must be lower on the graph
            years_list[year] = [[], []]
        # after that is taken care of, we need to determine if it's a second semester course
        # basically: does it have a prerequsite that is the same year level as itself?
        course = courses[key]
        is_second_sem = False
        for prereq in course.prereqs:
            if int(prereq[1][0]) == year: # if there is a prereq == this courses's year
                is_second_sem = True
        # now add to the right part of the list
        if not is_second_sem:
            years_list[year][0].append(course) # (can be taken) in first sem
        else:
            years_list[year][1].append(course) # in second sem

    # now we have a list with order precision down to semesters, we can start rendering the boxes
    current_col = 0
    current_row = 0
    coordinate_list = {} # list of x y coordinates
    for year in years_list: # for each year
        for sem in years_list[year]: # for each semester
            for course in sem: # for each course in this semester
                if current_col >= col_count: # if the number of boxes in this row goes out of limit
                    # reset to next row
                    current_row += 1
                    current_col = 0
                code_tuple = course.get_code_tuple() # get the course code tuple
                coordinate_list[code_tuple] = (current_col, current_row)
                current_col += 1 # to next col
            # reset row at the end of the semester list
            current_row += 1
            current_col = 0
        # end of the year's list, reset to next row
        current_row += 1
        current_col = 0

    # after we define the coordinates, we just need to transcribe them
    res = ""
    for code in coordinate_list:
        course = courses[code]
        # the coordinate list stores their xy coordinate
        x = coordinate_list[code][0] * (box_width + horizontal_gap) + base_margin_horizontal
        y = coordinate_list[code][1] * (box_height + vertical_gap) + base_margin_vertical
        div = course.generate_div_element(x, y)
        res += div
    return res, current_row

# pattern = re.compile("[0-9]") # pattern that find any number

# function to read a list of courses from a csv file
# text is the text in the file already retrieved as a string
def read_csv(text):
    lines = text.split("\n")
    res = {}
    for line in lines:
        # split into each value
        split = line.split(",")
        if len(split) < 6: # if malformed text (less than 6 values)
            continue
        # the first value is the dept name
        dept = split[0].strip().replace("'", "")
        # the second value is the code
        code = split[1].strip().replace("'", "")
        # third value is the credit
        credit = float(split[2].strip())
        # fourth value is the course name
        name = split[3].strip()
        if name.startswith("\""):
            name = name[1:-1]
        # fifth value is the prerequsite list, contained in '' or "", separated by space
        prereqs = split[4].strip().replace("'", "").replace("\"", "")
        prereqs = prereqs.split(" ")
        preq_list = []
        for prereq in prereqs:
            nums = re.findall("[0-9]", prereq) # this return a list of found text, so prereq = 'eecs2011' will give ['2', '0', '1', '1']
            mark = prereq.find(nums[0]) # now get the first number's position
            pdept = prereq[:mark] # now we can split the string into department and code
            pcode = prereq[mark:]
            preq_list.append((pdept, pcode)) # append to list
        # sixth and last element is full description
        desc = split[5].strip()
        if desc.startswith("\"") or desc.startswith("'"):
            desc = desc[1:-1]
        # finally, add them to the dict
        res[(dept, code)] = Course(dept, code, credit, name, preq_list, desc)
    return res

# function to read a json file to course list
def read_json(content):
    items = json.loads(content)
    items = items["courses"]
    res = {}
    for item in items:
        # the first value is the dept name
        dept = item["dept"]
        # the second value is the code
        code = item["code"]
        # third value is the credit
        credit = item["credit"]
        # fourth value is the course name
        name = item["name"]
        # fifth value is the prerequsite list, contained in '' or "", separated by space
        prereqs = item["prereq"]
        preq_list = []
        if prereqs != "":
            prereqs = prereqs.split(" ")
            for prereq in prereqs:
                nums = re.findall("[0-9]", prereq) # this return a list of found text, so prereq = 'eecs2011' will give ['2', '0', '1', '1']
                mark = prereq.find(nums[0]) # now get the first number's position
                pdept = prereq[:mark] # now we can split the string into department and code
                pcode = prereq[mark:]
                preq_list.append((pdept, pcode)) # append to list
        # sixth and last element is full description
        desc = item["desc"]
        # finally, add them to the dict
        res[(dept, code)] = Course(dept, code, credit, name, preq_list, desc)
    return res

def main():
    args = sys.argv # get command line arguments
    input_fil = args[1] # the first should be input file
    output_fil = args[2] if len(args) >= 3 else "generated.html" # the second is the output file's name

    input_open = open(input_fil, "r")
    content = input_open.read() # read the entire file

    courses_list = read_json(content) # convert into the dict like above
    # the arguments for the generate_2 function
    box_width = 12
    box_height = 4.5
    horizontal_gap = 2
    vertical_gap = 2.5
    base_margin_horizontal = 2
    base_margin_vertical = 2
    col_count = 6

    #html_output = generate_2(courses_list, 12, 4.5, 2, 2.5, 2, 4) # generate the html file
    html_output, total_row_ct = generate_2(courses_list, box_width, box_height, horizontal_gap, vertical_gap, base_margin_horizontal, base_margin_vertical, col_count) # generate the html file

    # now grab the index_new.html template file
    index_template = open("template_new.html").read()
    # replace the placeholder with the output
    final_output = index_template.replace("{{- courses_divs -}}", html_output)
    # update the size of the root div as well
    final_output = final_output.replace("{{- root_div_base_width -}}", f"{(box_width + horizontal_gap) * col_count - horizontal_gap + 2 * base_margin_horizontal}em")
    final_output = final_output.replace("{{- root_div_base_height -}}", f"{(box_height + vertical_gap) * total_row_ct - vertical_gap + 2 * base_margin_vertical}em")

    fil = open(output_fil, "w")
    fil.write(final_output)

# run the main function if this file is being ran
if __name__ == '__main__':
    main()
