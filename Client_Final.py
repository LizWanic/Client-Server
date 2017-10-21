#
# Elizabeth Wanic
# Programming Assignment 
# Step 2
# CS3502
# 21 February 2017
#

'''In order to run this program, Server_Final.py must also be running on a separate terminal. The program
can be run via the command line with the following syntax: python3 Client_Final.py localhost
It was created in and meant to be run with Python 3.6'''


import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check to make sure that an IP address has been provided
if len(sys.argv) < 2:
    print("Need to provide <hostname>, e.g., localhost in the command line")
    exit(1)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print("Connecting to %s port %s" % server_address)
sock.connect(server_address)

while True:

    try:
        #receive the first message
        data = sock.recv(45)
        decode = data.decode()

        print("  Received 1: ", end="")
        guess = input(decode)
        print("  Sending:                ", guess)
        encode = guess.encode()
        sock.sendall(encode)

        #receive the okay message
        data = sock.recv(45)
        decode = data.decode()

        print("  Received okay: ", decode)

        #receive the second message
        data = sock.recv(45)
        decode = data.decode()

        print("  Received 2: ", decode)

        #receive the third message
        data = sock.recv(45)
        decode = data.decode()

        print("  Received 3: ", decode)
        data = sock.recv(45)
        decode = data.decode()

        #receive the fourth message
        print("  Received 4: ", decode)
        if "Closing" in decode:
            print("\n                  Good-bye.\n")
            sock.close()
            break

    except Exception as e:
        print(e)
        # Closes the socket in case of an error
        sock.close()
        break

# Close the socket upon completion
sock.close()



