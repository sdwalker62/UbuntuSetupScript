#    ___                _        ___ _                      
#   / __|___  ___  __ _| |___   / __| |_  _ _ ___ _ __  ___ 
#  | (_ / _ \/ _ \/ _` | / -_) | (__| ' \| '_/ _ \ '  \/ -_)
#   \___\___/\___/\__, |_\___|  \___|_||_|_| \___/_|_|_\___|
#                 |___/                                     
                                                                                                            
from ..utilities import run, print_header                 


def exec_stage():

    # ========================================================== #
    #                      Section 0: Main                       #
    # ========================================================== #
    print_header('Installing Google Chrome')
    run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    run("sudo dpkg -i google-chrome-stable_current_amd64.deb")