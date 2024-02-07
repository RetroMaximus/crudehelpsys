import os
import sys
import json
import ast
from pathlib import *
import subprocess
import importlib
from importlib import util
import inspect

externalcmdclass = None
classcontainer = None
externalcmdclass = ""
jsonhelp = None

# "cRUDE Help Sys– simplifying command-line applications!
# Developed by the cRUDECrew, this script acts as a robust backbone, offering a
# straightforward solution for command execution and help requests in your Python projects.
# cRUDE Help Sys has a user-friendly approach that facilitates seamless command initiation through
# a dynamic system that allows the import and execution of custom commands stored outside
# the script,eliminating the need for constant modification. Ease of use is
# highlighted by its interactive console input listener, This enables users to effortlessly navigate
# and execute commands for simplicity and efficiency. cRUDE Help Sys simplifies command-line application
# development, offering a hassle-free experience for developers and users alike.
#
# Welcome to a world where command-line operations become a breeze - welcome to cRUDE Help Sys!"

global first_arg

class hrcolors:
    console_color_reset = "\033[0m"  # Reset
    console_color_red = "\033[31m"  # Red - Warning Error Alert Text
    console_color_purple = "\033[35m"  # Purple - Syntax Text
    console_color_green = "\033[32m"  # Green - Deco Text 1
    console_color_cyan = "\033[36m"  # Cyan - Deco Text 2
    console_color_blue="\033[0;34m"  # Blue - Deco text 3
    console_color_yellow = "\033[33m"  # Yellow - Important Text
    console_color_on_iblack = "\033[0;100m"  # Black Background
    console_color_textblink = "\033[5m"  # Blinking Text

class prj_details:
    enable_env = None
    grouporg = "cRUDECrew"
    scriptname = "crudehelpsys"
    spb = 1
    script_file = ""
    scriptver = 1.0
    shortcmdline = "chs"
    scriptdesc = ("Simplifying command-line applications!\n"
                  "Developed by the cRUDECrew, this script acts as a robust backbone, offering a\n"
                  "straightforward solution for command execution and help requests in your Python projects.\n"
                  "cRUDE Help Sys has a user-friendly approach that facilitates seamless command initiation through\n"
                  "a dynamic system that allows the import and execution of custom commands stored outside\n"
                  "the script,eliminating the need for constant modification. Ease of use is\n"
                  "highlighted by its interactive console input listener, This enables users to effortlessly navigate\n"
                  "and execute commands for simplicity and efficiency. cRUDE Help Sys simplifies command-line application\n"
                  "development, offering a hassle-free experience for developers and users alike.\n\n"

                  "Welcome to a world where command-line operations become a breeze - welcome to cRUDE Help Sys!\n\n")

