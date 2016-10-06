
import socket

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

    skt = socket.socket()
    skt.connect((HOST, PORT))

    help()

    while (1):
        textIn = input('Enter input: ')
        if textIn == 'help':
            help()
        else:
            skt.send(bytes(textIn, 'utf-8'))
            data = skt.recv(1024).strip().decode('utf-8')
            print('{0}\r\n'.format(data))
            if textIn == 'exit':
                break
    skt.close()


if __name__=="__main__":
    main()
