import http.server
import socketserver

# -- IP and the port of the server
IP = "127.0.0.1"  # Localhost means "I": your local machine
PORT = 8000


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def antibioticos(self, limit):
#lo primero que hacemos, será hablar con la FDA para que nos de los datos
        antibioticos = self.openfda_req(limit) #diccionario con la información

        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Nombre. Marca. Fabricante. ID. Propósito</p>'
                   '\n'
                   '<ul>\n')
        for drug in drugs['results']:

            
            if drug['openfda']:
                nombre = drug['openfda']['substance_name'][0]
               

                marca = drug['openfda']['brand_name'][0]

                fabricante = drug['openfda']['manufacturer_name'][0]
            else:
                nombre = "Desconocido"
                marca = "Desconocido"
                fabricante = "Desconocido"
            id = drug['id']

            try:
                proposito = drug['purpose'][0]
                
            except KeyError:
                proposito = "Desconocido"

            message += "<li>{}. {}. {}. {}. {}</li>\n".format(nombre, marca, fabricante, id, proposito)


        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        return message
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        print("Recurso pedido: {}".format(self.path))
        message = "" 

        recurso_list = self.path.split("?")
        print(recurso_list)
        doc = recurso_list[0]
        print("se abrirá", doc)
        if len(recurso_list) > 1:
            valores = recurso_list[1]
        else:
            valores = ""

        print("Archivo: {}, valores: {}".format(doc, valores))
        print("valores", (valores))
        # Send headers


        if valores:
            print("Hay valores introducidos")
            quita = valores.split("&")
            for element in quita:
                a = element.split("=")
                print(a[0], a[1])

        else:
            print("SIN PARAMETROS")


        if self.path == "/" or self.path == "/index" or self.path == " ":
            filename = "index.html"
            self.send_header('Content-type', 'text/html')

        elif valores == "firstname=Mickey&lastname=Mouse":
            filename = "new.html"
            self.send_header('Content-type', 'text/html')
        elif self.path == "/formulario":
            filename = "formulario.html"
            self.send_header('Content-type', 'text/html')
        elif self.path =="/formulariofda":
            filename = "formulariofda.html"
            
        else:
            filename = "error.html"
            
            print(self.path.split("?") , "jaj")
            self.send_header('Content-type', 'text/html')
            
	    
        a = self.end_headers()
        
        
        with open(filename, "r") as f:
            content = f.read()
        print("File to send: {}".format(filename))
        # Send message back to client
        message = content
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        
        print("File served!")
        print(self.path)
        return



# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer((IP, PORT), Handler)

print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
