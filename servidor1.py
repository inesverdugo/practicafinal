import http.server
import socketserver
import json
import http.client


servidor_rest = "api.fda.gov"
openfda_event = "/drug/label.json"
# -- IP and the port of the server
IP = "127.0.0.1"  # Localhost means "I": your local machine
PORT = 8000


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    servidor_rest = "api.fda.gov"
    openfda_event = "/drug/label.json"
    fda_componente  = "&search=active_ingredient:"
    fda_laboratorio ='&search=openfda.manufacturer_name:'
    def openfda_req(self, limit=1, search_str=""):
        """Realizar una peticion a openFPGA"""

        # Crear la cadena con la peticion
        req_str = "{}?limit={}".format("/drug/label.json", limit)


        # Si hay que hacer busqueda, añadirla a la cadena de peticion
        if search_str != "":
            req_str += "&{}".format(search_str)

        print("Recurso solicitado: {}".format(req_str))

        conn =http.client.HTTPSConnection(servidor_rest)


        # Enviar un mensaje de solicitud
        # Enviar un mensaje de solicitud
        conn.request("GET", req_str, None, {'User-Agent': 'http-client'})


        # Obtener la respuesta del servidor
        r1 = conn.getresponse()
        print(r1)

        #if r1.status == 404:
         #  print("ERROR. Recurso {} no encontrado".format(REST_RESOURCE_NAME))
          # exit(1)

        print("  * {} {}".format(r1.status, r1.reason))

        # Leer el contenido en json, y transformarlo en una cadena
        drugs_json = r1.read().decode("utf-8")
        
        conn.close()

        # ---- Procesar el contenido JSON

        return json.loads(drugs_json)



    def dame_web (self, lista):
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """

    def buscarempresa(self, empresa):
        #drugs = self.openfda_req(limit= 10)
    

        

        print(empresa)
        limite = 10
        empresas = []
        conexion = http.client.HTTPSConnection("api.fda.gov")
        conexion.request("GET", "/drug/label.json" + "?limit=" + str(limite) + '&search=openfda.manufacturer_name:'+ empresa)
        print("Mensaje enviado a la FDA")     

        respuesta = conexion.getresponse()
        respuesta1 = respuesta.read()
        datos = respuesta1.decode("utf8")
        json_datos = json.loads(datos)
        cosas = json_datos["results"]
        
        for cosa in cosas:
            empresas.append(cosa['openfda']['manufacturer_name'][0])
      
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in empresas:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """

       # if respuesta.status == 404:
        #    print("ERROR. Recurso {} no encontrado".format("/drug/label.json"))
         #   exit(1)

        return list_html


    def encontrarmedicamento(self, resultado):
            OPENFDA_API_URL="api.fda.gov"
            OPENFDA_API_DRUG='&search=active_ingredient:'
            OPENFDA_API_EVENT="/drug/label.json"

            #Por defecto 10 en este caso, no 1
            limit = 10


            drugs = []
            conn = http.client.HTTPSConnection(OPENFDA_API_URL)
        
            conn.request("GET", OPENFDA_API_EVENT + "?limit="+str(limit) + OPENFDA_API_DRUG + resultado)
            r1 = conn.getresponse()
            print(r1)
            data1 = r1.read()
            data = data1.decode("utf8")
            print(data)
            biblioteca_data = json.loads(data)
            print(biblioteca_data, "kdkdk")
            events_search_drug = biblioteca_data['results']
            for resultado in events_search_drug:
                if ('generic_name' in resultado['openfda']):
                    drugs.append(resultado['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')

            resultado_html = self.dame_web(drugs)
            self.wfile.write(bytes(resultado_html, "utf8"))

    def dame_web (self, lista):
        list_html = """
                                <html>
                                    <head>
                                        <title>OpenFDA Cool App</title>
                                    </head>
                                    <body>
                                        <ul>
                            """
        for item in lista:
            list_html += "<li>" + item + "</li>"

        list_html += """
                                        </ul>
                                    </body>
                                </html>
                            """



    def idmedicamento(self, drug, limit= 10):       
        self.send_response(200)

    # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        #a = self.openfda_req(limit= 10)
        medicamentos = []
        
        limit = 10
        conexion = http.client.HTTPSConnection(self.servidor_rest)
        conexion.request("GET", self.openfda_event + "?limit="+str(limit) + self.fda_componente + drug)
        print("Mensaje enviado a la FDA")

        respuesta = conexion.getresponse()
        print(respuesta)
        #print(a)
        #if a.status == 404:
         #   print("ERROR. Recurso {} no encontrado".format(self.openfda_event))
          #  exit(1)
 
       # print("  * {} {}".format(a.status, a.reason))
        medicamentos_json = respuesta.read().decode("utf-8")
        
        medicamentos = json.loads(medicamentos_json)
        print(medicamentos)
        buscar = medicamentos["results"]
    
        for resultado in buscar:
                if ('brand_name' in resultado['openfda']):
                    medicamentos.append(resultado['openfda']['brand_name'][0])
                print(medicamentos, "kk")
                list_html = """
		                        <html>
		                            <head>
		                                <title>OpenFDA Cool App</title>
		                            </head>
		                            <body>
		                                <ul>
		                    """
                for item in medicamentos:
                    list_html += "<li>" + item + "</li>"
                    list_html += """
		                                </ul>
		                            </body>
		                        </html>
		                    """
           
                    return list_html

                else:
                    medicamentos.append('Desconocido')
        print(medicamentos, "2")
  




    def separar(x):

        meta = drugs['meta']


        total = meta['results']['total']
        limit = meta['results']['limit']
        return meta

 

    def listamedicamentos(self, limit):
        """Devolver el mensaje con la peticion del listado de fármacos"""
        # Lanzar la peticion a openFDA
        # Establecer la conexion con el servidor
       # medicamentos = self.openfda_req(limit) 
        drugs = self.openfda_req(limit)  
     

        meta = drugs['meta']
       

        total = meta['results']['total']
        limit = meta['results']['limit']
 
        
        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>Lista de medicamentos\n'
                   '<body> \n'
                   '<p>A continuación le aparecerán los datos de los medicamentos. Ordenados por su : Componente. Nombre Comercial. Fabricante. ID. Uso</p>'
                   '\n'
                   '<ul>\n')

        # Campo RESULTS: contiene los resultados de la busqueda
        # drugs.results[0]
        for drug in drugs['results']:

            # Nombre del componente principal: drugs.openfda.substance_name[0]
            if drug['openfda']:
                nombre = drug['openfda']['substance_name'][0]
               

                # Marca: drugs.openfda.brand_name[0]
                marca = drug['openfda']['brand_name'][0]

                # Nombre del fabricante: drugs.openfda.manufacturer_name[0]
                fabricante = drug['openfda']['manufacturer_name'][0]
            else:
                nombre = "Desconocido"
                marca = "Desconocido"
                fabricante = "Desconocido"

            # Identificador: drugs.id
            id = drug['id']
            

            # Proposito: drugs.purpose[0]
            try:
                proposito = drug['purpose'][0]
                
            except KeyError:
                proposito = "Desconocido"

            message += "<li>Componente: {}. Marca: {}. Fabricante:  {}. Id: {}. Uso:  {}</li>\n".format(nombre, marca, fabricante, id, proposito)



        # Parte final del html
        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Volver</a>'
                    '</body>\n'
                    '</html>')

        return message

    def listaempresas(self, limit):
        drugs = self.openfda_req(limit)


        meta = drugs['meta']

        total = meta['results']['total']
        limite = meta['results']['limit']
        print("* Objetos recibidos: {} / {}".format(limite, total))
        
        message = (' <!DOCTYPE html>\n'
                   '<html lang="es">\n'
                   '<head>\n'
                   '    <meta charset="UTF-8">\n'
                   '</head>\n'
                   '<body>\n'
                   '<p>Fabricante</p>'
                   '\n'
                   '<ul>\n')
        for drug in drugs["results"]:
            if drug['openfda']:

                try:
                    message += "<li>{}</li>".format(drug['openfda']['manufacturer_name'][0])
                   
                except KeyError:
                    print("Desconocida")
                    pass

        # Parte final del html
        message += ('</ul>\n'
                    '\n'
                    '<a href="/">Home</a>'
                    '</body>\n'
                    '</html>')

        return message
    # GET
    def do_GET(self):
        limit = 1
        # Send response status code
        self.send_response(200)

        recurso_list = self.path.split("?")
     
        doc = recurso_list[0]
        print("se abrirá", doc)
        if len(recurso_list) > 1:
            valores = recurso_list[1]
            print("Hay valores introducidos")
            quita = valores.split("&")
            for element in quita:
                a = element.split("=")
                print(a[0], a[1])
        

        else:
            valores = "NO HAY VALORES INTRODUCIDOS"

        print("Archivo: {}, valores: {}".format(doc, valores))
      


        if self.path == "/" or self.path == "/index" or self.path == " ":
            filename = "formulario.html"
            self.send_header('Content-type', 'text/html')
          
            with open(filename, "r") as f:
                content = f.read()
            print("File to send: {}".format(filename))
            message = content
            

        elif doc == "/listDrugs":
           
            print("Lista de medicamentos")
            message = self.listamedicamentos(limit)
            self.send_header('Content-type', 'text/html')
        elif self.path == "/ListCompanies":
            message = self.listaempresas(limit= 10)
            self.send_header('Content-type', 'text/html')
        elif self.path.startswith("/SearchDrug"):
           
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            principio = self.path.split("=")
           
            try:
                if principio[2] != "":
                    medicamento = principio[1] + "=" + principio[2]
             

                else:
                    medicamento = principio[1] +"=" + "10"
         
            except IndexError:
                medicamento = principio[1] + "&limit=10"
            limit = 10
            print(medicamento, "dd")
            headers = {"Usuario": "http-client"}



           
            conexion = http.client.HTTPSConnection("api.fda.gov")
            conexion.request("GET", "/drug/label.json?&search=active_ingredient:%s" %medicamento, None, headers)
            print("Mensaje enviado a la FDA")     

            respuesta = conexion.getresponse()
            print(respuesta.status, respuesta.reason)
            respuesta2 = respuesta.read().decode("utf-8")
            
            conexion.close()
            med = json.loads(respuesta2)["results"]
            respuesta3 = ["<h1>Lista de medicamentos que contienen ese principio activo</h3><br>"]
            for n in med:
                try:
                    respuesta3.append("<li>"+n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    respuesta3.append("<li>Desconocido</li>")
            message = "".join(respuesta3)
         
            
            
       
        elif self.path.startswith("/SearchCompany"):

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            compañia = self.path.split("=")
           
            try:
                if compañia[2] != "":
                    empresa = compañia[1] + "=" + compañia[2]
             

                else:
                    empresa = compania[1] +"=" + "10"
         
            except IndexError:
                empresa = compañia[1] + "&limit=10"
            
            print(empresa, "dd")
            headers = {"Usuario": "http-client"}



           
            conexion = http.client.HTTPSConnection("api.fda.gov")
            conexion.request("GET", "/drug/label.json?&search=openfda.manufacturer_name:%s" %empresa, None, headers)
            print("Mensaje enviado a la FDA")     

            respuesta = conexion.getresponse()
            print(respuesta.status, respuesta.reason)
            respuesta2 = respuesta.read().decode("utf-8")
            
            conexion.close()
            med = json.loads(respuesta2)["results"]
            respuesta3 = ["<h1>Lista de medicamentos que trabaja la empresa introducida</h3><br>"]
            for n in med:
                try:
                    respuesta3.append("<li>"+n["openfda"]["generic_name"][0] + "</li>")
                except KeyError:
                    respuesta3.append("<li>Desconocido</li>")
            message = "".join(respuesta3)
         







            self.send_response(200)

            # Send headers
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()

            #limit = 10 
            #mpresa = self.path.split("=")[1]
            #print(empresa)
            
            
            #message = self.buscarempresa(empresa)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

          
       
        print("File served!")

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
