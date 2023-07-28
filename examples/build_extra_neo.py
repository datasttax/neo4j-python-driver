// Iniciar NEO -------------------

sudo update-alternatives --config java   // cambiar version de java

sudo $NEO4J_HOME/bin/neo4j console   // neo bin/neo4j start

abrir http://localhost:7474     // ruta del browser


// ---------------------------------------------------
// INSERTAR DATOS
// Crear personas involucradas (testigo, victima o sospechoso)
CREATE
(persona1:PERSONA{nombre:"Carlos Rojo", documento: 44800933, telefono: 11346273, trabajo:"Jardinero"}),
(persona2:PERSONA{nombre:"Pedro Verde", documento: 42938172, telefono: 11726481, trabajo:null}),
(persona3:PERSONA{nombre:"Marcos Amarillo", documento: 46734543, telefono: 114623423, trabajo:"Constructor"}),
(persona4:PERSONA{nombre:"Franco Violeta", documento: 41346823, telefono: 116345234, trabajo:"Arquitecto"}),

// Crear bienes de esas personas
(casa1:BIEN{descripción:"Mansion Madrid", tipo:"Casa"}),
(auto1:BIEN{descripción:"Ferrari Rojo", tipo:"Auto"}),

// Crear cuentas bancarias de esas personas
(cuenta1:CUENTA{banco:"Brubank", tipo:"Titular", numero:19283137}),
(cuenta2:CUENTA{banco:"BBVA", tipo:"Asociado", numero:93834712}),

// Crear delitos
(delito1:DELITO{tipo:"Robo", descripcion:"Robo de auto agravado por arma blanca", fecha:"14/07/2023", hora:"15:20", barrio:"Belgrano"}),
(delito2:DELITO{tipo:"Homicidio", descripcion:"Homicidio agravado por el vinculo", fecha:"08/09/2023", hora:"17:45", barrio:"Palermo"}),

// Crear relatos de los delitos
(relato1:RELATO{descripcion:"Mansion Madrid", tipo:"Casa"}),


// ---------------------------------------------------
// RELACIONES
// Registrar llamadas (entre personas involucradas)
(persona1)-[:LLAMADA{fecha:"14/07/2023", hora:"15:20"}]-> (persona2),

// Relacionar bienes
(persona1)-[:DUENO]-> (casa1),
(persona2)-[:DUENO]-> (auto1),

// Relacionar cuentas
(persona1)-[:TIENE]-> (cuenta1),
(persona2)-[:TIENE]-> (cuenta2),

// Relacionar relatos
(persona1)-[:DECLARA]-> (relato1),
(delito1)-[:TIENE]-> (relato1),

// Relacionar personas con delitos
(persona1)-[:SOSPECHOSO]-> (delito1),
(persona2)-[:VICTIMA]-> (delito1),
(persona3)-[:TESTIGO{tipo: "A favor"}]-> (delito1),
(persona4)-[:TESTIGO{tipo: "En contra"}]-> (delito1),

// Relacionar bienes afectados a delito
(delito1)-[:ASOCIADO]-> (auto1)


// ---------------------------------------------------
// QUERIES

// 1. Cuáles son los hechos que no tienen testigos
MATCH (delito:DELITO)
WHERE NOT EXISTS((:PERSONA)-[:TESTIGO]-> (delito)) 
RETURN delito

// 2. Quiénes son los sospechosos de un hecho determinado
MATCH (sospechoso:PERSONA)-[:SOSPECHOSO]-> (delito:DELITO{descripcion:"Robo de auto agravado por arma blanca"})
RETURN sospechoso


// 3. Quiénes son los testigos que favorecen a “Carlos” en el “Robo” de un “Auto”
MATCH (testigo:PERSONA)-[:TESTIGO{tipo: "A favor"}]-> (delito:DELITO{descripcion:"Robo de auto agravado por arma blanca", tipo:"Robo"})
WHERE (:PERSONA{nombre:"Carlos Rojo"})-[:SOSPECHOSO]-> (delito)
RETURN testigo


// 4. Cuáles son los bienes que pertenecen a personas sin trabajo
MATCH (persona:PERSONA)-[:DUENO]-> (bien:BIEN)
WHERE persona.trabajo IS NULL
RETURN bien

// 5. Quién es el dueño del auto por el cual se lo acusa a “Carlos”
MATCH (dueno:PERSONA)-[:DUENO]-> (bien:BIEN) 
WHERE ((:PERSONA{nombre: "Carlos Rojo"})-[:SOSPECHOSO]-> (:DELITO)-[:ASOCIADO]-> (bien:BIEN))
RETURN dueno

// otra forma usando 2 MATCH
MATCH (dueno:PERSONA)-[:DUENO]-> (bien:BIEN) 
MATCH (delito:DELITO)-[:ASOCIADO]-> (bien)
WHERE (:PERSONA{nombre: "Carlos Rojo"})-[:SOSPECHOSO]-> (delito)
RETURN dueno


// 6. Cuántos robos de casa se produjeron entre abril y mayo del 2019 en el barrio de Belgrano
MATCH(delito:DELITO{tipo:"Robo"})
WHERE delito.lugar = "Belgrano" AND delito.fecha >= "01/04/2019" AND delito.fecha <= "31/05/2019"
RETURN COUNT(delito)
