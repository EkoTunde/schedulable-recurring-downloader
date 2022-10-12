
import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import settings
from get_chrome_driver import GetChromeDriver


def main():

    # Install the driver:
    # Downloads ChromeDriver for the installed Chrome version on the machine
    # Adds the downloaded ChromeDriver to path
    get_driver = GetChromeDriver()

    # Download the stable driver version
    # Optional: use output_path= to specify where to download the driver
    # Optional: use extract=True to extract the zip file
    get_driver.download_stable_version(output_path=os.getcwd(), extract=True)

    edge_options = EdgeOptions()
    edge_options.add_experimental_option("prefs", {
        "download.default_directory": settings.DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    # edge_options.add_argument("--headless")
    driver = webdriver.Chrome()
    # driver = webdriver.Edge(
    #     executable_path='./msedgedriver.exe', options=edge_options)
    try:
        driver.get('https://www.sinergiasoftware.xyz/')

        instructions = None
        with open("instructions.json", "r", encoding='utf-8') as f:
            import json
            instructions = json.load(f)

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

        driver.close()
    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
