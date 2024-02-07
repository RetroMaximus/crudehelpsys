	Copy and paste everything below these two lines to your python script and adjust settings to your liking.
	Scroll to the bottom of the json structure for more instructions on how to setup the command class.

	At the top of my script I will setup cRUDE Help Sys and pass some variables to the listener. Note* I am adding the name of my
	CLI project this will show throughout the command line application. If you are able to setup bash a shortcmdline is provided
	to initiate commands as if it was the full script name.

	grouporg = "cRUDECrew"
    scriptname = "uniscraper"
    script_file = scriptname + ".py"
    scriptver = 1.0
    scriptdesc = "UniScraper is a tool used to scrape web data. Features data to exported to json html and sql."
    shortcmdline = "us"

    showpoweredby = 1
    # the option above will hide this message from ever appearing in the console.

    # Powered by cRUDEcREW 'cRUDE Help Sys' command line application
    # It would be appreciated if it was left enabled.

    # Before each command is initiated a
    # virtual environment can be enabled or disabled.
    # This is script wide not command specific.
    enable_venvironment = 1

    # This is the name of the class where commands exist.
    # This class is used to match help requests to commands
    CommandClassHolder = "CmdInit"

    # Pass this scripts details to cRUDE Help Sys
    chs.prj_details.showpowerdedby = showpoweredby
    chs.prj_details.enable_env = enable_venvironment
    chs.prj_details.grouporg = grouporg
    chs.prj_details.scriptname = scriptname
    chs.prj_details.script_file = script_file
    chs.prj_details.scriptver = 1.0
    chs.prj_details.scriptdesc = scriptdesc
    chs.prj_details.shortcmdline = "us"
    chs.hrclass.spb = prj_details.showpoweredby
    parent_script = os.path.basename(__file__)
    chs.hrclass.setclassholder(CommandClassHolder, parent_script)

    # The JSON structure below is called when a help term is requested.
    # if a match is found the corresponding details will be printed to screen
    chs.hrclass.jsonhelp = [
        {
            "helpdatastorage": [
                {
                    "name": "load",
                    "author": "Scr1ptAl1as",
                    "git": "http://dsfasfad.fsfesf.fs",
                    "requiredargs": "s, i",
                    "desc_0": "Load a node script to uniscrape v1.0.",
                    "desc_1": "filelocation = full file path\n"
                              "startstatus = 0 or 1.\n"
                              "If startstatus = 1 the node script will attempt to run as soon as it is loaded.",
                },
                {
                    "name": "unload",
                    "author": "Scr1ptAl1as",
                    "git": "http://dsfasfad.fsfesf.fs",
                    "requiredargs": "",
                    "desc_0": "Unload the currently loaded node script to uniscrape v1.0.",
                },
                {
                    "name": "run",
                    "author": "Scr1ptAl1as",
                    "git": "http://dsfasfad.fsfesf.fs",
                    "requiredargs": "",
                    "desc_0": "Run the currently loaded node script - uniscrape v1.0.",
                },
                {
                    "name": "stop",
                    "author": "Scr1ptAl1as",
                    "git": "http://dsfasfad.fsfesf.fs",
                    "requiredargs": "",
                    "desc_0": "Stop the node script if it is running - uniscrape v1.0.",
                },
                {
                    "name": "cje",
                    "author": "Scr1ptAl1as",
                    "git": "http://dsfasfad.fsfesf.fs",
                    "desc_0": "cje - cRUDE json editor - will manage the install package list",
                    "desc_1": "",
                    "desc_2": "'add' = Add a new package to the install list.",
                    "desc_3": "'insert' = Insert a item at position (x) to the package list.",
                    "desc_4": "'delete' = delete a package from the install package list.",
                    "desc_5": "'moveup' = Move the item based on its index up one position.",
                    "desc_6": "'movedown' = Move the item based on its index down one position.",
                    "desc_7": ""
                }
            ]
        }
    ]


Now inside of my script I will define a command class holder. This will act as a middle man to initiate commands when typed in
console

    class CmdInit:
    # Command Singleton instance

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CmdInit, cls).__new__(cls)

        return cls._instance

    def load(self, filelocation, startstatus):
        print("loading " + str(filelocation) + " " + str(startstatus))
    def unload(self):
        print("unloaded")

    def run(self):
        print("running?")

    def stop(self):
        print("stopped")

And the our last bit of setup exists in the main() def. All we have to do is make sure prj_details() and the listener is called
and the help system is now setup.

Note* if prj_details.parent_script is not provided a error will be thrown.

(No JSON Data found: Cannot initiate commands or request help.)

cRUDE Help Sys cannot find a script to listen to and in turn cannot find JSON data to initiate commands or match to help requests.


def main():
    prj_details()
    chs.consoleinputlistener(prj_details.parent_script)