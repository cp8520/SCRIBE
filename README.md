Thank you for downloading SCRIBE! Scribe is a notetaking tool that provides an updated timestamp in the ISO format in the PST timezone. Press copy & clear to copy the notes to your clipboard so you can paste them elsewhere. You can also paste them back in, select the text on-screen and paste your clipboard for a seamless handoff.

To run SCRIBE, simply download the latest release from the releases tab from here:[GoogleDrive/Scribe](https://drive.google.com/file/d/1YrX0Ex4Xd4GkGvx-XOl9OFQl5lkZ_PNU/view?usp=sharing). After the download is complete, extract the file and double click the .py file to run! You shouldn't need to install the application.

If you wish to run via an executable file, you will need to compile the program yourself. Depending on the OS you're using, will determine the steps you need to take.

First, regardless of your OS you will need to have these pre-requisites: 
1. Python 3.11.4 or below (there is a issue in python 3.11.5 with the module pyimod2_importers). You can install python 3.11.4 using this link: https://www.python.org/downloads/release/python-3114/ (Scroll down to Files to find download). Make sure to check the "Add to Path" box at the start of the installation.
2. pip (latest version should be installed with python 3.11.4)

To install the next modules, you will need to open the commmand line / terminal. 
* On Windows - Press the Windows Key + R and type CMD then press enter.
* On Mac - In the Finder , open the /Applications/Utilities folder, then double-click Terminal.

1. Then, install tzdata. In the command line window type in pip install tzdata --trusted-host pypi.org --trusted-host files.pythonhosted.org
2. Then, install flet. In the command line window type in pip install flet --trusted-host pypi.org --trusted-host files.pythonhosted.org

Windows: 
If you're using Windows and want a .exe, you will also need auto-py-to-exe. To install, using the command line window type in pip install auto-py-to-exe --trusted-host pypi.org --trusted-host files.pythonhosted.org
* Follow the instrustions here: https://pypi.org/project/auto-py-to-exe/

Mac: 
If you're using Mac and want a .dmg, you will also need py2app. To install, using the terminal type in pip install py2app --trusted-host pypi.org --trusted-host files.pythonhosted.org.
* Follow the instructions here: https://pypi.org/project/py2app/

