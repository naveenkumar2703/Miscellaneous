import time
from cloudmesh_client.common.Shell import Shell
from write2files import HostsWriter
from IPy import IP
import cmd
import os, sys
import getpass
import time

class VMS(cmd.Cmd):
    def setup(self, cloud="chameleon", user='cc'):

        self.cloud = 'cloud='+cloud
        self.cloudUser = user
        print "Ignore Error: \n Please define a key first, e.g.: cm key add --ssh <keyname> \n " \
              "-- If key has been successfully added into the database and uploaded into the cloud \n" \
              "Ignore Error: \n problem uploading key veera to cloud chameleon: Key pair 'veera' already exists.\n " \
              "******************************************************************************************************"
        # result = Shell.cm("reset")
        # print result
        # result = Shell.cm("key add --ssh")
        # print result
        # result = Shell.cm("key", "upload")
        # print result
        # result = Shell.cm("default", self.cloud)
        # print result
        # result = Shell.cm("refresh", "on")
        #print result

    def __init__(self):

        cmd.Cmd.__init__(self)
        self.prompt = '>> '
        self.n = 1
        self.floating_ip_list = []
        self.static_ip_list = []
        self.cloud = "cloud=chameleon"
        self.cloudUser = 'cc'
        self.assignIp = False
        self.masterIp = None
        self.userId = None
        # self.setup()

    def do_setCloud(self, cloud):

        self.cloud = "cloud=" + cloud
        self.setup(cloud=self.cloud)

    def do_setCloudUser(self, cloudUser):

        self.cloudUser = cloudUser

    def do_setAssignFloatingIp(self, assignIp):
        print 'floating ip is ' + str(assignIp)
        self.assignIp = assignIp

    def do_setUserId(self, userId):
        self.userId = userId
        print 'user id is set to '+ userId

    def do_setMasterIp(self, masterIp):
        self.masterIp = masterIp
        print 'master ip is set to '+ masterIp

    def do_boot(self, n):

        self.floating_ip_list = []
        self.static_ip_list = []
        try:

            for i in range(int(n)):
                floating_ip = None
                static_ip = None
                print "Starting to boot Virtual Machine : ", i + 1
                Shell.cm("vm", "boot --secgroup=naveen-def")
                if self.assignIp:
                    fip_result = Shell.cm("vm", "ip assign")  # floating IP
                    floating_ip = fip_result.split(' ')[-2][:-6]

                try:
                    if self.assignIp:
                        IP(floating_ip)
                    # the below cmd is the "cm vm ip show" as ip is not getting updated automatically in the DB
                        Shell.cm("vm", "ip assign")

                    n = 0
                    while n < 5 and i >= len(self.static_ip_list):
                        sip_info = Shell.cm("vm", "list")
                        lines = sip_info.split('\n')
                        for lin in lines:
                            if self.userId in lin:
                                items = lin.split('|')
                                static_ip = items[5].strip()
                                if static_ip not in self.static_ip_list and static_ip is not self.masterIp:
                                    self.static_ip_list.append(static_ip)
                                    break
                        print 'Sleeping for' + str(10 * n) + ' seconds as ip not assigned'
                        time.sleep(10 * n)
                        n += 1
                        if n > 4:
                            raise Exception('Unable to assign ips')


                except Exception as e:
                    print e
                    print "floating IP error encountered"
                    print "Stopping to create further VMs"
                    break

                self.floating_ip_list.append(floating_ip)


        except ValueError:

            self.help_boot()

        if len(self.floating_ip_list) == 0 and self.assignIp:

            print "No VMs created"

        else:

            print "Returning IPs of VMs created"
            print "Floating IPs list    :", self.floating_ip_list
            print "Static IPs list      :", self.static_ip_list
            print "wirting IPs to respective files ..."
            print 'VM user :', self.assignIp
            HW = HostsWriter()
            print self.static_ip_list
            HW.writeIPs(staticIPs=self.static_ip_list, floatingIPs=self.floating_ip_list,
                        ansible_ssh_user=self.cloudUser, floating_ip=self.assignIp, masterIp=self.masterIp)

            # starting ansible
            if os.path.exists(os.environ['HOME'] + '/.ssh/known_hosts'):
                os.remove(os.environ['HOME'] + '/.ssh/known_hosts')

            print "Running the ansible-playbook for zepplin"

            # taking password
            password = getpass.getpass("Enter ansible valut password: ")
            tempPassFile = open('.log.txt', 'w')
            tempPassFile.write(password)
            tempPassFile.close()
            startTime = time.time()
            if 'chameleon' in self.cloud:
                deployment_logs = os.popen(
                'ansible-playbook Zeppelin.yml -i hosts --vault-password-file .log.txt').read()
            else:
                deployment_logs = os.popen(
                    'ansible-playbook Zeppelin_jetstream.yml -i hosts --vault-password-file .log.txt').read()

            os.remove('.log.txt')
            endTime = time.time()

            totalDeployTime = endTime - startTime
            print "Time taken to depoly ", n, " virtual machines for zeppelin is ", totalDeployTime

            # writing logs
            tempDepLog = open('deployment_logs', 'w')
            tempDepLog.write(deployment_logs)
            tempDepLog.close()

            # checking logs
            deployment_logs_lines = deployment_logs.splitlines()

            wordList = []
            for line in deployment_logs_lines:
                words = line.split(' ')
                for word in words:
                    wordList.append(word)

            if "fatal" in wordList or '"Decryption' in wordList or "failed" in wordList or 'fatal:' in wordList:
                print "Check deployment logs for errors during deployment"
            else:
                print "Deployment Successful"

    def do_delete(self, names):

        names = str(names).split(' ')
        for name in names:
            delete_machine = "delete " + name
            print delete_machine
            result = Shell.cm("vm", delete_machine)
            print result

    def do_quit(self, arg):

        sys.exit(1)

    def do_getFloatingIPs(self):

        print "Floating IPs of all Machines", self.floating_ip_list

    def do_getStaticIPs(self):
        print "Static IPs of all Machines", self.static_ip_list

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        self.stdout.write('*** Unknown syntax: %s\n' % line)

    # ---------Documentation-----------------

    def help_boot(self):

        print "syntax: boot [count]\n"
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          boot [n]     boots 3 vms one after the other"

    def help_quit(self):

        print "syntax: quit or q\n",
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          quit         terminates the application"
        print "          q            terminates the application"

    def help_getFloatingIPs(self):

        print "syntax: getFloatingIPs()\n",
        print "usage: "
        print "       |  command          |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          getFloatingIPs()    returns the Floating IPs of all machines"

    def help_getStaticIPs(self):

        print "syntax: getStaticIPs()\n",
        print "usage: "
        print "       |  command          |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          getStaticIPs()    returns the Static IPs of all machines"

    def help_delete(self):

        print "syntax: delete [names]\n",
        print "usage: "
        print "       |  command        |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          delete v-001      deletes machine v-001"
        print "          delete v-002      deletes machine v-001"
        print "          delete v*         deletes all machines starting with v"

    def help_setCloud(self):

        print "internal method"

    def help_setCloudUser(self):
        print "syntax: setCloudUser [user name]\n"
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          setCloudUser ubuntu     sets user name as 'ubuntu' to connect to vms"

    def help_setAssignFloatingIp(self):
        print "syntax: setAssignFloatingIp [True/False]\n"
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          setAssignFloatingIp False     sets whether floating ip need to be created"

    def help_setMasterIp(self):
        print "syntax: setMasterIp [xxx.xxx.xxx.xxx]\n"
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          setMasterIp 123.123.123.123     sets master ip as 123.123.123.123 to start zeppelin and spark"

    def help_setUserId(self):
        print "syntax: setUserId [user id]\n"
        print "usage: "
        print "       |  command   |  description                                        "
        print "        ------------------------------------------------------------------"
        print "          setUserId yourUserName     sets user name as your user name"

    # ---------shortcuts----------------------
    do_q = do_quit
    do_exit = do_quit
    help_q = help_quit
    help_exit = help_quit




if __name__ == "__main__":
    vms = VMS()
    vms.cmdloop()

