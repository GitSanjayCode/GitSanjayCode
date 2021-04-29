import csv
import xml.etree.cElementTree as ET

components = {"Final Statement":1,"HR Incentive Data":2,"HR Practical Data":3}

root = ET.Element("root")
with open('xml1.csv','r') as csvfile:
        csvreader = csv.reader(csvfile)
        i=0
        compType=0
        compLineNum=0
        metricId=0
        colValue = []
        rowValue = []
        for row in csvreader:
                        if row[0] in components:
                                comp=row[0]
                                print('New Component :',comp)
                                compType = components.get(comp)
                                print(compType)
                                component = ET.SubElement(root, "Component",name=comp)
                                compLineNum=0
                                metricId=0
                                continue
                        if compType == 1:
                           print('Inside comp type =1')
                           for column in row:
                               if column not in (None,""):
                                  i=i+1
                                  if i%2 != 0:  
                                     nameAttribute=column
                                     nameAttribute=nameAttribute[:-1]
                                     print(nameAttribute)
                                  else:
                                     textValue=column
                                     print(textValue)
                                     ET.SubElement(component, "Metric",name=nameAttribute.strip()).text=textValue.strip()
                        elif compType == 2:
                                compLineNum = compLineNum+1
                                print('Inside comp type = 2')
                                if compLineNum == 1:
                                   colValue = []
                                   for column in row:
                                       if column not in (None,""):
                                          colValue.append(column)
                                   print(colValue)
                                else:
                                     rowValue=[]
                                     for column in row:
                                         if column not in (None,""):
                                           rowValue.append(column)
                                     print(rowValue)
                                     if len(rowValue) != 0:
                                        if len(rowValue) == (len(colValue)+1):
                                             print('Can be added in xml')
                                             for i,val in enumerate(rowValue):
                                                 if i==0:
                                                    continue
                                                 else:
                                                    nameAttribute=(rowValue[0]+':'+colValue[i-1])
                                                    textValue=val
                                                    ET.SubElement(component, "Metric",name=nameAttribute.strip()).text=textValue
                                        else:
                                             nameAttribute=rowValue[0]
                                             textValue=rowValue[1]
                                             ET.SubElement(component, "Metric",name=nameAttribute.strip()).text=textValue
                                continue
                        elif compType == 3:
                                compLineNum = compLineNum+1
                                print('Inside comp type = 3')
                                if compLineNum == 1:
                                   colValue = []
                                   for column in row:
                                       if column not in (None,""):
                                          colValue.append(column)
                                   print(colValue)
                                else:
                                        rowValue=[]
                                        for column in row:
                                            if column not in (None,""):
                                               rowValue.append(column)
                                        print(rowValue)
                                        if len(rowValue) != 0: 
                                           if len(rowValue) == len(colValue):  
                                              print('Can be added in xml')
                                              metricId = metricId+1
                                              print(metricId)
                                              metric = ET.SubElement(component, "Metric",id=str(metricId))
                                              for i,val in enumerate(rowValue):
                                                  nameAttribute=colValue[i]
                                                  textValue=val
                                                  print(nameAttribute)
                                                  print(textValue)
                                                  ET.SubElement(metric, "SubMetric",name=nameAttribute).text=textValue
                                           else:
                                               nameAttribute=rowValue[0]
                                               textValue=rowValue[1]
                                               print(nameAttribute)
                                               print(textValue)
                                               ET.SubElement(component, "Metric",name=nameAttribute).text=textValue
                                               
csvfile.close()
tree = ET.ElementTree(root)
tree.write("xml1.xml")


