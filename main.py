import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = "./drivers/chromedriver-mac-arm64.zip"

options = Options()
options.headless = True
options.add_argument("--window-size=800,1000")
driver = webdriver.Chrome(options=options)


def dig_car_data(parent: WebElement, xpath_selector: str = ".//", parents: list = (), level: int = 1):
    if level >= 4:
        return [*parents, parent.get_attribute("innerText")]

    # delay
    # time.sleep(0.2 if level == 1 else 0.3 if level == 2 else 0.4)
    time.sleep(0.15 * (level - 1) if level > 1 else 0.15)

    child_elements = parent.find_elements(By.XPATH, xpath_selector)

    results = []

    for elem in child_elements:
        # get current element's references
        elem_value = elem.get_attribute("innerText")

        # print current element's data
        indentation_str = "\t" * (level - 1) + str(level) if level > 1 else str(level)
        print(f'{indentation_str}: {elem_value}')

        elem_expander = elem.find_element(By.XPATH, ".//a[contains(@class, 'navlabellink')]")

        # delay
        # time.sleep(0.2 if level == 1 else 0.3 if level == 2 else 0.4)
        time.sleep(0.15 * (level - 1) if level > 1 else 0.15)

        # wait for current element to be available
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(elem_expander)).click()
        actions = ActionChains(driver)
        actions.move_to_element(elem_expander).click().perform()

        # recursive call using current element as parent
        results.append(
            dig_car_data(elem, ".//div[contains(@class, 'ranavnode')]", [*parents, elem_value.strip()], level + 1)
        )

    return results


def print_hi():
    driver.get("https://www.rockauto.com/")

    root_elem = driver.find_element(By.XPATH, "/*")

    root_elem.find_element(By.ID, 'cbxYear2004').click()

    time.sleep(1)

    # dig_car_data(root_elem, ".//a[contains(@class, 'navlabellink')]")
    # dig_car_data(root_elem, ".//div[contains(@class, 'ranavnode')]")
    res = dig_car_data(root_elem, './/div[@class="ranavnode"]')

    with open("last_scrapped.html", "w") as f:
        f.writelines(driver.page_source)

    time.sleep(5 * 60)
    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
