# =============================================================================
# SISTEMA DE BIBLIOTECA UNIVERSITARIA
# =============================================================================
# Taller 1 - Programacion Orientada a Objetos
# Universidade - Materia de Programacion
#
# Este sistema implementa 5 funcionalidades principales, cada una demostrando
# un paradigma de programacion distinto con comentarios explicitos que
# justifican su aplicacion segun la teoria de paradigmas.
#
# Funcionalidades:
#   1. Registrar Libros   -> POO (clases, encapsulamiento, abstraccion)
#   2. Buscar Libros      -> Programacion Estructurada (secuencia, seleccion, iteracion)
#   3. Prestar Libros     -> Programacion Imperativa (mutacion de estado, flujo explicito)
#   4. Devolver Libros    -> Programacion Imperativa (mutacion de estado, flujo explicito)
#   5. Mostrar Estadisticas -> Abstraccion de Datos / TAD (especificacion vs implementacion)
#
# Ejecucion:
#   python biblioteca.py
# =============================================================================

import os
from datetime import datetime
from abc import ABC, abstractmethod


# ******************************************************************************
# SECCION 1: REGISTRAR LIBROS
# ******************************************************************************
# PARADIGMA: Programacion Orientada a Objetos (POO)
#
# QUE HACE: Permite registrar nuevos libros en el sistema de biblioteca.
#   Cada libro se crea como un OBJETO de la clase Libro, con sus propios
#   atributos de estado encapsulados.
#
# QUE PARADIGMA USA: POO, basado en tres pilares fundamentales:
#   - CLASE: Plantilla que define que es un Libro (atributos y comportamientos).
#   - ENCAPSULAMIENTO: Los atributos son privados (prefijo __) y solo se
#     accede a ellos mediante metodos publicos (getters/setters). Esto
#     protege la integridad de los datos impidiendo acceso externo directo.
#   - ABSTRACCION: La clase Libro expone una interfaz simplificada (get_titulo,
#     esta_disponible, marcar_prestado) sin revelar como internamente se
#     gestiona el estado. El usuario de la clase no necesita saber que hay
#     un atributo __disponible, solo llama a esta_disponible().
#
# POR QUE REPRESENTA POO TEORICAMENTE:
#   En POO, el mundo real se modela como OBJETOS que combinan datos y
#   comportamiento en una sola unidad. Aqui, un "Libro" no es solo un string
#   o un diccionario: es un objeto con identidad propia, que puede saber si
#   esta disponible (metodo) y cambiar su estado de forma controlada.
#   La creacion de INSTANCIAS (Libro("Titulo", "Autor", "ISBN")) demuestra
#   que cada libro es una entidad independiente con su propio estado.
# ******************************************************************************


