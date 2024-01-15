## About

This repository contains code and relevant documentation for the health-systems (HealthSys) project group.
The project in question; **investigate how to deal with noise and motion artifacts in physiological sensor data**.

## Getting started

The development environment is Microsoft Visual Studio Code (VSCode) which can be downloaded [here](https://code.visualstudio.com/#alt-downloads).
Git and GitHub will be used for source control (i.e collaboration). If you do not already have a GitHub account you can sign-up for free [here](https://github.com/signup).
In addition to GitHub you will also need Git to work with source control. Both Linux and MacOS comes shipped with Git by default, if you use Windows you will first have to download and install it [here](https://git-scm.com/download/win).

After you have installed VSCode, installed Git (if applicable) and signed up for GitHub it's time to configure the development environment.

1. Launch VSCode and follow initial setup steps, then log in using your GitHub account when asked.
2. On the left-hand side, navigate to "Extensions" (or press `Ctrl+Shift+X`), search for and install `GitHub Pull Requests and Issues`.
3. On the left-hand side, navigate to "Source Control" (or press `Ctrl+Shift+G`) and click on `Clone a Repository`. If you're logged into GitHub you should be able to choose the `HealthSys` repository. Pick a local directory (folder) to house the project and clone it.
4. Open the project when prompted. Next, open a terminal by navigating to `Terminal -> New Terminal` on the upper side of your screen.
5. In the terminal, run the following commands (replacing name and email with your GitHub username and email):
   1. `git config --global user.name "YourName"`
   2. `git config --global user.email "youremail@yourdomain.com"`
6. Now lets make a commit test. Open this `README.md` file and add some text, maybe `hello world! /MyName` or such at the bottom. Then, save the file (`Ctrl+s`) and go to "Source Control" (`Ctrl+Shift+G`).
7. In the text box, write a short message such as `commit test by MyName`, then press `Ctrl+Enter` to commit directly to the main repository.
8. Press `sync`. If all went smoothly your text should now show up on [GitHub](https://github.com/Stylback/HealthSyS#readme).

Before other people can see your commit locally they will have to sync, that goes for you aswell in order to see other peoples commits.

When using Git there are some rules to follow:
- Always make a comment. GitHub will not allow so called "empty commits". If you try to make a commit without writing a comment it simply won't push it.
- Always start your "coding session" with a sync. This will esnure that you don't work with old code that might've been changed by someone else. If you don't want to do it manually every time, you can configure automatic sync in the VSCode settings.
- If you're working with a file that you believe someone else is also working on, it's best to save your changes to either a seperate branch (that is NOT main) or to save it to a seperate file (such as `peak_detection_test_jonas.py`). This is in order to avoid a so-called merge conflict.
- In case of a merge conflict, you will be prompted by VSCode and Git to "clean up your repository". Resolving merge conflicts can be complex for someone just starting out with Git. VSCode should present you with a window where you can compare your commit with the conflicting commit, here you simply choose what to keep and what to discard. When everything is resolved you mark it as "resolved". When in doubt, use your search engine of choice.

The work-flow when using Git comes down to four steps:
1. Pull the latest updates to the repository (this is facilitated by the sync button).
2. Make some changes to the repository.
3. Stage the changes (this is faciliated by saving the files that have been changed).
4. Write a message, then push the changes to the repository (this is facilitated by `Ctrl+Enter` in the "Source Control" menu)

Or shorter:

```
pull -> code -> stage -> message -> push
```

## Coding in Python

With the developement environment up and running we will need to make some additional configurations to run Python code.

First you need to make sure you have the Python 3 programming language installed on your computer. Both Linux and MacOS (usually) comes shipped with Python 3 by default while Windows will almost always have to installed it seperately. To install Python 3, visit [this](https://www.python.org/downloads/) webpage and install the latest stable version for your OS.

After a successful install, the next thing in order is to download the Python extension for VSCode. Navigate to "Extensions" (or press `Ctrl+Shift+X`), search for and install the `Python` extension from Microsoft. This extension is a bundle that will give you all the necessary components to work with Python in VSCode, it will also provide you with linting (syntax highlighting, code suggestion etc.).

With all the neccesary requirements installed, let's test that everything works as it should. In this repository, create a file named `yourname.py` and open it in a tab. In it, paste the following code:

```py
s1 = "hello"
s2 = "world"
print(s1+ " " + s2)
```

In the lower right corner you will see a warning symbol with the text `Select Interpreter`, press it and select the Python interpreter with the latest version (in my case, `Python 3.10.12 64-bit`). In the upper right corner you will see a run icon (hovering over it displays `Run Python File`), press it and a terminal should pop-up with the following message:

```bash
YourName@ComputerName:~/path-to-HealthSys/$ /HealthSyS/yourname.py
hello world
```

If it displays `hello world` like above, congratulations! You now have a fully working Python environment.

### It didn't work

If nothing appeared in the Python Interpretor menu, restart VSCode and try again (if you're on MacOS, make sure you pick `quit` to really close the application). 

If you were met with the following error:

```
An Invalid Python interpreter is selected, please try changing it to enable features such as IntelliSense, linting, and debugging. See output for more details regarding why the interpreter is invalid.
```

Follow the error message.

## Tips and resources

### Installing libraries

Some Python libraries (such as `numpy`) require that you download them first before you can import them. This is the step that most beginners to Python get wrong, they will download libraries to locations that VSCode can't see. Here are my step-by-step tips to download a Python library when working in VSCode:

1. Open up a terminal in VSCode. In the terminal, upgrade `pip`:

```bash
python -m pip install -U pip
```

If you're met with an error, you might need to replace either `python` for `python3`, `pip` for `pip3` or both. When you have a command that works, take note of which variation was needed for the next step.

2. While still in the terminal, install the Python library using `pip`. In this example we will install `numpy`:

```bash
python -m pip install numpy
```

If successfull the terminal should display some form of progress bar showing that it's downloading the library. That's it, you can now import the library by adding `import numpy` at the top of your Python file.

### Use aliases

When using a function from an external library you need to specify it with `libraryName.functionName()` in your code. A common practice to avoid typing `libraryName` everytime you need that function is to use an alias. When you use and alias you replace `libraryName` with something else (usually shorter) that is easier to type. To use an alias you need to specify it when importing the library at the start of your Python file with `import libraryName as alias`. As an example, here we are creating an alias for `numpy` called `np`, a common practice:

```py
import numpy as np

a1D = np.array([1, 2, 3, 4]) # creates a 1D array with the elements 1-4 in it.

print(a1D)
```

If the library has a sublibrary you can alias that as well, `from numpy import linalg as lg` is valid syntax. Do note that you cannot create an alias for a specific function, `import numpy.array as arr` for example is invalid.

### Comments and documentation

To create single line comments, use a hashtag (`#`):

```py
a = 1
b = 2
c = a + b # c is 3
```

For multi-line comments, use two sets of tripple quotes (`""" """`).

```py
"""
The code belows assigns two sets of integrers to two variables, a and b.
It then take the sum of these two variables and store it in another variable, c.
"""

a = 1
b = 2
c = a + b
```

When writing a function it's considered best practice to include a **typehint** and a **docstring**. A **typehint** tells the user what type the function will take as input and what it will output (float, int, string etc.), a typehint is declared in the same line as the function declaration using either `:` for input or `->` for output:

```py
def helloWorld(s: int) -> str:
   print("Hello world, the answer to life is: " + str(s))
   return
```

A **docstring** tells the user what the function is supposed to do, think of it as helpful documentaton to aid the user in using the function correctly. A docstring is declared using two sets of tripple quotes, similar to multi-line comments. The docstring needs to be at the very start of the function to not get confused with a normal multi-line comment:

```py
def helloWorld(s: int) -> str:
   """This function takes an integrer as input and outputs a string.
   It is a reference to "The Hitchhiker's Guide to the Galaxy", where a great AI is asked what the meaning of life is and outputs "42".
   """

   print("Hello world, the answer to life is: " + str(s))
   return
```
### Style Guide for Python

Coding conventions:

| Type | Public | Intenal |
| :--- | :--- | :--- |
| Packages | `lower_with_under` |  | 
| Modules | `lower_with_under` | `_lower_with_under` | 
| Classes | `CapWords` | `_CapWords` | 
| Exceptions | `CapWords` |  | 
| Functions | `lower_with_under()` | `_lower_with_under()` | 
| Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` | 
| Global/Class Variables | `lower_with_under` | `_lower_with_under` | 
| Instance Variables | `lower_with_under` | `_lower_with_under` | 
| Methods Names | `lower_with_under()` | `_lower_with_under()` | 
| Function/Method Parameters | `lower_with_under` |  | 
| Local Variables | `lower_with_under` |  | 

hello world! /Ania

Hello World! /Axel

Hello World! /Farzan