#!/usr/bin/env python
# -*- coding: utf-8 -*-
# C:\Python27\ArcGIS10.6\python.exe arcserver_cleaning_lists.py
# ---------------------------------------------------------------------------
import os, csv, json, datetime, time, arcpy

# You can setup the server variable to do a batch process on multiple servers.
# However, depending on the size the script may not run corectly.
# It is recommended to run one or two servers at a time.
servers = [
    {"server": "\\\\server_name_here\\arcgisserver"}
]

def create_lists():
    with open("mxds_list.csv", 'wb') as mxd_csv, open("features_list.csv", 'wb') as feature_csv, open("service_list.csv", 'wb') as service_csv:
        mxd_writer = csv.writer(mxd_csv, delimiter=',')
        feature_writer = csv.writer(feature_csv, delimiter=',')
        # broken_writer = csv.writer(broken_csv, delimiter=',')
        service_writer = csv.writer(service_csv, delimiter=',')

        mxd_writer.writerow(["mxd" , "environment"])
        feature_writer.writerow(["mxd" , "layer" , "source"])
        # broken_writer.writerow(["mxd" , "layer" , "source"])
        service_writer.writerow(["server", "mxd"])

        for server in servers:
            for root, dirs, files in os.walk(server['server']):
                for file in files:
                    if file.endswith(".mxd"):
                        mxd = os.path.join(root, file)
                        environment = server['server'][2:-13]
                        mxd_writer.writerow([mxd,environment])

                        m = arcpy.mapping.MapDocument(mxd)
                        for lyr in arcpy.mapping.ListLayers(m):
                            if lyr.supports("DATASOURCE"):
                                layer = lyr.name
                                source = lyr.dataSource
                                feature_writer.writerows(zip([mxd], [layer], [source]))

                        # brknList = arcpy.mapping.ListBrokenDataSources(m)
                        # for brk in brknList:
                        #     layer = brk.name
                        #     source = brk.dataSource
                        #     broken_writer.writerows(zip([mxd], [layer], [source]))

                    if file.endswith("manifest.json"):
                        manifest = os.path.join(root, file)
                        pm = parse_manifest(manifest)
                        service_writer.writerow([pm[0], pm[1]])

def parse_manifest(manifest):
    with open(manifest, 'r') as m:
        j = json.load(m)
        return j['resources'][0]['clientName'] , j['resources'][0]['onPremisePath']

def main():
    print("\n    Start Time : " + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    create_lists()
    print("\n    End Time : " +  str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " \n\n    COMPLETED!")

if __name__ == '__main__':
    main()