class Libro:
    """
    CLASE ABSTRACTA DE LIBRO.

    Representa la ABSTRACCION de un libro dentro del sistema.
    Define la INTERFAZ PUBLICA (que puede hacer un libro) y oculta
    la IMPLEMENTACION (como lo hace internamente).

    Atributos publicos: ninguno (todo esta encapsulado).
    Atributos privados: __titulo, __autor, __isbn, __disponible, __fecha_prestamo.

    Este diseno demuestra ENCAPSULAMIENTO: el estado interno del objeto
    solo puede ser modificado a traves de metodos controlados (marcar_prestado,
    marcar_devuelto), nunca desde fuera de la clase.
    """

    def __init__(self, titulo, autor, isbn):
        """
        CONSTRUCTOR: crea una instancia nueva de Libro.

        Los atributos se definen con prefijo __ (nombre mangling) para
        hacerlos PRIVADOS. Esto es encapsulamiento real: codigo externo
        no puede hacer libro.__titulo = "otro" directamente.
        """
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn
        self.__disponible = True
        self.__fecha_prestamo = None

    @property
    def titulo(self):
        """Propiedad de solo lectura: retorna el titulo del libro."""
        return self.__titulo

    @property
    def autor(self):
        """Propiedad de solo lectura: retorna el autor del libro."""
        return self.__autor

    @property
    def isbn(self):
        """Propiedad de solo lectura: retorna el ISBN del libro."""
        return self.__isbn

    @property
    def disponible(self):
        """Propiedad de solo lectura: retorna True si el libro esta disponible."""
        return self.__disponible

    @property
    def fecha_prestamo(self):
        """Propiedad de solo lectura: retorna la fecha del prestamo actual."""
        return self.__fecha_prestamo

    def esta_disponible(self):
        """
        Indica si el libro esta disponible para prestamo.
        ABSTRACCION: el usuario no necesita saber que hay un atributo
        __disponible, solo llama a este metodo y recibe True/False.
        """
        return self.__disponible

    def marcar_prestado(self):
        """
        Cambia el estado del libro a "prestado" y registra la fecha.
        ENCAPSULAMIENTO: solo este metodo puede modificar __disponible
        y __fecha_prestamo. Ningun codigo externo puede hacerlo directamente.
        """
        self.__disponible = False
        self.__fecha_prestamo = datetime.now().strftime("%d/%m/%Y %H:%M")

    def marcar_devuelto(self):
        """
        Cambia el estado del libro a "disponible" y limpia la fecha.
        ENCAPSULAMIENTO: solo este metodo puede modificar __disponible
        y __fecha_prestamo desde False/fecha a True/None.
        """
        self.__disponible = True
        self.__fecha_prestamo = None

    def __str__(self):
        """Representacion legible del libro para impresion por consola."""
        estado = "Disponible" if self.__disponible else "Prestado"
        return (f"  ISBN: {self.__isbn} | Titulo: {self.__titulo} | "
                f"Autor: {self.__autor} | Estado: {estado}")

    def to_dict(self):
        """
        ABSTRACCION: convierte el objeto a diccionario para acceso externo.
        En lugar de exponer atributos privados, se ofrece esta interfaz
        controlada que retorna una copia de los datos en formato seguro.
        """
        return {
            "titulo": self.__titulo,
            "autor": self.__autor,
            "isbn": self.__isbn,
            "disponible": self.__disponible,
            "fecha_prestamo": self.__fecha_prestamo
        }


# ******************************************************************************
# SECCION 2: BUSCAR LIBROS
# ******************************************************************************
# PARADIGMA: Programacion Estructurada
#
# QUE HACE: Permite buscar libros en el catalogo segun un criterio
#   (titulo, autor o ISBN) y retorna los resultados encontrados.
#
# QUE PARADIGMA USA: Programacion Estructurada, que se basa en el uso
#   ERICTO de tres estructuras de control basicas:
#   - SECUENCIA: Instrucciones que se ejecutan una tras otra, de arriba
#     hacia abajo, sin saltos.
#   - SELECCION: Estructuras if/elif/else que eligen entre caminos.
#   - ITERACION: Bucles for/while que repiten bloques de codigo.
#
#   PROHIBICION: No se usa break, continue, return dentro de bucles, ni
#   goto, ni saltos incondicionales de codigo. El flujo siempre es predecible.
#
# POR QUE REPRESENTA ESTRUCTURADA TEORICAMENTE:
#   La programacion estructurada (Dijkstra, 1968) demostro que todo programa
#   puede expresarse solo con secuencia, seleccion e iteracion. Esta funcion
#   es un ejemplo puro: recorre una lista (iteracion), elige campo (seleccion),
#   compara valores (seleccion), y acumula resultados (secuencia). No hay
#   saltos, no hay alteracion del flujo, el codigo se lee linealmente.
# ******************************************************************************

