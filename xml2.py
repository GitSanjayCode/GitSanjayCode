import csv
import xml.etree.cElementTree as ET

root = ET.Element("root")
testcase = ET.SubElement(root, "TestCase")
with open('xml2.csv','r') as csvfile:
    csvreader = csv.reader(csvfile)
    lineNum = 0
    attribute = []
    testdata = []
    for row in csvreader:
        if not ''.join(row).strip():
            print('Empty Line')
            continue
        else:
            lineNum = lineNum+1
            if lineNum == 1:
               attribute=row
               print(attribute)
            else:
               testdata=row
               if(len(testdata) != 0):
                  print('Inside')
                  print(testdata)
                  for i,val in enumerate(testdata):
                      nameAttribute=attribute[i]
                      textValue=val
                      ET.SubElement(testcase, "Metric",name=nameAttribute).text=textValue

csvfile.close()       
tree = ET.ElementTree(root)
tree.write("xml2.xml")
