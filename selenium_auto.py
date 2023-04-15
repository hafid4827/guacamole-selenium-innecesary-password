# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

from os.path import abspath
from time import sleep

from globals_xpath import _SELECT_DICT, _CHECKBOX_LIST


def init_selenium(url: str, optional_screen: bool = True):
    services = Service(executable_path=abspath("./geckodriver"))
    driver = webdriver.Firefox(service=services)

    if optional_screen:
        driver.fullscreen_window()  # esto hace grande la pantalla

    driver.get(url)
    return driver


def item_selected_iteractive(driver: object, items_select: dict, selected: str) -> None:
    element_dict = items_select[selected]
    extract_text = driver.find_element(by=By.XPATH, value=element_dict)
    return extract_text.text


def select_dict_interactive(driver: object, items_select: dict) -> None:
    temporal_var = {}
    for iter_item in items_select:
        temporal_result = item_selected_iteractive(driver=driver,
                                                   items_select=items_select,
                                                   selected=iter_item)
        if temporal_result != "":
            temporal_var[iter_item] = temporal_result
    return temporal_var


def exe(trasmisor):
    # logic automatization
    url_page = "https://www.avast.com/es-mx/random-password-generator#pc"
    driver = init_selenium(url=url_page)
    sleep(5)
    # item_selected_iteractive()

    super_dict = {}

    select_dict = select_dict_interactive(driver, _SELECT_DICT)
    checkbox_list = select_dict_interactive(driver, _CHECKBOX_LIST)

    super_dict["_SELECT_DICT"] = select_dict
    super_dict["_CHECKBOX_LIST"] = checkbox_list

    # se envia a travez del tunel a la interfaz
    trasmisor.send(super_dict)
    # sleep(5)
    # closed
    # driver.close()