class hrclass:
    classcontainer = None
    externalcmdclass = ""
    jsonhelp = None
    def __init__(self, cls):
        cls.classcontainer = None
        cls.externalcmdclass = None  # Make it an instance attribute
        cls.externalclasspath = ""

    def launchcmd(cmd_arg, frommainscript, fullscriptpath):
        # Extract the arguments passed to the command
        launchedargs = cmd_arg[2:]
        lcmd, totalargs = cmd_arg[1], len(cmd_arg) - 2

        # Check if the external command class holder is available
        if hrclass.externalcmdclass is None:
            print(hrcolors.console_color_red + "Cannot find the command class holder in the script this command was called from.", hrcolors.console_color_reset)
            exit()

        # Dynamically import the external command class
        cmd_init_instance = dynamically_import(fullscriptpath, hrclass.externalcmdclass)
        first_arg = frommainscript

        def common_checks(arg_count):
            # Filter out None values from cmd_arg
            non_none_args = [arg for arg in cmd_arg[2:2 + arg_count] if arg is not None]
            arg_list = non_none_args + [None] * (arg_count - len(non_none_args))
            arg_request_result = hrclass.argrequest(lcmd, first_arg)

            # Perform argument checks using hrclass.verify
            if hrclass.verify(arg_request_result, arg_list, lcmd, frommainscript):
                return True

        # Dynamically get the method from cmd_init_instance
        cmd_method = getattr(cmd_init_instance, lcmd, None)

        # Check if the method is callable and has the __call__ attribute
        if callable(cmd_method) and hasattr(cmd_method, '__call__'):
            # Check if the total number of arguments matches the expected number
            if totalargs == len(inspect.signature(cmd_method).parameters) and common_checks(totalargs):
                cmd_method(*launchedargs)
            else:
                print(hrcolors.console_color_yellow + "\nInvalid Command" + hrcolors.console_color_reset + " - "
                "Use" + hrcolors.console_color_purple+ f" '{first_arg} help' " + hrcolors.console_color_reset + ""
                " in command line without quotes for more information.", hrcolors.console_color_textblink,
                      hrcolors.console_color_green +"\n\nReady!\n"+ hrcolors.console_color_reset)
                exit()
        else:
            print(hrcolors.console_color_yellow + "\nInvalid Command" + hrcolors.console_color_reset + " - "
                    "Use" + hrcolors.console_color_purple + f" '{first_arg} help' "
                    f"" + hrcolors.console_color_reset + " in command line without quotes for"
                    "more information.", hrcolors.console_color_textblink,
                      hrcolors.console_color_green +"\n\nReady!\n" + hrcolors.console_color_reset)


        # Exit the script after command execution
        exit()

    def checkcmdcache(cmd, args, first_arg, classcontainer):
        # Get the total number of command-line arguments
        n = len(sys.argv)

        # Match the command and perform corresponding actions
        match cmd:
            case "quit":
                # Exit the script
                exit()

            case "no_cmds":
                print(f"\n'{prj_details.welcommsg}")

            case "help":
                # Display help information
                print(hrcolors.console_color_green + '\n' + f"{prj_details.grouporg} " + hrcolors.console_color_cyan
                      + f" - {prj_details.scriptname} - " + hrcolors.console_color_reset + f"{prj_details.scriptver} - "
                      + hrcolors.console_color_blue + "Help" + hrcolors.console_color_reset)
                print(f'{prj_details.scriptdesc}')
                # Check if a specific help term is provided
                if len(args) == 3:
                    external_script_path = os.path.abspath(sys.argv[0])
                    hrclass.helprequest(args[2], first_arg, external_script_path)
                else:
                    print(hrcolors.console_color_yellow + "\nInvalid Help Request" + hrcolors.console_color_reset + " - Use a one-word search term.\n")
                # Exit the script
                exit()

            case _:
                # Iterate through command-line arguments
                for x in range(1, n):
                    cmd_args = sys.argv

                # Get the absolute path of the script
                external_script_path = os.path.abspath(sys.argv[0])

                # Launch the command using hrclass.launchcmd
                hrclass.launchcmd(cmd_args, first_arg, external_script_path)

                # Exit the script
                exit()

    def argrequest(helpreq, homescript):
        # Check if jsonhelp is available and not empty
        if len(hrclass.jsonhelp) > 0:
            try:
                # Check if jsonhelp is an instance attribute
                if hasattr(hrclass, 'jsonhelp'):
                    for cmd_data in hrclass.jsonhelp[0]["helpdatastorage"]:
                        if cmd_data["name"] == helpreq:
                            required_args = cmd_data.get("requiredargs", "")
                            return tuple(required_args.split(", ")) if required_args else ()

                # If jsonhelp is a class attribute, access it directly
                elif 'jsonhelp' in hrclass.__dict__:
                    for cmd_data in hrclass.jsonhelp[0]["helpdatastorage"]:
                        if cmd_data["name"] == helpreq:
                            required_args = cmd_data.get("requiredargs", "")
                            return tuple(required_args.split(", ")) if required_args else ()

                # Print message if no help is found for the term
                print(hrcolors.console_color_yellow + "\nNo help for this term: " + hrcolors.console_color_red + helpreq + hrcolors.console_color_reset)
                return ()
                # Existing code if any more custom checks needed can be added here...

            except Exception as e:
                # Handle exceptions and print error information
                print(hrcolors.console_color_yellow + f"An error occurred:" + hrcolors.console_color_reset + hrcolors.console_color_bpurple + f"{e}" + hrcolors.console_color_reset)
                import traceback
                traceback.print_exc()
        else:
            # Print error message if no JSON help data is provided
            print(hrcolors.console_color_red + f"Error: " + hrcolors.console_color_yellow + " No JSON help data provided in " + hrcolors.console_color_purple + "{homescript}" + hrcolors.console_color_reset + ". Cannot find any help results.")

    @staticmethod
    def encr(e_text, k):
        e_chrs = [chr(ord(char) ^ int(k)) for char in e_text]
        e_k = ''.join(e_chrs)
        return e_k

    @staticmethod
    def d(d_text, k):
        d_chrs = [chr(ord(char) ^ int(k)) for char in d_text]
        d_k = ''.join(d_chrs)
        return d_k

    @classmethod
    def setclassholder(cls, class_name, class_path):
        # Set the class holder dynamically

        cls.classcontainer = globals().get(class_name)
        cls.externalcmdclass = class_name
        cls.externalclasspath = class_path

    def getclasspath(self):
        return self.externalclasspath

    def getclassholder(self):
        return self.externalcmdclass

    def helprequest(helpreq, homescript, class_script_path):
        # Check if the help request is "None" and exit
        if helpreq == "None":
            exit()

        allcmddefs = set()

        # Function to traverse the AST and collect command definitions
        def collect_cmd_defs(node):
            if isinstance(node, ast.ClassDef) and node.name == hrclass.externalcmdclass:
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name != '__new__':
                        allcmddefs.add(child.name)

        # Parse the AST from the file
        parsed_ast = ast.parse(open(class_script_path).read())

        # Traverse the AST to collect command definitions
        for node in ast.walk(parsed_ast):
            collect_cmd_defs(node)

        # ppb()
        # Process the help request based on the collected command definitions
        if helpreq in allcmddefs:

            print("\nHelp results for: ", hrcolors.console_color_green + helpreq, hrcolors.console_color_reset)
            hrclass.getjsonstructure(helpreq)
            print(hrcolors.console_color_yellow + f"\nUsage" + hrcolors.console_color_purple + f" : {hrclass.genfunctionlist(helpreq, homescript)}\n" + hrcolors.console_color_reset)

            exit()
        elif helpreq == "list":

            print(f"\nListing all Commands -  Type '{homescript} help cmd' without quotes for more deatils.\n"
                  f"                        Only the first line of the descriptiton is shown\n")
            allcmds = hrclass.gencommandlist(homescript).split(", ")
            for cmd in allcmds:
                print(hrcolors.console_color_purple + cmd + hrcolors.console_color_yellow + " - "
                      + hrcolors.console_color_reset + (hrclass.getjsonlisting(cmd)) + "\n"
                      + hrcolors.console_color_reset)
            print(hrcolors.console_color_red + "Done Listing\n" + hrcolors.console_color_reset)
        else:
            print("\n" + hrcolors.console_color_yellow + "No help for this term: " + hrcolors.console_color_red + helpreq, hrcolors.console_color_reset)

    def getjsonlisting(bycmd):
        temparchdata = hrclass.jsonhelp
        archivedata = temparchdata[0]

        # Iterate through the help items and print details for the specified command
        for helpitem in archivedata.get("helpdatastorage", []):
            if helpitem.get('name') == bycmd:
                 # Iterate through the description items and print each one
                for descnum in range(len(helpitem) - 2):
                    cmddesc = helpitem.get(f"desc_{descnum}")
                    if cmddesc is not None:
                        return cmddesc

    def getjsonstructure(bycmd):
        temparchdata = hrclass.jsonhelp
        archivedata = temparchdata[0]

        # Iterate through the help items and print details for the specified command
        for helpitem in archivedata.get("helpdatastorage", []):
            if helpitem.get('name') == bycmd:
                print(f"\nAuthor: {helpitem.get('author', '')}")
                print(f"Git: {helpitem.get('git', '')}\n")
                print(hrcolors.console_color_on_iblack + "Description:" + hrcolors.console_color_reset)

                # Iterate through the description items and print each one
                for descnum in range(len(helpitem) - 2):
                    cmddesc = helpitem.get(f"desc_{descnum}")
                    if cmddesc is not None:
                        print(cmddesc)

    def verify(checkargs, compared, helpreq, homescript):
        global argpass
        arg_types = {"s": str, "i": int, "o": object, "a": any, "": None}

        # Check if both checkargs and compared are empty
        if not checkargs and not compared:
            return True

        for x, arg in enumerate(checkargs, start=2):
            arg_type = arg_types.get(arg)

            # Check if the argument type is valid
            if arg_type is None:
                print(f"\nCannot continue.",hrcolors.console_color_yellow + f"Invalid argument type:", hrcolors.console_color_textblink + hrcolors.console_color_red + f" {arg}.", hrcolors.console_color_reset)
                argpass = False

            try:
                # Try to convert the compared value to the specified argument type
                val = arg_type(compared[x - 2])
            except ValueError:
                print(f"\nCannot continue. Argument ({x - 1}) is not a {arg}.")
                argpass = False
                return False

        return True

    def gencommandlist(homescript):
        allcmddefs = set()  # Variable to store all command definitions

        # Function to traverse the AST and collect command definitions
        def collect_cmd_defs(node):
            if isinstance(node, ast.ClassDef) and node.name == hrclass.externalcmdclass:
                for child in node.body:
                    # print(child)
                    if isinstance(child, ast.FunctionDef) and child.name != '__new__':
                        allcmddefs.add(child.name)

        # Parse the AST from the file
        parsed_ast = ast.parse(Path(homescript).read_text())
        # Traverse the AST to collect command definitions
        for node in ast.walk(parsed_ast):
            collect_cmd_defs(node)
        # Return the list of command definitions
        return ', '.join(sorted(allcmddefs))

    def genfunctionlist(bycmd, homescript):
        allcmddefs = {}  # Dictionary to store command definitions and their arguments

        # Function to traverse the AST and collect command definitions
        def collect_cmd_defs(node):
            if isinstance(node, ast.ClassDef) and node.name == hrclass.externalcmdclass:
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name != '__new__':
                        # Store function name and its arguments in the dictionary
                        allcmddefs[child.name] = [arg.arg for arg in child.args.args]

        # Parse the AST from the file
        parsed_ast = ast.parse(Path(homescript).read_text())
        # Traverse the AST to collect command definitions
        for node in ast.walk(parsed_ast):
            collect_cmd_defs(node)

        if bycmd in allcmddefs:
            arguments = ', '.join(allcmddefs[bycmd])

            # Remove "self" only if it is present in arguments
            if "self" in arguments:
                usageargs = arguments.replace("self,", "").replace("self", "").replace(",", "")
            else:
                usageargs = arguments.replace("self,", "").replace("self", "").replace(",", "")

            return f"{homescript} {bycmd}{usageargs}"
        else:
            return f"{homescript} {bycmd}"

