# DOCUMENTACION TECNICA

## Sistema de Biblioteca Universitaria — Taller 1

**Paradigmas de Programacion:** POO, Estructurada, Imperativa, TAD

**Archivos:** `index.html` (aplicacion web) | `biblioteca.py` (interfaz de linea de comandos)

---

## 1. RESUMEN EJECUTIVO

El sistema de Biblioteca Universitaria es una aplicacion completa que gestiona el registro, busqueda, prestamo, devolucion y estadisticas de libros. Lo particular de este proyecto es que **cada funcionalidad esta implementada usando un paradigma de programacion diferente**, demostrando que un mismo problema puede resolverse de multiples formas.

### Funcionalidades implementadas

| # | Funcionalidad | Paradigma | Descripcion |
|---|--------------|-----------|-------------|
| 1 | Registrar libros | **POO** | Clase `Libro` con atributos privados, encapsulamiento y abstraccion |
| 2 | Buscar libros | **Estructurada** | Busqueda con `while`, `if/else`, sin `break`/`continue`/`return` en bucles |
| 3 | Prestar libros | **Imperativa** | Mutacion directa de variables globales, pasos secuenciales visibles |
| 4 | Devolver libros | **Imperativa** | Mismo patron: mutacion explicita de estado paso a paso |
| 5 | Estadisticas | **TAD** | Clase abstracta (especificacion) + clase concreta (implementacion) |

### Archivos del proyecto

- **`index.html`** — Aplicacion web completa (1419 lineas). Todo inline: HTML + CSS + JavaScript. Usa Tailwind CSS, animaciones, localStorage y la API de Google Books.
- **`biblioteca.py`** — Interfaz CLI en Python (725 lineas). Menu interactivo con los mismos 5 procesos y paradigmas.
- **`DOCUMENTACION.md`** — Este archivo.

---

## 2. PARADIGMA 1: PROGRAMACION ORIENTADA A OBJETOS (POO)

### 2.1 Que es POO

La POO organiza el codigo en **clases** que agrupan datos (atributos) y comportamiento (metodos) en una sola unidad. Los principios fundamentales son:

- **Encapsulamiento:** Los atributos internos estan protegidos y solo se accede mediante metodos controlados.
- **Abstraccion:** El usuario externo no necesita saber como funciona internamente, solo que metodos estan disponibles.
- **Instanciacion:** Cada objeto es una copia independiente con su propio estado.

### 2.2 Que se hizo

Se creo la clase `Libro` que es la base de todo el sistema. Cada libro es un objeto con atributos **privados** que no pueden modificarse directamente desde fuera de la clase.

### 2.3 Implementacion en JavaScript (`index.html`)

```javascript
// PARADIGMA 1: POO - Clase Libro
// Atributos PRIVADOS usando # (hash). Solo accesibles dentro de la clase.
class Libro {
    constructor(titulo, autor, isbn) {
        this.#titulo = titulo;          // Atributo privado
        this.#autor = autor;            // Atributo privado
        this.#isbn = isbn;              // Atributo privado
        this.#disponible = true;        // Estado interno
        this.#fechaPrestamo = null;     // Fecha de prestamo
    }

    // GETTERS: Lectura controlada (abstraccion)
    get titulo() { return this.#titulo; }
    get autor() { return this.#autor; }
    get isbn() { return this.#isbn; }
    get fechaPrestamo() { return this.#fechaPrestamo; }

    disponible() { return this.#disponible; }

    // Mutacion controlada: solo la clase puede cambiar su estado
    marcarPrestado() {
        this.#disponible = false;
        const ahora = new Date();
        this.#fechaPrestamo = ahora.toLocaleDateString() + ' ' + ahora.toLocaleTimeString();
    }

    marcarDevuelto() {
        this.#disponible = true;
        this.#fechaPrestamo = null;
    }

    // Serializacion para persistencia
    toJSON() {
        return { titulo: this.#titulo, autor: this.#autor, isbn: this.#isbn, disponible: this.#disponible };
    }

    static fromJSON(data) {
        const libro = new Libro(data.titulo, data.autor, data.isbn);
        if (!data.disponible) libro.marcarPrestado();
        return libro;
    }
}
```

