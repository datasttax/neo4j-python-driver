from neo4j import GraphDatabase
import os
import time

class NeoApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def crear_nodo_persona(self, nombre, dni, telefono, trabajo):
        with self.driver.session() as session:
            result = session.execute_write(self.crear_nodo_persona_neo, nombre, dni, telefono, trabajo)
            print(result)

    def crear_nodo_delito(self, tipo, descripcion, fecha, hora, barrio):
        with self.driver.session() as session:
            result = session.execute_write(self.crear_nodo_delito_neo, tipo, descripcion, fecha, hora, barrio)
            print(result)

    # Función para crear Relacion (persona sospechoso/testigo/victima de delito)
    def crear_relacion_sospechoso_delito(self, nombre_persona, numero_delito, relacion):
        with self.driver.session() as session:
            result = session.execute_write(self.crear_nodo_delito_neo, nombre_persona, numero_delito, relacion)
            print(result)


    def dueno_auto(self):
        with self.driver.session() as session:
            result = session.execute_write(self.dueno_auto_neo)
            print(result)

    def sospechosos_delito(self, delito):
        with self.driver.session() as session:
            results = session.execute_write(self.sospechosos_delito_neo, delito)
            for result in results:
                print(result)


    @staticmethod
    def crear_nodo_persona_neo(tx, nombre, dni, telefono, trabajo):
        result = tx.run("CREATE (persona1:PERSONA{nombre:$nombre, documento:$documento, telefono:$telefono trabajo:$trabajo})", nombre=nombre, dni=dni, telefono=telefono, trabajo=trabajo)
        return result.single()[0]

    @staticmethod
    def crear_nodo_delito_neo(tx, tipo, descripcion, fecha, hora, barrio):
        result = tx.run("CREATE (delito1:DELITO{tipo:$robo, descripcion:$descripcion, fecha:$fecha, hora:$hora, barrio:$barrio})", tipo=tipo, descripcion=descripcion, fecha=fecha, hora=hora, barrio=barrio)
        return result.single()[0]

    @staticmethod
    def dueno_auto_neo(tx):
        result = tx.run("""MATCH (dueno:PERSONA)-[:DUENO]-> (bien:BIEN) WHERE ((:PERSONA{nombre: "Carlos Rojo"})-[:SOSPECHOSO]-> (:DELITO)-[:ASOCIADO]-> (bien:BIEN)) RETURN dueno.nombre""")
        return result.single()[0]

    @staticmethod
    def sospechosos_delito_neo(tx, delito):
        results = tx.run("""MATCH (sospechoso:PERSONA)-[:SOSPECHOSO]-> (delito:DELITO{descripcion:$delito}) RETURN sospechoso.nombre""", delito=delito)
        return results

    @staticmethod
    def crear_relacion_sospechoso_delito_neo(tx, nombre_persona, numero_delito, relacion):
        relacion = relacion.capitalize() # para que quede en mayuscula
        result = tx.run("""MATCH (persona:PERSONA{nombre:$nombre_persona}) MATCH (delito:DELITO{numero:$numero_delito}) CREATE (persona)-[:$relacion]->(delito)""", nombre_persona=nombre_persona, numero_delito=numero_delito, relacion=relacion)
        return result.single()[0]





print("Bienvenido")
os.system("cls")
print("Elija una operacion (ingrese el numero)")
print("1. Crear un nodo")
print("2. Crear una relacion")
print("3. Quien es el dueño del auto por el cual se lo acusa a Carlos")
print("4. Quienes son los sospechosos de un delito determinado")

neo = NeoApp("bolt://localhost:7474", "neo4j", "uade1234")

def menu():

    opcion = input("numero de la operacionr: ")

    if opcion == "1":
        os.system("cls")
        print("1 Crear un nodo ------------")

        # input tipo de nodo (persona, delito)
        tipo_nodo = input("tipo de nodo (persona, delito): ")

        if tipo_nodo == "persona":
            nombre = input("nombre: ")
            dni = input("dni: ")
            telefono = input("telefono: ")
            trabajo = input("trabajo: ")

            neo.crear_nodo_persona(nombre, dni, telefono, trabajo)

        elif tipo_nodo == "delito":
            tipo = input("tipo: ")
            descripcion = input("descripcion: ")
            fecha = input("fecha: ")
            hora = input("fecha: ")
            barrio = input("barrio: ")

            neo.crear_nodo_delito(tipo, descripcion, fecha, hora, barrio)

        else:
            print("tipo de nodo incorrecto")

        time.sleep(5)
        menu()

    elif opcion == "2":
        os.system("cls")
        print("2 Crear una relacion ------------")
        nombre_persona= input("nombre persona: ")
        numero_delito = input("numero delito: ")
        relacion = input("relacion (sospechoso, testigo, victima): ")

        # se podría agregar si la persona no existe (hay que hacer otra query de neo)
        neo.crear_relacion_sospechoso_delito(nombre_persona, numero_delito, relacion)
        time.sleep(5)
        menu()


    elif opcion == "3":
        os.system("cls")
        print("3 Quien es el duseño del auto por el cual se lo acusa a Carlos ------------")
        neo.dueno_auto()
        time.sleep(5)
        menu()

    elif opcion == "4":
        os.system("cls")
        print("4 Quienes son los sospechosos de un hecho determinado ------------")
        delito = input("delito: ")
        neo.sospechosos_delito(delito)
        time.sleep(5)
        menu()

    else:
        os.system("cls")
        print("Opcion incorrecta")
        menu()


menu()
