# ArcServer Cleaning Tool

This script is used to help you determine what ESRI related files are being used to create map services. It can also be used to identify mxds with broken data sources.

The script creates several csv files with different information to parse through. These file describe the following:
* list of mxds that exist on a given server
* list of mxds used by map services on a given server
* list of feature used for each mxd
* list of features that have broken data sources


## Instructions
```
  # Change your directory
  cd your\directory

  # Run the script
  C:\Python27\ArcGIS10.6\python.exe sde_cleaning_list.py
```
