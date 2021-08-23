SSLazy SSL grader
=================

Run> python3 sslgrader.py <domain>

To-do: add argument checking, element sanitisation.    
       
On Github, there are many SSLLab API SSL grading scripts and independent SSL checker scripts. But all of them (as of Jan 2021) do not cover TLS 1.3 grading. Hence the born of this SSL grading script. Feeding JSON is a piece of cake, just ingest the JSON to Manager like JQ and cherrypick what you need. Rather this script goes for VERBOSE scrapping with REGEX element parsing instead, adding another edge over what is already seen on Github primarily SSLAB API JSON.

Design 
       
          Script \____________________________ SSLyse <----- Website SSL info
                                                             
              |____ciphersuite.info TLS info
                                                             
              |____ (open to extension e.g. SSLLAB JSON API)
              
    
This is based on SSLyze 4.1.0 with ciphersuite.info API - https://ciphersuite.info/cs/?singlepage=true

Files

SSLazy SSL grader
=================

Run> python3 sslgrader.py <domain>

To-do: add argument checking, element sanitisation.    
       
On Github, there are many SSLLab API SSL grading scripts and independent SSL checker scripts.
But all of them (as of Jan 2021) do not cover TLS 1.3 grading. Hence the born of this SSL scripts.
Feeding JSON is a piece of cake, just ingest the JSON to JQ and cherrypick what you need. This script can easily add this.
Rather this script goes for VERBOSE scrapping with REGEX element parsing instead, this will give another edge over what is already seen on Github (primariy SSLAB API JSON)

Design 
       
          Script \____________________________ SSLyse <----- Website SSL info
                                                             
              |____ciphersuite.info TLS info
                                                             
              |____ (open to extension e.g. SSLLAB JSON API)
              
    
This is based on SSLyze 4.1.0 with ciphersuite.info API - https://ciphersuite.info/cs/?singlepage=true

Files
1.     ciphersuite-mapping.py - Test Puller script for ciphersuite.info
2.     ciphersuite-scoring.py - Test Mapping script for ciphersuite.info
3.     ciphersuite-mapping.data_2021Aug - a data sample
4.     data.txt - a save copied of ciphersuite.info data with curl
5.     sslgrader.py - the SSL grading script.
                                                             
    
100% grading consists of 3 scoring sections and 1 non-scoring issue checker section.

1.	Certificate amount to 30% maximum out of 100%
    Pass will get 30%, failed is 0%

2.	Protocol Support amount to 30% maximum out of 100%
    TLS1.3 and TLS1.2 both will get 30%, only TLS1.3 will get 20%
    Older protocols such as TLS1.0 or SSLv3 will get -15%
  
3.	Cipher Suite (with Key Exchange) amount to 40% maximum out of 100%
    Secure status will get 40% 
    Recommended status will get 30% 
    Weak status will get 20%
    Insecure status will get -100%

4.	Known Issue detection amount to immediate failure amount to -199% out of 100%
    robot             	Test a server for the ROBOT vulnerability.
    openssl_ccs       Test a server for the OpenSSL CCS Injection
                       	 vulnerability (CVE-2014-0224).
    heartbleed        Test a server for the OpenSSL Heartbleed
                        	vulnerability.
    fallback          Test a server for the TLS_FALLBACK_SCSV mechanism to
                        prevent downgrade attacks
    reneg             Test a server for for insecure TLS renegotiation and
                        client-initiated renegotiation.

Scoring table
Excellent = 100% 
A	   >= 80%
B	   >= 70% 
C	   >= 50%
F 	   < 50%

Test Case 1 for A
Certificate PASSED, Protocol Support TLS 1.2 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 80% 

Test Case 2 for A
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 90% 

Test Case 3 for B 
Certificate FAILED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 30% + Cipher Suite = 40% :: Total = 70% 

Test Case 4 for C 
Certificate FAILED, Protocol Support TLS 1.3 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 50% 

Test Case 5 for F 
Certificate FAILED, Protocol Support TLS 1.0 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 0% + Cipher Suite = 40% :: Total = 40% 

Test Case 6 for – 
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has insecure status.
Certificate = 30% + Protocol Support = 30% + Cipher Suite = -100% :: Total = -40% 

Test Case 7 for Excellent 
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 30% + Cipher Suite = 40% :: Total = 100% 

Output
======

kali@kali:~/Downloads/sslyze$ python3 sslgrader.py www.google.com
www.google.com
<<< Start SSL Grading <<<
Certificate integrity OK
TLS13 OK
TLS12 OK
Older SSL/TLS Found
Vulnerable Issue Not Found
<<< End SSL Grading <<<
>>>Start Computing score>>>
Certificate score is: 30
TLS support score is: 15
TLS discount score is: 0
Cipher Suite score is: 20
>>>Total SSL grade for  www.google.com  is  65 /100. Grade is  C . >>>

kali@kali:~/Downloads/sslyze$ python3 sslgrader.py www.ocbc.com
www.ocbc.com
<<< Start SSL Grading <<<
Certificate integrity OK
TLS13 OK
TLS12 OK
Older SSL/TLS Not Found
Vulnerable Issue Not Found
<<< End SSL Grading <<<
>>>Start Computing score>>>
Certificate score is: 30
TLS support score is: 30
TLS discount score is: 0
Cipher Suite score is: 30
>>>Total SSL grade for  www.ocbc.com  is  90 /100. Grade is  A . >>>


                                                             
    