def buscar_libros(lista_libros, criterio, valor):
    """
    Busca libros en la lista segun un criterio y un valor de busqueda.

    PARADIGMA ESTRUCTURADO:
    - SECUENCIA: Las instrucciones se ejecutan linea tras linea.
    - SELECCION: if/elif/else elige el campo de busqueda.
    - ITERACION: while recorre la lista completa sin saltos.
    - PROHIBICION CUMPLIDA: No hay break, continue ni return dentro del bucle.
      El flujo es completamente predecible y lineal.

    Retorna una lista con los libros que coinciden con la busqueda.
    """
    resultados = []
    valor_minusculas = valor.lower()

    indice = 0
    cantidad_libros = len(lista_libros)

    while indice < cantidad_libros:
        libro_actual = lista_libros[indice]
        datos = libro_actual.to_dict()

        if criterio == "1":
            campo = datos["titulo"]
        elif criterio == "2":
            campo = datos["autor"]
        elif criterio == "3":
            campo = datos["isbn"]
        else:
            campo = ""
            print("  [!] Criterio no valido. Use 1, 2 o 3.")

        if len(campo) > 0 and valor_minusculas in campo.lower():
            resultados.append(libro_actual)

        indice = indice + 1

    return resultados


def mostrar_resultados_busqueda(resultados):
    """Muestra los resultados de una busqueda por consola."""
    if len(resultados) == 0:
        print("\n  No se encontraron libros con ese criterio.")
    else:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):")
        print("  " + "-" * 65)
        for libro in resultados:
            print(libro)
        print("  " + "-" * 65)


def menu_buscar_libros(lista_libros):
    """Sub-menu de busqueda. Orquesta la interaccion con el usuario."""
    print("\n  --- BUSCAR LIBROS ---")
    print("  Criterios de busqueda:")
    print("    1. Por titulo")
    print("    2. Por autor")
    print("    3. Por ISBN")
    criterio = input("  Seleccione criterio (1/2/3): ")
    valor = input("  Ingrese termino de busqueda: ")

    resultados = buscar_libros(lista_libros, criterio, valor)
    mostrar_resultados_busqueda(resultados)


# ******************************************************************************
# SECCION 3: PRESTAR Y DEVOLVER LIBROS
# ******************************************************************************
# PARADIGMA: Programacion Imperativa
#
# QUE HACE: Permite prestar un libro a un usuario (cambiar su estado a
#   "prestado") y devolverlo (cambiar su estado a "disponible").
#
# QUE PARADIGMA USA: Programacion Imperativa, que se centra en describir
#   PASO A PASO como se realizan las operaciones mediante instrucciones
#   que modifican el estado del programa. Caracteristicas clave:
#   - MUTACION DIRECTA: Las variables se modifican explicitamente en memoria
#     (ej: disponible = False, contador += 1, lista.append()).
#   - FLUJO EXPLICITO: Cada paso se ejecuta en orden, con control visible
#     de cuando cambia cada variable.
#   - ESTADO COMPARTIDO: Las variables globales (lista_libros,
#     prestamos_realizados) son el "estado" que estas funciones mutan.
#
# POR QUE REPRESENTA IMPERATIVA TEORICAMENTE:
#   El paradigma imperativo es el mas antiguo y natural: se describe el
#   ALGORITMO como una receta. "Primero busca el libro, luego verifica si
#   esta disponible, luego cambia su estado, luego registra el prestamo."
#   Cada instruccion MODIFICA el estado de la memoria. No se retornan
#   valores nuevos (como en funcional), se MUTAN los existentes.
#   Las variables globales lista_libros, prestamos_realizados y
#   contador_id_prestamo representan el ESTADO MUTABLE del sistema.
# ******************************************************************************

lista_libros = []
prestamos_realizados = []
contador_id_prestamo = 0


def registrar_libro_imperativo(titulo, autor, isbn):
    """
    Registra un libro nuevo en el sistema.
    PARADIGMA IMPERATIVO: Mutacion directa del estado global lista_libros.
    """
    nuevo_libro = Libro(titulo, autor, isbn)
    lista_libros.append(nuevo_libro)
    print(f"  [OK] Libro '{titulo}' registrado exitosamente.")


