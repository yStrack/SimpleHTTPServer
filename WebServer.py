from sys import exit
from os import fork
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
import time

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
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; encoding=utf8\nContent-Length: '+str(len(response_data))+'\n'
                    except Exception as e:
                        print('Execption:', e)
                        response_data = "<html><body><center><h1>Error 404: File not found</h1></center></body></html>"
                        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; encoding=utf8\nContent-Length: '+str(len(response_data))+'\n'
                        
                time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                response_header += 'Date: {now}\n'.format(now=time_now)
                response_header += 'Server: WebServer\n'
                response_header += 'Connection: close\n\n'

                response = response_header + response_data
                print(response)

                conn.send(response_header.encode())
                conn.send(response_data.encode())
                time.sleep(20)
                conn.close()
                # filho sai do programa
                exit()
            # Pai fica responsável pelo socket do servidor
            else:
                conn.close()
    
    def endServer(self,sig, unused):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            pass

        exit(1)