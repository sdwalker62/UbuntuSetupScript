version = 1.0


# -- Imports -- #
import os
import subprocess 
import sys
from subprocess import CalledProcessError, run, PIPE
import yaml


def run_cmd(cmd):
  return run(
    cmd, 
    shell=True, 
    stdout=PIPE, 
    stderr=PIPE, 
    check=True).stdout.decode('utf-8')


# -- pip install things -- #
 # check if pip is installed
try: 
  cmd = 'which pip'
  run(cmd, shell=True, check=True)
except CalledProcessError:
  cmd = 'apt-get -y install python3-pip'
  _ = run_cmd(cmd)
  import pip

def pip_install(package):
    pip.main(['install', package])

try: 
  from termcolor import colored
except ImportError:
    pip_install('termcolor')
    from termcolor import colored


def print_header(msg, index, color):
  print('\n')
  print(colored(str(index) + '. ' + msg, color, attrs=['bold']))
  print('\n')

# -- Introduction -- #
title = """
  _   _ _             _          ___      _               ___         _      _   
 | | | | |__ _  _ _ _| |_ _  _  / __| ___| |_ _  _ _ __  / __| __ _ _(_)_ __| |_ 
 | |_| | '_ \ || | ' \  _| || | \__ \/ -_)  _| || | '_ \ \__ \/ _| '_| | '_ \  _|
  \___/|_.__/\_,_|_||_\__|\_,_| |___/\___|\__|\_,_| .__/ |___/\__|_| |_| .__/\__|
                                                  |_|                  |_|                                        |_|                  |_|             
"""

intro_text = """
This script will download and install the following items: \n
1. zsh \n
2. oh-my-zsh \n
3. pyenv \n
4. fonts \n
5. VS Code \n
6. Docker \n
7. Flutter \n
8. Jetbrains Toolbox \n
9. Google Chrome \n
10. kde \n\n
11. necessary tools \n

The script will ask for some basic information to generate the necessary ssh keys for git. 
After that information is provided it will proceed without user input. 

"""
print(colored(title, 'green'))
print(colored('version: ' + str(version), 'blue', attrs=['bold']))
print(intro_text)


# -- Check for root privileges -- # 
#if os.geteuid() != 0: 
#  print(colored('This script requires root privileges to operate properly.', 'red', attrs=['bold'])) 
#  sys.exit()


# -- Gather necessary user information for Github ssh keys -- #
print('Your GitHub email is required for setting up ssh properly. Enter the email you use for your GitHub account:')
#github_email = input()


def check_for_prereq(prereq):
  print('checking for prerequisites \'' + prereq + '\'')
  res = run_cmd('apt-cache policy ' + prereq)
  parse_res = yaml.safe_load(res)
  if parse_res[prereq]['Installed'] == '(none)':
    print(prereq + ' is not installed!')
    return False
  else:
    return True


def check_and_install_pkg(pkg):
  pkg_exists = check_for_prereq(pkg)
  if not pkg_exists:
    print('Installing ' + pkg)
    _ = run_cmd('apt-get install ' + pkg)


# -- Install fonts -- #
print_header('Installing fonts', 1, 'blue')
_ = run_cmd('mkdir firacode_nf')
_ = run_cmd('mkdir firamono_nf')
_ = run_cmd('mkdir firacode')

# Install FiraCode NerdFont
_ = run_cmd('cd firacode_nf')
url = """
https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip
"""
cmd = 'curl ' + url
_ = run_cmd(cmd)
_ = run_cmd('unzip FiraCode.zip')
_ = run_cmd('cp Fira\ Code\ Bold\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Code\ Light\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Code\ Medium\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Code\ Regular\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Code\ Retina\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')


# Install FiraMono NerdFont
_ = run_cmd('cd ../firamono_nf')
url = """
https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraMono.zip
"""
cmd = 'curl ' + url
_ = run_cmd(cmd)
_ = run_cmd('unzip FiraMono.zip')
_ = run_cmd('cp Fira\ Mono\ Bold\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Mono\ Medium\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')
_ = run_cmd('cp Fira\ Mono\ Regular\ Nerd\ Font\ Complete.otf ~/.local/share/fonts')

_ = run_cmd('cd ..')


# -- Install zsh -- #
print_header('Installing zsh', 2, 'blue')
check_and_install_pkg('zsh')


# -- Install oh-my-zsh -- #
print_header('Installing oh-my-zsh', 3, 'blue')
check_and_install_pkg('curl')
install_cmd = """
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
"""
_ = run_cmd(install_cmd)


# -- Install powerlevel10k -- #
print_header('Installing powerlevel10k', 4, 'blue')
install_cmd = """
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
"""
_ = run_cmd(install_cmd)