def dynamically_import(full_script_path, class_name):
    try:
        remenvpath = os.path.dirname(__file__).split(os.sep)

        # Create a module specification
        spec = importlib.util.spec_from_file_location("confirmed", full_script_path)

        # Load the module from the specification
        script_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_module)

        # Get the class from the module
        script_class = getattr(script_module, class_name)

        # Instantiate the class
        instance = script_class()
        return instance
    except ImportError as e:
        print(f"Error importing module '{full_script_path}': {e}")
        return None
    except AttributeError as a:
        print(f"Error: Class '{class_name}' not found in module '{full_script_path}': {a}")
        return None

def activate_virtualenv():
    # Get the path to the directory containing the current script
    # script_directory = os.path.dirname(os.path.abspath(os.path.join('.venv/Scripts/', 'activate_this.py')))
    bat_directory = os.path.dirname(os.path.abspath(os.path.join('activate.bat')))
    script_directory = os.path.dirname(os.path.abspath(os.path.join('activate_this.py')))
    # Determine the platform (Windows, macOS, Linux)
    platform = sys.platform.lower()
    # Define the path to the activate_this.py script based on the platform
    activate_script_path = None
    if platform.startswith('win'):
        activate_script_path = os.path.join(bat_directory, '.venv', 'Scripts', 'activate.bat')

    elif platform.startswith('darwin') or platform.startswith('linux'):
        activate_script_path = os.path.join(script_directory, '.venv', 'Bin', 'activate_this.py')
    else:
        print("Unsupported operating system")
        sys.exit(1)
    # Check if the activate_this.py script exists
    if not os.path.exists(activate_script_path):
        print(f"Error: activate_this.py not found at {activate_script_path}")
        sys.exit(1)
    if platform.startswith('win'):
        subprocess.run([r"" + activate_script_path])
    else:
        # Execute the activate_this.py script
        exec(open(activate_script_path).read(), {'__file__': activate_script_path})
    print("Virtual environment activated!")

