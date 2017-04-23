Deployment instructions for Apache Zeppelin & Spark usinng Ansible.

Prerequisites: Python, ChameleonCloud Client, Ansible, IPy (Python package)

OS: Ubuntu

Download all the files.

USING MULTIPLE FLOATING IPs

1) Set current directory to Zeppelin
2) Generate passwordless SSH named spark_rsa in cd. 
2) Launch az.py using command "python az.py"
3) set user id (chameleon or jetstream user id), cloud (chameleon or jetstream) and cloud user (cc for chameleon and ubuntu for jetstream)
   Example (jetstream):
   >> setUserId nramaraj
   >> setCloud jetstream
   >> setCloudUser ubuntu

   Example (chameleon)
   >> setUserId nramaraj
   >> setCloud chameleon
   >> setCloudUser cc
4) now mention numer of nodes and start using boot
   Example: boot 3

Now 3 nodes will boot and will give master nodes
Enter ansible vault password to decrypt and yes if StrictHostKeyChecking is enabled.
In a browser, Launch Zeppelin from http://masterip:8080 and spark ui from port 8082

USING SINGLE FLOATING IPs
1) Boot vm with floating IP and ports 8080 to 8085 open
2) Get files from git hub.
3) Set current directory to Zeppelin
4) Launch az.py using command "python az.py"
5) set master ip, user id (chameleon or jetstream user id), cloud (chameleon or $
   Example (jetstream):
   >> setMasterIp 192.168.1.5
   >> setUserId nramaraj
   >> setCloud jetstream
   >> setCloudUser ubuntu

   Example (chameleon)
   >> setMasterIp 192.168.1.5
   >> setUserId nramaraj
   >> setCloud chameleon
   >> setCloudUser cc
   
  The master ip is static ip of the current machine.

4) now mention numer of nodes and start using boot
   Example: boot 3

   Now 3 slave nodes will boot and install in current master node

Enter ansible vault password to decrypt and yes if StrictHostKeyCheck is enabled.

In a browser, Launch Zeppelin from http://masterip:8080 and spark ui in port 8082

Use help for additional information. 

Other important commands are startSpark, startZeppelin, stopSpark and stopZeppelin

   
