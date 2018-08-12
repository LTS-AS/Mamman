import platform, subprocess, win32com.client as win32
from jinja2 import Template
from logging import info
from os import getenv
from pprint import pprint

def dummy_function(pystray_object, menu_item):
    print(menu_item.__dict__)

def report_sucking(pystray_object, menu_item):
    with open("mamman/plugins/demo_report_sucking.jinja", mode="r", encoding="utf-8") as file_:
        template = Template(file_.read())
    email_body = template.render(
        user_name=getenv('username'),
        software_version=pystray_object._title,
        os_version = platform.platform()
        )
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'havard.line@gmail.com'
    mail.Subject = str(pystray_object._title)+' SUCK!'
    mail.Body = email_body
    mail.Display(True)
    info(__name__+' - report_sucking, '+str(menu_item))

class Plugin:
    def __init__(self, *args, **kwargs):
        info(__name__+' - Plugin init ("demo"):'+ str(args)+ str(kwargs))
        self.allow_reports = True

    # The menu_items property are default for all plugins.
    # It is possible to return an empty array if no MenuItems should be generated.
    @property
    def menu_items(self):
        return [{'text': 'Repport issue', 'function': report_sucking}]
            
p = Plugin()

if __name__ == "__main__":
    # Create dummy pystray class to be able to run file
    class MyClass:
        _title = "Title"
    
    report_sucking(MyClass, 'Topic')
