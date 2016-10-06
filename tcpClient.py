
import socket
import sys

HOST = 'lab11power.ddns.net'
PORT = 4908

def help():
    print("Available Commands:")
    print("on\tTurn load on")
    print("off\tTurn load off")
    print("readV\tRead voltage value")
    print("readI\tRead current value")
    print("readW\tRead wattage value")
    print("watt=XX\tSet load to XX W")
    print("amp=XX\tSet load to XX A")
    print("help\tDisplay help")
    print("exit\tTurn load off and exit application\n")

def main():
    version2 = True if sys.version_info[0] < 3 else False

    skt = socket.socket()
    skt.connect((HOST, PORT))

    help()

    while (1):
        if version2:
            textIn = raw_input('Enter input: ')
        else:
            textIn = input('Enter input: ')

        if textIn == 'help':
            help()
        else:
            if version2:
                skt.send(textIn)
            else:
                skt.send(bytes(textIn, 'utf-8'))
            data = skt.recv(1024).strip().decode('utf-8')
            print('{0}\r\n'.format(data))
            if textIn == 'exit':
                break
    skt.close()


if __name__=="__main__":
    main()
