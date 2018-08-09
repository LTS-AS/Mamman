class Plugin:
    from pystray import MenuItem
    
    def __init__(self, *args, **kwargs):
        print('Plugin init ("demo"):', args, kwargs)

    def function_in_plugin(self):
        print("Plugin success")

    @property
    def menu_items(self):
        return ["Plugin menu item"]

    def run_menu_item(self, item_name):
        return True

    
