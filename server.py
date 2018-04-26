import socket 
import sys
import select

host = '140.141.225.187' 
port = 50000 

backlog = 5 
recvsize = 1024 

# server's listener socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Release listener socket immediately when program exits, 
# avoid socket.error: [Errno 48] Address already in use
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host,port)) 

print('PassiveHost0 listening on port', port)
server.listen(backlog)

inputs = [ server ]        # Maintain the list of all sockets/fds from which we may get input
# inputs = [server, sys.stdin]

while inputs:
    
    print("DBG> Waiting for next available input", file=sys.stderr)
    
    # Blocking call to select() waiting for I/O channels to be "ready"
    
    readset, writeset, exceptset = select.select(inputs, [], [])
    print("DBG> select() returned, so there must be some work to do", file=sys.stderr)
    
    #iterate over items in the readset
    for channel in readset:
        if channel is server:
            # client is making a connect(), so accept() would not block
            
            peer, addr = server.accept()
            print('Accepted connection from', addr, file=sys.stderr)
            inputs.append(peer)
        else:
            data = channel.recv(recvsize)
            if data != b"":
                print("{}: {}".format(channel.getpeername(), data), file=sys.stderr)
            else:
                print('DBG> Closing', channel.getpeername(), file=sys.stderr)
                inputs.remove(channel)
                channel.close()
                if len(inputs) == 1:
                    inputs.pop()
                
print("DBG> No more available channels, terminating loop", file=sys.stderr)
server.close()
