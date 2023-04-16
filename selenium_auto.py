# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from os.path import abspath
from time import sleep

from globals_xpath import _SELECT_DICT, _CHECKBOX_LIST_LABEL, _CHECKBOX_LIST_ID


def init_selenium(url: str, optional_screen: bool = True):
    firefox_option = Options()
    firefox_option.add_argument('--headless')

    services = Service(executable_path=abspath("./geckodriver"),)
    # esto abre el navegador
    driver = webdriver.Firefox(service=services, options=firefox_option)
    if optional_screen:
        driver.fullscreen_window()  # esto hace grande la pantalla

    driver.get(url)
    return driver


def item_selected_iteractive(driver: object, items_select: dict, selected: str) -> None:
    element_dict = items_select[selected]
    extract_text = driver.find_element(by=By.XPATH, value=element_dict)
    return extract_text.text


def item_selected_checkbox_value_iteractive(driver: object, items_select: dict, selected: str) -> None:
    element_dict = items_select[selected]
    extract_text = driver.find_element(by=By.XPATH, value=element_dict)
    return extract_text.get_attribute("checked")


def select_dict_interactive(driver: object, items_select: dict, funt: any) -> None:
    temporal_var = {}
    for iter_item in items_select:
        temporal_result = funt(driver=driver,
                               items_select=items_select,
                               selected=iter_item)
        if temporal_result != "":
            temporal_var[iter_item] = temporal_result
    return temporal_var


def send_key_range(driver: object, element: str, range_default: int = 15, move: int = 10):
    slider = driver.find_element(by=By.XPATH, value=element)
    count = range_default

    while count < move:
        slider.send_keys(Keys.RIGHT)
        count += 1

    while count > move:
        slider.send_keys(Keys.LEFT)
        count -= 1


def exe(trasmisor, move_send: int) -> None:
    # logic automatization
    url_page = "https://www.avast.com/es-mx/random-password-generator#pc"
    driver = init_selenium(url=url_page)
    sleep(5)

    slider_is = _SELECT_DICT['slider_len_password']
    send_key_range(
        driver=driver,
        element=slider_is,
        move=move_send
    )

    super_dict = {}
    select_dict = select_dict_interactive(
        driver=driver,
        items_select=_SELECT_DICT,
        funt=item_selected_iteractive
    )
    checkbox_list = select_dict_interactive(
        driver=driver,
        items_select=_CHECKBOX_LIST_LABEL,
        funt=item_selected_iteractive
    )
    checkbox_list_id = select_dict_interactive(
        driver=driver,
        items_select=_CHECKBOX_LIST_ID,
        funt=item_selected_checkbox_value_iteractive
    )

    super_dict["_SELECT_DICT"] = select_dict
    super_dict["_CHECKBOX_LIST"] = checkbox_list
    super_dict["_CHECKBOX_LIST_ID"] = checkbox_list_id

    # se envia a travez del tunel a la interfaz
    trasmisor.send(super_dict)
    driver.close()
