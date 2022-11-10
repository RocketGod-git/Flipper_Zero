from socket import socket, AF_INET, SOCK_STREAM

HOST = input("Enter the host IP\n> ")
PORT = 1234

server_connection = socket(AF_INET, SOCK_STREAM)
server_connection.connect((HOST, PORT))

while True:
    print("    Menu")
    print("1. Trigger BSOD")
    print("2. Set timer")
    print("3. Get remaining time")
    print("4. Close connection")
    print("Select an option")
    operation = input("> ")
    if operation != "1" and operation != "2" and operation != "3" and operation != "4":
        print("\nInvalid option\n")
        continue

    if operation == "2":
        print("Enter the amount of seconds")
        timing = int(input("> "))
        if timing < 0:
            print("Only positive integers, try again")
            continue
        operation += f";{timing}"

    if operation == "4":
        server_connection.close()
        print("Connection closed")
        break

    try:
        server_connection.sendall(bytes(operation.encode(encoding="utf8")))
        data = server_connection.recv(1024)
        print("\n[Response]", data.decode(encoding="utf8"))
        print("")
    except BrokenPipeError:
        print("Connection was closed")
        server_connection.close()
        break

