from logging import info

class Plugin:
    def __init__(self, *args, **kwargs):
        info(__name__+' - Plugin init ("demo"):'+ str(args)+ str(kwargs))

    def function_in_plugin(self):
        info("Plugin success")

    @property
    def menu_items(self):
        return ["Plugin menu item"]

    def run_menu_item(self, item_name):
        info(item_name)