def deactivate_virtualenv():
    # Get the path to the directory containing the current script
    # script_directory = os.path.dirname(os.path.abspath(os.path.join('.venv/Scripts/', 'activate_this.py')))
    bat_directory = os.path.dirname(os.path.abspath(os.path.join('deactivate.bat')))
    script_directory = os.path.dirname(os.path.abspath(os.path.join('deactivate_this.py')))
    # Determine the platform (Windows, macOS, Linux)
    platform = sys.platform.lower()
    # Define the path the activate_this.py script based on the platform
    activate_script_path = None
    if platform.startswith('win'):
        activate_script_path = os.path.join(bat_directory, '.venv', 'Scripts', 'deactivate.bat')

    elif platform.startswith('darwin') or platform.startswith('linux'):
        activate_script_path = os.path.join(script_directory, '.venv', 'Bin', 'deactivate_this.py')
    else:
        print("Unsupported operating system")
        sys.exit(1)
    # Check if the activate_this.py script exists
    if not os.path.exists(activate_script_path):
        print(f"Error: activate_this.py not found at {activate_script_path}")
        sys.exit(1)
    if platform.startswith('win'):
        subprocess.run([r"" + activate_script_path])
    else:
        # Execute the activate_this.py script
        exec(open(activate_script_path).read(), {'__file__': activate_script_path})
    print("Virtual environment deactivated!")

