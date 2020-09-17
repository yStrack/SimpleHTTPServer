from sys import exit
from os import fork
# import socket
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from signal import signal, SIGINT

class WebServer:
    def __init__(self):
        # self.host = socket.gethostname() # Nome do host do servidor
        self.port = 8080 # Porta p/ conexao
        # self.static_dir = "static" # Diretorio onde os arquivos .html estão localizados

    def start(self):
        # Criando socket
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind(('', self.port)) # Bind
            print("Servidor rodando")
        except:
            print("Erro ao criar servidor")
            exit(1)

        self.socket.listen(0) # Listen
        while(True):
            conn, client = self.socket.accept()
            print('CLIENT', conn)

            # Criando processos para atender conexão simultanea
            pid = fork() # 0 é o filho, pid é o pai

            # Filho atua sobre o socket com cliente
            if pid == 0:
                self.socket.close()
                
                data = conn.recv(1024).decode() # data chega em bytes
                if not data:
                    break

                request_method = data.split()[0] # Primeiro comando é o GET
                file_path = data.split()[1] # Resto é o diretorio para acesso do arquivo html

                # Verifica qual o metodo da requisição (só implementamos o GET)
                if request_method == 'GET':
                    try:
                        file = open('.' + file_path,'r')
                        response_data = file.read()
                        file.close()
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; encoding=utf8\nContent-Length: '+str(len(response_data))+'\nConnection: close'
                    except Exception as e:
                        print('Execption:', e)
                        response_header = 'HTTP/1.1 404 Not Found\r\n'
                        response_data = "<html><body><center><h1>Error 404: File not found</h1></center></body></html>"
                        
                        
                response = response_header.encode() + response_data.encode()
                print(response)
                conn.send(response_header.encode())
                conn.send(response_data.encode())
                conn.close()
                # filho sai do programa
                exit()
            # Pai fica responsável pelo socket do servidor
            else:
                conn.close()


        

ws = WebServer()
ws.start()
def endServer(sig, unused):
    try:
        ws.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        pass

    exit(1)

signal(SIGINT, endServer)