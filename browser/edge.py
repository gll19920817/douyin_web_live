from selenium import webdriver
from selenium.webdriver import Proxy, DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

from config.helper import config
from browser.IDriver import IDriver
from selenium.webdriver.edge.options import Options


class EdgeDriver(IDriver):
    def __init__(self):
        super(EdgeDriver, self).__init__()
        options = Options()
        if config()['webdriver']['headless']:
            options.add_argument("--headless")
        options.add_argument('--proxy-server=%s:%s' % (config()['mitm']['host'], config()['mitm']['port']))
        options.add_argument('-ignore-certificate-errors')
        options.add_argument('-ignore -ssl-errors')
        options.add_argument('--incognito')
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = "%s:%s" % (config()['mitm']['host'], config()['mitm']['port'])
        proxy.ssl_proxy = "%s:%s" % (config()['mitm']['host'], config()['mitm']['port'])
        capabilities = DesiredCapabilities.EDGE
        proxy.add_to_capabilities(capabilities)

        self.browser = webdriver.Chrome(options=options,
                                        desired_capabilities=capabilities,
                                        executable_path=config()['webdriver']['edge']['bin']
                                        )

    def new_tab(self) -> str:
        current_window_handles = self.browser.window_handles
        self.browser.execute_script("window.open('')")
        new_window_handles = self.browser.window_handles
        for _handle in new_window_handles:
            if _handle not in current_window_handles:
                return _handle
        return ""

    def change_tab(self, tab_handler: str):
        if tab_handler not in self.browser.window_handles:
            return
        if tab_handler == self.browser.current_window_handle:
            return
        self.browser.switch_to.window(tab_handler)

    def open_url(self, url: str, tab_handler: str = ""):
        if tab_handler != "":
            self.change_tab(tab_handler)
        self.browser.get(url)

    def screenshot(self, tab_handler: str = "") -> str:
        cur_handle = self.browser.current_window_handle
        if tab_handler != "":
            self.change_tab(tab_handler)
        b64 = self.browser.get_screenshot_as_base64()
        self.change_tab(cur_handle)
        return b64