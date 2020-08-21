from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import html2text
import stringcase

base_url = "https://leetcode.com/problems/find-lucky-integer-in-an-array/"
driver = webdriver.Chrome()
driver.get(base_url)

h = html2text.HTML2Text()
h.ignore_emphasis = True

wait_time = 10


def wait_for_element(css_class_name):
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, css_class_name))
    )
    return element


def strip_text(css_class_name):
    element = wait_for_element(css_class_name)
    content = h.handle(element.get_attribute('innerHTML'))
    return content


def scrape_page():

    title = stringcase.spinalcase(strip_text('css-v3d350').split('.')[1].replace(" ", "").strip())
    content = strip_text('content__u3I1')
    code = driver.find_elements_by_css_selector("pre[class=' CodeMirror-line ']")

    formatted_code = ''

    for line in code:
        line_html = line.get_attribute('innerHTML')
        line_text = h.handle(line_html)
        formatted_code += line_text.strip()

    f = open("algorithms/" + title, "w")
    f.write(content + "Exp Starter Code:\n" + formatted_code)

    try:
        next_button = driver.find_element_by_xpath("//button[@data-cy = 'next-question-btn']")
        next_button.click()
        scrape_page()
    except TimeoutError:
        return


def scrape():
    input('Enter any key to begin? ')
    scrape_page()
    driver.quit()


scrape()
