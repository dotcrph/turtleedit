# turtleedit

> A very basic but customizable text editor built with wxWidgets

## 🎨 Features

* Customizable
* Portable
* Plugin support
* wxWidgets base

## 🖌️ How to change apperance

Turtleedit automatically loads a file named ```main.json``` in ```./config/``` 
directory upon loading. You can check out 
[```examples/minimal/config/main.json```](examples/minimal/config/main.json) 
for a default config file. Note that turtleedit also automatically tries to 
read ```insert.font``` property, though it is not present in the default 
config JSON. See 
[```examples/fancy/config/main.json```](examples/fancy/config/main.json) 
for an example custom config.

## 💾 How to load and write plugins

After initializing the widgets, turtleedit executes a file named ```init.py```
in ```./plugins/``` directory. This file is meant to import and execute other 
```.py``` files located in ```./plugins/```. You can access turtleedit API 
via ```te.``` in ```init.py```, although you still have to pass a reference to 
```te.``` to the other scripts (because of how horribly I have implemented the 
API system). See the [minimal](examples/minimal/plugins) and 
[fancy](examples/fancy/plugins) examples.
