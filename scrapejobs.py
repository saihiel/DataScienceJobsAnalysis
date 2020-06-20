import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import pyautogui
from tkinter import filedialog, Tk
import tkinter.messagebox as tm
import os
from urllib.request import urlopen
import pandas as pd
import numpy as np
import requests
import csv
import datetime

import login

class EasyApplyBot:

    MAX_APPLICATIONS = 3000

    def __init__(self,username,password, language, position, location): #, resumeloctn):

        dirpath = os.getcwd()

        self.language = language
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(chrome_options=self.options, executable_path = dirpath + "/chromedriver")
        self.start_linkedin(username,password)


    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("user-agent=Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393")
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        #options.add_argument('--disable-gpu')
        #options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        return options

    def start_linkedin(self,username,password):
        print("\nLogging in.....\n \nPlease wait :) \n ")
        self.browser.get("https://www.linkedin.com/uas/login")
        try:
            user_field = self.browser.find_element_by_id("username")
            pw_field = self.browser.find_element_by_id("password")
            user_field.click()
            user_field.send_keys(username)
            user_field.send_keys(Keys.TAB)
            time.sleep(1)
            pw_field.click()
            pw_field.send_keys(password)
            pw_field.send_keys(Keys.ENTER)
            time.sleep(1)
        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found on glassdoor.com")

    def wait_for_login(self):
        if language == "en":
             title = "Sign In to LinkedIn"
        elif language == "es":
             title = "Inicia sesión"
        elif language == "pt":
             title = "Entrar no LinkedIn"

        time.sleep(1)

        while True:
            if self.browser.title != title:
                print("\nStarting LinkedIn bot\n")
                break
            else:
                time.sleep(1)
                print("\nPlease Login to your LinkedIn account\n")

    def fill_data(self):
        self.browser.set_window_size(0, 0)
        self.browser.set_window_position(2000, 2000)
        os.system("reset")

        self.position = position
        self.location = "&location=" + location

    def start_apply(self):
        self.fill_data()
        self.applications_loop()

    def applications_loop(self):

        count_application = 1
        count_job = 0
        jobs_per_page = 0

        os.system("reset")

        print("\nLooking for jobs.. Please wait..\n")

        self.browser.set_window_position(0, 0)
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)
        
        print("\nLooking for jobs.. Please wait..\n")

        while count_application < self.MAX_APPLICATIONS:
            # sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(3.5, 6.9))
            self.load_page(sleep=1)
            page = BeautifulSoup(self.browser.page_source, 'lxml')

            jobs = self.get_job_links(page)

            if not jobs:
                print("Jobs not found")
                break

            for job in jobs:
                temp = {}

                count_job += 1
                job_page = self.get_job_page(job)

                #position_number = str(count_job + jobs_per_page)
                position_number = str(count_application)
                print(f"\nPosition {position_number}:\n {self.browser.title} \n") # {string_easy} \n")
                print(job,'\n')

                now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                temp ['timestamp'] = str(now)
                temp ['url'] = ('https://www.linkedin.com'+job)

                """
                click button see more
                """
                
                try :
                    wrapper = self.browser.find_element_by_xpath(
                        "//div[@class='cta-wrap']"
                        )
                    wrapper.find_element_by_class_name(
                        'artdeco-button'
                        ).click()
                    self.load_page(sleep=1)
                except Exception as e:
                    print('******* Job not valid *******\n')
                    print(e)
                    # exit(1)

                """
                Get data
                """
                # Top Section
                try:
                    top_section = self.browser.find_element_by_class_name(
                        'justify-space-between.display-flex.align-items-stretch.mb4')
                    top_section = top_section.find_element_by_class_name(
                        'mt6.ml5.flex-grow-1')
                    company_info = self.browser.find_element_by_xpath(
                        '//h3[@class="jobs-top-card__company-info t-14 mt1"]'
                    )
                except Exception as e:
                    print('Top Section not collected. Error - \n', e)
                    top_section = None
                    company_info = None
                # position
                try:
                    temp['position'] = self.browser.find_element_by_xpath(
                        '//h1[@class="jobs-top-card__job-title t-24"]'
                        ).text.strip()
                except Exception as e1:
                    print('position Error:\n', e1)
                    temp['position'] = None

                # company name
                try:
                    temp['company_name'] = company_info.find_element_by_tag_name('a').text.strip()
                except Exception as e1:
                    print('company_name Error:\n', e1)
                    temp['company_name'] = None

                # job location
                try:
                    temp['company_location'] = company_info.find_element_by_class_name('jobs-top-card__bullet').text.strip()
                except Exception as e1:
                    print('company_location Error:\n', e1)
                    temp['company_location'] = None

                # date posted
                try:
                    posting_info = top_section.find_element_by_class_name('mt1.full-width.flex-grow-1.t-14.t-black--light')
                    temp['posting_date'] = posting_info.find_element_by_xpath('./span[2]').text.strip()
                except Exception as e1:
                    print('posting_date Error:\n', e1)
                    temp['posting_date'] = None

                # Bottom Section
                try:
                    bottom_section = self.browser.find_element_by_class_name(
                        'jobs-box.jobs-box--fadein.jobs-premium-applicant-insights.container-premium.ember-view')
                    bottom_section_top_half = bottom_section.find_element_by_xpath('./div[2]')
                    bottom_section_bottom_half = bottom_section.find_element_by_xpath('./div[3]')
                except Exception as e:
                    print('Bottom Section not collected. Error - \n', e)
                    bottom_section = None
                    bottom_section_bottom_half = None
                    bottom_section_top_half = None

                # total num applicants
                try:
                    temp['num_applicants'] = self.browser.find_element_by_class_name('jobs-premium-applicant-insights__list-num.t-24.t-black--light.t-light.pr2').text.strip()
                except:
                    try:
                        applicants_total = self.browser.find_element_by_class_name(
                            '"t-14.t-black.t-bold"').text.strip()
                        index_start = applicants_total.find('of ')+3
                        index_end = applicants_total.find('appli')
                        temp['num_applicants'] = applicants_total[index_start:index_end]
                    except Exception as e1:
                        print('num_applicants Error:\n', e1)
                        temp['num_applicants'] = None

                # skills
                try:
                    skills_premium_insights = bottom_section_top_half.find_element_by_class_name('jobs-details-premium-insight.jobs-details-premium-insight--row.top-skills.ember-view')
                    all_skills = skills_premium_insights.find_element_by_class_name(
                        'jobs-premium-applicant-insights__list.pt2.ph0.pb0')
                    all_skills_list = all_skills.find_elements_by_tag_name("li")
                    skills = []
                    # print('len: skills list collected', len(all_skills_list))
                    for i in all_skills_list:
                        skill = i.find_element_by_tag_name('p').text.strip()
                        # print('Skill: ', skill)
                        skills.append(skill)
                    temp['skills'] = skills
                except Exception as e1:
                    print('Skills  Error:\n', e1)
                    temp['skills'] = None

                # break down of applicant seniority
                try:
                    seniority_breakdown_premium = bottom_section_bottom_half.find_element_by_class_name('jobs-details-premium-insight.jobs-details-premium-insight--row.jobs-details-premium-insight--left-column.applicant-experience.ember-view')
                    num_applicants_breakdown = seniority_breakdown_premium.find_element_by_class_name('jobs-details-premium-insight__list')
                    num_breakdown_list = num_applicants_breakdown.find_elements_by_tag_name("li")
                    applicants_breakdown = []
                    for i in num_breakdown_list:
                        applicants_breakdown.append(i.find_element_by_tag_name('p').text.strip())
                    temp['num_app_breakdown'] = applicants_breakdown
                except Exception as e1:
                    print('applicant seniority breakdown Error:\n', e1)
                    temp['num_app_breakdown'] = None

                # education
                try:
                    applicants_education = self.browser.find_element_by_class_name('jobs-details-premium-insight.jobs-details-premium-insight--row.applicant-education.ember-view')
                    type_applicants_breakdown = applicants_education.find_element_by_class_name('jobs-details-premium-insight__list.jobs-premium-applicant-insights__list')
                    list_of_applicant_types = type_applicants_breakdown.find_elements_by_tag_name("li")
                    education_breakdown = []
                    # print('len: education list collected', len(list_of_applicant_types))
                    for i in list_of_applicant_types:
                        edu_text = ''
                        edu_text += i.find_element_by_xpath('./span[1]').text.strip()
                        edu_text += '% '
                        edu_text += i.find_element_by_xpath('./span[2]').text.strip()
                        education_breakdown.append(edu_text)
                    temp['edu_breakdown'] = education_breakdown
                except Exception as e1:
                    print('Education breakdown Error:\n', e1)
                    temp['edu_breakdown'] = None

                # Job Details Section
                try:
                    job_details = self.browser.find_element_by_class_name('jobs-description__details')
                except Exception as e:
                    print('Job Details not collected. Error - \n', e)
                    job_details=None

                # Job seniority
                try:
                    temp['seniority'] = job_details.find_element_by_class_name('jobs-box__body.js-formatted-exp-body').text.strip()
                except Exception as e1:
                    print('seniority Error:\n', e1)
                    temp['seniority'] = None

                # employment type
                try:
                    temp['employment_type'] = job_details.find_element_by_class_name(
                        'jobs-box__body.js-formatted-employment-status-body').text.strip()
                except Exception as e1:
                    print('employment_type Error:\n', e1)
                    temp['employment_type'] = None

                # industry
                try:
                    industries = job_details.find_element_by_class_name(
                        'jobs-box__list.jobs-description-details__list.js-formatted-industries-list')
                    industries_list = industries.find_elements_by_tag_name("li")
                    industry_names = []
                    for industry in industries_list:
                        industry_names.append(industry.text.strip())
                    temp['industry'] = industry_names
                except Exception as e1:
                    print('industry Error:\n', e1)
                    temp['industry'] = None

                # job details
                try:
                    temp['job_description'] = self.browser.find_element_by_xpath(
                        '//div[@id="job-details"]'
                    ).text.strip().replace('\n', ', ')
                except Exception as e1:
                    print('job_description Error:\n', e1)
                    temp['job_description'] = None
                    # temp['company'] = None
                
                try:
                    temp['company description'] = self.browser.find_element_by_id(
                        'company-description-text'
                        ).text.strip()
                except:
                    temp['company description'] = None

                """
                Write to file
                """

                data = temp
                with open('output.csv', 'a', newline='') as f:
                    try:
                        writer = csv.writer(f)
                        writer.writerow(data.values())
                        print('Job added to output.csv')
                    except:
                        print('*** Ooopss, NOT able to write job to output, sorry :(')

                


                """
                Count application and set sleep time
                """
                count_application = count_application + 1

                if count_application % 20 == 0:
                    sleepTime = random.randint(290, 500)
                    print('\n\n****************************************\n\n')
                    print('Time for a nap - see you in ', sleepTime/60, ' min')
                    print('\n\n****************************************\n\n')
                    time.sleep (sleepTime)

                if count_job == len(jobs):
                    jobs_per_page = jobs_per_page + 25
                    count_job = 0
                    print('\n\n****************************************\n\n')
                    print('Going to next jobs page, YEAAAHHH!!')
                    print('\n\n****************************************\n\n')
                    self.avoid_lock()
                    self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)

        self.finish_apply()

    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:
                if '/jobs/view' in url:
                    links.append(url)
        return set(links)

    def get_job_page(self, job):
        root = 'www.linkedin.com'
        if root not in job:
            job = 'https://www.linkedin.com'+job
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

    def got_easy_apply(self, page):
        button = page.find("button", class_="jobs-s-apply__button js-apply-button")
        return len(str(button)) > 4

    def get_easy_apply_button(self):
        button_class = "jobs-s-apply--top-card jobs-s-apply--fadein inline-flex mr2 jobs-s-apply ember-view"
        button = self.job_page.find("div", class_=button_class)
        return button

    def easy_apply_xpath(self):
        button = self.get_easy_apply_button()
        button_inner_html = str(button)
        list_of_words = button_inner_html.split()
        next_word = [word for word in list_of_words if "ember" in word and "id" in word]
        ember = next_word[0][:-1]
        xpath = '//*[@'+ember+']/button'
        return xpath

    def click_button(self, xpath):
        triggerDropDown = self.browser.find_element_by_xpath(xpath)
        time.sleep(0.5)
        triggerDropDown.click()
        time.sleep(1)

    def load_page(self, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(sleep)

        if sleep != 1:
            self.browser.execute_script("window.scrollTo(0,0);")
            time.sleep(sleep * 3)

        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def avoid_lock(self):
        x, y = pyautogui.position()
        pyautogui.moveTo(x+200, y, duration=1.0)
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.keyDown('cmd')
        pyautogui.press('esc')
        pyautogui.keyUp('cmd')
        time.sleep(0.5)
        pyautogui.press('esc')

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            #"https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=" +
            "https://www.linkedin.com/jobs/search/?keywords=" +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.avoid_lock()
        self.load_page()
        return (self.browser, jobs_per_page)

    def finish_apply(self):
        self.browser.close()


if __name__ == '__main__':

    # set use of gui (T/F)
    useGUI = False
    
    # use gui
    if useGUI == True:

        app = login.LoginGUI()
        app.mainloop()

        #get user info info
        username=app.frames["StartPage"].username
        password=app.frames["StartPage"].password
        language=app.frames["PageOne"].language
        position=app.frames["PageTwo"].position
        location_code=app.frames["PageThree"].location_code
        if location_code == 1:
            location=app.frames["PageThree"].location
        else:
            location = app.frames["PageFour"].location
        resumeloctn=app.frames["PageFive"].resumeloctn

    # no gui
    if useGUI == False:

        username = 'bakshisaihiel@gmail.com'
        password = 'saihiels'
        language = 'en'
        position = '(data science OR data analyst) NOT (software engineer OR software developer)'
        location = 'Greater Toronto Area Metropolitan Area'

    # print input
    print("\nThese is your input:")

    print  ("\nUsername:  "+ username,
        "\nPassword:  "+ password,
        "\nLanguage:  "+ language,
        "\nPosition:  "+ position,
        "\nLocation:  "+ location)
    
    print("\nLet's scrape some jobs!\n")
    
    # start bot
    bot = EasyApplyBot(username,password, language, position, location) #, resumeloctn)
    bot.start_apply()
