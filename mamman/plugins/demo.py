class Plugin:
    from pystray import MenuItem
    
    def __init__(self, *args, **kwargs):
        print('Plugin init ("demo"):', args, kwargs)

    def function_in_plugin(self):
        print("Plugin success")

    def menu_items(self):
        return [self.MenuItem("Plugin menu item", self.function_in_plugin)]

    
