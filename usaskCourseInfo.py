from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver.exe',options=chrome_options)
# open browser and go to link
driver.get('http://www.usask.ca/calendar/coursecat/?subj_code=ACB#results')
driver.maximize_window()
time.sleep(1)
subjects = Select(driver.find_element_by_xpath('//*[@id="subj-code"]'))
select_subject_list = [o.get_attribute('value') for o in subjects.options]
json_file = open("cour_info.json", "w+")
courses = {}
for i in select_subject_list:
    subjects = Select(driver.find_element_by_xpath('//*[@id="subj-code"]'))
    subjects.select_by_value(i)
    driver.find_element_by_xpath('//*[@id="course-search"]/div[3]/div/button').click()
    strongs = driver.find_elements_by_tag_name('strong')
    for i in strongs:
        value = i.text
        if " " in value and 'Prerequisite' not in value and 'Permission' not in value and 'Department' not in value and 'Students' not in value:
            # course name format: abc 123.n - t1/t2(nlec-nlab...)
            course_infos = value.split(" ")
            courseName = course_infos[0]+course_infos[1].split(".")[0]
            lecInfo = ""
            if len(course_infos) > 2:
                if '(' in course_infos[3]:
                    lecInfo = ''.join((course_infos[3].split("(")[1][:-1]).split("-"))
                lecInfo = ''.join(c for c in lecInfo if c.isalpha())
            try:
                course_number = int(course_infos[1].split(".")[0])
                if lecInfo != "" and course_number < 800 and course_number > 100:
                    courses[courseName] = lecInfo
            except:
                pass
json_file.write(json.dumps(courses))