def prestar_libro():
    """
    Presta un libro al usuario si esta disponible.
    PARADIGMA IMPERATIVO: Control secuencial explicito con mutacion de estado.
    """
    print("\n  --- PRESTAR LIBRO ---")

    if len(lista_libros) == 0:
        print("  [!] No hay libros registrados en el sistema.")
        return

    isbn = input("  Ingrese el ISBN del libro a prestar: ")

    encontrado = False
    libro_actual = None
    indice = 0
    while indice < len(lista_libros):
        libro_candidato = lista_libros[indice]
        if libro_candidato.isbn == isbn:
            encontrado = True
            libro_actual = libro_candidato
        indice = indice + 1

    if encontrado is False:
        print(f"  [!] No se encontro un libro con ISBN '{isbn}'.")
        return

    if libro_actual.esta_disponible() is False:
        titulo = libro_actual.titulo
        print(f"  [!] El libro '{titulo}' ya esta prestado.")
        return

    libro_actual.marcar_prestado()

    contador_id_prestamo_nuevo = contador_id_prestamo + 1
    registro = {
        "id": contador_id_prestamo_nuevo,
        "isbn": isbn,
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "devuelto": False
    }
    prestamos_realizados.append(registro)

    titulo = libro_actual.titulo
    print(f"  [OK] Libro '{titulo}' prestado exitosamente.")
    print(f"       ID de prestamo: #{contador_id_prestamo_nuevo}")


def devolver_libro():
    """
    Devuelve un libro previamente prestado.
    PARADIGMA IMPERATIVO: Flujo secuencial con mutacion explicita de estado.
    """
    print("\n  --- DEVOLVER LIBRO ---")

    if len(prestamos_realizados) == 0:
        print("  [!] No hay prestamos registrados.")
        return

    print("  Prestamos activos:")
    hay_activos = False
    indice_p = 0
    while indice_p < len(prestamos_realizados):
        prestamo = prestamos_realizados[indice_p]
        if prestamo["devuelto"] is False:
            indice_l = 0
            libro_encontrado = None
            while indice_l < len(lista_libros):
                if lista_libros[indice_l].isbn == prestamo["isbn"]:
                    libro_encontrado = lista_libros[indice_l]
                indice_l = indice_l + 1
            if libro_encontrado is not None:
                pid = prestamo["id"]
                pisbn = prestamo["isbn"]
                pnombre = libro_encontrado.titulo
                pfecha = prestamo["fecha"]
                print(f"    ID #{pid} | ISBN: {pisbn} | Libro: {pnombre} | Fecha: {pfecha}")
                hay_activos = True
        indice_p = indice_p + 1

    if hay_activos is False:
        print("  No hay prestamos activos para devolver.")
        return

    try:
        id_prestamo = int(input("  Ingrese el ID del prestamo a devolver: "))
    except ValueError:
        print("  [!] Debe ingresar un numero entero valido.")
        return

    prestamo_encontrado = None
    indice = 0
    while indice < len(prestamos_realizados):
        if prestamos_realizados[indice]["id"] == id_prestamo:
            prestamo_encontrado = prestamos_realizados[indice]
        indice = indice + 1

    if prestamo_encontrado is None:
        print(f"  [!] No se encontro un prestamo con ID #{id_prestamo}.")
        return

    if prestamo_encontrado["devuelto"] is True:
        print(f"  [!] El prestamo #{id_prestamo} ya fue devuelto anteriormente.")
        return

    prestamo_encontrado["devuelto"] = True

    indice = 0
    while indice < len(lista_libros):
        if lista_libros[indice].isbn == prestamo_encontrado["isbn"]:
            lista_libros[indice].marcar_devuelto()
            print(f"  [OK] Libro '{lista_libros[indice].titulo}' devuelto exitosamente.")
        indice = indice + 1


