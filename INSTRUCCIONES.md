# Guia de Instalacion y Ejecucion

Guia detallada para la puesta en marcha, verificacion y pruebas de carga del entorno con HAProxy, Docker, FastAPI y React.

## Tabla de Contenidos

1. [Prerrequisitos](#1-prerrequisitos)
2. [Instalacion de Docker](#2-instalacion-de-docker)
3. [Verificacion de Docker](#3-verificacion-de-docker)
4. [Estructura del Proyecto](#4-estructura-del-proyecto)
5. [Construccion y Despliegue](#5-construccion-y-despliegue)
6. [Verificacion de Servicios](#6-verificacion-de-servicios)
7. [Pruebas de Funcionamiento](#7-pruebas-de-funcionamiento)
8. [Verificacion del Balanceo de Carga](#8-verificacion-del-balanceo-de-carga)
9. [Monitoreo en HAProxy Stats](#9-monitoreo-en-haproxy-stats)
10. [Pruebas de Rendimiento con JMeter](#10-pruebas-de-rendimiento-con-jmeter)
11. [Comandos Utiles de Docker](#11-comandos-utiles-de-docker)
12. [Detencion y Limpieza](#12-detencion-y-limpieza)
13. [Solucion de Problemas Frecuentes](#13-solucion-de-problemas-frecuentes)

---

## 1. Prerrequisitos

### Software

- **Docker Desktop** (en Windows/macOS) o **Docker Engine + Docker Compose v2** (en Linux).
- **Git** (opcional, para clonar y gestionar el repositorio).
- **Apache JMeter 5.6+** (opcional, para ejecutar las pruebas de carga).
- **Java JRE/JDK 8+** (necesario solo si se utiliza JMeter).
- **curl** o PowerShell (para pruebas de endpoint por consola).

### Requisitos del Sistema

- Sistema Operativo: Windows 10/11 (64-bit), Linux o macOS.
- Puertos libres: `80` (HAProxy) y `3000` (Frontend).

---

## 2. Instalacion de Docker

### En Windows

1. Descargar el instalador desde el sitio oficial de Docker: https://www.docker.com/products/docker-desktop/
2. Ejecutar `Docker Desktop Installer.exe`.
3. Asegurarse de mantener seleccionada la opcion de usar WSL 2.
4. Reiniciar el equipo si el instalador lo solicita.
5. Iniciar Docker Desktop y esperar hasta que el servicio este en estado activo (running).

### En macOS

1. Descargar Docker Desktop (Intel o Apple Silicon segun el procesador) desde el sitio web oficial.
2. Abrir el archivo `.dmg` y arrastrar Docker a la carpeta `Applications`.
3. Abrir la aplicacion y conceder los permisos del sistema requeridos.

### En Linux (Ubuntu / Debian)

```bash
# Actualizar indices de paquetes
sudo apt-get update

# Instalar dependencias previas
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Agregar clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine y Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Permitir ejecutar docker sin sudo (opcional)
sudo usermod -aG docker $USER
```

---

## 3. Verificacion de Docker

Abrir una terminal y ejecutar las siguientes comprobaciones:

```bash
# Version de Docker
docker --version

# Version de Docker Compose
docker compose version

# Estado del demonio
docker info
```

Si `docker info` responde sin errores de conexion con el socket o demonio, el entorno esta listo.

---

## 4. Estructura del Proyecto

```
docker-haproxy-main/
|-- backend/
|   |-- Dockerfile
|   `-- main.py
|-- frontend/
|   |-- src/
|   |   |-- App.jsx
|   |   `-- main.jsx
|   |-- Dockerfile
|   |-- index.html
|   |-- package.json
|   `-- vite.config.js
|-- haproxy/
|   `-- haproxy.cfg
|-- jmeter/
|   `-- haproxy_load_test.jmx
|-- docs/
|   `-- architecture.png
|-- docker-compose.yml
|-- INSTRUCCIONES.md
`-- README.md
```

---

## 5. Construccion y Despliegue

Situarse en el directorio raiz del proyecto (donde reside `docker-compose.yml`):

```bash
cd docker-haproxy-main
```

### Iniciar en primer plano

Permite observar las salidas de log directamente en la terminal:

```bash
docker compose up --build
```

### Iniciar en segundo plano (modo detached)

```bash
docker compose up --build -d
```

---

## 6. Verificacion de Servicios

Listar los contenedores creados para confirmar que esten en ejecucion:

```bash
docker compose ps
```

Deberian visualizarse 5 contenedores activos:
- `docker-haproxy-main-backend1-1` (puerto interno 8000)
- `docker-haproxy-main-backend2-1` (puerto interno 8000)
- `docker-haproxy-main-backend3-1` (puerto interno 8000)
- `docker-haproxy-main-frontend-1` (puerto 3000 mapeado)
- `docker-haproxy-main-haproxy-1`  (puerto 80 mapeado)

Para inspeccionar los logs:

```bash
# Todos los servicios
docker compose logs -f

# Un servicio especifico
docker compose logs backend1
docker compose logs haproxy
docker compose logs frontend
```

---

## 7. Pruebas de Funcionamiento

### 7.1 Acceso al Frontend

Abrir en el navegador:
`http://localhost:3000`

Se presentara la interfaz web que consulta al backend y despliega la respuesta indicando que servidor respondio.

### 7.2 Acceso a la API a traves de HAProxy

Abrir en el navegador o consultar via terminal:
`http://localhost/api/hello`

Ejemplo de respuesta:

```json
{
  "message": "Hello from FastAPI! (served by backend1)",
  "instance": "backend1",
  "hostname": "9d8ef2a1c0b3"
}
```

---

## 8. Verificacion del Balanceo de Carga

Para comprobar que las peticiones se alternan entre las tres instancias disponibles bajo el esquema round-robin:

### En PowerShell (Windows)

```powershell
1..9 | ForEach-Object {
    $res = Invoke-RestMethod http://localhost/api/hello
    Write-Host "Peticion $_ -> $($res.instance)"
}
```

### En Bash (Linux / macOS)

```bash
for i in {1..9}; do
    echo -n "Peticion $i: "
    curl -s http://localhost/api/hello | grep -o '"instance":"[^"]*"'
done
```

Resultado esperado: la propiedad `instance` ira alternando secuencialmente entre `backend1`, `backend2` y `backend3`.

---

## 9. Monitoreo en HAProxy Stats

El balanceador expone una consola de monitoreo en tiempo real:

- URL: `http://localhost/stats`
- Frecuencia de refresco: Cada 5 segundos.

Informacion disponible:
- Estado operativo de cada servidor (`UP` o `DOWN`).
- Total de peticiones recibidas y distribuidas por cada nodo.
- Tiempos de respuesta y volumen de bytes procesados.

---

## 10. Pruebas de Rendimiento con JMeter

### 10.1 Preparacion

1. Descargar Apache JMeter desde https://jmeter.apache.org/download_jmeter.cgi
2. Descomprimir el archivo en una ruta accesible.
3. Ejecutar el binario correspondiente:
   - Windows: `bin/jmeter.bat`
   - Linux/macOS: `bin/jmeter.sh`

### 10.2 Carga del Plan

1. Ir a **File -> Open**.
2. Navegar hasta `docker-haproxy-main/jmeter/haproxy_load_test.jmx`.
3. Seleccionar el archivo y abrirlo.

### 10.3 Parametros de la Prueba

El plan cuenta con la siguiente configuracion base:
- Grupo de hilos (Thread Group): 20 usuarios concurrentes.
- Periodo de subida (Ramp-Up): 10 segundos.
- Contador de bucles (Loop Count): 50 iteraciones por hilo.
- Total de solicitudes: 1,000 peticiones HTTP GET a `http://localhost:80/api/hello`.

### 10.4 Ejecucion y Analisis

1. Presionar el boton **Start** (icono de reproduccion verde o `Ctrl+R`).
2. Una vez concluida la prueba, revisar los componentes de resultados:
   - **Summary Report**: Evaluar throughput, porcentaje de error (debe mantenerse en 0%) y tiempos promedio de respuesta.
   - **Response Time Graph**: Visualizar la dispersion de tiempos de respuesta en el tiempo.
   - **View Results Tree**: Examinar el codigo de estado y cuerpo de peticiones individuales.

---

## 11. Comandos Utiles de Docker

### Gestion de Contenedores

```bash
# Ver contenedores en ejecucion
docker compose ps

# Ver todos los contenedores (incluyendo detenidos)
docker compose ps -a

# Reiniciar todos los servicios
docker compose restart

# Reiniciar un contenedor especifico
docker compose restart backend2
```

### Inspeccion de Recursos

```bash
# Ver consumo de CPU y memoria de los contenedores
docker stats

# Ver redes activas de Docker
docker network ls

# Inspeccionar la red interna del proyecto
docker network inspect docker-haproxy-main_app-net
```

### Ejecucion de Comandos Internos

```bash
# Acceder a la shell de un backend
docker compose exec backend1 sh

# Comprobar version de Python dentro del backend
docker compose exec backend1 python --version

# Acceder a la shell del frontend
docker compose exec frontend sh
```

---

## 12. Detencion y Limpieza

### Detener los servicios sin eliminarlos

```bash
docker compose stop
```

### Detener y eliminar contenedores y redes

```bash
docker compose down
```

### Eliminar contenedores, redes e imagenes generadas

```bash
docker compose down --rmi all
```

---

## 13. Solucion de Problemas Frecuentes

### Error: "Cannot connect to the Docker daemon"

- **Causa**: El servicio de Docker Desktop o el demonio dockerd no se encuentra en ejecucion.
- **Solucion**: Iniciar Docker Desktop y aguardar a que el estado confirme que el motor esta activo antes de volver a ejecutar comandos de Docker.

### Error: "port is already allocated" (conflicto en puerto 80 o 3000)

- **Causa**: Otro proceso en el host (como IIS, Apache o un servidor web local) ya esta escuchando en el puerto solicitado.
- **Solucion**:
  - En Windows, identificar que proceso ocupa el puerto:
    ```cmd
    netstat -ano | findstr :80
    ```
  - Detener el proceso o servicio conflictivo, o bien reasignar el puerto en `docker-compose.yml` (por ejemplo, cambiando `"80:80"` por `"8080:80"`).

### El frontend reporta "Fallo en la llamada a la API"

- **Causa**: El frontend no logra resolver o comunicarse con el proxy de HAProxy.
- **Solucion**:
  1. Verificar que HAProxy y las tres instancias esten arriba mediante `docker compose ps`.
  2. Probar el endpoint directamente desde la terminal con `curl http://localhost/api/hello`.
  3. Comprobar los logs de HAProxy con `docker compose logs haproxy`.

### Las peticiones no balancean y responden siempre desde la misma instancia

- **Causa**: Health checks fallando o contenedores no registrados correctamente en el pool.
- **Solucion**:
  1. Ingresar a `http://localhost/stats` y verificar que los tres backends aparezcan con estado `UP`.
  2. Si alguno figura como `DOWN`, revisar sus logs con `docker compose logs backend1` (o el numero correspondiente).
