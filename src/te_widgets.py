import te_cfg as cfg
import te_logging as log

import tkinter as tk

root = tk.Tk()
text = tk.Text(root)
lines = tk.Text(root)
footer = tk.Label(root)

isFullscreen: bool = False
textSize: int = 16
textFont: str = "Courier New"

lineNumPosStr: str = cfg.get(str, "lineNumbers", "position")

lineNumPos: int = 0 if lineNumPosStr == "left" \
                    else 1 if lineNumPosStr == "right" else -1

def setTitle(title: str):
    root.title(title)

def configure():
    global isFullscreen, textSize

    configureRoot()
    configureIcon()
    configureFullscreen()
    configureText()
    configureCaret()
    configureLineNumbers()
    configureFooter()

def configureRoot() -> None:
    root.geometry(str(cfg.get(int, "root", "width")) 
                    + "x" + str(cfg.get(int, "root", "height")))

def configureIcon() -> None:
    try:
        root.iconbitmap("data/turtleicon.ico")
    except Exception as e:
        # I am using 'except Exception' here because 
        # invalid icon should never crash the program
        log.error(f"Something went wrong while trying to get the app icon! ({e})")

def configureFullscreen() -> None:
    isFullscreen = cfg.get(bool, "root", "fullscreen")
    root.attributes("-fullscreen", isFullscreen)

def configureText() -> None:
    # text.configure(yscrollcommand = updateTextScroll)

    textFont = cfg.get(str, "insert", "font")
    textSize = cfg.get(int, "insert", "fontSize")

    text.configure(
        bg      = cfg.get(str, "insert", "bgColor"),
        fg      = cfg.get(str, "insert", "fgColor"),
        font    = (textFont, textSize),
        relief  = cfg.get(str, "insert", "relief"),
        wrap    = 'none'
    )

def configureCaret() -> None:
    text.configure(
        insertbackground    = cfg.get(str, "caret", "color"),
        insertwidth         = cfg.get(int, "caret", "width")
    )

def configureLineNumbers() -> None:
    if lineNumPos >= 0:
        lines.configure(
            bg      = cfg.get(str, "lineNumbers", "bgColor"),
            fg      = cfg.get(str, "lineNumbers", "fgColor"),
            font    = (textFont, textSize),
            relief  = cfg.get(str, "lineNumbers", "relief"),
            wrap    = 'none'
        )

def configureFooter() -> None:
    pass
    # if footer:
    #     footer.configure(anchor='w')
    #     footer.configure(bg=userConfig['footerBg'],
    #                     fg=userConfig['footerFg'],
    #                     font=(userConfig['footerFont'], userConfig['footerFontSize']),
    #                     relief=userConfig['footerRelief'])
    #     updateFooter()

def placeWidgets():
    root.rowconfigure(0, weight=1)

    if lineNumPos >= 0:
        root.columnconfigure(lineNumPos, weight = 0)
        root.columnconfigure(1 - lineNumPos, weight = 1)

        text.grid(
            row = 0, 
            column = 1 - lineNumPos, 
            sticky='news'
        )

        lines.grid(
            row = 0, 
            column = lineNumPos, 
            sticky='ns'
        )

    # if userConfig['enableFooter']:
    #     w.footer.grid(row=1, column=0, columnspan=2, sticky='news')

