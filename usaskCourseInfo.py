from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import json
import pprint
# load driver
driver = webdriver.Chrome(executable_path='chromedriver.exe')
# open browser and go to link
driver.get('https://pawnss.usask.ca/ban/bwckschd.p_disp_dyn_sched')
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
        value = strongs.text
        if " " in value:
            # course name format: abc 123.n - t1/t2(nlec-nlab...)
            course_infos = value.split(" ")
            courseName = course_infos[0]+course_infos[1].split(".")[0]
            lecInfo = ''.join(c for c in ''.join((course_infos[3].split("(")[1][:-1]).split("-")) if not c.isdigit())
            courses[courseName] = lecInfo
json_file.write(json.dump(courses))