# ******************************************************************************
# SECCION 4: MOSTRAR ESTADISTICAS
# ******************************************************************************
# PARADIGMA: Abstraccion de Datos (TAD - Tipo Abstracto de Datos)
#
# QUE HACE: Calcula metricas sobre el catalogo de libros (total,
#   disponibles, prestados, porcentajes) y las muestra por pantalla.
#
# QUE PARADIGMA USA: Abstraccion de Datos (TAD), que se basa en:
#   - ESPECIFICACION: Definir QUE OPERACIONES existen y QUE RETORNA cada una,
#     sin decir COMO se implementan internamente.
#   - IMPLEMENTACION: El codigo concreto que realiza los calculos, que puede
#     cambiar sin afectar a quien usa la especificacion.
#   - NO MUTACION: Las funciones calculan metricas SIN modificar la lista
#     original. Los datos de entrada quedan intactos.
#
# POR QUE REPRESENTA TAD TEORICAMENTE:
#   Un TAD separa el QUE (interfaz) del COMO (implementacion). Aqui,
#   EstadisticasBiblioteca es la ESPECIFICACION: define que existen
#   metodos como total_libros(), disponibles(), prestados(), etc.
#   CalculadoraEstadisticas es la IMPLEMENTACION: define que cada metodo
#   recorre la lista y cuenta. Si manana cambiamos la implementacion
#   (ej: usar una base de datos), la especificacion no cambia.
#   Ademas, ninguna funcion MODIFICA la lista original: solo LEE y CALCULA.
#   Esto garantiza que las estadisticas son un "snapshot" informativo.
# ******************************************************************************

class EstadisticasBiblioteca(ABC):
    """
    CLASE ABSTRACTA (ESPECIFICACION del TAD).

    Define la INTERFAZ PUBLICA de las operaciones estadisticas.
    Es la ESPECIFICACION: dice QUE METODOS existen y QUE RETORNA cada uno,
    pero NO dice COMO se implementan internamente.
    """

    @abstractmethod
    def total_libros(self):
        """ESPECIFICACION: Retorna el total de libros registrados."""
        pass

    @abstractmethod
    def disponibles(self):
        """ESPECIFICACION: Retorna la cantidad de libros disponibles."""
        pass

    @abstractmethod
    def prestados(self):
        """ESPECIFICACION: Retorna la cantidad de libros prestados."""
        pass

    @abstractmethod
    def porcentaje_disponibles(self):
        """ESPECIFICACION: Retorna el porcentaje de libros disponibles."""
        pass

    @abstractmethod
    def porcentaje_prestados(self):
        """ESPECIFICACION: Retorna el porcentaje de libros prestados."""
        pass

    @abstractmethod
    def catalogo_completo(self):
        """ESPECIFICACION: Retorna una lista con los titulos de todos los libros."""
        pass

    @abstractmethod
    def libros_por_tema(self, tema):
        """ESPECIFICACION: Retorna libros cuyo titulo contenga el tema dado."""
        pass


