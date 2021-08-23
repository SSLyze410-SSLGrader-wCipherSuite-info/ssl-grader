import re

with open ("data.txt", "r") as myfile:
    data=myfile.read()
	
#print(data)
regex = re.compile(r"<li><a class=\"long-string\" href=\"\/cs\/(.*)\/\">\n                    <span class=\"badge bg-fixed-width bg-.*\">(.*)</span>", re.MULTILINE)
matches = [m.groups() for m in regex.finditer(data)]

for m in matches:
    stren = 0
    if re.match("Secure",m[1]):
        stren = 40

    if re.match("Recommended",m[1]):
        stren = 30

    if re.match("Weak",m[1]):
        stren = -100

    if re.match("Insecure",m[1]):
        stren = -110

    print("Cipher Suite Name: %s Score: %s" % (m[0], stren))
#print(m.group(1))
