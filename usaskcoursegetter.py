from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import pprint
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://pawnss.usask.ca/ban/bwckschd.p_disp_dyn_sched')
driver.maximize_window()
time.sleep(1)
term = Select(driver.find_elements_by_tag_name('select')[0])
all_terms = [o.get_attribute('value') for o in term.options]
term.select_by_value(all_terms[3])
driver.find_elements_by_tag_name('input')[1].click()
time.sleep(1)
subjects = Select(driver.find_elements_by_tag_name('select')[0])
all_subjects = [o.get_attribute('value') for o in subjects.options]
subjects.select_by_value(all_subjects[3])
campus = Select(driver.find_elements_by_tag_name('select')[2])
campus.deselect_all()
all_campus = [o.get_attribute('value') for o in campus.options]
campus.select_by_value(all_campus[1])
campus.select_by_value(all_campus[13])
driver.find_elements_by_tag_name('input')[0].click()
trs = driver.find_elements_by_class_name("datadisplaytable")[0].find_elements_by_tag_name('tr')
classInfo = {}
# iterate over all the rows
for tr in trs:
    tds = tr.find_elements_by_tag_name('td')
    if len(tds) > 1:
        subject = tds[2].text
        course_number = tds[3].text
        course = subject.strip() + course_number.strip()
        if course != "CRNSubj":
            if course == "":
                course = list(classInfo.keys())[-1]
            if course not in classInfo:
                classInfo[course] = {
                    "LEC": [],
                    "OTHER": []
                }
            new_section = {
                "CRN": tds[1].text,
                "SEC": tds[4].text,
                "TYPE": tds[8].text,
                "DAY": tds[9].text,
                "TIME": tds[10].text,
                "AVAIL": tds[11].text,
                "TEACH": tds[12].text,
                "DATE": tds[13].text,
                "LABED": False
            }
            if new_section["TYPE"] != "LEC":
                classInfo[course]["OTHER"].append(new_section)
            else:
                classInfo[course]["LEC"].append(new_section)
pprint.pprint(classInfo)

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

