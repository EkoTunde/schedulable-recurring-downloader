import time
from app.app import Application
import settings
import tkinter as tk

# Import selenium stuff
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
# from templates import SCRIPT

# from utils import create_script


def drive():
    edge_options = EdgeOptions()
    edge_options.add_experimental_option("prefs", {
        "download.default_directory": settings.DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    # edge_options.add_argument("--headless")
    driver = webdriver.Edge(
        executable_path='./msedgedriver.exe', options=edge_options)
    try:
        driver.get('https://www.sinergiasoftware.xyz/')
        # 'https://www.browserstack.com/test-on-the-right-mobile-devices')

        instructions = None
        with open("instructions.json", "r", encoding='utf-8') as f:
            import json
            instructions = json.load(f)

        print(By.PARTIAL_LINK_TEXT)
        for instruction in instructions["instructions"]:
            by = instruction["by"]
            val = instruction["value"]
            element = driver.find_element(by, val)
            actions = instruction["actions"]
            for action in actions:
                name = action["name"]
                if hasattr(element, name):
                    attr = getattr(element, name)
                    if callable(attr):
                        args = action["args"]
                        kwargs = action["kwargs"]
                        attr(*args, **kwargs)
        # email = driver.find_element('id', 'id_email')
        # email.send_keys("jcmacielhenning@gmail.com")
        # password = driver.find_element('id', 'id_password')
        # password.send_keys("ai2X8hCXbCA@lZWv")
        # password.submit()
        # driver.find_element(By.PARTIAL_LINK_TEXT, "Descargar APK").click()

        # print(a_s)
        # gotit = driver.find_element('id', 'accept-cookie-notification')
        # gotit.click()
        # downloadcsv = driver.find_element('css selector', '.icon-csv')
        # downloadcsv.click()
        time.sleep(100000)
        driver.close()
    except Exception as e:
        print("Error:", e)


def main():
    root = tk.Tk()
    root.geometry(settings.APP_GEOMETRY)
    root.title("Schedulable recurring downloader")
    root.resizable(False, False)
    app = Application(root)
    app.mainloop()


if __name__ == '__main__':
    main()
