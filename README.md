# Libros Universitarios - Sistema de Biblioteca

Sistema interactivo de gestion de biblioteca universitaria que implementa **4 paradigmas de programacion** en una sola aplicacion. Cada funcionalidad demuestra un enfoque distinto del desarrollo de software.

## Paradigmas de Programacion

| # | Funcionalidad | Paradigma | Descripcion |
|---|--------------|-----------|-------------|
| 1 | Registrar libros | **POO** | Clase Libro con atributos privados, encapsulamiento y abstraccion |
| 2 | Buscar libros | **Estructurada** | Busqueda con while, if/else, sin break/continue/return en bucles |
| 3 | Prestar libros | **Imperativa** | Mutacion directa de variables globales, pasos secuenciales visibles |
| 4 | Devolver libros | **Imperativa** | Mismo patron: mutacion explicita de estado paso a paso |
| 5 | Estadisticas | **TAD** | Clase abstracta (especificacion) + clase concreta (implementacion) |

## Tecnologias

- **Python** - Interfaz de linea de comandos (CLI)
- **HTML/CSS/JavaScript** - Aplicacion web completa
- **Tailwind CSS** - Framework de estilos (via CDN)
- **Google Books API** - Busqueda automatica de libros por ISBN
- **localStorage** - Persistencia de datos en el navegador

## Estructura del Proyecto

`
├── index.html          # Aplicacion web completa (~1400 lineas)
├── biblioteca.py       # Interfaz CLI en Python (725 lineas)
├── DOCUMENTACION.md    # Documentacion tecnica detallada
├── DOCUMENTACION.docx  # Documento Word con documentacion
├── .gitignore          # Archivos ignorados por Git
└── README.md           # Este archivo
`

## Como Ejecutar

### Aplicacion Web

1. Abrir index.html en cualquier navegador moderno
2. Hacer click en **"Cargar Demo"** para cargar 8 libros de prueba
3. Usar el menu de navegacion para explorar las funcionalidades
4. Los badges de paradigma abren modales con teoria

### Aplicacion CLI (Python)

`ash
python biblioteca.py
`

- Menu interactivo con 8 opciones
- Los libros de prueba se cargan con la opcion 6
- Cada opcion indica que paradigma utiliza

## Funcionalidades

### 1. Registrar Libros (POO)
- Clase Libro con atributos privados (#titulo, #autor, #isbn)
- Encapsulamiento real: acceso solo mediante getters
- Busqueda automatica por ISBN via Google Books API

### 2. Buscar Libros (Estructurada)
- Busqueda por titulo, autor o ISBN
- Implementada exclusivamente con while + if/else
- Sin break, continue ni return dentro del bucle

### 3. Prestar Libros (Imperativa)
- Mutacion directa de variables globales
- Control secuencial explicito paso a paso
- Registro de prestamos con ID unico

### 4. Devolver Libros (Imperativa)
- Flujo secuencial con mutacion explicita de estado
- El libro vuelve a disponible y el prestamo se marca como devuelto

### 5. Estadisticas (TAD)
- Clase abstracta EstadisticasBiblioteca (especificacion)
- Clase concreta CalculadoraEstadisticas (implementacion)
- Calculo de totales, disponibilidad y porcentajes

## Datos de Prueba

El sistema incluye 8 libros pre-cargados:

| Titulo | Autor | ISBN |
|--------|-------|------|
| Cien Anos de Soledad | Gabriel Garcia Marquez | 978-0307474728 |
| Don Quijote de la Mancha | Miguel de Cervantes | 978-8420412146 |
| La Sombra del Viento | Carlos Ruiz Zafon | 978-84-08-04364-5 |
| Breve Historia del Tiempo | Stephen Hawking | 978-0553380163 |
| El Arte de Programar | Donald Knuth | 978-0201896831 |
| Ciencia e Ingenieria de Materiales | William Callister | 978-1119405498 |
| Python Programming | John Zelle | 978-1590282755 |
| Matematicas Discretas | Kenneth Rosen | 978-0073383095 |

## Autor

**EduarJIM** - eworstef12@gmail.com

## Licencia

Proyecto educativo - Taller 1 de Programacion Orientada a Objetos