from paramiko import client

class ssh:
    client = None

    def __init__(self, address, username, password):
        print("Connecting to server.")
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False, timeout=20)

    def sendCommand(self, command):
        if(self.client):
            print("send command")
            stdin, stdout, stderr = self.client.exec_command(command)

            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"
                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    print(str(alldata, "utf8"))
        else:
            print("Connection not opened.")
# try:           
    # connection1 = ssh("192.168.1.101", "pi", "slave2ai")
    # connection1.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection2 = ssh("192.168.1.102", "pi", "slave2ai")
    # connection2.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection3 = ssh("192.168.1.103", "pi", "slave2ai")
    # connection3.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection4 = ssh("192.168.1.104", "pi", "slave2ai")
    # connection4.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection5 = ssh("192.168.1.105", "pi", "slave2ai")
    # connection5.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection6 = ssh("192.168.1.106", "pi", "slave2ai")
    # connection6.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass
# try:
    # connection7 = ssh("localhost", "pi", "slave2ai")
    # connection7.sendCommand("sudo halt > /dev/null 2>&1 &")
# except:
    # pass