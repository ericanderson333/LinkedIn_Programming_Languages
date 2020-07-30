import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import time
import os
#path to chrome webdriver
chrome_path = 'your chrome path here'

#Build Main DataFrame and Lists of objects to pass through
Cols = ['DATA', 'SOFTWARE', 'NETWORK', 'DATABASE', 'CLOUD', 'WEB', 'AUTOMATION', 'SECURITY', 'UI', 'UX', 'IT', 'BACKEND',
        'FRONTEND', 'INFORMATION TECHNOLOGY', 'DESIGN DEVELOPER', 'CYBERSECURITY', 'DEBUG', 'SOLUTIONS', 'STACK']
Rows = ['JAVA', 'JAVASCRIPT', 'C++', '.NET', 'PYTHON', 'SHELL', 'RUBY', 'PERL', 'SQL', 'MYSQL', 'AWS', 'PUPPET',
        'C#', 'HTML', 'CSS', 'PHP', 'NODE', 'SWIFT', 'R', 'TYPESCRIPT', 'MATLAB', 'SAS']
main_df = pd.DataFrame(index=Rows, columns=Cols)
main_df = main_df.fillna(0)

#build dataframe for counted list
count = ['COUNT', 'MISSED DATA']
count_df = pd.DataFrame(index=count, columns=Cols)
count_df = count_df.fillna(0)

#Web Elements to access:
url = 'https://www.linkedin.com/jobs/search?keywords={}&location=Portland%2C%20Oregon%2C%20United%20States&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
class_name="result-card job-result-card result-card--with-hover-state"
jobs_element = 'li[data-row="{}"]' #USE THIS ONE
description_src = 'div[class="show-more-less-html__markup"]'
show_button = 'button[class="show-more-less-html__button show-more-less-html__button--more"]'
title_element = 'h2[class="topcard__title"]'

def get_data():
    for item in Cols:
        print(item.split(' ')[0])
        job_count, missed_count = scroll_data(item)
        count_df[item][count[0]] = job_count
        count_df[item][count[1]] = missed_count


def scroll_data(job_title):
    browser = webdriver.Chrome(chrome_path)
    #pass in job title through search bar and go to url
    browser.get(url.format(job_title.replace(' ', '-')))
    time.sleep(1)

    #for scrolling
    elem = browser.find_element_by_tag_name("body")
    more_jobs = 'See more jobs'
    aria = browser.find_element_by_css_selector('button[aria-label="Load more results"]')
    #while no_of_pagedowns:
    while aria.text != more_jobs:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        aria = browser.find_element_by_css_selector('button[aria-label="Load more results"]')
    #src_page for src of whole scrolled page
    src_page =browser.page_source
    #create list of all the jobs loaded on the page (So we can traverse through each job in for loop)
    soup = BeautifulSoup(src_page, 'html.parser')
    jobs_elem = soup.find_all('li', class_=class_name)
    #c = count how mny jobs, o = count many jobs were skipped because of error
    c = 0
    o = 0
    for count, rows in enumerate(jobs_elem):
        try:
            #use count for row of job listing, work on timing for each button
            test = browser.find_element_by_css_selector(jobs_element.format(count+1))
            test.click()
            time.sleep(2)
            title = browser.find_element_by_css_selector(title_element)
            #to only check title with the first word of each job comparisson to see if meet criteria
            time.sleep(0.3)
            if title.text.upper().count(job_title.split(' ')[0]) < 1:
                continue
            #clicks show button to get all data to compare
            test = browser.find_element_by_css_selector(show_button)
            test.click()
            time.sleep(1)
            #pass in all data to compare into description info which will contain text as string type
            description_info = browser.find_element_by_css_selector(description_src)
            compare_data(job_title, description_info.text)
            c += 1
            print(main_df)
        except ElementNotInteractableException:
            o += 1
            continue
        except StaleElementReferenceException:
            o += 1
            continue
    browser.close()
    return c, o


def compare_data(job_title, description_to_comp):
    for item in Rows:
        description_to_comp.replace(',', ' , ').replace('/', ' / ').replace('-', ' - ')
        if description_to_comp.upper().count(item) > 0:
            main_df[job_title][item] += 1
            print('1')

def merge_categories():
    df = pd.read_csv('data/job_lang_data.csv')
    count_df = pd.read_csv('data/job_count.csv')
    new_cols = ['DATA SCIENCE', 'SOFTWARE DEV', 'NETWORKS', 'DATABASES', 'CLOUD DEV', 'WEB DESIGN', 'AUTOMATIONS',
                'SECURITY/CYBERSECURITY', 'INFORMATION TECH', 'DEBUGGER', 'STACKS']
    for i, item in enumerate(new_cols):
        if i == 0:
            df[item] = df['DATA']
            count_df[item] = count_df['DATA']
        elif i == 1:
            df[item] = df['SOFTWARE'] + df['BACKEND']
            count_df[item] = count_df['SOFTWARE'] + count_df['BACKEND']
        elif i == 2:
            df[item] = df['NETWORK']
            count_df[item] = count_df['NETWORK']
        elif i == 3:
            df[item] = df['DATABASE']
            count_df[item] = count_df['DATABASE']
        elif i == 4:
            df[item] = df['CLOUD']
            count_df[item] = count_df['CLOUD']
        elif i == 5:
            df[item] = df['WEB'] + df['UI'] + df['UX'] + df['FRONTEND'] + df['DESIGN DEVELOPER']
            count_df[item] = count_df['WEB'] + count_df['UI'] + count_df['UX'] + count_df['FRONTEND'] + \
                                   count_df['DESIGN DEVELOPER']
        elif i == 6:
            df[item] = df['AUTOMATION']
            count_df[item] = count_df['AUTOMATION']
        elif i == 7:
            df[item] = df['SECURITY'] + df['CYBERSECURITY']
            count_df[item] = count_df['SECURITY'] + count_df['CYBERSECURITY']
        elif i == 8:
            df[item] = df['IT'] + df['INFORMATION TECHNOLOGY']
            count_df[item] = count_df['IT'] + count_df['INFORMATION TECHNOLOGY']
        elif i == 9:
            df[item] = df['DEBUG'] + df['SOLUTIONS']
            count_df[item] = count_df['DEBUG'] + count_df['SOLUTIONS']
        elif i == 10:
            df[item] = df['STACK']
            count_df[item] = count_df['STACK']
    df.drop(Cols, axis=1, inplace=True)
    count_df.drop(Cols, axis=1, inplace=True)
    df.to_csv('data/merged_job_lang_data.csv')
    count_df.to_csv('data/merged_job_count_data.csv')

if __name__ == '__main__':
    #scrape linkedin for all jobs listed above, main_df and count df are global variables
    #takes roughly 2-3 hours to parse through
    #ALSO, DONT USE 'R' COLUMN. DOESNT ACCOUNT FOR LANGAUGE BUT READS IN EVERY R VALUE, BAD
    get_data()
    #create path for data
    if not os.path.exists('data'):
        os.makedirs('data')
    main_df.to_csv('data/job_lang_data.csv')
    count_df.to_csv('data/job_count.csv')
    #merge all data into their collective categories
    merge_categories()

