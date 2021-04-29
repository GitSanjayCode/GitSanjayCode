import xml.etree.ElementTree as ET

tree1 = ET.parse('xml1.xml')
tree2 = ET.parse('xml2.xml')

root1 = tree1.getroot()
root2 = tree2.getroot()

print(root1.findtext("./Component[@name='Final Statement']/Metric[@name='Emp Sid']"))
print(root1.findtext("./Component[@name='HR Practical Data']/Metric[@id='2']/SubMetric[@name='Loan3']"))

if (root1.findtext("./doc[@name='Component']/field1[@name='eno']") == root2.findtext("./Component/Metric[@name='asdfasd']")):
    print('Matched')
