import os
import subprocess
import sys
from colorama import Fore, init

init(autoreset=True)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_directory_and_venv(directory):
    print(f"{Fore.YELLOW}Checking if the directory '{directory}' exists...")

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"{Fore.GREEN}Directory '{directory}' created successfully.")
    else:
        print(f"{Fore.CYAN}Directory '{directory}' already exists.")

    venv_path = os.path.join(directory, "venv")
    print(f"{Fore.YELLOW}Creating virtual environment at '{venv_path}'...")
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    print(f"{Fore.GREEN}Virtual environment created successfully at '{venv_path}'.")
    return venv_path

def install_packages(venv_path):
    installed_packages = []
    
    pip_executable = os.path.join(venv_path, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
    packages_file = os.path.join(os.path.dirname(__file__), "packages.txt")
    
    if os.path.exists(packages_file):
        print(f"{Fore.YELLOW}Found 'packages.txt'. Installing packages...")
        clear_terminal()
        with open(packages_file, "r") as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        if packages:
            for package in packages:
                user_input = input(f"{Fore.CYAN}Do you want to install the package '{package}'? (y/n): ").strip().lower()
                if user_input == 'y':
                    print(f"{Fore.YELLOW}Installing package: {package}...")
                    try:
                        subprocess.run([pip_executable, "install", package], check=True)
                        print(f"{Fore.GREEN}Package '{package}' installed successfully.")
                        installed_packages.append(package)
                    except subprocess.CalledProcessError as e:
                        print(f"{Fore.RED}Error occurred while installing package '{package}': {e}")
                else:
                    print(f"{Fore.MAGENTA}Skipping package '{package}'.")
        else:
            print(f"{Fore.YELLOW}No packages found in 'packages.txt'.")
    else:
        print(f"{Fore.RED}No 'packages.txt' found at {packages_file}. Skipping package installation.")
    
    return installed_packages

def create_django_project(directory):
    project_name = input(f"{Fore.CYAN}Enter the name of your Django project: ").strip()
    project_path = os.path.join(directory, project_name)
    
    if not os.path.exists(project_path):
        print(f"{Fore.YELLOW}Creating project directory at {project_path}...")
        os.makedirs(project_path)
        print(f"{Fore.GREEN}Project directory created at {project_path}.")
    
    print(f"{Fore.YELLOW}Creating Django project '{project_name}'...")
    subprocess.run([os.path.join(directory, "venv", "Scripts", "python" if os.name == "nt" else "python3"),
                    "-m", "django", "startproject", project_name, project_path], check=True)
    print(f"{Fore.GREEN}Django project '{project_name}' created successfully at {project_path}.")

def open_in_vs_code(directory):
    user_input = input(f"{Fore.CYAN}Do you want to open the project in VS Code? (y/n): ").strip().lower()
    if user_input == 'y':
        print(f"{Fore.YELLOW}Opening project in VS Code...")
        os.system(f"code {directory}")
        print(f"{Fore.GREEN}VS Code opened with the project.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create a venv and install packages in the specified directory.")
    parser.add_argument("-i", "--input", required=True, help="Path to the directory where venv should be created.")
    args = parser.parse_args()

    directory = os.path.abspath(args.input)
    print(directory)
    print(f"{Fore.CYAN}Starting process to create virtual environment in '{directory}'...\n")
    
    venv_path = create_directory_and_venv(directory)
    
    installed_packages = install_packages(venv_path)
    clear_terminal()
    print(f"{Fore.GREEN}All packages and virtual environment installed successfully.\n")
    
    if 'Django' in installed_packages:
        user_input = input(f"{Fore.CYAN}Do you want to create a Django project? (y/n): ").strip().lower()
        if user_input == 'y':
            create_django_project(directory)

    open_in_vs_code(directory)

    print(f"{Fore.GREEN}Setup completed successfully. You can now start your Django project.")

if __name__ == "__main__":
    main()