class CalculadoraEstadisticas(EstadisticasBiblioteca):
    """
    CLASE CONCRETA (IMPLEMENTACION del TAD).

    Hereda de EstadisticasBiblioteca (la especificacion) y proporciona
    la implementacion concreta de cada metodo.

    IMPORTANTE: Ningun metodo de esta clase MODIFICA la lista original.
    Solo LEE los datos y CALCULA resultados nuevos.
    """

    def __init__(self, lista_libros):
        """RECIBE la lista de libros como referencia de solo lectura."""
        self._libros = lista_libros

    def total_libros(self):
        """IMPLEMENTACION: Cuenta los elementos en la lista."""
        return len(self._libros)

    def disponibles(self):
        """IMPLEMENTACION: Cuenta libros donde disponible es True."""
        contador = 0
        indice = 0
        while indice < len(self._libros):
            if self._libros[indice].esta_disponible() is True:
                contador = contador + 1
            indice = indice + 1
        return contador

    def prestados(self):
        """IMPLEMENTACION: Cuenta libros donde disponible es False."""
        contador = 0
        indice = 0
        while indice < len(self._libros):
            if self._libros[indice].esta_disponible() is False:
                contador = contador + 1
            indice = indice + 1
        return contador

    def porcentaje_disponibles(self):
        """IMPLEMENTACION: Calcula (disponibles / total) * 100."""
        total = self.total_libros()
        disp = self.disponibles()
        if total > 0:
            return (disp / total) * 100
        return 0.0

    def porcentaje_prestados(self):
        """IMPLEMENTACION: Calcula (prestados / total) * 100."""
        total = self.total_libros()
        pres = self.prestados()
        if total > 0:
            return (pres / total) * 100
        return 0.0

    def catalogo_completo(self):
        """IMPLEMENTACION: Recorre la lista y extrae los titulos."""
        titulos = []
        indice = 0
        while indice < len(self._libros):
            titulos.append(self._libros[indice].titulo)
            indice = indice + 1
        return titulos

    def libros_por_tema(self, tema):
        """IMPLEMENTACION: Recorre la lista y filtra por tema."""
        tema_minuscula = tema.lower()
        encontrados = []
        indice = 0
        while indice < len(self._libros):
            titulo_libro = self._libros[indice].titulo
            if tema_minuscula in titulo_libro.lower():
                encontrados.append(titulo_libro)
            indice = indice + 1
        return encontrados


def mostrar_estadisticas(lista):
    """
    Funcion que usa el TAD para mostrar estadisticas por consola.
    Delega todo a CalculadoraEstadisticas (implementacion concreta del TAD).
    """
    print("\n  --- ESTADISTICAS DE LA BIBLIOTECA ---")
    print("  " + "=" * 45)

    calc = CalculadoraEstadisticas(lista)

    total = calc.total_libros()
    disp = calc.disponibles()
    pres = calc.prestados()
    pct_disp = calc.porcentaje_disponibles()
    pct_pres = calc.porcentaje_prestados()
    catalogo = calc.catalogo_completo()
    ciencia = calc.libros_por_tema("ciencia")

    print(f"  Total de libros registrados:  {total}")
    print(f"  Libros disponibles:           {disp} ({pct_disp:.1f}%)")
    print(f"  Libros prestados:             {pres} ({pct_pres:.1f}%)")
    print("  " + "-" * 45)

    if len(catalogo) > 0:
        print("  Catalogo completo:")
        for titulo in catalogo:
            print(f"    - {titulo}")
    else:
        print("  El catalogo esta vacio.")

    if len(ciencia) > 0:
        print("  " + "-" * 45)
        print(f"  Libros con 'ciencia' en el titulo: {len(ciencia)}")
        for t in ciencia:
            print(f"    - {t}")

    print("  " + "=" * 45)


# ******************************************************************************
# SECCION 5: INTERFAZ - MENU INTERACTIVO
# ******************************************************************************
# El menu principal usa un CICLO ESTRUCTURADO (while con bandera) para
# permitir al usuario probar todas las funcionalidades del sistema.
# El ciclo es predecible: inicia con continuar=True y termina cuando
# el usuario selecciona la opcion de salida.
# ******************************************************************************

def cargar_datos_prueba():
    """Carga 8 libros de ejemplo para facilitar las pruebas del sistema."""
    libros_ejemplo = [
        ("Cien Anos de Soledad", "Gabriel Garcia Marquez", "978-0307474728"),
        ("Don Quijote de la Mancha", "Miguel de Cervantes", "978-8420412146"),
        ("La Sombra del Viento", "Carlos Ruiz Zafon", "978-84-08-04364-5"),
        ("Breve Historia del Tiempo", "Stephen Hawking", "978-0553380163"),
        ("El Arte de Programar", "Donald Knuth", "978-0201896831"),
        ("Ciencia e Ingenieria de Materiales", "William Callister", "978-1119405498"),
        ("Python Programming: An Introduction to Computer Science", "John Zelle", "978-1590282755"),
        ("Matematicas Discretas", "Kenneth Rosen", "978-0073383095"),
    ]

    for titulo, autor, isbn in libros_ejemplo:
        registrar_libro_imperativo(titulo, autor, isbn)


