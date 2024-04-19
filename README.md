# Melp
REST API with CRUD operations for Melp startup.

### Descripción
Esta API RESTful proporciona información sobre restaurantes y permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar). La API está diseñada para ser utilizada por la aplicación Melp, que ofrece información útil sobre restaurantes a los usuarios.

### Funcionalidades

* **Importar datos:** Se incluye un script que permite importar datos de restaurantes desde un archivo CSV.
* **Operaciones CRUD:**
    * **Crear:** Agrega un nuevo restaurante a la base de datos.
    * **Leer:** Obtiene una lista de restaurantes o un restaurante específico por ID.
    * **Actualizar:** Modifica la información de un restaurante existente.
    * **Eliminar:** Elimina un restaurante de la base de datos.
* **Estadísticas:** El endpoint `/restaurants/statistics` devuelve estadísticas sobre los restaurantes dentro de un radio específico alrededor de un punto dado.

### Tecnologías Utilizadas
* **Backend:** Python
* **Base de datos:** PostgreSQL con la extensión PostGIS
* **Framework web:** Flask
* **Control de versiones:** Git
* **Despliegue:** Heroku

### Endpoints de la API

**Restaurantes:**

* `GET /restaurants`: Obtiene una lista de todos los restaurantes.
* `GET /restaurants/{id}`: Obtiene un restaurante por ID.
* `POST /restaurants`: Crea un nuevo restaurante.
* `PUT /restaurants/{id}`: Actualiza un restaurante existente.
* `DELETE /restaurants/{id}`: Elimina un restaurante.

**Estadísticas:**

* `GET /restaurants/statistics?latitude=x&longitude=y&radius=z`: Obtiene estadísticas de los restaurantes dentro de un radio específico alrededor de un punto dado.
