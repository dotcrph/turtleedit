# from datetime import datetime
# import sys

import te_cfg as cfg
# import te_utils as utils
# import te_io as io
import te_widgets as widgets
import te_logging as log

linesCount: int = 1

openedFile = None

# Binds config setup
# try:
#     binds = cfgparser.readConfig('turtlebinds.txt')
# except Exception as error:
#     writeToLog(f'Invalid binds! ({error})')
#     binds = {}

# Binds setup
# def createBindings():
#     text.bind('<ButtonRelease-1>', onKeyPress)
#     #text.bind('<Button-1>', onKeyPress)
#     text.bind('<B1-Motion>', onKeyPress)
#     text.bind('<KeyPress>', onKeyPress)
#     text.bind('<KeyRelease>', onKeyRelease)
#
#     # Parameters
#     for key, value in binds.items():
#         try:
#             root.bind(key, eval(value))
#         except Exception as error:
#             writeToLog(f'Invalid bind! ({error}), ignoring')
#
# initFunctions = [setupConfig, configureWidgets]
# mainFunctions = [initializeWidgets, createBindings]

def main():
    # Call init functions
    # for function in initFunctions:
    #     function()

    # Remove extra line at line 0
    # updateLines()
    widgets.lines.configure(state='normal')
    widgets.lines.delete('1.0')
    widgets.lines.configure(state='disabled')

    # Call main functions
    # for function in mainFunctions:
    #     function()

    # updateFooterLoop()

    cfg.setupConfig()

    widgets.placeWidgets()
    widgets.configure()

    widgets.root.mainloop()

if __name__ == '__main__':
    main()
