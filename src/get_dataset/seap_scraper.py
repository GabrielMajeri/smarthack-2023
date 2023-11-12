import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from get_dataset.create_table import Tender_procedures
from get_dataset.create_table import Tender_documents


WEB_PORTAL = "https://www.e-licitatie.ro/pub/notices/c-notice/v2/view/"
LAND_ACQUISITION_PDFS = r"C:\Users\Stefan\Desktop\Facultate\GitHubProjects\SH\land_acquisition_pdfs"
FIELDS = [('Denumire si adrese', 'strong', 'institution_name'),
          ('Tipul autoritatii contractante', 'span', 'institution_type'),
          ('Activitate principala', 'span', 'activity_type'),
          ('Titlu', 'span', 'tender_name'),
          ('Cod CPV principal', 'span', 'CPV_code'),
          ('Tipul contractului', 'span', 'contract_type'),
          ('Descriere succinta', 'span', 'short_desc'),
          ('Descrierea achizitiei publice', 'span', 'long_desc'),
          ('Criterii de atribuire', 'span', 'criteria_signing'),
          ('Capacitatea de exercitare a activitatii profesionale', 'span', 'activity_capacity'),
          ('Capacitatea tehnica si profesionala', 'span', 'technical_capacity')]


def get_url():
    current_url = driver.current_url
    return current_url


def get_tender_id():
    acquisition_nbr_str = driver.find_element(By.XPATH,
                                              '//*[@id="container-sizing"]/div[1]/div[1]/div/div/h1/span[2]').text
    pattern = re.search(r'\[([^\]]+)\]', acquisition_nbr_str)
    _acquisition_nbr = pattern.group(1)
    return _acquisition_nbr


def section(_search_text, _element):
    xpath_expression = f"//*[contains(text(), '{_search_text}')]"
    element_with_text = driver.find_element(By.XPATH, xpath_expression)

    next_sibling = element_with_text.find_element(By.XPATH, 'following-sibling::*')

    value = next_sibling.find_element(By.CSS_SELECTOR, _element).text
    return value


def get_sections():
    result = []
    for field in range(len(FIELDS)):
        try:
            value = section(FIELDS[field][0], FIELDS[field][1])
            result.append(value)
        except:
            result.append(None)
            #print(f'# {field[2]}:' + str('NULL'))
    return result


def get_estimated_value():
    xpath_expression = f"//*[contains(text(), 'Valoarea totala estimata')]"
    element_with_text = driver.find_element(By.XPATH, xpath_expression)
    next_sibling = element_with_text.find_element(By.XPATH, 'following-sibling::*')
    div_element = next_sibling.find_element(By.CLASS_NAME, 's-row.u-displayfield.ng-scope')

    _min_value = ''
    _max_value = ''
    _currency = ''
    raw_estimated_value = div_element.text

    if raw_estimated_value.find('Intervalul') != -1:
        pattern = r'(?<![\d.,])[0-9]+(?:[.,][0-9]+)*(?![\d.,])'
        matches = re.findall(pattern, raw_estimated_value)
        _min_value = matches[0]
        _max_value = matches[1]

        pattern = r'Moneda: (\w{3})'
        match = re.findall(pattern, raw_estimated_value)
        _currency = match[0]
    elif raw_estimated_value.find('Valoarea totala estimata') != -1:
        pattern = r'(?<![\d.,])[0-9]+(?:[.,][0-9]+)*(?![\d.,])'
        matches = re.findall(pattern, raw_estimated_value)
        _min_value = matches[0]
        _max_value = matches[0]

        pattern = r'Moneda: (\w{3})'
        match = re.findall(pattern, raw_estimated_value)
        _currency = match[0]
    else:
        _min_value = None
        _max_value = None
        _currency = None

    return _min_value, _max_value, _currency, raw_estimated_value


