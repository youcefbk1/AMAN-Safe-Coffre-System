   def start_raspberry_script(self):
        """
        Starts the Raspberry Pi script remotely using SSH.
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to Raspberry Pi (Change IP, username, and password)
            ssh.connect(hostname="raspberrypi.local", username="aman", password="aman")

            # Kill any previous instance of the script
            ssh.exec_command("pkill -f raspberry_script.py")

            # Start the Raspberry Pi script in the background
            ssh.exec_command("nohup python3 /home/aman/aman/raspberry_script.py &")

            print("Raspberry Pi script started successfully.")
            ssh.close()

        except Exception as e:
            print(f"Error starting Raspberry Pi script: {e}")