**Por que es POO:**
- Los atributos `#titulo`, `#autor`, `#isbn`, `#disponible` son **privados** (solo accesibles dentro de la clase)
- Los getters permiten **leer** pero no **escribir** directamente
- La unica forma de cambiar el estado es usando `marcarPrestado()` o `marcarDevuelto()` (encapsulamiento)
- `static fromJSON()` es un metodo estatico que crea instancias desde datos serializados (factory method)

### 2.4 Implementacion en Python (`biblioteca.py`)

```python
class Libro:
    """
    Clase que representa un libro en la biblioteca.
    Atributos privados: __titulo, __autor, __isbn, __disponible, __fecha_prestamo
    """
    def __init__(self, titulo, autor, isbn):
        self.__titulo = titulo          # Atributo privado (name mangling)
        self.__autor = autor
        self.__isbn = isbn
        self.__disponible = True
        self.__fecha_prestamo = None

    # PROPIEDADES: Solo lectura (abstraccion)
    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def isbn(self):
        return self.__isbn

    @property
    def disponible(self):
        return self.__disponible

    def esta_disponible(self):
        return self.__disponible

    def marcar_prestado(self):
        self.__disponible = False
        self.__fecha_prestamo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def marcar_devuelto(self):
        self.__disponible = True
        self.__fecha_prestamo = None
```

**Por que es POO en Python:**
- Los atributos `__` usan **name mangling** de Python, lo que impide acceso externo directo
- Los decoradores `@property` crean propiedades de solo lectura
- El comportamiento esta encapsulado en metodos de la clase

---

## 3. PARADIGMA 2: PROGRAMACION ESTRUCTURADA

### 3.1 Que es Programacion Estructurada

Es un paradigma que organiza el codigo usando tres estructuras basicas:
- **Secuencia:** Instrucciones ejecutadas en orden lineal
- **Seleccion:** Decisiones con `if`/`else`
- **Iteracion:** Repeticiones con `while` o `for`

La regla clave es: **no se usan saltos incondicionales** (`break`, `continue`, `return` dentro de bucles). El flujo siempre es predecible y lineal.

### 3.2 Que se hizo

La funcion `buscarLibros()` implementa la busqueda de libros usando exclusivamente `while` + `if/else`, sin ningun `break`, `continue` o `return` dentro del bucle.

### 3.3 Implementacion en JavaScript

```javascript
// PARADIGMA 2: PROGRAMACION ESTRUCTURADA
// Busqueda usando while + if/else, sin break/continue/return en el bucle.
function buscarLibros() {
    const criterio = document.getElementById('buscarCriterio').value;
    const valor = document.getElementById('buscarInput').value.toLowerCase().trim();
    const resultados = [];
    let indice = 0;

    // WHILE: Iteracion controlada con indice manual
    while (indice < listaLibros.length) {
        let coincide = false;
        const libro = listaLibros[indice];

        // IF/ELSE IF/ELSE: Seleccion multiple para elegir campo
        if (criterio === '1') {
            if (libro.titulo.toLowerCase().indexOf(valor) !== -1) { coincide = true; }
        } else if (criterio === '2') {
            if (libro.autor.toLowerCase().indexOf(valor) !== -1) { coincide = true; }
        } else {
            if (libro.isbn.indexOf(valor) !== -1) { coincide = true; }
        }

        if (coincide) { resultados.push(libro); }
        indice = indice + 1;  // Incremento manual, sin i++
    }

    // Renderizar resultados
    let html = '';
    let i = 0;
    while (i < resultados.length) {
        const l = resultados[i];
        html += '<div>...' + l.titulo + '...</div>';
        i = i + 1;
    }
    contenedor.innerHTML = html;
}
```

**Por que es Estructurada:**
- Solo usa `while` para iterar (sin `for` con incremento automatico)
- Solo usa `if/else if/else` para seleccion
- **No hay `break`, `continue` ni `return` dentro del bucle** — el flujo siempre llega al `indice = indice + 1`
- El codigo es predecible: siempre ejecuta todas las iteraciones

### 3.4 Implementacion en Python

