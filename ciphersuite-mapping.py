import re

with open ("data.txt", "r") as myfile:
    data=myfile.read()
	
#print(data)
regex = re.compile(r"<li><a class=\"long-string\" href=\"\/cs\/(.*)\/\">\n                    <span class=\"badge bg-fixed-width bg-.*\">(.*)</span>", re.MULTILINE)
matches = [m.groups() for m in regex.finditer(data)]

for m in matches:
    print("Cipher Suite Name: %s Status: %s" % (m[0], m[1]))
#print(m.group(1))
