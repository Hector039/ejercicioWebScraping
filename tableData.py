import random
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def getTableData(driver, connection):
    anchors = driver.find_elements(By.CLASS_NAME, 'btn-group')

    i = 0
    while i < len(anchors):
        time.sleep(random.uniform(2, 5))
        anchors = driver.find_elements(By.CLASS_NAME, 'btn-group')
        anchors[i].click()

        time.sleep(random.uniform(2, 5))
        try:
            ultimaActuacion = driver.find_element(By.XPATH, value='//*[@id="expediente:action-table"]/tbody/tr[1]/td[3]/span[2]').text
        except NoSuchElementException:
            ultimaActuacion = ''
        
        expediente = driver.find_element(By.XPATH, value='//*[@id="expediente:j_idt90:j_idt91"]/div/div[1]/div/div/div[2]/span').text
        jurisdiccion = driver.find_element(By.ID, value='expediente:j_idt90:detailCamera').text
        dependencia = driver.find_element(By.ID, value='expediente:j_idt90:detailDependencia').text
        situacion = driver.find_element(By.ID, value='expediente:j_idt90:detailSituation').text
        caratula = driver.find_element(By.ID, value='expediente:j_idt90:detailCover').text
        
        time.sleep(random.uniform(1, 2))
        driver.find_element(By.ID, value='expediente:j_idt261:header:inactive').click()
        time.sleep(random.uniform(2, 5))

        try:
            demandado = driver.find_element(By.XPATH, value='//*[@id="expediente:participantsTable:0:j_idt270"]/span[2]').text
        except NoSuchElementException:
            demandado = ''
        try:
            actor = driver.find_element(By.XPATH, value='//*[@id="expediente:participantsTable:1:j_idt270"]/span[2]').text
        except NoSuchElementException:
            actor = ''

        
        cursor = connection.cursor()
        sql = f"INSERT INTO data (expediente, jurisdiccion, dependencia, situacion, caratula, ultimaActuacion, demandado, actor) VALUES ('{expediente}', '{jurisdiccion}', '{dependencia}', '{situacion}', '{caratula}', '{ultimaActuacion}', '{demandado}', '{actor}');"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        time.sleep(random.uniform(2, 5))

        i += 1

        driver.find_element(By.XPATH, '//*[@id="expediente:j_idt78"]/div/a').click()