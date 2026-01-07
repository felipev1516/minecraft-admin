'''
Author: Felipe Valadez
Date: 2023-09-15
Description: 

python script to utilize the TCP/IP protocol to send and receive data over a network.
We'll be using the socket library in Python to create a simple TCP/IP client and server.
Hybrid program that can function as both a client and a server based on user input.

Implementation Details:

- Session Restore Logic:
    We will create a separate text file to store the last used IP address and port number.(file name: last_session.txt)
    Client will read from this file upon startup to restore the last session.

- Asynchronous Event Handling for sockets:
    We need to implement a event handling mechanism for incoming connections and data reception by using asynchronous programming with the asyncio library or threading.
    URL: https://stackoverflow.com/questions/78532840/handling-synchronous-socket-reads-and-asynchronous-events-in-python

- Tasking:
    use asyncio.gather
'''


import argparse
import os

if __name__ == "__main__":
    import socket
    import sys
    import subprocess
    import asyncio
    from signal import SIGINT
    from argparse import ArgumentParser
    
    parser = None
    args = None
    
    # Commands to obtain local IP address based on OS
    nt_ip_cmd = "powershell -Command \"(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi').IPAddress\""
    posix_ip_cmd = "ifconfig | awk '/^wlan0:.*/{getline; print $2}'"

    def os_check() -> tuple:
        # Check the operating system
        if os.name == 'nt':
            # Windows
            return "Windows", nt_ip_cmd
        elif os.name == 'posix':
            # macOS or Linux
            return "Linux/macOS", posix_ip_cmd
        else:
            print("Unsupported operating system")
            sys.exit(1)
    
    def parse() -> None:
        epilog='''
        Example usage:
        To Host a server: python com.py -m HOST -p 10000 -i 192.168.1.100
        To Connect to a server: python com.py -m CLIENT -i 192.156.12.3 -p 10000
        To Ping a server: python com.py -m CLIENT -i 192.156.12.3 -p 10000 -P
        '''

        global  parser; parser = ArgumentParser(prog="com.py",description="TCP/IP client and server",formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
        
        parser.add_argument("-m", "--mode", help="Mode to use (HOST for server, CLIENT for client)",)
        parser.add_argument("-r", "--remote", help="Set remote mode (connect to a remote server)")
        parser.add_argument("-i", "--ip", help="IP address to use for the TCP/IP connection")
        parser.add_argument("-p", "--port", type=int, help="Port number to use for the TCP/IP connection")
        parser.add_argument("-P", "--ping", help="Ping a server as a client Example: python com.py -i 192.168.1.100 -p 10000 --ping", action="store_true")
        parser.add_argument("-M", "--message", help="Data to send to the server")
        global args; args = parser.parse_args()

    def _mode() -> str:
        # Manually select mode
        while True:
            command = str.upper(input("Select Mode (HOST/CLIENT): "))
            if command == "HOST" or command == "H":
                break
            elif command == "CLIENT" or command == "C":
                break
            else:
                print("Invalid Mode. Please select HOST or CLIENT.")
        return command

    def _ip() -> str:
        # Manually select IP address
        while True:
            try:
                command = str(input("Input IP Address: "))
                if command != "":
                    break
                else:
                    continue
            except ValueError:
                    print("Invalid IP Address. Please input a valid IP address.")
        return command
    
    def _port() -> int:
         # Manually select port number
        while True:
            try:
                command = int(input("Select Port Number (10000-10002): "))
                if command >= 10000 and command <= 10002:
                    break
                else:
                    continue
            except ValueError:
                print("Invalid Port Number. Please select 10000, 10001, or 10002.")
        return int(command)

    def _remote() -> str:
        # Manually select remote mode
        
        while True:
            try:
                if args.remote is None:
                    command = str.upper(input("Remote Mode? (YES/NO, ON/OFF, 1/0): "))
                else:
                    if str(args.remote).upper().equals("0"):
                        command = "0"
                    else:
                        command = "1"
                
                if command == "1" or command == "ON" or command == "Y" or command == "YES":
                    command = "0.0.0.0"
                    break
                elif command == "0" or command == "NO" or command == "N" or command == "OFF":
                    if os.name == 'posix':
                        command = subprocess.check_output(posix_ip_cmd, shell=True).decode()
                        print (f"Detected IP Address: {command.strip()}")
                        command = str(command.strip())
                    else:
                        #command = "127.0.0.1"
                        command = subprocess.check_output(nt_ip_cmd, shell=True).decode()
                        print (f"Detected IP Address: {command.strip()}")
                    break
                else:
                    print("Invalid Input. Please select (YES/NO, ON/OFF, 1/0).")
            except ValueError:
                print("Invalid Input. Please select (YES/NO, ON/OFF, 1/0).")
    
            
        return command
    
    async def test_connection(ip: str, port: int) -> None:
        try:
            writer = await asyncio.open_connection(host=ip, port=port)
            print(f"Successfully connected to {ip}:{port}")
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"Failed to connect to {ip}:{port} - {e}")
            writer.close()
            await writer.wait_closed()

    # Info: https://docs.python.org/3/glossary.html#term-coroutine
    # Coroutine to handle receiving data
    async def receive_data(reader: asyncio.StreamReader) -> None:
        try:
            async with asyncio.timeout(3):
                data = await reader.read(1024)
            print(f"Received: {data.decode()}")
        except asyncio.CancelledError:
            return
        except asyncio.TimeoutError:
            return
    
    # coroutine to handle sending data
    async def send_data(writer: asyncio.StreamWriter) -> None:
        try:
            async with asyncio.timeout(5):
                message = input("(Ctrl+C To Exit)\n>:")
                writer.write(message.encode())
            writer.drain()
        except asyncio.CancelledError:
            return
        except asyncio.TimeoutError:
            return
    
    async def communication(reader:asyncio.StreamReader,writer:asyncio.StreamWriter) -> None:
        try:
            while True:
                try:
                    print("Communication 1")
                    # Create a coroutine to receive data
                    # This Task will print client response
                    
                    await receive_data(reader)
                    await send_data(writer)
                except KeyboardInterrupt:
                    writer.close()
                    await writer.wait_closed()
                    break
        except KeyboardInterrupt:
            pass
        
    '''
    async asyncio.start_server(client_connected_cb,..)

    The client_connected_cb callback is called whenever a new client connection is 
    established. It receives a (reader, writer) pair as two arguments,
    instances of the StreamReader and StreamWriter classes.

    client_connected_cb can be a plain callable or a coroutine function; if it is 
    a coroutine function, it will be automatically scheduled as a Task.
    '''
    async def server() -> None:
        # Create a TCP/IP socket
        
        print('starting up on %s port %s' % (args.ip, args.port))
        # This is a loop
        server = await asyncio.start_server(client_connected_cb=communication,host=args.ip, port=args.port)
        async with server:
            await server.serve_forever()

    
    async def client() -> None:
        try:
            async with asyncio.timeout(300):
                reader, writer = await asyncio.open_connection(host=args.ip,port=args.port)
                await communication(reader,writer)
        #except TimeoutError:
        #    print("TIMEOUT ERROR: Host not available Disconnecting")
        except asyncio.CancelledError:
            print(f"Connection Error")
        except KeyboardInterrupt:
            print(f"Closing...")
            
    
    def prompt():

        if args.mode is None:
            args.mode = _mode()
       
        if args.mode == "CLIENT": 
            if args.ip is None:
                args.ip = _ip()
            if args.port is None:
                args.port = _port()
        else:
            args.ip = _remote()
            args.port = 10000
        return
    
    '''
    Note: We already have a exception handler for keyboard interuption in the main function below
    so no need to add another in other functions
    '''
    if __name__ == "__main__":
        parse()
        #print (f"{os_check()}")
        
        if args.ip and args.port and args.ping:
            client()
        else:
            # Create two concurrent loops for client and server
            prompt()
            asyncio.run(server()) if str(args.mode).upper() == "HOST" else asyncio.run(client())
                
                    
        
       


    