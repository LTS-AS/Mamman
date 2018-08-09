# -*- coding: utf-8 -*
"""Main part of the Mamman application

This module encapsulates the UI and the state-machine for application control

Example:
 python main.py

Todo:
    * Populate menu-array
    * Move Plugin_container class to separate file
    * Establish model class?

More info:
   https://lts.no
   https://github.com/lts-as

"""

import importlib, subprocess, sys, threading
from queue import Queue
from mamman.environment import userdir
from pystray import Icon, Menu, MenuItem
from PIL import Image
from automat import MethodicalMachine
from os import getcwd, path, startfile
from mamman import model

#============================ tools start
def tracer(old_state, input, new_state):
    "Tracer function for debugging"
    print("old_state:", old_state, "input:", input, "new state:", new_state)
#============================ tools end
#============================ event handelers start
def event_click_available():
    "UI event: User is enabeling the available flag"
    print('UI event: click')
    menu.user_available = not menu.user_available

def event_default():
    "UI event: Single click on icon"
    startfile('https://lts.no/tjenester/eplan')

def event_ready():
    "Event: Mamman is ready for use"
    client_machine.reading_finished()

def event_new_process(icon, item):
    "UI event: Establish new process"
    print(icon)
    print(item)

def event_open_task(icon, item):
    "UI event: Open task folder"
    print(icon)
    print(item)

def event_exit():
    "UI event: Exit"
    client_machine.close_application()

def event_plugin_item_click(icon, tasting):
    "UI event: a plugin element is clicked"
    print('UI event: a plugin element is clicked')
#============================ event handelers end
#============================ plugin encapsulation class start
class Plugin_container:
    def __init__(self, plugin_id, plugin_name):
        self.id = plugin_id
        self.name = plugin_name
        self.module = importlib.import_module("mamman.plugins."+plugin_name)
        self.obj = self.module.Plugin()
#============================ plugin encapsulation class end
#============================ state machine start
class Client_machine(object):
    "Finite state-machine for the Mamman client"
    from mamman.api import connection
    from mamman.crypto import tools

    _machine = MethodicalMachine()
    _connection = None
    _icon = None
    _plugin_names = ["demo"]
    p = []

    setTrace = _machine._setTrace # making trace-function available. Usefull debugging feature

    #============================ inputs
    @_machine.input()
    def initiate_application(self):
        "Initiate connection to server"

    @_machine.input()
    def reading_finished(self):
        "Add tasks to menu"

    @_machine.input()
    def toggle_available(self):
        "Toggle availability flag"

    @_machine.input()
    def close_application(self):
        "The user put in some beans."

    #============================ outputs
    @_machine.output()
    def _initiate_application(self):
        "Establish all parts of the application"
        self._icon = Icon(name='Mamman',
                          icon=Image.open(path.join(globalpath, 'res', 'logo_yellow.png')),
                          title='LTS AS, Mamman 0.1')
        self._icon.visible = True

        # connect the menu to the menu_items variable to make the menu dynamic
        menu.items.append(MenuItem('Avslutt Mamman', event_exit))

        # Establish plugins in Plugin_container classes
        plugin_id = 0
        for plugin_name in self._plugin_names:
            plugin_id += 1
            self.p.append(Plugin_container(plugin_id, plugin_name))
        


        self._icon.menu = Menu(lambda: (
            menu.items[i]
            for i in range(len(menu.items))))

        event_ready() # Mark that the process is finished by trigging an event
        self._icon.run() #_icon.run is last because it is not ending before _icon.stop

    @_machine.output()
    def _verify_user(self):
        "Connect to API and verify user"
        self._connection = self.connection()
        credentials = self.tools(userdir.crypto).get_credentials()
        user_key = self._connection.post('user', credentials)['resource'][0]['key']
        if user_key != None:
            print("ATOMATIC event: User login OK\n", user_key)

    @_machine.output()
    def _list_tasks(self):
        "Populate tasks in the the icon menu"
        self._icon.icon = Image.open(path.join(globalpath, 'res', 'logo_blue.png'))
        for plugin in self.p:
            for element in plugin.obj.menu_items:
                menu.items.append(MenuItem(element, event_plugin_item_click, checked=None, radio=False))

    @_machine.output()
    def _close_application(self):
        "Close the application"
        self._icon.menu = None
        #self._icon.visible = False
        self._icon.stop()
        q.join()       # block until all tasks are done

    @_machine.serializer()
    def get_state(self, state):
        "Returning the internal machine state"
        return state

    #============================ states
    @_machine.state(initial=True)
    def starting(self):
        "In this state, you have not yet connected"

    @_machine.state()
    def reading(self):
        "In this state, you are loading tasks"

    @_machine.state()
    def listing(self):
        "In this state, the UI lists available tasks"

    @_machine.state()
    def working(self):
        "In this state, you are working on a task"

    @_machine.state()
    def ending(self):
        "In this state, you are shutting down the application."

    #============================ transitions
    # When we don't any connection, upon connecting, we will be connected
    starting.upon(
        initiate_application,
        enter=reading,
        outputs=[
            _initiate_application
            ]
        )

    starting.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )

    reading.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )

    reading.upon(
        reading_finished,
        enter=listing,
        outputs=[
            _list_tasks
            ]
        )

    listing.upon(
        close_application,
        enter=ending,
        outputs=[
            _close_application
            ]
        )
#============================ state machine end

if __name__ == "__main__":
    # Establishing asyncronus task queue
    q = Queue()

    # Worker
    def worker():
        while True:
            item = q.get()
            print(item)
            q.task_done()
    
    # Establish a number of worker threads
    for i in range(10):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    if getattr(sys, 'frozen', False):
        # An executable file includes all resources
        globalpath = sys._MEIPASS
    else:
        # The application is not packaged up in one file
        globalpath = path.dirname(path.realpath(__file__))

    # All state belongs to the model
    menu = model.menu
    client_machine = Client_machine()
    client_machine.setTrace(tracer)
    client_machine.initiate_application()