def consoleinputlistener(frommainscript):
    # Set the script file in project details
    prj_details.script_file = frommainscript

    # Check and activate/deactivate virtual environment based on configuration
    if prj_details.enable_env == 1:
        # If not in a virtual environment, activate it
        if not is_virtualenv():
            activate_virtualenv()

    else:
        if is_virtualenv():
            deactivate_virtualenv()

    # Get command line arguments
    args = sys.argv
    cmd = ""

    # Get the script file name and its base name
    first_arg = frommainscript.split(os.sep)[-1].split('.')[0] + ".py"
    or_fromenv = first_arg.split('.', 1)
    n = len(sys.argv)

    # Check if JSON help data is available

    if hrclass.jsonhelp == None or len(hrclass.jsonhelp) <= 0:
        print(hrcolors.console_color_red + "No JSON Data found: " + hrcolors.console_color_yellow + "Cannot initiate commands or request help.",
              hrcolors.console_color_reset)
        exit()

    # Iterate through command line arguments
    for x in range(0, n):
        # Check if the current argument matches certain conditions
        if (sys.argv[x] == first_arg or sys.argv[x] == or_fromenv[0] or prj_details.shortcmdline == sys.argv[x]
                or prj_details.scriptname == sys.argv[x] or prj_details.scriptname.lower() == sys.argv[x]):
            arg_value = len(sys.argv)
            # Check if only the script name is provided as an argument
            if arg_value == 1:
                cmd = 'no_cmds'
                print(hrcolors.console_color_green + "\nWelcome \n" + hrcolors.console_color_cyan
                      + prj_details.scriptname +  hrcolors.console_color_reset +  " - " + str(prj_details.scriptver)
                      + " - " + hrcolors.console_color_blue + prj_details.grouporg + hrcolors.console_color_reset
                      + "\n\n" + prj_details.scriptdesc)

                print("\nFor a list of commands type " + hrcolors.console_color_purple + "'"
                      + prj_details.script_file + " help list'" + hrcolors.console_color_reset
                      + " without the quotes.\n")

            else:
                # Get the next argument as the command and call checkcmdcache
                cmd = sys.argv[x + 1]
                args = sys.argv
                hrclass.checkcmdcache(cmd, args, first_arg, classcontainer)
        else:
            # Handle invalid command case
            cmd = sys.argv[x]
            print(hrcolors.console_color_yellow + "\nInvalid Command" + hrcolors.console_color_reset
                  + " - Use" + hrcolors.console_color_purple +" '" + first_arg + " help'"
                  + hrcolors.console_color_reset + " in command line without "
                  "quotes for more information. \n'"
                  + first_arg + " help gui' without quotes\n \nReady!\n")

