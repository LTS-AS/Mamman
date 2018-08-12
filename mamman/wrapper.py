import importlib

class Plugin_wrapper:
    def __init__(self, plugin_id, plugin_name):
        self.id = plugin_id
        self.name = plugin_name
        self.module = importlib.import_module("plugins."+plugin_name)
        self.obj = self.module.Plugin()
