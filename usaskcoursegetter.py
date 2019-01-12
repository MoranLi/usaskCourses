from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import json


class GetCourseInfoPAWS:

    def load_driver(self):
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        return driver

    def select_term(self, driver, term):
        # open the browser and go to link
        driver.get('https://pawnss.usask.ca/ban/bwckschd.p_disp_dyn_sched')
        # position to select element use to select term
        select_term = Select(driver.find_elements_by_tag_name('select')[0])
        # select term base on user input
        select_term.select_by_value(term)
        return driver

    def select_subject(self, driver, subjects):
        # position to select element use to select subject
        select_subjects = Select(driver.find_elements_by_tag_name('select')[0])
        # the format of each course
        for i in subjects:
            select_subjects.select_by_value(i)
        return driver

    def select_campus(self, driver, campus):
        # select campus, currently main campus and web
        select_campus = Select(driver.find_elements_by_tag_name('select')[2])
        # deselect all since all is default option
        select_campus.deselect_all()
        # allow user to not select any campus, use default setting ( saskatoon main campus and web)
        if not campus:
            select_campus.select_by_index(1)
            select_campus.select_by_index(13)
        else:
            for i in campus:
                select_campus.select_by_value(i)
        return driver

    def combine_subject_and_number(self, courses):
        class_info = {}
        for i in range(0, len(courses[0])):
            class_info[courses[0][i] + courses[1][i]] = {}
        return class_info

    def new_section(self, tds):
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
        return new_section


    def get_section_info(self, driver, courses):

        # we only need top consider course selected by the user, but no need to other course in subject selected by user
        class_info = self.combine_subject_and_number(courses)
        # dict stroe all the course info

        # loaded in to course info page
        # the page is showing in a table, so we only need table row(tr)
        trs = driver.find_elements_by_class_name("datadisplaytable")[0].find_elements_by_tag_name('tr')
        # store the last main ( usually LEC/LAB type) course find
        # used for course have 1+ combine course
        # for instance LAB for phys155
        # the first row is first day`s lab, followed by several rows of days have lab
        last_class_need_additional = None
        # iterate over all the rows
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            # len(tds) == 1 means this is only one section, usually an information section to tell subject etc
            if len(tds) > 1:
                subject = tds[2].text
                course_number = tds[3].text
                # course with perspective will have a * after course name, need to remove
                if course_number[-1] == "*":
                    course_number = course_number[:-1]
                # get the course_name
                course = subject.strip() + course_number.strip()
                # for the first row of each subject, it is an information row explain following row, we need to skip it
                if course != "CRNSubj":
                    # a section with no course name means it is subclass of previous section, just get a copy of that
                    if course == "":
                        # the key of a dict in python is ordered by insert sequence, so we can just use the last one
                        course = list(class_info.keys())[-1]
                    if course in class_info:
                        # create new section object
                        new_section = self.new_section(tds)
                        # store new course type if it is not in class
                        # since we need all type to combine to one course selection info
                        if new_section["TYPE"] not in class_info[course]:
                            class_info[course][new_section["TYPE"]] = []
                        # set the new last_class_need_additional
                        # since we know if a course append with CRN, it must be a new section
                        # otherwise it is combination section to previous section
                        if new_section["CRN"] != " ":
                            last_class_need_additional = new_section
                            class_info[course][new_section["TYPE"]].append(new_section)
                        else:
                            last_class_need_additional["SUBCLASS"].append(new_section)
        return class_info

    def get_course_info_paws(self,term, courses, campus):
        # load driver
        driver = self.load_driver()
        # select term
        driver = self.select_term(driver, term)
        # click submit, to go to next page, driver will auto-load next page
        driver.find_elements_by_tag_name('input')[1].click()
        # select subject
        driver = self.select_subject(driver, courses[0])
        # select campus
        driver = self.select_campus(driver, campus)
        time.sleep(3)
        # click submit, to go to next page, driver will auto-load next page
        driver.find_elements_by_tag_name('input')[0].click()
        # get class info
        class_info = self.get_section_info(driver, courses)
        return class_info

if __name__ == "__main__":
    courses = [
        ['CMPT', 'CHEM', 'PHYS', 'MATH', 'ECON'],
        ['145', '115', '117', '116', '114']
    ]
    get_course_info = GetCourseInfoPAWS()
    open('section_info.json', 'w+').write(json.dumps(get_course_info.get_course_info_paws('201901',courses,None)))


