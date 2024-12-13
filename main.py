import random
import time
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from dbConnection import dbConn
from driverConfig import setDriver
from tableData import getTableData

load_dotenv()
connection = dbConn()
driver = setDriver()

retry = 0
while retry < 6:
    try:
        driver.maximize_window()
        driver.get(os.environ['URL'])
        time.sleep(random.uniform(1, 2))
        driver.execute_script("window.open('https://www.google.com', '_blank');")
        time.sleep(random.uniform(1, 2))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(random.uniform(1, 2))
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(random.uniform(4, 7))
        driver.find_element(By.ID, value='formPublica:porParte:header:inactive').click()

        time.sleep(random.uniform(1, 5))
        jurisdiccionSelect = driver.find_element(By.ID, value='formPublica:camaraPartes')
        time.sleep(random.uniform(1, 4))
        selectValues = jurisdiccionSelect.find_elements(By.TAG_NAME,value='option')

        for value in selectValues:
            if value.get_attribute("value") == '10':
                value.click()

        driver.find_element(By.ID, value='formPublica:nomIntervParte').send_keys('residuos')
        time.sleep(random.uniform(3, 9))

        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, value='//*[@id="recaptcha-anchor"]/div[1]').click()

        time.sleep(random.uniform(8, 12))
        driver.switch_to.default_content()

        driver.find_element(By.ID, value='formPublica:buscarPorParteButton').click()
        time.sleep(random.uniform(4, 7))
        break
    except Exception:
        retry += 1
        time.sleep(random.uniform(4, 7))
        driver.refresh()
else:
    driver.quit()    


getTableData(driver, connection)

try:
    nextButton = driver.find_element(By.ID, 'j_idt118:j_idt208:j_idt215').click()
    time.sleep(random.uniform(2, 5))
    getTableData(driver, connection)
except NoSuchElementException:
    driver.quit()
    connection.close()
