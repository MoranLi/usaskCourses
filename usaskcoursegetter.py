from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import pprint
import json
json_file = open("sect_info.json", "w+")
# load driver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
# open browser and go to link
driver.get('https://pawnss.usask.ca/ban/bwckschd.p_disp_dyn_sched')
driver.maximize_window()
time.sleep(1)
term = Select(driver.find_elements_by_tag_name('select')[0])
all_terms = [o.get_attribute('value') for o in term.options]
# select term, current 2019 winter
term.select_by_value(all_terms[3])
driver.find_elements_by_tag_name('input')[1].click()
time.sleep(1)
subjects = Select(driver.find_elements_by_tag_name('select')[0])
all_subjects = [o.get_attribute('value') for o in subjects.options]
# select subject, currently physics and agriculture
# chemistry for case a class have 3 section
subjects.select_by_value(all_subjects[27])
# physics for case a lab repeat per 2 week
#subjects.select_by_value(all_subjects[111])
# agriculture basic test case
#subjects.select_by_value(all_subjects[3])
# select campus, currently main campus and web
campus = Select(driver.find_elements_by_tag_name('select')[2])
# deselect all since all is default option
campus.deselect_all()
all_campus = [o.get_attribute('value') for o in campus.options]
campus.select_by_value(all_campus[1])
campus.select_by_value(all_campus[13])
driver.find_elements_by_tag_name('input')[0].click()
# loaded in to course info page
trs = driver.find_elements_by_class_name("datadisplaytable")[0].find_elements_by_tag_name('tr')
classInfo = {}
lastClassNeedAdditional = None
# iterate over all the rows
for tr in trs:
    tds = tr.find_elements_by_tag_name('td')
    # len(tds) == 1 means this is only one section, usually an information section to tell subject etc
    if len(tds) > 1:
        subject = tds[2].text
        course_number = tds[3].text
        if course_number[-1] == "*":
            course_number=course_number[:-1]
        course = subject.strip() + course_number.strip()
        if course != "CRNSubj":
            if course == "":
                course = list(classInfo.keys())[-1]
            if course not in classInfo:
                classInfo[course] = {}
            # SUBCLASS referes to section combine with it
            new_section = {
                "CRN": tds[1].text,
                "SEC": tds[4].text,
                "TYPE": tds[8].text,
                "DAY": tds[9].text,
                "TIME": tds[10].text,
                "AVAIL": tds[12].text,
                "TEACH": tds[13].text,
                "DATE": tds[14].text,
                "SUBCLASS": []
            }
            if new_section["TYPE"] not in classInfo[course]:
                classInfo[course][new_section["TYPE"]] = []
            classInfo[course][new_section["TYPE"]].append(new_section)
course_key = list(classInfo.keys())
for course in course_key:
    keys = list(classInfo[course].keys())
    for i,k in enumerate(keys):
        for j in classInfo[course][k]:
            if i+1 < len(keys):
                j["SUBCLASS"] = classInfo[course][keys[i+1]]
json_file.write(json.dumps(classInfo))

'''
class course_info:

    def request_course_info(term, campus, courses):
        # find friver
        driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # request page
        driver.get('https://pawnss.usask.ca/ban/bwckschd.p_disp_dyn_sched')
        driver.maximize_window()
        time.sleep(1)
        # select term
        termes = Select(driver.find_elements_by_tag_name('select')[0])
        termes.select_by_value(term)
        driver.find_elements_by_tag_name('input')[1].click()
        time.sleep(1)
        # select campus and subject
        subjects = Select(driver.find_elements_by_tag_name('select')[0])
        for i in courses:
            subjects.select_by_value(i["course_title"])
        campuses = Select(driver.find_elements_by_tag_name('select')[2])
        campuses.deselect_all()
        campuses.select_by_value(campus)
        campuses.select_by_value(all_campus[13])
        driver.find_elements_by_tag_name('input')[0].click()
 '''

