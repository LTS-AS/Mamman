# -*- coding: utf-8 -*
"""Main part of the Mamman application

This module encapsulates the UI and the state-machine for application control

Example:
 python main.py

Todo:
    * Establish model class?

More info:
   https://github.com/lts-as
   https://lts.no

"""
from automat import MethodicalMachine
import logging, subprocess, sys, threading
from os import path, startfile
from pystray import Icon, Menu, MenuItem
from PIL import Image
from queue import Queue
from wrapper import Plugin_wrapper

#============================ tools start
def state_tracer(old_state, input_, new_state):
    "Tracer function for debugging"
    logging.info("state_tracer - old_state:"+ old_state+ ", input:"+ input_+ ", new state:"+ new_state)
#============================ tools end
#============================ event handelers start
def event_click_default():
    "UI event: Single click on icon"
    startfile('https://lts.no/tjenester/eplan')

def event_all_loaded():
    "Event: Mamman is ready for use"
    client_machine.reading_finished()

def event_click_exit():
    "UI event: Exit"
    client_machine.close_application()
#============================ event handelers end
#============================ state machine start
class Model(object):
    "Finite state-machine for the Mamman client"
    _machine = MethodicalMachine()
    _icon = None
    _menu_cache = []
    _plugin_names = ["demo"]
    p = []

    setTrace = _machine._setTrace # making trace-function available. Usefull debugging feature
    #============================ inputs
    @_machine.input()
    def initiate_application(self):
        "Initiate application and plugins"

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
                          icon=Image.open(path.join(globalpath, '..','res', 'logo_yellow.png')),
                          title='Mamman 0.1')
        self._icon.visible = True

        # connect the menu to the menu_items variable to make the menu dynamic
        self._menu_cache.append(MenuItem('Avslutt Mamman', event_click_exit))
        self._menu_cache.append(MenuItem('Default item', event_click_default, visible=False, default=True))

        # Establish plugins in Plugin_wrapper classes
        for plugin_id, plugin_name in enumerate(self._plugin_names):
            plugin_id += 1
            self.p.append(Plugin_wrapper(plugin_id, plugin_name))

        self._icon.menu = Menu(lambda: (
            self._menu_cache[i]
            for i in range(len(self._menu_cache))))

        event_all_loaded() # Mark that the process is finished by trigging an event
        self._icon.run() #_icon.run is last because it is not ending before _icon.stop

    @_machine.output()
    def _list_tasks(self):
        "Populate tasks in the the icon menu"
        self._icon.icon = Image.open(path.join(globalpath, '..', 'res', 'logo_blue.png'))
        for plugin in self.p:
            # Adding separator betwean every plugin
            self._menu_cache.append(Menu.SEPARATOR)
            for element in plugin.obj.menu_items:
                self._menu_cache.append(MenuItem(
                    element['text'],
                    element['function'],
                    checked=None,
                    radio=False,
                    # enabled=element['enabled'])
                    ))

    @_machine.output()
    def _close_application(self):
        "Close the application"
        self._icon.menu = None
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
    logging.basicConfig(level="INFO")
    # Worker
    def worker():
        while True:
            item = q.get()
            print('start')
            item()
            print('end')
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
    client_machine = Model()
    client_machine.setTrace(state_tracer)
    client_machine.initiate_application()
