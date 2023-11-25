import paramiko

class SCPUploader:
    def __init__(self):
        # SSH connection details (replace with your own)
        self.ssh_host = 'host ip'
        self.ssh_user = 'username'
        self.ssh_password = 'password'
        self.ssh_port = 22

    def upload_file(self, filename):
        try:
            # Connect to the Windows host using SSH
            with paramiko.Transport((self.ssh_host, self.ssh_port)) as transport:
                transport.connect(username=self.ssh_user, password=self.ssh_password)
                scp = paramiko.SFTPClient.from_transport(transport)

                # Upload the file to the Windows host
                scp.put(filename, f'C:\\Users\\Ben_P\\Desktop\\{filename}')

                print(f"File 'C:\\Users\\Ben_P\\Desktop\\{filename}' uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file: {e}")

# Uncomment the following line if you want to test SCP upload separately
# SCPUploader().upload_file('packets.pcap')