```python
def buscar_libros(lista_libros, criterio, valor):
    """
    Busqueda estrictamente estructurada:
    - Secuencia: paso a paso lineal
    - Seleccion: if/elif/else
    - Iteracion: while con indice manual
    - Sin break, continue o return dentro del bucle
    """
    resultados = []
    indice = 0
    cantidad_libros = len(lista_libros)

    while indice < cantidad_libros:
        coincide = False
        libro = lista_libros[indice]

        if criterio == 1:    # Buscar por titulo
            if valor.lower() in libro.titulo.lower():
                coincide = True
        elif criterio == 2:  # Buscar por autor
            if valor.lower() in libro.autor.lower():
                coincide = True
        else:                # Buscar por ISBN
            if valor in libro.isbn:
                coincide = True

        if coincide:
            resultados.append(libro)

        indice = indice + 1   # Siempre se incrementa, sin break

    return resultados
```

---

## 4. PARADIGMA 3: PROGRAMACION IMPERATIVA

### 4.1 Que es Programacion Imperativa

Es el paradigma mas antiguo: describe **COMO** se realizan las operaciones mediante instrucciones que modifican el estado del programa paso a paso. Las caracteristicas principales son:

- **Mutacion directa:** Las variables se modifican explicitamente
- **Estado compartido:** Variables globales representan el estado del sistema
- **Efectos colaterales:** Las funciones modifican datos externos
- **Flujo explicito:** Cada paso se ejecuta en orden visible

### 4.2 Que se hizo

Las funciones de **registrar**, **prestar** y **devolver** libros todas usan el patron imperativo: pasos explicitos con mutacion directa de variables globales.

### 4.3 Prestamo de libros — Cada paso documentado

```javascript
// PARADIGMA IMPERATIVO: Prestamo de libro
function confirmarPrestamo() {
    // PASO 1: LEER el estado actual
    const isbn = prestamoSeleccionado.isbn;

    // PASO 2: BUSCAR el libro (while + mutacion de indice)
    let encontrado = false;
    let idx = 0;
    while (idx < listaLibros.length) {
        if (listaLibros[idx].isbn === isbn) {
            encontrado = true;
        }
        idx = idx + 1;
    }

    // PASO 3: MUTAR el estado del libro
    // Antes: libro.disponible = true, fechaPrestamo = null
    prestamoSeleccionado.marcarPrestado();
    // Despues: libro.disponible = false, fechaPrestamo = "25/7/2026 14:30:00"

    // PASO 4: MUTAR el contador global
    // Antes: contadorIdPrestamo = N
    contadorIdPrestamo = contadorIdPrestamo + 1;
    // Despues: contadorIdPrestamo = N+1

    // PASO 5: MUTAR la lista de prestamos
    // Antes: prestamosRealizados = [...]
    prestamosRealizados.push({
        id: contadorIdPrestamo,
        isbn: isbn,
        titulo: prestamoSeleccionado.titulo,
        fecha: prestamoSeleccionado.fechaPrestamo,
        devuelto: false
    });
    // Despues: prestamosRealizados tiene un registro nuevo

    // PASO 6: PERSISTIR y ACTUALIZAR interfaz
    guardarDatos();
    renderizarLibros();
    renderizarSelectPrestamos();
    renderizarPrestamos();
    renderizarDevolver();
    renderizarEstadisticas();
}
```

**Por que es Imperativa:**
- Cada paso **modifica** una variable o el DOM de forma explicita
- Los comentarios documentan el estado ANTES y DESPUES de cada mutacion
- Las variables globales (`listaLibros`, `prestamosRealizados`, `contadorIdPrestamo`) son el estado compartido
- No hay retorno de valores puros; el efecto es la mutacion del estado

### 4.4 Devolucion de libros

