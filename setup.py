version = 1.0


# -- Imports -- #
import os
import subprocess 
import sys
from subprocess import CalledProcessError, PIPE
import functools

user = 'dalton'
home = '/home/' + user

def run_cmd(cmd):
  return subprocess.run(
    cmd, 
    shell=True, 
    stdout=PIPE, 
    stderr=PIPE, 
    check=True).stdout.decode('utf-8')


# -- pip install things -- #
 # check if pip is installed
try: 
  cmd = 'which pip'
  subprocess.run(cmd, shell=True, check=True)
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

run = functools.partial(subprocess.run, shell=True)


def check_for_prereq(prereq):
  print('checking for prerequisites \'' + prereq + '\'')
  res = run_cmd('apt-cache policy ' + prereq)
  if res.split('Installed:')[1][2:6] == 'none':
    print(prereq + ' is not installed!')
    return False
  else:
    return True


def check_and_install_pkg(pkg):
  pkg_exists = check_for_prereq(pkg)
  if not pkg_exists:
    print('Installing ' + pkg)
    run('apt-get -y install ' + pkg)

# -- Install pyenv -- #
cmd = """
sudo apt-get update; sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

"""
run(cmd)
run(" git clone https://github.com/pyenv/pyenv.git " + home + "/.pyenv")



# -- Install fonts -- #
print_header('Installing fonts', 1, 'green')
check_and_install_pkg('wget')
run('mkdir firacode_nf')
run('mkdir firamono_nf')
run('mkdir ' + home + '/.local/share/fonts')

# Install FiraCode NerdFont
url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip"
cmd = 'wget ' + url
run(cmd)
run('unzip FiraCode.zip -d firacode_nf')
run('cp firacode_nf/Fira\ Code\ Bold\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firacode_nf/Fira\ Code\ Light\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firacode_nf/Fira\ Code\ Medium\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firacode_nf/Fira\ Code\ Regular\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firacode_nf/Fira\ Code\ Retina\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')

# Install FiraMono NerdFont
url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraMono.zip"
cmd = 'wget ' + url
run(cmd)
run('unzip FiraMono.zip -d firamono_nf')
run('cp firamono_nf/Fira\ Mono\ Bold\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firamono_nf/Fira\ Mono\ Medium\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')
run('cp firamono_nf/Fira\ Mono\ Regular\ Nerd\ Font\ Complete.otf ' + home + '/.local/share/fonts/')

# Clean up
run('rm FiraCode.zip')
run('rm FiraMono.zip')
run('rm -r firacode_nf')
run('rm -r firamono_nf')


# -- Install zsh -- #
print_header('Installing zsh', 2, 'green')
check_and_install_pkg('zsh')
run('cp .zshrc ' + home)

# -- Install oh-my-zsh -- #
print_header('Installing oh-my-zsh', 3, 'green')
check_and_install_pkg('curl')
run("git clone https://github.com/ohmyzsh/ohmyzsh.git " + home + "/.oh-my-zsh")
install_cmd = "sh -c \"$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sed 's:env zsh::g' | sed 's:chsh -s .*$::g')\""
run(install_cmd)


# -- Install powerlevel10k -- #
print_header('Installing powerlevel10k', 4, 'green')
install_cmd = "git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-" + home + "/.oh-my-zsh/custom}/themes/powerlevel10k"
run(install_cmd)
run('cp .p10k.zsh ' + home)
