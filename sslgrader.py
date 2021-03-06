import sys
import subprocess
import re
import os

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
banner = ""

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
    global banner
    outputfile += stdoutcertdata

    global cert_score
    if re.search("FAILED", stdoutcertdata):
        print('Certificate FAILED')
        banner += "Certificate FAILED\n"
        cert_score = -30
    else:
        print('Certificate integrity OK')
        banner += "Certificate integrity OK\n"
        cert_score = 30

    stdoutTLS13data = subprocess.getoutput(python_version + " -m sslyze --tlsv1_3 " + webdomain)
    #print(stdoutTLS13data)
    outputfile += stdoutTLS13data
    gTLS += (findTLS(stdoutTLS13data))

    global TLS_support_score
    if re.search("The server accepted the", stdoutTLS13data):
        print('TLS13 OK')
        banner += "TLS13 OK\n"
        TLS_support_score += 20
    else:
        print('TLS13 Not Found')
        banner += "TLS13 Not Found\n"

    stdoutTLS12data = subprocess.getoutput(python_version + " -m sslyze --tlsv1_2 " + webdomain)
    #print(stdoutTLS12data)
    outputfile += stdoutTLS12data
    gTLS += (findTLS(stdoutTLS12data))

    if re.search("The server accepted the", stdoutTLS12data):
        print('TLS12 OK')
        banner += "TLS12 OK\n"
        TLS_support_score += 10
    else:
        print('TLS12 Not Found')
        banner += "TLS12 Not Found\n"

    stdoutTLSOtherdata = subprocess.getoutput(python_version + " -m sslyze --sslv3 --sslv2 --tlsv1 --tlsv1_1 " + webdomain)
    #print(stdoutTLSOtherdata)
    outputfile += stdoutTLSOtherdata
    gTLS += (findTLS(stdoutTLSOtherdata))

    if re.search("The server accepted the", stdoutTLSOtherdata):
        print('Older SSL/TLS Found')
        banner += "Older SSL/TLS Found\n"
        TLS_support_score += -15
    else:
        print('Older SSL/TLS Not Found')
        banner += "Older SSL/TLS Not Found\n"

    stdoutDISdata = subprocess.getoutput(python_version + " -m sslyze --robot --openssl_ccs --heartbleed --fallback --reneg  " + webdomain)
    #print(stdoutDISdata)
    outputfile += stdoutDISdata

    global discount_score
    if re.search("VULNERABLE", stdoutDISdata):
        print('Vulnerable Issue Found')
        banner += "Vulnerable Issue Found\n"
        discount_score += -199
    else:
        print('Vulnerable Issue Not Found')
        banner += "Vulnerable Issue Not Found\n"

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
banner = "<<< Start SSL Grading <<<\n" + banner
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

print("<<< End SSL Grading <<<")
banner += "<<< End SSL Grading <<<\n"
total_score = cert_score + TLS_support_score + discount_score + ciphersuite_keyex_strength_score
banner1 = ">>>Start Computing score>>>" \
             + "\nCertificate score is:" +  str(cert_score) \
             + "\nTLS support score is:" + str(TLS_support_score) \
             + "\nTLS discount score is:" + str(discount_score) \
             + "\nCipher Suite score is:" + str(ciphersuite_keyex_strength_score) \
             + "\n>>>Total SSL grade for " + str(sys.argv[1]) + " is " + str(total_score) + "/100. Grade is " + determine_grade(int(total_score)) + ". >>>\n"

print(banner1)

try:
    os.makedirs('results')
except OSError as e:
    pass


#subprocess.getoutput("echo \"" + banner + "\" > results\/" + str(sys.argv[1]) + ".txt")
#subprocess.getoutput("echo \"" + banner1 + "\" >> results\/" + str(sys.argv[1]) + ".txt")
#subprocess.getoutput("echo \"" + str(outputfile) + "\" >> results\/" + str(sys.argv[1]) + ".txt")
#print(outputfile)

new_path = "results/" + str(sys.argv[1]) + ".txt"
new_handler = open(new_path,'w')
new_handler.write(banner + banner1 + outputfile)
new_handler.close()
print(banner + banner1 + outputfile)

#stdoutML_CSV = subprocess.getoutput("echo \"" \
#                                         + str(sys.argv[1]) + "," \
#                                         + determine_grade(int(total_score)) + "," \
#                                         + str(total_score) + "," \
#                                         + str(cert_score) + "," \
#                                         + str(TLS_support_score) + "," \
#                                         + str(discount_score) + "," \
#                                         + str(ciphersuite_keyex_strength_score) \
#                                         + "\" >> SSLayzeSummary.txt" \
#                                    )

new_path = "SSLayzeSummary.txt"
new_handler = open(new_path,'a')
new_handler.write(str(sys.argv[1]) + "," \
		+ determine_grade(int(total_score)) + "," \
		+ str(total_score) + "," \
		+ str(cert_score) + "," \
                + str(TLS_support_score) + "," \
                + str(discount_score) + "\n" \
                )

new_handler.close()

