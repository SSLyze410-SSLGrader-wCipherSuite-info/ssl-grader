SSLazy SSL grader
=================

Run> python3 sslgrader.py #www.example.com# (on Kali only)

To-do: add Windows support ,argument checking, threading, element sanitisation ,more error checking/controls (good enough to run) 

       
On Github, there are many SSLLab API SSL grading scripts and independent SSL checker scripts.
But all of them (as of Q2 2021) do not cover TLS 1.3 grading. Hence the born of this SSL scripts.
Feeding JSON is a piece of cake, just ingest the JSON to JQ and cherrypick what you need. This script can easily add this.
Rather this script goes for VERBOSE scrapping, wrapping with REGEX element parsing instead, this will give another edge over what is already seen on Github (primarily SSLAB API JSON)


Design
======  
          Script (wrapping)
              |   \____________________________ SSLyse <----- Website SSL info
               (wrapping)                                               
              |____ciphersuite.info TLS info
              (json)                                               
              |____ (open to extension e.g. SSLLAB JSON API)
              
    
This is based on SSLyze 4.1.0 with ciphersuite.info API - https://ciphersuite.info/cs/?singlepage=true


Files
=====
1.     ciphersuite-mapping.py - Test Puller script for ciphersuite.info
2.     ciphersuite-scoring.py - Test Mapping script for ciphersuite.info
3.     ciphersuite-mapping.data_2021Aug - a data sample
4.     data.txt - a save copied of ciphersuite.info data with curl
5.     sslgrader.py - the SSL grading script.
                                                             
    
100% grading consists of 3 scoring sections (1 to 3) and 1 non-scoring issue checker section.
=============================================================================================
1.	       Certificate amount to 30% maximum out of 100%
              Pass will get 30%, failed is 0%

2.	       Protocol Support amount to 30% maximum out of 100%
              TLS1.3 and TLS1.2 both will get 30%, only TLS1.3 will get 20%
              Older protocols such as TLS1.0 or SSLv3 will get -15% discount factor
  
3.	       Cipher Suite (with Key Exchange) amount to 40% maximum out of 100%
              Secure status will get 40% 
              Recommended status will get 30% 
              Weak status will get 20%
              Insecure status will get -100% discount factor

4.	       Known Issue detection amount to immediate failure amount to -199% out of 100%
              robot             Test a server for the ROBOT vulnerability.
              openssl_ccs       Test a server for the OpenSSL CCS Injection vulnerability (CVE-2014-0224).
              heartbleed        Test a server for the OpenSSL Heartbleed vulnerability.
              fallback          Test a server for the TLS_FALLBACK_SCSV mechanism to prevent downgrade attacks.  
              reneg             Test a server for for insecure TLS renegotiation and client-initiated renegotiation.


Total score = part 1(30%) + part 2(30%) + part 3(60%) + part 4 (discount percentage -199% if found)

Scoring table
=============
       Excellent = 100% 
       A	   >= 80%
       B	   >= 70% 
       C	   >= 50%
       F 	   < 50%


Test Case 1 for A Grade
=======================
       Certificate PASSED, Protocol Support TLS 1.2 and Cipher Suite has secure status.
       Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 80% 

Test Case 2 for A Grade
=======================
       Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
       Certificate = 30% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 90% 

Test Case 3 for B Grade
=======================
       Certificate FAILED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has secure status.
       Certificate = 0% + Protocol Support = 30% + Cipher Suite = 40% :: Total = 70% 

Test Case 4 for C Grade
=======================
       Certificate FAILED, Protocol Support TLS 1.3 and Cipher Suite has secure status.
       Certificate = 0% + Protocol Support = 10% + Cipher Suite = 40% :: Total = 50% 

Test Case 5 for F Grade
=======================
       Certificate FAILED, Protocol Support TLS 1.0 and Cipher Suite has secure status.
       Certificate = 0% + Protocol Support = 0% + Cipher Suite = 40% :: Total = 40% 