def mostrar_menu():
    """Muestra el menu principal con las opciones disponibles."""
    print()
    print("  ===============================================")
    print("      SISTEMA DE BIBLIOTECA UNIVERSITARIA")
    print("  ===============================================")
    print("  1. Registrar libro          [POO]")
    print("  2. Buscar libros            [Estructurada]")
    print("  3. Prestar libro            [Imperativa]")
    print("  4. Devolver libro           [Imperativa]")
    print("  5. Mostrar estadisticas     [TAD]")
    print("  6. Cargar datos de prueba")
    print("  7. Mostrar todos los libros")
    print("  0. Salir")
    print("  ===============================================")
    print("  Los corchetes indican el paradigma utilizado.")
    print()


def menu_registrar():
    """Sub-menu para registrar un libro nuevo. Crea instancias de la clase Libro (POO)."""
    print("\n  --- REGISTRAR LIBRO (POO) ---")
    titulo = input("  Titulo: ").strip()
    autor = input("  Autor: ").strip()
    isbn = input("  ISBN: ").strip()

    if not titulo or not autor or not isbn:
        print("  [!] Todos los campos son obligatorios.")
        return

    indice = 0
    duplicado = False
    while indice < len(lista_libros):
        if lista_libros[indice].isbn == isbn:
            duplicado = True
        indice = indice + 1

    if duplicado is True:
        print(f"  [!] Ya existe un libro con ISBN '{isbn}'.")
        return

    registrar_libro_imperativo(titulo, autor, isbn)


def mostrar_todos_los_libros():
    """Muestra todos los libros registrados en el catalogo."""
    print("\n  --- CATALOGO COMPLETO ---")
    if len(lista_libros) == 0:
        print("  No hay libros registrados.")
        return

    print(f"  Total: {len(lista_libros)} libro(s)")
    print("  " + "-" * 65)
    for libro in lista_libros:
        print(libro)
    print("  " + "-" * 65)


def main():
    """
    Funcion principal: bucle del menu interactivo.
    Usa un CICLO ESTRUCTURADO (while con bandera 'continuar').
    """
    print("\n  Bienvenido al Sistema de Biblioteca Universitaria.")
    print("  Este sistema demuestra 4 paradigmas de programacion.")
    print("  Cada opcion del menu indica entre corchetes el paradigma usado.\n")

    continuar = True

    while continuar:
        mostrar_menu()
        opcion = input("  Seleccione una opcion (0-7): ")

        if opcion == "1":
            menu_registrar()
        elif opcion == "2":
            menu_buscar_libros(lista_libros)
        elif opcion == "3":
            prestar_libro()
        elif opcion == "4":
            devolver_libro()
        elif opcion == "5":
            mostrar_estadisticas(lista_libros)
        elif opcion == "6":
            print("\n  Cargando libros de ejemplo...")
            cargar_datos_prueba()
            print(f"  [OK] Se cargaron {len(lista_libros)} libros de prueba.")
        elif opcion == "7":
            mostrar_todos_los_libros()
        elif opcion == "0":
            print("\n  Saliendo del sistema...")
            print("  Gracias por usar la Biblioteca Universitaria.\n")
            continuar = False
        else:
            print("\n  [!] Opcion no valida. Ingrese un numero del 0 al 7.")

        if continuar:
            input("\n  Presione Enter para continuar...")


if __name__ == "__main__":
    main()

