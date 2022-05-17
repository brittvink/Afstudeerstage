# Afstudeerstage

README alleen voor de website

Install the required packages. Consider using a virtual environment to ensure the right version of packages are used.

python3 -m venv <name of virtual environment>
source <name of virtual environment>/bin/activate

  The python packager manager (pip) and the requirements file can be used to install all the necessary packages. Note that the requirements.txt file includes depedencies with their correct versions. Therefore, include the flag --no-dependencies when installing the packages to prevent unnecessary upgrading.

pip install -r requirements.txt

  You can exit the virtual environment by typing:

deactivate
  
  
  
  Run website (go to website/)
  
  python3 manage.py runserver
  