def read_file_as_binary(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def pdf(_acquisition_nbr):
    search_text = 'Documente de atribuire'
    xpath_expression = f"//*[contains(text(), '{search_text}')]"
    element_with_text = driver.find_element(By.XPATH, xpath_expression)

    parent_element = element_with_text.find_element(By.XPATH, '..')

    a_tags = parent_element.find_elements(By.TAG_NAME, "a")
    for a_tag in a_tags:
        output_string = re.sub(r'\[.*?\]', '', a_tag.text)
        output_string = output_string.strip()
        _doc_name = output_string

        _down_link = a_tag.get_attribute("down-link")

        a_tag.click()
        time.sleep(5)
        file_path = LAND_ACQUISITION_PDFS + f'\{_doc_name}'
        _doc_content = read_file_as_binary(file_path)

        _tender_id = _acquisition_nbr

        print("Document Name: {}".format(_doc_name))
        print("Download Link: {}".format(_down_link))
        print("Document Content: {}".format(_doc_content))
        print("Tender ID: {}".format(_tender_id))

        new_tender_documents = Tender_documents(
            doc_name=_doc_name,
            down_link=_down_link,
            doc_content=_doc_content,
            tender_id=_tender_id
        )

        session.add(new_tender_documents)
        session.commit()

        os.remove(file_path)


def scrape_acquisitions():
    _url = get_url()
    _tender_id = get_tender_id()
    _institution_name, _institution_type, _activity_type, _tender_name, _CPV_code, _contract_type, \
    _short_desc, _long_desc, _criteria_signing, _activity_capacity, _technical_capacity = get_sections()
    _min_value, _max_value, _currency, _raw_estimated_value = get_estimated_value()

    print("URL: {}".format(_url))
    print("Tender ID: {}".format(_tender_id))
    print("Institution Name: {}".format(_institution_name))
    print("Institution Type: {}".format(_institution_type))
    print("Activity Type: {}".format(_activity_type))
    print("Tender Name: {}".format(_tender_name))
    print("CPV Code: {}".format(_CPV_code))
    print("Contract Type: {}".format(_contract_type))
    print("Short Description: {}".format(_short_desc))
    print("Long Description: {}".format(_long_desc))
    print("Criteria Signing: {}".format(_criteria_signing))
    print("Activity Capacity: {}".format(_activity_capacity))
    print("Technical Capacity: {}".format(_technical_capacity))
    print("Min Value: {}".format(_min_value))
    print("Max Value: {}".format(_max_value))
    print("Currency: {}".format(_currency))
    print("Raw Estimated Value: {}".format(_raw_estimated_value))

    new_data = Tender_procedures(
        url=_url,
        tender_id=_tender_id,
        institution_name=_institution_name,
        institution_type=_institution_type,
        activity_type=_activity_type,
        tender_name=_tender_name,
        CPV_code=_CPV_code,
        contract_type=_contract_type,
        short_desc=_short_desc,
        long_desc=_long_desc,
        criteria_signing=_criteria_signing,
        activity_capacity=_activity_capacity,
        technical_capacity=_technical_capacity,
        min_estimated_value=_min_value,
        max_estimated_value=_max_value,
        currency=_currency,
        raw_estimated_value=_raw_estimated_value
    )
    session.add(new_data)
    session.commit()

    pdf(_tender_id)


urll = URL.create(
        drivername="postgresql",
        username="smarthack",
        password="12345",
        host="123.45.67.890",
        port="12345",
        database="smarthack"
    )
engine = create_engine(urll)

Session = sessionmaker(bind=engine)
session = Session()

print(session)


#
# Set download folder
#
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": LAND_ACQUISITION_PDFS}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument("--enable-precise-memory-info")

#
# Create driver
#
driver = webdriver.Chrome(options=chromeOptions)
driver.implicitly_wait(2)

START_ACQ = 100065057
NBR_ACQ = 5000
COUNT = 0

#
# Access SEAP portal
#
curr_acq = 0
while curr_acq < NBR_ACQ:
    url_id = START_ACQ + curr_acq

    try:
        driver.get(WEB_PORTAL + str(url_id))
        time.sleep(2)

        scrape_acquisitions()

        COUNT += 1
        print("NO. OF RECORDS:" + str(COUNT))
    except:
        pass
    curr_acq += 1


driver.quit()