```javascript
function confirmarDevolucion() {
    // PASO 1: Encontrar el prestamo por ID
    let idx = 0;
    while (idx < prestamosRealizados.length) {
        if (prestamosRealizados[idx].id === prestamoSeleccionado.id) {
            // PASO 2: MUTAR el prestamo
            // Antes: prestamo.devuelto = false
            prestamosRealizados[idx].devuelto = true;
            // Despues: prestamo.devuelto = true
        }
        idx = idx + 1;
    }

    // PASO 3: Encontrar el libro y MUTAR su estado
    let i = 0;
    while (i < listaLibros.length) {
        if (listaLibros[i].isbn === prestamoSeleccionado.isbn) {
            // Antes: libro.disponible = false
            listaLibros[i].marcarDevuelto();
            // Despues: libro.disponible = true, fechaPrestamo = null
        }
        i = i + 1;
    }

    // PASO 4: Persistir y actualizar todo
    guardarDatos();
    renderizarLibros();
    renderizarSelectPrestamos();
    renderizarPrestamos();
    renderizarDevolver();
    renderizarEstadisticas();
}
```

### 4.5 Busqueda por ISBN — Integracion con API

Se agrego una funcionalidad que usa **Google Books API** para buscar libros automaticamente por ISBN:

```javascript
async function buscarPorISBN() {
    const isbn = document.getElementById('isbnBusqueda').value.trim().replace(/-/g, '');

    // PASO 1: Hacer request HTTP a la API
    const response = await fetch('https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn);
    const data = await response.json();

    // PASO 2: Validar resultados
    if (!data.items || data.items.length === 0) {
        contenedor.innerHTML = '<p>No encontrado</p>';
        return;
    }

    // PASO 3: Extraer datos del libro
    const vol = data.items[0].volumeInfo;
    const titulo = vol.title;
    const autores = vol.authors.join(', ');
    const portada = vol.imageLinks.thumbnail;

    // PASO 4: Mutar el DOM para mostrar preview
    contenedor.innerHTML = '<div>...' + titulo + '...</div>';
}

function agregarLibroDesdeAPI(boton) {
    // TRANSFERIR datos de la API al formulario
    document.getElementById('regTitulo').value = boton.getAttribute('data-titulo');
    document.getElementById('regAutor').value = boton.getAttribute('data-autor');
    document.getElementById('regISBN').value = boton.getAttribute('data-isbn');
}
```

---

## 5. PARADIGMA 4: TIPOS ABSTRACTOS DE DATOS (TAD)

### 5.1 Que es un TAD

Un TAD separa la **especificacion** (QUE operaciones existen) de la **implementacion** (COMO se ejecutan). Se define una interfaz抽象a que puede tener multiples implementaciones concretas. Los principios son:

- **Especificacion:** Define que operaciones existen y que retornan
- **Implementacion:** El codigo concreto que realiza los calculos
- **No mutacion:** Las funciones solo LEEN datos, nunca los modifican
- **Encapsulamiento:** La implementacion puede cambiar sin afectar al usuario

### 5.2 Que se hizo

Se crearon dos clases:
1. `EstadisticasBiblioteca` — Clase **abstracta** (especificacion)
2. `CalculadoraEstadisticas` — Clase **concreta** (implementacion)

### 5.3 Especificacion — Clase Abstracta

```javascript
// PARADIGMA TAD: ESPECIFICACION
// Define QUE operaciones existen, sin implementar ninguna.
class EstadisticasBiblioteca {
    totalLibros() { throw new Error('Metodo no implementado'); }
    disponibles() { throw new Error('Metodo no implementado'); }
    prestados() { throw new Error('Metodo no implementado'); }
    porcentajeDisponibles() { throw new Error('Metodo no implementado'); }
    porcentajePrestados() { throw new Error('Metodo no implementado'); }
}
```

```python
# Python: Clase abstracta con ABC y @abstractmethod
from abc import ABC, abstractmethod

class EstadisticasBiblioteca(ABC):
    @abstractmethod
    def total_libros(self): pass

    @abstractmethod
    def disponibles(self): pass

    @abstractmethod
    def prestados(self): pass

    @abstractmethod
    def porcentaje_disponibles(self): pass

    @abstractmethod
    def porcentaje_prestados(self): pass

    @abstractmethod
    def catalogo_completo(self): pass

    @abstractmethod
    def libros_por_tema(self, tema): pass
```

**Por que es especificacion:**
- Solo define la **firma** de cada metodo (nombre, que retorna)
- No contiene logica concreta
- Lanza error si se intenta usar directamente
- En Python, `ABC` + `@abstractmethod` fuerza que subclases implementen todo