100% consists of 3 scoring sections and 1 non-scoring issue checker section.

1.	Certificate amount to 30% maximum out of 100%
    Pass will get 30%, failed is 0%

2.	Protocol Support amount to 30% maximum out of 100%
    TLS1.3 and TLS1.2 both will get 30%, only TLS1.3 will get 20%
    Older protocols such as TLS1.0 or SSLv3 will get -15%
  
3.	Cipher Suite (with Key Exchange) amount to 40% maximum out of 100%
    Secure status will get 40% 
    Recommended status will get 30% 
    Weak status will get 20%
    Insecure status will get -100%

4.	Known Issue detection amount to immediate failure amount to -199% out of 100%
    robot             	Test a server for the ROBOT vulnerability.
    openssl_ccs       Test a server for the OpenSSL CCS Injection
                       	 vulnerability (CVE-2014-0224).
    heartbleed        Test a server for the OpenSSL Heartbleed
                        	vulnerability.
    fallback          Test a server for the TLS_FALLBACK_SCSV mechanism to
                        prevent downgrade attacks
    reneg             Test a server for for insecure TLS renegotiation and
                        client-initiated renegotiation.

Scoring table
Excellent = 100% 
A	   >= 80%
B	   >= 70% 
C	   >= 50%
F 	   < 50%

Test Case 1 for A
Certificate PASSED, Protocol Support TLS 1.2 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 80% 

Test Case 2 for A
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 90% 

Test Case 3 for B 
Certificate FAILED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 30% + Cipher Suite = 40% :: Total = 70% 

Test Case 4 for C 
Certificate FAILED, Protocol Support TLS 1.3 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 50% 

Test Case 5 for F 
Certificate FAILED, Protocol Support TLS 1.0 and Cipher Suite has secure status.
Certificate = 0% + Protocol Support = 0% + Cipher Suite = 40% :: Total = 40% 

Test Case 6 for – 
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has insecure status.
Certificate = 30% + Protocol Support = 30% + Cipher Suite = -100% :: Total = -40% 

Test Case 7 for Excellent 
Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
Certificate = 30% + Protocol Support = 30% + Cipher Suite = 40% :: Total = 100% 

Output
======

kali@kali:~/Downloads/sslyze$ python3 sslgrader.py www.google.com
www.google.com
<<< Start SSL Grading <<<
Certificate integrity OK
TLS13 OK
TLS12 OK
Older SSL/TLS Found
Vulnerable Issue Not Found
<<< End SSL Grading <<<
>>>Start Computing score>>>
Certificate score is: 30
TLS support score is: 15
TLS discount score is: 0
Cipher Suite score is: 20
>>>Total SSL grade for  www.google.com  is  65 /100. Grade is  C . >>>

kali@kali:~/Downloads/sslyze$ python3 sslgrader.py www.ocbc.com
www.ocbc.com
<<< Start SSL Grading <<<
Certificate integrity OK
TLS13 OK
TLS12 OK
Older SSL/TLS Not Found
Vulnerable Issue Not Found
<<< End SSL Grading <<<
>>>Start Computing score>>>
Certificate score is: 30
TLS support score is: 30
TLS discount score is: 0
Cipher Suite score is: 30
>>>Total SSL grade for  www.ocbc.com  is  90 /100. Grade is  A . >>>


SSLyze
======

![Run Tests](https://github.com/nabla-c0d3/sslyze/workflows/Run%20Tests/badge.svg)
[![Downloads](https://pepy.tech/badge/sslyze)](https://pepy.tech/badge/sslyze)
[![PyPI version](https://img.shields.io/pypi/v/sslyze.svg)](https://pypi.org/project/sslyze/)
[![Python version](https://img.shields.io/pypi/pyversions/sslyze.svg)](https://pypi.org/project/sslyze/)

SSLyze is a fast and powerful SSL/TLS scanning library.

It allows you to analyze the SSL/TLS configuration of a server by connecting to it, in order to detect various
issues (bad certificate, weak cipher suites, Heartbleed, ROBOT, TLS 1.3 support, etc.).

SSLyze can either be used as a command line tool or as a Python library.

Key features
------------

* Fully [documented Python API](https://nabla-c0d3.github.io/sslyze/documentation/), in order to run scans and process 
the results directly from Python.
* Support for TLS 1.3 and early data (0-RTT) testing.
* Scans are automatically dispatched among multiple workers, making them very fast.
* Performance testing: session resumption and TLS tickets support.
* Security testing: weak cipher suites, supported curves, ROBOT, Heartbleed and more.
* Server certificate validation and revocation checking through OCSP stapling.
* Support for StartTLS handshakes on SMTP, XMPP, LDAP, POP, IMAP, RDP, PostGres and FTP.
* Scan results can be written to a JSON file for further processing.
* And much more!

Quick start
-----------

SSLyze can be installed directly via pip:

    $ pip install --upgrade setuptools pip
    $ pip install --upgrade sslyze
    $ python -m sslyze www.yahoo.com www.google.com "[2607:f8b0:400a:807::2004]:443"

Documentation
-------------

Documentation is [available here][documentation].

License
-------
SSLazy SSL grader - Copyright (c) 2021 qTIbqT95oKqurzqyozuaoz9cqTqhoj==
       
SSLyse - Copyright (c) 2021 Alban Diquet
SSLyze is made available under the terms of the GNU Affero General Public License (AGPL). See LICENSE.txt for details and exceptions.     
[documentation]: https://nabla-c0d3.github.io/sslyze/documentation