Test Case 6 for F Grade
=======================
       Certificate PASSED, Protocol Support TLS 1.2 and TLS 1.3 and Cipher Suite has insecure status.
       Certificate = 30% + Protocol Support = 30% + Cipher Suite = -100% :: Total = -40% 

Test Case 7 for Excellent
=========================
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


       kali@kali:~/Downloads/sslyze$ python3 sslgrader.py www.bankofchina.com
       www.bankofchina.com
       <<< Start SSL Grading <<<
       Certificate integrity OK
       TLS13 Not Found
       TLS12 OK
       Older SSL/TLS Found
       Vulnerable Issue Found
       <<< End SSL Grading <<<
       >>>Start Computing score>>>
       Certificate score is:30
       TLS support score is:-5
       TLS discount score is:-199
       Cipher Suite score is:20
       >>>Total SSL grade for www.bankofchina.com is -154/100. Grade is F. >>>

Detail Result
=============
Go to results/#domain#.txt, all executed detail reports are saved in this folder.
Manually purge results/#domain#.txt files as needed, script will only append data to it.

Example Detail Report - www.bankofchina.com
       
       kali@kali:~/Downloads/sslyze$ cat results/www.bankofchina.com.txt
       <<< Start SSL Grading <<<
       Certificate integrity OK
       TLS13 Not Found
       TLS12 OK
       Older SSL/TLS Found
       Vulnerable Issue Found
       <<< End SSL Grading <<<

       >>>Start Computing score>>>
       Certificate score is:30
       TLS support score is:-5
       TLS discount score is:-199
       Cipher Suite score is:20
       >>>Total SSL grade for www.bankofchina.com is -154/100. Grade is F. >>>

       CHECKING HOST(S) AVAILABILITY
 
       www.bankofchina.com:443                       => 123.124.191.45

       SCAN RESULTS FOR WWW.BANKOFCHINA.COM:443 - 123.124.191.45

       * Certificates Information:
        Hostname sent for SNI:             www.bankofchina.com
        Number of certificates detected:   1
       
       Certificate #0 ( _RSAPublicKey )
        SHA1 Fingerprint:                  24e635c8dbb7783ba9232285eaa58ec4895ee6c1
        Common Name:                       www.bankofchina.com
        Issuer:                            Secure Site Pro Extended Validation CA G2
        Serial Number:                     20984255454740395246010106896176242556
        Not Before:                        2019-11-26
        Not After:                         2021-11-26
        Public Key Algorithm:              _RSAPublicKey
        Signature Algorithm:               sha256
        Key Size:                          2048
        Exponent:                          65537
        DNS Subject Alternative Names:     ['www.bankofchina.com']

       Certificate #0 - Trust
        Hostname Validation:               OK - Certificate matches server hostname
        Android CA Store (9.0.0_r9):       OK - Certificate is trusted
        Apple CA Store (iOS 14, iPadOS 14, macOS 11, watchOS 7, and tvOS 14):OK - Certificate is trusted
        Java CA Store (jdk-13.0.2):        OK - Certificate is trusted
        Mozilla CA Store (2021-01-24):     OK - Certificate is trusted, Extended Validation
        Windows CA Store (2021-02-08):     OK - Certificate is trusted
        Symantec 2018 Deprecation:         OK - Not a Symantec-issued certificate
        Received Chain:                    www.bankofchina.com --> Secure Site Pro Extended Validation CA G2
        Verified Chain:                    www.bankofchina.com --> Secure Site Pro Extended Validation CA G2 --> DigiCert High Assurance EV Root CA
        Received Chain Contains Anchor:    OK - Anchor certificate not sent
        Received Chain Order:              OK - Order is valid
        Verified Chain contains SHA1:      OK - No SHA1-signed certificate in the verified certificate chain

      Certificate #0 - Extensions
        OCSP Must-Staple:                  NOT SUPPORTED - Extension not found
        Certificate Transparency:          OK - 3 SCTs included

      Certificate #0 - OCSP Stapling
                                          NOT SUPPORTED - Server did not send back an OCSP response

      * TLS 1.3 Cipher Suites:
       Attempted to connect using 5 cipher suites; the server rejected all cipher suites.

      * TLS 1.2 Cipher Suites:
       Attempted to connect using 156 cipher suites.

      The server accepted the following 4 cipher suites:
         TLS_RSA_WITH_AES_256_CBC_SHA                      256
         TLS_RSA_WITH_AES_128_CBC_SHA                      128
         TLS_RSA_WITH_3DES_EDE_CBC_SHA                     168
         TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256             128       ECDH: prime256v1 (256 bits)

       The group of cipher suites supported by the server has the following properties:
        Forward Secrecy                    OK - Supported
        Legacy RC4 Algorithm               OK - Not Supported

       * TLS 1.1 Cipher Suites:
       Attempted to connect using 80 cipher suites.

       The server accepted the following 3 cipher suites:
         TLS_RSA_WITH_AES_256_CBC_SHA                      256
         TLS_RSA_WITH_AES_128_CBC_SHA                      128
         TLS_RSA_WITH_3DES_EDE_CBC_SHA                     168

       The group of cipher suites supported by the server has the following properties:
        Forward Secrecy                    INSECURE - Not Supported
        Legacy RC4 Algorithm               OK - Not Supported

       * TLS 1.0 Cipher Suites:
       Attempted to connect using 80 cipher suites.

       The server accepted the following 3 cipher suites:
         TLS_RSA_WITH_AES_256_CBC_SHA                      256
         TLS_RSA_WITH_AES_128_CBC_SHA                      128
         TLS_RSA_WITH_3DES_EDE_CBC_SHA                     168

       The group of cipher suites supported by the server has the following properties:
         Forward Secrecy                    INSECURE - Not Supported
         Legacy RC4 Algorithm               OK - Not Supported

       * SSL 3.0 Cipher Suites:
       Attempted to connect using 80 cipher suites; the server rejected all cipher suites.

       * SSL 2.0 Cipher Suites:
        Attempted to connect using 7 cipher suites; the server rejected all cipher suites.
 
       * ROBOT Attack:
                                           VULNERABLE - Strong oracle, a real attack is possible.

       * OpenSSL Heartbleed:
                                           OK - Not vulnerable to Heartbleed

       * Downgrade Attacks:
        TLS_FALLBACK_SCSV:                 OK - Supported

       * Session Renegotiation:
        Client Renegotiation DoS Attack:   OK - Not vulnerable
        Secure Renegotiation:              OK - Supported

       * OpenSSL CCS Injection:
                                           OK - Not vulnerable to OpenSSL CCS injection


