final Neo4j

Persona:
nombre
apellido
dni
telefono
trabajo
parentesco
afinidad
tipo (sospechoso/victima)

llamada:
origen
destino
fecha
hora

bien
descripcion
datos_extra

cuenta:
descripcion

hecho:
descripcion
fecha
hora
ciudad
tipo (ej: robo de casa)

relato:
descripcion

Creacion de nodos:

Persona:----------------------------------------------------
dni
nombre
apellido
telefono
trabajo
parentesco
afinidad

CREATE (:Persona {dni:40524976, nombre:"Juan", apellido:"Perez", telefono: 1123547898, trabajo:"carpintero"}),
       (:Persona {dni: 44555121, nombre: "Carlos", apellido: "Montes", telefono: 1138574586, trabajo: "mecanico"}),
       (:Persona {dni: 11223344, nombre: "María", apellido: "López", telefono: 1144556677, trabajo: "abogada"}),
       (:Persona {dni: 22334455, nombre: "Ana", apellido: "Gómez", telefono: 1155667788, trabajo: "no tiene"}),
       (:Persona {dni: 33667788, nombre: "Pedro", apellido: "Ramírez", telefono: 1166778899, trabajo: "comerciante"}),
       (:Persona {dni: 99001122, nombre: "Laura", apellido: "Fernández", telefono: 1177889900, trabajo: ""}),
       (:Persona {dni: 77889900, nombre: "Andrés", apellido: "Silva", telefono: 1188990011, trabajo: "ingeniero"}),
       (:Persona {dni:44213456, nombre:"Josefina", apellido:"Dominguez", telefono:1124579874, trabajo: ""}),
       (:Persona {dni: 33559988, nombre: "Luis", apellido:"Gómez", telefono: 1167890098, trabajo: ""}),
       (:Persona {dni: 22334455, nombre: "Marta", apellido: "Sánchez", telefono: 1133224455, trabajo: ""});

(los que tienen trabajo = "" es porque son testigos, esto último lo indicamos en la relacion, lo mismo para los sospechosos y victimas)

llamada: (es una asociación) -----------------------------------------
origen  (personax)
destino (persona!=x)
fecha
hora

MATCH (juan:Persona {dni: 40524976})
MATCH (maria:Persona {dni: 11223344})
CREATE (juan)-[:LLAMADA {fecha: "03/09/2023", hora: "11:20"}]->(maria)

MATCH (carlos:Persona {dni: 44555121})
MATCH (pedro:Persona {dni: 33667788})
CREATE (carlos)-[:LLAMADA {fecha: "25/09/2023", hora: "16:40"}]->(pedro)

MATCH (laura:Persona {dni: 99001122})
MATCH (andres:Persona {dni: 77889900})
CREATE (laura)-[:LLAMADA {fecha: "10/10/2023", hora: "12:00"}]->(andres)

MATCH (ana:Persona {dni: 22334455})
MATCH (carlos:Persona {dni: 44555121})
CREATE (ana)-[:LLAMADA {fecha: "15/09/2023", hora: "20:05"}]->(carlos)

bien_registrado: --------------------------------------------------
descripcion
datos_extra

create (bien: Bien {descripcion:"auto",datos_extra:"volskwagen rojo, patente AC5-EH8, aproximadamente 50000km"}),

(bien:Bien {descripcion: "motocicleta", datos_extra: "Honda CB500F, color negro, modelo 2022, 8000km"}),

(bien:Bien {descripcion: "computadora", datos_extra: "Laptop Dell XPS 15, 16GB RAM, 512GB SSD, Core i7"}),

(bien:Bien {descripcion: "bicicleta", datos_extra: "Mountain Bike Scott Aspect 950, ruedas de 29 pulgadas, suspensión delantera"}),

(bien:Bien {descripcion: "joya", datos_extra: "Anillo de diamante, oro blanco, talla 16"}),

(bien:Bien {descripcion:"Departamento",datos_extra:"Monoambiente 20 metros cuadrados"}),

(bien:Bien {descripcion: "Casa", datos_extra: "Casa de dos pisos con jardín, 3 habitaciones, 2 baños"}),

(bien:Bien {descripcion: "Local Comercial", datos_extra: "Local en zona céntrica, 50 metros cuadrados, ideal para tienda"}),

(bien:Bien {descripcion: "Oficina", datos_extra: "Oficina amoblada con aire acondicionado y conexión a internet"}),