def is_virtualenv():
    # Powered by check.
    def ppb():
        # key = 867530
        # temp_k = ''.join(f"chr({int(ord(digit))})" for digit in str(key))
        # print(temp_k)

        # print(hrclass.encrypt("Powered by cRUDEcREW 'cRUDE Help Sys' CLI app"))
        # print(hrclass.decrypt("󓲚󓲥󓲽󓲯󓲸󓲯󓲮󓳪󓲨󓲳󓳪󓲩󓲘󓲟󓲎󓲏󓲩󓲘󓲏󓲝󓳪󓳭󓲩󓲘󓲟󓲎󓲏󓳪󓲂󓲯󓲦󓲺󓳪󓲙󓲳󓲹󓳭󓳪󓲉󓲆󓲃󓳪󓲫󓲺󓲺"))
        k = chr(56) + chr(54) + chr(55) + chr(53) + chr(51) + chr(48)
        if prj_details.spb == 1: print("\n" + hrcolors.console_color_yellow +
                                       hrclass.d(
                                           "󓲚󓲥󓲽󓲯󓲸󓲯󓲮󓳪󓲨󓲳󓳪󓲩󓲘󓲟󓲎󓲏󓲩󓲘󓲏󓲝󓳪󓳭󓲩󓲘󓲟󓲎󓲏󓳪󓲂󓲯󓲦󓲺󓳪󓲙󓲳󓲹󓳭󓳪󓲉󓲆󓲃󓳪󓲫󓲺󓲺", k),
                                       hrcolors.console_color_reset)
    ppb()
    # Check if running inside a virtual environment
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

def main():
    if prj_details.enable_env == 1:
        # If not in a virtual environment, activate it
        if not is_virtualenv():
            activate_virtualenv()

    else:
        if is_virtualenv():
            deactivate_virtualenv()

    isfile_arg = os.path.basename(__file__)
    fromhome = os.path.basename(hrclass.externalclasspath)
    consoleinputlistener(isfile_arg, fromhome)

if __name__ == "__main__":
    main()
