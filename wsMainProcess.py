import random
import time
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tableData import getTableData
from driverConfig import setDriver
from dotenv import load_dotenv
from dbConnection import dbConn

load_dotenv()
connection = dbConn()

def wsProcess(query):
    driver = setDriver()
    retry = 0
    while retry < 6:
        try:
            driver.get(os.environ['URL'])
            time.sleep(random.uniform(4, 7))
            driver.find_element(By.ID, value='formPublica:porParte:header:inactive').click()

            time.sleep(random.uniform(1, 5))
            jurisdiccionSelect = driver.find_element(By.ID, value='formPublica:camaraPartes')
            time.sleep(random.uniform(1, 4))
            selectValues = jurisdiccionSelect.find_elements(By.TAG_NAME,value='option')

            for value in selectValues:
                if value.get_attribute("value") == '10':
                    value.click()

            driver.find_element(By.ID, value='formPublica:nomIntervParte').send_keys(query)
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
        driver.find_element(By.ID, 'j_idt118:j_idt208:j_idt215').click()
        time.sleep(random.uniform(2, 5))
        getTableData(driver, connection)
    except NoSuchElementException:
        driver.quit()
        connection.close()

def getData():
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM data;"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as error:
        return {'message': error}
    