Machine Learning
================
SSLayzeSummary.txt is created in Parent folder to arrange the data into comma separated values (CSV) for ML such as Weka.
Manually purge SSLayzeSummary.txt as needed, script will only append data to it.

       kali@kali:~/Downloads/sslyze$ cat SSLayzeSummary.txt
       www.ocbc.com,A,90,30,30,0,30
       www.bankofchina.com,F,-154,30,-5,-199,20
       test-dv-rsa.ssl.com,F,5,-30,15,0,20
       expired-ecc-ev.ssl.com,F,5,-30,15,0,20

       CSV Schema                                 
       1. Domain
       2. Grade
       3. Total Score
       4. Certificate Score
       5. TLS Support Score
       6. Discount Score
       7. Cipher Suite i.e. Key Exchange, Bits strenght score
 

Researcher
==========
Planning to use this grading script for massive scrapping / web crawlering exercise? If so, please pinned the ciphersuite.info lookup data to a file instead of curl lookup. Or else I will foresee ratelimiting similar to SSLlab API applied by ciphersuite.info. ***WARNING*** Play nice.

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

Donation to Crypto Wallet
-------------------------
Developer need to eat too.

       ETH    0x7759366012ba41039a8d9aa7f4240b2c1423eea7
       USDT   0x7759366012ba41039a8d9aa7f4240b2c1423eea7
       BTC    1FS14XSENZwZqEfLKp1bGN39Xj9FoEBPSg
       BNB    bnb136ns6lfw4zs5hg4n85vdthaad7hq5m4gtkgf23, BNB Memo 386821235
