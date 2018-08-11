from logging import info

menu_item_names = ['Plugin menu item','Second plugin menu item']

class Plugin:
    def __init__(self, *args, **kwargs):
        info(__name__+' - Plugin init ("demo"):'+ str(args)+ str(kwargs))

    @property
    def menu_items(self):
        return menu_item_names

    @staticmethod
    def run_menu_item(pystray_object, text):
        print("run_menu_item executing", __name__, text)
