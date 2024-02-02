# ------------- Import -------------
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yaml



driver = webdriver.Chrome()

# ------------- Open LMS -------------
def open_lms():
    global driver
    #  ------------- URL -------------
    driver = webdriver.Chrome()
    url = "https://vulms.vu.edu.pk/"
    driver.get(url)

def login(student_id,password):
    # ------------- Enter UserName Input -------------
    email_input = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/form/div[3]/div/div[2]/div[2]/div[1]/input")
    email_input.send_keys(student_id)
    password_input = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/form/div[3]/div/div[2]/div[2]/div[2]/div[1]/input")
    password_input.send_keys(password)
    sign_btn = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/form/div[3]/div/div[2]/div[2]/div[3]/input")
    sign_btn.click()

def check_feedback_page():

    # -----------------------------------Check for feedback page---------------------------
    feedback_xpath = "/html/body/form/table/tbody/tr[1]/td/table[1]/tbody/tr/td[2]/input"
    try:
        # Attempt to find the element using the specified XPath
        feeback =  driver.find_element(By.XPATH,feedback_xpath)
        skip_survey = driver.find_element(By.XPATH,feedback_xpath)
        skip_survey.click()
        
        # If the element is found, execute the specific function
    except NoSuchElementException:
        # If the element is not found, handle the condition as needed
        print(f"XPath for FeedBack page not found. Handling the condition.")
    # -----------------------------------Feedback Page Handeled---------------------------


def select_course(course_id):
    # ------------- Select the Course to Open Lecture -------------
    gen_id = "MainContent_gvCourseList_lbtnCurrentLesson_"
    course_id = str(int(course_id)-1)
    select_course = gen_id+course_id
    course = driver.find_element(By.ID,select_course)
    course.click()
    
def load_config(file_path='stu_config.yml'):
    # ------------- Creditential in Main file -------------
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data


def navigate_lecture():
    # ------------- Desired Course Opened -------------
    print("Entered Navigation phase...")
    next_btn = driver.find_element(By.XPATH,"/html/body/form/div[2]/div/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li[2]/a")
    while (True): #This loop Controls how many time it iterates (infinite)
        quiz_complete_status = (driver.find_element(By.XPATH,"/html/body/form/div[2]/div/div[6]/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[2]/span[1]")).text
        reading_complete_status = (driver.find_element(By.XPATH,"/html/body/form/div[2]/div/div[6]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/span[1]")).text
        video_complete_status = (driver.find_element(By.XPATH,"/html/body/form/div[2]/div/div[6]/div[2]/div/div/div/div[2]/div[2]/div[3]/div/div[2]/span[1]")).text
        count = 1
        # ------------- Click Next Button when available -------------
        try:
            next_btn_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/div[2]/div/div[6]/div[2]/div/div/div/div[1]/div[2]/ul/li[2]/a")))
            next_btn_2.click()
            count = count +1
            print(f"Clicked Next {count}")
        except Exception as e:
            pass


def driver():
    # ------------- Driver function -------------
    config = load_config()
    student_id = config.get('student_id', None)
    password = config.get('password', None)
    course_id = str(config.get('course_id', None))
    open_lms()
    time.sleep(5)
    login(student_id,password)
    time.sleep(5)
    check_feedback_page()
    time.sleep(5)
    select_course(course_id)
    time.sleep(5)
    navigate_lecture()
    print("Out of Navigation")
    time.sleep(50)
        


driver()