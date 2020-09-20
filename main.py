from WebServer import WebServer
from signal import signal, SIGINT

def main():
    ws = WebServer()
    signal(SIGINT, ws.endServer)
    ws.start()

if __name__ == '__main__':
    main()