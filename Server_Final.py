#
# Elizabeth Wanic
# Programming Assignment 
# Step 2
# CS3502
# 21 February 2017
#

'''In order to run this program, Client_Final.py must also be running on a separate terminal. The program
can be run via the command line with the following syntax: python3 Server_Final.py localhost
It was created in and meant to be run with Python 3.6'''

import socket
import sys
import time
import sched
import threading
import random


def game_quit():

    for connection_address_tuple in connectionList:
        print("  Closing connection for player", connection_address_tuple[0])
        message = "  Closing your connection.                   " 
        print("  Sending: ", message)
        encode = message.encode()
        connection_address_tuple[1].sendall(encode)
        connection_address_tuple[1].close()

    print("\n  Waiting for a new connection.\n  A new game has started.")
 
    reset()
    return

def reset():
    global guesses 
    guesses = []
    global connectionList
    connectionList = []
    global player 
    player = 0

    global accepting_new_players
    accepting_new_players = True

    return

def results():
    print("\n  Timer up! ")
    print("  Determining the winner now.")
    global accepting_new_players
    accepting_new_players = False
    
    answer = random.randint(1,100)

    winner = guesses[0]

    for i in range(0, len(connectionList)):
        if abs(guesses[i] - answer) <= abs(winner - answer):
            winner = guesses[i]  
            win_play = i
        else:
            pass #do nothing
    print("  The winner is player", win_play)
    print("  Delivering the results to the players")
    print("\n")

    for connection_address_tuple in connectionList:
        
        if guesses[connection_address_tuple[0]] == 250:
            message = "  Your guess was invalid. The answer was " + str(answer) + "  "
        else:
            message = "  Your guess was " + str(guesses[connection_address_tuple[0]]) +\
            " and the answer was " + str(answer) + "    "
        
        encode = message.encode()
        connection_address_tuple[1].sendall(encode)

        if guesses[connection_address_tuple[0]] == winner:
            message2 = "  You were the winner! =)                   "
        else:
            message2 = "  Better luck next time!                    "

        encode2 = message2.encode()
        connection_address_tuple[1].sendall(encode2)

    game_quit()

def client_thread(connection, client_address, player_number):

    try:
        message = "  Hello!  Guess a number between 1 and 100.  "
        print("\n  New client")
        print("  Sending: ", message)
        encode = message.encode()
        connection.sendall(encode)
        
        while True:

            guess = connection.recv(45) #45 characters at a time
            
            if guess:

                guess = guess.decode()
                

                if guess.isdigit() != True:
                    print("\n")
                    print("  Invalid guess received from player", player_number,".")
                    message = "  Invalid guess.  Please wait and play again."
                    print("  Sending: ", message)
                    guesses[player_number] = 250 #cannot be the winner
                    encode = message.encode()
                    connection.sendall(encode)
                    break # wait for results to not kill the server


                elif int(guess) <= 100 and int(guess) >= 1:
                    print("\n")
                    print("  Message received.")
                    print("  Player", player_number, "guessed: ", guess)
                    guesses[player_number] = int(guess)

                    message = "  You guessed " + guess + "                           "
                    print("  Sending: ", message)
                    encode = message.encode()
                    connection.sendall(encode)

                    break #Wait for results

                else:
                    print("\n")
                    print("  Invalid guess received from player", player_number,".")
                    message = "  Invalid guess.  Please wait and play again."
                    print("  Sending: ", message)
                    guesses[player_number] = 250 #cannot be the winner
                    encode = message.encode()
                    connection.sendall(encode)
                    break # wait for results to not kill the server

            else:
                break


    except Exception as e:
        print(e)
        connection.close()
        
## MAIN ##
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) < 2:
    print ("\n    Error message")
    print ("    Please provide <hostname>, e.g. localhost, in the command line\n\
    Please specify game time (in seconds) after hostname\n")
    exit(1)

if len(sys.argv) < 3:
    print ("\n  Error message")
    print("  Please specify game time (in seconds) after hostname\n")
    exit(1)
    
# Bind the socket to the address given on the command line
server_name = sys.argv[1]
tInterval = int(sys.argv[2])
server_address = (server_name, 10000)
print("  Starting up on %s port %s" % server_address)
sock.bind(server_address)
sock.listen(1)

accepting_new_players = True
guesses = []
connectionList = []
player = 0

while True:

    print("\n  Waiting for a new connection")
    if accepting_new_players == True:
        connection, client_address = sock.accept()
        connectionList.append(  (player, connection, client_address)  )
        guesses.append(0)
        t = threading.Thread(target=client_thread, args = (connection, client_address, player))
        t.start()
        print("  Starting thread.  Player number is ", player)

        if player == 1:
            t = threading.Timer(tInterval, results)
            t.start()

        player += 1

# Close the socket upon completion
sock.close()