(bien:Bien {descripcion: "Bodega", datos_extra: "Bodega de almacenamiento de 100 metros cuadrados"});

cuenta: -----------------------------------------------------
descripcion

no hice esto, es irrelevante para las querys... Las llamadas tambien son irrelevantes pero no me di cuenta y las hice igual.

hecho: -----------------------------------------------------
descripcion
fecha
hora
ciudad
tipo (ej: robo)

CREATE (hecho1:Hecho {descripcion: "Robo de telefono a mano armada con intento fallido de homicidio", fecha: date('2023-07-25'), hora: time('14:30:00'), ciudad: "Caballito", tipo: "robo"}),

(hecho2:Hecho {descripcion: "Robo de vehiculo mientras el dueño compraba en un supermercado", fecha: date('2023-07-26'), hora: time('09:15:00'), ciudad: "Belgrano", tipo: "robo"}),

(hecho3:Hecho {descripcion: "Homicidio en primer grado en el monoambiente de la victima", fecha: date('2023-07-27'), hora: time('17:45:00'), ciudad: "La Plata", tipo: "homicidio"});

relato: -----------------------------------------------------
descripcion

create 
(relato1:Relato {descripcion:"desde lejos vi como el hombre rompía el vidrio de la ventana del auto, lo encendia y se lo llevaba"}),

(relato2:Relato {descripcion: "Vi como un hombre le disparaba al conductor de un auto, lo sacaba del mismo y se llevaba el auto"}),

(relato3:Relato {descripcion: "Presencié una situación en la que un individuo disparaba contra el conductor de un vehículo, posteriormente lo expulsaba del automóvil y se lo llevaba."});

-----------------------------------------------------------------------

Creacion de relaciones:

la idea de las mismas es crearlas a la vez que creamos los nodos, pero sino lo hacemos, tenemos que luego matchear por algo a cada nodo que queremos asociar porque la asignación de una variable desaparece luego de la ejecución de create (por ejemplo juan:Persona, luego de la ejecución, ese "juan" no es mas referenciable).

MATCH (juan:Persona {dni: 40524976})
MATCH (maria:Persona {dni: 11223344})
CREATE (juan)-[:LLAMADA {fecha: "03/09/2023", hora: "11:20"}]->(maria)

Hecho -> Testigo:

MATCH (hecho1:Hecho {fecha: date('2023-07-25'),ciudad: "Caballito", tipo: "robo"}),
      (persona1:Persona {dni: 44213456}),
      (persona2:Persona {dni: 22334455})
CREATE (hecho1)-[:TESTIGO]->(persona1),
       (hecho1)-[:TESTIGO]->(persona2),

MATCH (hecho2:Hecho {fecha: date('2023-07-26'),ciudad: "Belgrano", tipo: "robo"}), (persona1:Persona {dni: 33559988})
CREATE (hecho2)-[:TESTIGO]->(persona1)

Hecho -> Sospechoso:

MATCH (laura:Persona {dni: 99001122}), (hecho1) WHERE id(hecho1) = 98
CREATE (hecho1)-[:SOSPECHOSO]->(laura);

MATCH (carlos:Persona {dni: 44555121}), (hecho2) WHERE id(hecho2) = 99
CREATE (hecho2)-[:SOSPECHOSO]->(carlos);

MATCH (ana:Persona {dni: 22334455}), (hecho2) WHERE id(hecho2) = 99
CREATE (hecho2)-[:SOSPECHOSO]->(ana);

MATCH (juan:Persona {dni: 40524976}), (hecho3) WHERE id(hecho3) = 100
CREATE (hecho3)-[:SOSPECHOSO]->(juan);

Testigo -> (favorece) -> Sospechoso:

MATCH (luis:Persona {dni: 33559988}), (carlos:Persona {dni: 44555121})
CREATE (luis)-[:FAVORECE]->(carlos)

Personas -> Bienes:

MATCH (ana:Persona {dni: 22334455}), (bien:Bien{descripcion:"bicicleta"})
CREATE (ana)-[:REGISTRA]->(bien)

MATCH (pedro:Persona {dni: 33667788}), (bien:Bien{descripcion:"auto"})
CREATE (pedro)-[:REGISTRA]->(bien)

match (persona:Persona {dni:1144556677}), (bien:Bien {descripcion:"Casa"}) create (persona) -[:REGISTRA]-> (bien)

Hecho -> Victima:

match (hecho:Hecho{robado:"automovil"}),(pedro:Persona{dni:33667788})
CREATE (hecho)-[:VICTIMA]->(pedro)

----------------------------------------------------------------------

Respondiendo las Querys:

1. ¿Cuáles son los hechos que no tienen testigos?

MATCH (h:Hecho) WHERE NOT EXISTS ((h)-[:TESTIGO]->()) RETURN h

2. ¿Quiénes son los sospechosos de un hecho determinado?

match (p:Persona),(h:Hecho{descripcion:"Robo de telefono a mano armada con intento fallido de homicidio"}) WHERE EXISTS 
((h)-[:SOSPECHOSO]->(p)) RETURN p

3. ¿Quiénes son los testigos que favorecen a “Carlos” en el “Robo” de un “Auto”?

MATCH (hecho:Hecho {tipo: "robo", robado: "automovil"})-[:TESTIGO]->(testigo:Persona),				     (testigo)-[:FAVORECE]->(carlos:Persona {nombre: "Carlos"})

4. ¿Cuáles son los bienes que pertenecen a personas sin trabajo?

match (persona:Persona{trabajo:"no tiene"}) -[:REGISTRA]-> (bien:Bien)
return bien

5. ¿Quién es el dueño del auto por el cual se lo acusa a “Carlos”?

match ((robo:Hecho{robado:"automovil"})-[:SOSPECHOSO]->(carlos:Persona{nombre:"Carlos"})),((robo)-[:VICTIMA]->(dueño:Persona)) return dueño

6. ¿Cuántos robos de casa se produjeron entre abril y mayo del 2019 en el barrio de Belgrano?

match (hecho:Hecho{tipo:"robo",robado:"casa"}) where hecho.fecha >= date('2019-04-01') and hecho.fecha <= date('2019-04-30') and hecho.ciudad = "Belgrano" return count(hecho)

----------------------------------------------------------------------
En Python:

1. Cargar un nodo.
2. Cargar una relación entre dos nodos existentes.
3. ¿Quién es el dueño del auto por el cual se lo acusa a “Carlos”?
4. ¿Quiénes son los sospechosos de un hecho determinado?

----------------------------------------------------------------------

from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "uade1234"))


# 1) Cargar un nodo:
def cargar_nodo_bien():
    print ("Cargar un nodo del tipo 'Bien'")
    print()
    nombre = input("Ingrese el nombre del bien: ")
    descripcion = input("Ingrese la descripcion del bien: ")
    with driver.session() as session:
        session.run("create (bien: Bien {descripcion: '" + nombre + "',datos_extra: '" + descripcion + "' })")

#cargar_nodo_bien()

# 2) Cargar una relación entre dos nodos existentes.

def cargar_relacion_registra():
    print ("Cargar una relacion 'REGISTRA' entre un nodo Persona y un nodo Bien")
    print()
    dni = int(input("Ingrese el dni de la persona que registra el bien: "))
    bien = input("Ingrese el nombre del bien: ")
    with driver.session() as session:
        session.run ("match (persona:Persona {dni:" + str(dni) + "}), (bien:Bien {descripcion:'" + bien +"'}) create (persona) -[:REGISTRA]-> (bien)")

#cargar_relacion_registra()

# 3) ¿Quién es el dueño del auto por el cual se lo acusa a “Carlos”?

def query5 ():
    with driver.session() as session:
        resultado = session.run("match ((robo:Hecho{robado:'automovil'})-[:SOSPECHOSO]->(carlos:Persona{nombre:'Carlos'})),((robo)-[:VICTIMA]->(dueño:Persona)) return dueño")
        
        node = resultado.single()[0] #si el resultado no fuese un único nodo, sacamos el .sigle(), antes de esto iría un for i in resultado
        nombre = node["nombre"]
        apellido = node["apellido"]
        print("El Dueño es:", nombre +" "+apellido)

#query5()

# 4) ¿Quiénes son los sospechosos de un hecho determinado?

def query2 ():
    with driver.session() as session:
        resultado = session.run("match (p:Persona),(h:Hecho{descripcion:'Robo de vehiculo mientras el dueño compraba en un supermercado'}) WHERE EXISTS ((h)-[:SOSPECHOSO]->(p)) RETURN p")
        for i in resultado:
            node = i[0] 
            nombre = node["nombre"]
            apellido = node["apellido"]
            print("Sospechoso:", nombre +" "+apellido)

#query2()
