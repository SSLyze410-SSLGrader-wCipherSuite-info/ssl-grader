import sys
import subprocess
import re

python_version="/usr/bin/python3.9"
cert_score = 0
TLS_support_score = 0
discount_score = 0
ciphersuite_keyex_strength_score = 0
total_score = 0
gDIC = {}
aDIC = {}
gTLS = []
webdomain = ""
outputfile = ""

def main():
    # print command line arguments
    for arg in sys.argv[1:]:
        print(arg)

if __name__ == "__main__":
    main()

def populateCipherSuiteDictionary(gDIC):
    stdoutCURLdata = subprocess.getoutput("curl -v https://ciphersuite.info/cs/?singlepage=true > data.txt")

    with open ("data.txt", "r") as myfile:
        data=myfile.read()

    #print(data)
    regex = re.compile(r"<li><a class=\"long-string\" href=\"\/cs\/(.*)\/\">\n                    <span class=\"badge bg-fixed-width bg-.*\">(.*)</span>", re.MULTILINE)
    matches = [m.groups() for m in regex.finditer(data)]

    #fd = {}
    for m in matches:
        stren = 0
        if re.match("Secure",m[1]):
            stren = 0

        if re.match("Recommended",m[1]):
            stren = -10

        if re.match("Weak",m[1]):
            stren = -20

        if re.match("Insecure",m[1]):
            stren = -110

        #print("Cipher Suite Name: %s Score: %s" % (m[0], stren))
        key = m[0]
        val = stren
        gDIC[key] = int(val)

    #print DICTIONARY with respective discount values
    #print(fd)
    return gDIC

def findTLS(stdout):
    matched = re.findall(r"\s+(TLS\S+)\s+\d+", stdout, re.MULTILINE)
    #print(matched)
    return(matched)

def sslyzeDomain(webdomain, gTLS):
    stdoutcertdata = subprocess.getoutput(python_version + " -m sslyze --certinfo " + webdomain)
    #print(stdoutcertdata)
    global outputfile
    outputfile += stdoutcertdata

    global cert_score
    if re.search("FAILED", stdoutcertdata):
        print('Certificate FAILED')
        cert_score = -30
    else:
        print('Certificate integrity OK')
        cert_score = 30

    stdoutTLS13data = subprocess.getoutput(python_version + " -m sslyze --tlsv1_3 " + webdomain)
    #print(stdoutTLS13data)
    outputfile += stdoutTLS13data
    gTLS += (findTLS(stdoutTLS13data))

    global TLS_support_score
    if re.search("The server accepted the", stdoutTLS13data):
        print('TLS13 OK')
        TLS_support_score += 20
    else:
        print('TLS13 Not Found')

    stdoutTLS12data = subprocess.getoutput(python_version + " -m sslyze --tlsv1_2 " + webdomain)
    #print(stdoutTLS12data)
    outputfile += stdoutTLS12data
    gTLS += (findTLS(stdoutTLS12data))

    if re.search("The server accepted the", stdoutTLS12data):
        print('TLS12 OK')
        TLS_support_score += 10
    else:
        print('TLS12 Not Found')

    stdoutTLSOtherdata = subprocess.getoutput(python_version + " -m sslyze --sslv3 --sslv2 --tlsv1 --tlsv1_1 " + webdomain)
    #print(stdoutTLSOtherdata)
    outputfile += stdoutTLSOtherdata
    gTLS += (findTLS(stdoutTLSOtherdata))

    if re.search("The server accepted the", stdoutTLSOtherdata):
        print('Older SSL/TLS Found')
        TLS_support_score += -15
    else:
        print('Older SSL/TLS Not Found')

    stdoutDISdata = subprocess.getoutput(python_version + " -m sslyze --robot --openssl_ccs --heartbleed --fallback --reneg  " + webdomain)
    #print(stdoutDISdata)
    outputfile += stdoutDISdata

    global discount_score
    if re.search("VULNERABLE", stdoutDISdata):
        print('Vulnerable Issue Found')
        discount_score += -199
    else:
        print('Vulnerable Issue Not Found')

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

def determine_grade(scores):
    if scores == 100:
        return 'Excellent'
    elif scores >= 80 and scores <= 99:
        return 'A'
    elif scores >= 70 and scores <= 79:
        return 'B'
    elif scores >= 50 and scores <= 69:
        return 'C'
    else:
        return 'F'

print("<<< Start SSL Grading <<<")
#print(populateCipherSuiteDictionary(gDIC))
populateCipherSuiteDictionary(gDIC)
sslyzeDomain(str(sys.argv[1]), gTLS)
#print(gTLS)

for k, v in gDIC.items():
    if k in gTLS:
        #print(k)
        append_value(aDIC, k, v)

# PRINT out the temp DICTIONARY used to store the pull TLS scoring
#print(aDIC)

# Using min() + list comprehension + values()
# Finding min value keys in dictionary

#ciphersuite_keyex_strength_score = min(aDIC.values())
#print(ciphersuite_keyex_strength_score)

try:
    ciphersuite_keyex_strength_score = min(aDIC.values())
except:
    ciphersuite_keyex_strength_score = -99

ciphersuite_keyex_strength_score = 40 + ciphersuite_keyex_strength_score

total_score = cert_score + TLS_support_score + discount_score + ciphersuite_keyex_strength_score
print("<<< End SSL Grading <<<\n>>>Start Computing score>>>")
print("Certificate score is:", cert_score)
print("TLS support score is:", TLS_support_score)
print("TLS discount score is:", discount_score)
print("Cipher Suite score is:", ciphersuite_keyex_strength_score)
print(">>>Total SSL grade for ",str(str(sys.argv[1]))," is ",total_score,"/100. Grade is ", determine_grade(int(total_score)),". >>>")

print("",outputfile)