### 5.4 Implementacion — Clase Concreta

```javascript
// PARADIGMA TAD: IMPLEMENTACION CONCRETA
class CalculadoraEstadisticas extends EstadisticasBiblioteca {
    constructor(libros) {
        super();
        this._libros = libros;  // Referencia a datos (solo lectura)
    }

    totalLibros() { return this._libros.length; }

    disponibles() {
        let count = 0, i = 0;
        while (i < this._libros.length) {
            if (this._libros[i].disponible()) { count = count + 1; }
            i = i + 1;
        }
        return count;
    }

    prestados() {
        let count = 0, i = 0;
        while (i < this._libros.length) {
            if (!this._libros[i].disponible()) { count = count + 1; }
            i = i + 1;
        }
        return count;
    }

    porcentajeDisponibles() {
        const total = this.totalLibros();
        if (total === 0) return 0;
        return (this.disponibles() / total) * 100;
    }

    porcentajePrestados() {
        const total = this.totalLibros();
        if (total === 0) return 0;
        return (this.prestados() / total) * 100;
    }
}
```

```python
class CalculadoraEstadisticas(EstadisticasBiblioteca):
    def __init__(self, lista_libros):
        self._libros = lista_libros  # Solo lectura, sin mutacion

    def total_libros(self):
        return len(self._libros)

    def disponibles(self):
        count = 0
        i = 0
        while i < len(self._libros):
            if self._libros[i].esta_disponible():
                count = count + 1
            i = i + 1
        return count

    def prestados(self):
        count = 0
        i = 0
        while i < len(self._libros):
            if not self._libros[i].esta_disponible():
                count = count + 1
            i = i + 1
        return count

    def porcentaje_disponibles(self):
        total = self.total_libros()
        if total == 0:
            return 0
        return (self.disponibles() / total) * 100

    def porcentaje_prestados(self):
        total = self.total_libros()
        if total == 0:
            return 0
        return (self.prestados() / total) * 100
```

**Por que es implementacion:**
- Hereda de la clase abstracta y **sobreescribe** todos los metodos
- Contiene la logica concreta (contar con `while`, calcular porcentajes)
- Solo **lee** datos (`this._libros`), nunca los modifica
- La interfaz externa no cambia: se llama `calculadora.totalLibros()` igual que antes

---

## 6. INTEGRACION DE LOS 4 PARADIGMAS

Los 4 paradigmas no compiten entre si; **colaboran** en un mismo sistema:

```
┌─────────────────────────────────────────────┐
│              USUARIO                         │
│  Registrar | Buscar | Prestar | Estadisticas │
└──────┬──────────┬────────┬──────────┬───────┘
       │          │        │          │
       ▼          ▼        ▼          ▼
   ┌───────┐ ┌────────┐ ┌───────┐ ┌──────┐
   │  POO  │ │ESTRUCT.│ │IMPER. │ │ TAD  │
   │Libro()│ │buscar()│ │prestar│ │Calc()│
   └───┬───┘ └────┬───┘ └───┬───┘ └──┬───┘
       │          │         │        │
       ▼          ▼         ▼        ▼
   ┌──────────────────────────────────────┐
   │         listaLibros (global)          │
   │         prestamosRealizados (global)  │
   └──────────────────────────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   localStorage  │
            │  (persistencia) │
            └─────────────────┘
```

- **POO** crea los objetos `Libro` que todos los demas paradigmas usan
- **Estructurada** busca en la lista sin modificar nada
- **Imperativa** muta el estado (prestar/devolver) y actualiza la interfaz
- **TAD** calcula estadisticas solo leyendo los datos

---

## 7. PERSISTENCIA DE DATOS

### 7.1 localStorage (JavaScript)

Los datos se guardan en el navegador del usuario usando `localStorage`, que es un almacenamiento clave-valor persistente:

```javascript
function guardarDatos() {
    const datos = {
        libros: listaLibros.map(l => l.toJSON()),  // Serializar cada Libro
        prestamos: prestamosRealizados,
        contadorId: contadorIdPrestamo
    };
    localStorage.setItem('biblioteca', JSON.stringify(datos));
}

function cargarDatos() {
    const raw = localStorage.getItem('biblioteca');
    if (!raw) return;
    const datos = JSON.parse(raw);
    listaLibros = (datos.libros || []).map(d => Libro.fromJSON(d));  // Reconstruir objetos
    prestamosRealizados = datos.prestamos || [];
    contadorIdPrestamo = datos.contadorId || 0;
}
```

- **`toJSON()`** serializa cada `Libro` a un objeto plano (sin metodos, sin privados)
- **`fromJSON()`** reconstruye la instancia `Libro` desde el objeto plano
- Los datos persisten entre sesiones del navegador

### 7.2 Datos de prueba

Se incluyen 8 libros pre-cargados con ISBNs verificados:

| # | Titulo | Autor | ISBN |
|---|--------|-------|------|
| 1 | Cien anos de soledad | Gabriel Garcia Marquez | 978-0307474728 |
| 2 | Don Quijote de la Mancha | Miguel de Cervantes | 978-8420412146 |
| 3 | La Sombra del Viento | Carlos Ruiz Zafon | 978-84-08-04364-5 |
| 4 | Breve Historia del Tiempo | Stephen Hawking | 978-0553380163 |
| 5 | The Art of Computer Programming | Donald Knuth | 978-0201896831 |
| 6 | Materials Science and Engineering | William Callister | 978-1119405498 |
| 7 | Python Programming: An Introduction to Computer Science | John Zelle | 978-1590282755 |
| 8 | Discrete Mathematics and Its Applications | Kenneth Rosen | 978-0073383095 |

---

## 8. INTERFAZ DE USUARIO (HTML)

### 8.1 Diseno visual

- **Framework:** Tailwind CSS (via CDN)
- **Paleta:** Nocturne blue (`#0f172a`), emerald (`#10b981`), gold (`#f59e0b`)
- **Tipografia:** Inter (Google Fonts), pesos 300-900
- **Iconografia:** Lucide Icons (via CDN)

### 8.2 Animaciones y efectos

| Efecto | Descripcion |
|--------|-------------|
| **Splash Screen** | Pantalla de carga animada con libro flotante y barra de progreso |
| **Scroll Reveal** | Elementos aparecen con fade+slide al hacer scroll (IntersectionObserver) |
| **3D Hover** | Tarjetas con efecto 3D al pasar el mouse (perspective + rotate) |
| **Pulse Button** | Efecto ripple al hacer click en botones |
| **Modal Animations** | Modales con fade-in y scale-up |
| **Paradigm Badges** | Badges que agrandan al hover y abren modal de teoria |
| **Toast Notifications** | Notificaciones deslizantes desde la derecha |
| **Animated Counters** | Numeros que cuentan de 0 al valor final (requestAnimationFrame) |

### 8.3 API externa

Se integra **Google Books API** para busqueda automatica por ISBN:
- Endpoint: `https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}`
- No requiere API key para uso basico (limite: 1000 requests/dia)
- Retorna: titulo, autor, portada, descripcion, paginas, ISBN, categorias

---

## 9. COMO EJECUTAR

### Aplicacion Web
1. Abrir `index.html` en cualquier navegador moderno
2. Hacer click en "Cargar Demo" para cargar los 8 libros de prueba
3. Usar el menu de navegacion para explorar las 5 funcionalidades
4. Los badges de paradigma abren modales con teoria

### Aplicacion CLI (Python)
```bash
python biblioteca.py
```
- Menu interactivo con 8 opciones
- Los libros de prueba se cargan con la opcion 6
- Cada opcion indica que paradigma utiliza

---

## 10. CONCLUSIONES

Este proyecto demuestra que los 4 paradigmas de programacion no son mutuamente excluyentes sino **complementarios**:

- **POO** es ideal para modelar entidades del mundo real con estado y comportamiento encapsulado
- **Programacion Estructurada** garantiza codigo predecible y facil de seguir
- **Programacion Imperativa** es natural para operaciones que modifican el estado del sistema
- **TAD** permite separar la interfaz de la implementacion, facilitando mantenimiento y testing

La combinacion de todos ellos en una sola aplicacion produce un sistema robusto, documentado y mantenible.
