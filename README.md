# Graduation internship Britt Vink, topic modelling on text-data
In this project repository all different scripts used in this project are present. During the project the goal was to better uderstand textdata, using topic modelling and finding similarity. This is done using different clustering methods and vectorizing data to find distances between articles.

## Introduction
In the last few years a lot of research is done on the topics of sustainability, since there is a growing interest in how to transfer to a more sustainable society. These articles are published in papers and often later on numerous of websites. Some news sites, like ScienceDaily, write the headlines and main ideas about these articles, so the articles are easier to read.
Researchers of the KCBBE are doing research on numerous of topics involving sustainability and life science. They are interested in the latest updates in the field. Since there are a lot of articles it is hard to find those that are relevant to the research. During this project an algorithm is made to find relatedness between articles. This project was proposed with the purpose of making a web interface to find the articles that are related to their research projects more easily.

In this repository there are diffent folder, respreseting diffent parts of the project.
* Documentation shows the hmtl pages with the documentation of all script used in this projects
* Website shows all scripts used to make a web-interface
* Scripts shows all scripts used to get the data, pre-process and process it.

## Prerequisites

The scripts are written in Python v3.7.4. To run the scripts the folowing packages have to be installed
 * numpy (v1.19.5)
 * pandas (v1.2.1)
 * statsmodels (v0.12.2)
 * matplotlib (v3.3.4)
 * seaborn (v0.11.1)

See 'Installing' on how to install these packages. Note that the performance / reliability of this program on other versions is not guaranteed.

### Installing

Install the required packages. Consider using a virtual environment to ensure the right version of packages are used.
```
python3 -m venv <name of virtual environment>
source <name of virtual environment>/bin/activate
```

The python packager manager (pip) and the requirements file can be used to install all the necessary packages. Note that the requirements.txt file includes depedencies with their correct versions. Therefore, include the flag --no-dependencies when installing the packages to prevent unnecessary upgrading.
```
pip install -r requirements.txt --no-dependencies
```
You can exit the virtual environment by typing:
```
deactivate  
```

## Usage

### documentation
By opening index.html the documentation is shown. If documentation in the scripts changes the html pages should be made again clustering
```
sphinx-apidoc -o . ../scripts -f
make html
```

### scripts
Scripts can be run using
```
scriptname -h
```

### website
The website can be run using
```
python3 manage.py runserver
```  

## Author  

Britt Vink *(1)*

1. Hanzehogeschool Groningen, Instituut for Life Science and Technology, Groningen, Nederland

contact: b.vink@st.hanze.nl
