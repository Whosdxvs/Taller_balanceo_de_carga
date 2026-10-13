# 📖 Instrucciones Detalladas — Paso a Paso

Guía completa para configurar, ejecutar y probar el proyecto de balanceo de carga desde cero. No se salta ningún paso.

---

## 📋 Tabla de Contenidos

1. [Prerrequisitos](#1-prerrequisitos)
2. [Instalación de Docker Desktop](#2-instalación-de-docker-desktop)
3. [Verificar la Instalación de Docker](#3-verificar-la-instalación-de-docker)
4. [Clonar o Descargar el Proyecto](#4-clonar-o-descargar-el-proyecto)
5. [Entender la Estructura del Proyecto](#5-entender-la-estructura-del-proyecto)
6. [Construir y Levantar los Contenedores](#6-construir-y-levantar-los-contenedores)
7. [Verificar que los Contenedores Están Corriendo](#7-verificar-que-los-contenedores-están-corriendo)
8. [Probar la Aplicación](#8-probar-la-aplicación)
9. [Verificar el Balanceo de Carga](#9-verificar-el-balanceo-de-carga)
10. [Monitorear con HAProxy Stats](#10-monitorear-con-haproxy-stats)
11. [Pruebas de Carga con JMeter](#11-pruebas-de-carga-con-jmeter)
12. [Comandos Docker Útiles](#12-comandos-docker-útiles)
13. [Detener y Limpiar Todo](#13-detener-y-limpiar-todo)
14. [Solución de Problemas](#14-solución-de-problemas)

---

## 1. Prerrequisitos

Antes de comenzar, asegúrate de tener lo siguiente instalado en tu computadora:

### Software Necesario

| Software | Versión Mínima | Para qué se usa |
|----------|---------------|-----------------|
| **Docker Desktop** | 4.0+ | Ejecutar contenedores |
| **Docker Compose** | v2 (incluido en Docker Desktop) | Orquestar múltiples contenedores |
| **Git** (opcional) | Cualquiera | Clonar el repositorio |
| **Apache JMeter** (opcional) | 5.6+ | Pruebas de carga |
| **curl** (opcional) | Cualquiera | Probar endpoints desde terminal |

### Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11, macOS 10.15+, o Linux
- **RAM**: Mínimo 4 GB libres (recomendado 8 GB)
- **Espacio en disco**: Al menos 5 GB libres
- **Puertos disponibles**: 80 y 3000 (no deben estar en uso por otra aplicación)

---

## 2. Instalación de Docker Desktop

### En Windows

1. **Descargar Docker Desktop**:
   - Ve a https://www.docker.com/products/docker-desktop/
   - Haz clic en **"Download for Windows"**.
   - Descarga el archivo `Docker Desktop Installer.exe`.

2. **Instalar**:
   - Ejecuta el instalador descargado.
   - Acepta los términos de licencia.
   - En las opciones de configuración:
     - ✅ Marca **"Use WSL 2 instead of Hyper-V"** (recomendado para Windows).
     - ✅ Marca **"Add shortcut to desktop"**.
   - Haz clic en **"Ok"** e **"Install"**.
   - Espera a que termine la instalación.

3. **Reiniciar Windows**:
   - Cuando lo pida, reinicia tu computadora.

4. **Iniciar Docker Desktop**:
   - Después de reiniciar, abre **Docker Desktop** desde el menú de inicio o el acceso directo del escritorio.
   - Espera a que el ícono de Docker en la barra de tareas muestre **"Docker Desktop is running"** (el ícono de la ballena deja de moverse).
   - Si es la primera vez, acepta los términos de servicio.

5. **Habilitar WSL 2** (si no lo tienes):
   - Abre **PowerShell como Administrador** y ejecuta:
   ```powershell
   wsl --install
   ```
   - Reinicia si es necesario.

### En macOS

1. Descarga Docker Desktop desde https://www.docker.com/products/docker-desktop/
2. Abre el archivo `.dmg` descargado.
3. Arrastra el ícono de Docker a la carpeta **Applications**.
4. Abre Docker Desktop desde **Applications**.
5. Espera a que el ícono de Docker en la barra superior muestre que está corriendo.

### En Linux (Ubuntu/Debian)

```bash
# Actualizar paquetes
sudo apt-get update

# Instalar dependencias
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Añadir clave GPG de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadir repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine y Docker Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Añadir tu usuario al grupo docker (para no necesitar sudo)
sudo usermod -aG docker $USER

# Cerrar sesión y volver a abrirla para que el cambio de grupo tome efecto
```

---

## 3. Verificar la Instalación de Docker

Abre una **terminal** (PowerShell en Windows, Terminal en macOS/Linux) y ejecuta los siguientes comandos uno por uno:

### 3.1 Verificar Docker

```bash
docker --version
```

**Salida esperada** (la versión puede variar):
```
Docker version 24.0.7, build afdd53b
```

### 3.2 Verificar Docker Compose

```bash
docker compose version
```

**Salida esperada**:
```
Docker Compose version v2.23.0
```

### 3.3 Verificar que Docker está corriendo

```bash
docker info
```

**Salida esperada**: Debería mostrar información del sistema Docker sin errores. Si ves un error como "Cannot connect to the Docker daemon", significa que Docker Desktop no está corriendo. Ábrelo desde el menú de inicio.

### 3.4 Probar con un contenedor de prueba

```bash
docker run hello-world
```

**Salida esperada**: Un mensaje que dice "Hello from Docker!" seguido de una explicación. Esto confirma que Docker puede descargar imágenes y ejecutar contenedores correctamente.

---

## 4. Clonar o Descargar el Proyecto

### Opción A: Si tienes el proyecto en un repositorio Git

```bash
git clone <URL_DEL_REPOSITORIO>
cd docker-haproxy-main
```

### Opción B: Si descargaste el ZIP

1. Descarga el archivo ZIP del proyecto.
2. Descomprímelo en una ubicación conveniente.
3. Abre una terminal y navega a la carpeta del proyecto:

```bash
cd "C:\Users\TU_USUARIO\Desktop\Taller balanceo de carga\docker-haproxy-main"
```

> **⚠ Importante**: Reemplaza `TU_USUARIO` con tu nombre de usuario real de Windows.

### Verificar que estás en la carpeta correcta

```bash
dir
```

Deberías ver:
```
backend/
frontend/
haproxy/
jmeter/
docker-compose.yml
README.md
INSTRUCCIONES.md
```

---

## 5. Entender la Estructura del Proyecto

Antes de ejecutar nada, revisemos qué hace cada parte:

```
docker-haproxy-main/
│
├── backend/                    ← Código del servidor API
│   ├── Dockerfile              ← Instrucciones para construir la imagen del backend
│   └── main.py                 ← Código Python con FastAPI
│
├── frontend/                   ← Código de la interfaz web
│   ├── src/
│   │   ├── App.jsx             ← Componente principal de React
│   │   └── main.jsx            ← Punto de entrada de React
│   ├── Dockerfile              ← Instrucciones para construir la imagen del frontend
│   ├── index.html              ← Página HTML base
│   ├── package.json            ← Lista de dependencias de Node.js
│   └── vite.config.js          ← Configuración del servidor de desarrollo
│
├── haproxy/                    ← Configuración del balanceador de carga
│   └── haproxy.cfg             ← Reglas de balanceo y enrutamiento
│
├── jmeter/                     ← Pruebas de rendimiento
│   └── haproxy_load_test.jmx   ← Plan de pruebas de JMeter
│
└── docker-compose.yml          ← Archivo maestro que orquesta todos los servicios
```

---

## 6. Construir y Levantar los Contenedores

### 6.1 Asegúrate de que Docker Desktop está corriendo

Verifica que el ícono de Docker (🐋) en la barra de tareas esté activo. Si no lo está, abre Docker Desktop y espera a que inicie completamente.

### 6.2 Abre una terminal en la carpeta del proyecto

```bash
cd "C:\Users\TU_USUARIO\Desktop\Taller balanceo de carga\docker-haproxy-main"
```

### 6.3 Construir las imágenes y levantar los contenedores

Ejecuta el siguiente comando:

```bash
docker compose up --build
```

**Explicación de las banderas**:
- `docker compose`: Herramienta para manejar múltiples contenedores.
- `up`: Crea e inicia los contenedores definidos en `docker-compose.yml`.
- `--build`: Fuerza la reconstrucción de las imágenes Docker (importante la primera vez o cuando cambias código).

### 6.4 ¿Qué pasa cuando ejecutas este comando?

Docker realizará los siguientes pasos automáticamente:

1. **Crear la red** `app-net` (red interna de Docker tipo bridge).
2. **Construir la imagen del backend**:
   - Descarga la imagen base `python:3.11-slim` (~50 MB).
   - Instala `fastapi` y `uvicorn` con pip.
   - Copia `main.py` al contenedor.
3. **Construir la imagen del frontend**:
   - Descarga la imagen base `node:18-alpine` (~120 MB).
   - Ejecuta `npm install` para instalar React, Vite y plugins.
   - Copia el código fuente.
4. **Descargar la imagen de HAProxy** (`haproxy:2.8`).
5. **Crear 5 contenedores**:
   - `backend1`, `backend2`, `backend3`
   - `haproxy`
   - `frontend`
6. **Iniciar todos los contenedores** respetando las dependencias.

### 6.5 Tiempo estimado

- **Primera ejecución**: 2-5 minutos (descarga imágenes + instala dependencias).
- **Ejecuciones posteriores**: 10-30 segundos (usa caché de Docker).

### 6.6 ¿Cómo saber que todo está listo?

Verás mensajes como estos en la terminal:

```
✔ Network docker-haproxy-main_app-net  Created
✔ Container docker-haproxy-main-backend1-1  Created
✔ Container docker-haproxy-main-backend2-1  Created
✔ Container docker-haproxy-main-backend3-1  Created
✔ Container docker-haproxy-main-haproxy-1   Created
✔ Container docker-haproxy-main-frontend-1  Created
```

Y luego logs como:

```
backend1-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
backend2-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
backend3-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
frontend-1  |   VITE v4.5.x  ready in xxx ms
frontend-1  |   ➜  Local:   http://localhost:3000/
```

> **⚠ No cierres esta terminal**. Los logs se muestran en tiempo real. Si la cierras, los contenedores se detendrán.

### 6.7 Ejecutar en segundo plano (modo detached)

Si prefieres que los contenedores corran en segundo plano y liberar la terminal:

```bash
docker compose up --build -d
```

La bandera `-d` (detached) ejecuta los contenedores en segundo plano. Para ver los logs después:

```bash
docker compose logs -f
```

La bandera `-f` (follow) muestra los logs en tiempo real. Presiona `Ctrl+C` para dejar de verlos (los contenedores siguen corriendo).

---

## 7. Verificar que los Contenedores Están Corriendo

### 7.1 Listar contenedores activos

Abre una **nueva terminal** (sin cerrar la anterior si no usaste `-d`) y ejecuta:

```bash
docker compose ps
```

**Salida esperada**:

```
NAME                                  SERVICE    STATUS    PORTS
docker-haproxy-main-backend1-1        backend1   Up        8000/tcp
docker-haproxy-main-backend2-1        backend2   Up        8000/tcp
docker-haproxy-main-backend3-1        backend3   Up        8000/tcp
docker-haproxy-main-frontend-1        frontend   Up        0.0.0.0:3000->3000/tcp
docker-haproxy-main-haproxy-1         haproxy    Up        0.0.0.0:80->80/tcp
```

Los 5 contenedores deben estar en estado **Up**.

### 7.2 Ver los logs de un servicio específico

```bash
# Ver logs del backend1
docker compose logs backend1

# Ver logs del haproxy
docker compose logs haproxy

# Ver logs del frontend
docker compose logs frontend
```

### 7.3 Ver los logs de todos los servicios en tiempo real

```bash
docker compose logs -f
```

---

## 8. Probar la Aplicación

### 8.1 Probar el Frontend (Navegador)

1. Abre tu **navegador web** (Chrome, Firefox, Edge, etc.).
2. Ve a: **http://localhost:3000**
3. Deberías ver:
   - Un fondo azul con gradiente.
   - El título "🚀 React + FastAPI + HAProxy".
   - Un mensaje como: **"Hello from FastAPI! (served by backend1)"**.

4. **Recarga la página** varias veces (`F5` o `Ctrl+R`). El nombre de la instancia debería cambiar entre `backend1`, `backend2` y `backend3`.

### 8.2 Probar la API directamente (Navegador)

1. Abre una nueva pestaña.
2. Ve a: **http://localhost/api/hello**
3. Verás una respuesta JSON como:

```json
{
  "message": "Hello from FastAPI! (served by backend2)",
  "instance": "backend2",
  "hostname": "a1b2c3d4e5f6"
}
```

4. **Recarga** varias veces para ver el balanceo.

### 8.3 Probar la API con curl (Terminal)

Abre una terminal y ejecuta:

```bash
curl http://localhost/api/hello
```

**Salida esperada**:
```json
{"message":"Hello from FastAPI! (served by backend1)","instance":"backend1","hostname":"abc123"}
```

Ejecútalo varias veces para ver cómo alterna entre instancias.

---

## 9. Verificar el Balanceo de Carga

### 9.1 Test rápido con múltiples peticiones

**En Windows (PowerShell)**:

```powershell
for ($i=1; $i -le 9; $i++) { 
    Write-Host "Petición ${i}:" -NoNewline
    (Invoke-RestMethod http://localhost/api/hello).instance 
}
```

**En Linux/macOS (Bash)**:

```bash
for i in {1..9}; do
    echo "Petición $i: $(curl -s http://localhost/api/hello | grep -o '"instance":"[^"]*"')"
done
```

**Salida esperada** (patrón round-robin):

```
Petición 1: backend1
Petición 2: backend2
Petición 3: backend3
Petición 4: backend1
Petición 5: backend2
Petición 6: backend3
Petición 7: backend1
Petición 8: backend2
Petición 9: backend3
```

### 9.2 ¿Qué demuestra esto?

- Las peticiones se **distribuyen equitativamente** entre los 3 backends.
- El algoritmo **round-robin** alterna en orden: 1 → 2 → 3 → 1 → 2 → 3...
- Ningún backend recibe más carga que otro.

---

## 10. Monitorear con HAProxy Stats

### 10.1 Acceder al Dashboard

1. Abre tu navegador.
2. Ve a: **http://localhost/stats**
3. Verás el dashboard de HAProxy con estadísticas en tiempo real.

### 10.2 ¿Qué información muestra?

- **Sesiones actuales**: Cuántas conexiones hay activas.
- **Bytes in/out**: Tráfico de datos.
- **Status de cada backend**: Si está UP (🟢) o DOWN (🔴).
- **Peticiones por backend**: Cuántas peticiones ha recibido cada instancia.
- **Tiempos de respuesta**: Latencia promedio de cada backend.

### 10.3 Estadísticas en tiempo real

El dashboard se auto-refresca cada 5 segundos. Puedes ejecutar el test de carga y observar cómo las métricas cambian en tiempo real.

---

## 11. Pruebas de Carga con JMeter

### 11.1 Instalar Apache JMeter

#### Descargar

1. Ve a https://jmeter.apache.org/download_jmeter.cgi
2. Descarga el archivo ZIP de la sección **Binaries** (ej: `apache-jmeter-5.6.3.zip`).
3. Descomprime el ZIP en una ubicación conveniente (ej: `C:\jmeter`).

#### Requisito: Java

JMeter necesita **Java 8+** instalado. Verifica con:

```bash
java -version
```

Si no tienes Java, descárgalo desde https://adoptium.net/

### 11.2 Abrir JMeter

#### En Windows

```bash
C:\jmeter\bin\jmeter.bat
```

O navega a la carpeta `bin` del JMeter y haz doble clic en `jmeter.bat`.

#### En macOS/Linux

```bash
/ruta/a/jmeter/bin/jmeter.sh
```

### 11.3 Cargar el Plan de Pruebas

1. En JMeter, ve a **File → Open** (o `Ctrl+O`).
2. Navega hasta la carpeta del proyecto: `docker-haproxy-main/jmeter/`.
3. Selecciona el archivo `haproxy_load_test.jmx`.
4. Haz clic en **Open**.

### 11.4 Revisar la Configuración del Test

En el panel izquierdo verás:

```
🧪 HAProxy Load Test Plan
└── 👥 Concurrent Users (Thread Group)
    ├── 🌐 GET /api/hello (HTTP Request)
    ├── 🌳 View Results Tree (Listener)
    ├── 📊 Summary Report (Listener)
    └── 📈 Response Time Graph (Listener)
```

**Parámetros del Thread Group**:
- **Number of Threads**: 20 (usuarios concurrentes)
- **Ramp-Up Period**: 10 segundos
- **Loop Count**: 50

Esto significa: JMeter creará 20 usuarios virtuales en 10 segundos, y cada uno hará 50 peticiones = **1000 peticiones totales**.

### 11.5 Ejecutar las Pruebas

1. **Asegúrate** de que los contenedores Docker están corriendo.
2. En JMeter, haz clic en el botón verde **▶ Start** (o `Ctrl+R`).
3. Espera a que termine (verás el progreso en la esquina superior derecha).

### 11.6 Ver los Resultados

#### View Results Tree

- Haz clic en **View Results Tree** en el panel izquierdo.
- Verás cada petición individual con:
  - ✅ Verde = exitosa
  - ❌ Roja = fallida
- Haz clic en una petición para ver los detalles del request y response.

#### Summary Report

- Haz clic en **Summary Report** en el panel izquierdo.
- Verás una tabla con métricas agregadas:

| Métrica | Descripción |
|---------|-------------|
| **# Samples** | Número total de peticiones |
| **Average** | Tiempo promedio de respuesta (ms) |
| **Min** | Tiempo mínimo de respuesta (ms) |
| **Max** | Tiempo máximo de respuesta (ms) |
| **Std. Dev.** | Desviación estándar |
| **Error %** | Porcentaje de errores |
| **Throughput** | Peticiones por segundo |
| **KB/sec** | Kilobytes por segundo |

#### Response Time Graph

- Haz clic en **Response Time Graph** en el panel izquierdo.
- Haz clic en el botón **Display Graph**.
- Verás una gráfica del tiempo de respuesta a lo largo del tiempo.

### 11.7 Experimentar con Diferentes Configuraciones

Puedes modificar los parámetros del Thread Group para probar diferentes escenarios:

| Escenario | Threads | Loops | Total Requests |
|-----------|---------|-------|---------------|
| Carga baja | 5 | 20 | 100 |
| Carga media | 20 | 50 | 1,000 |
| Carga alta | 50 | 100 | 5,000 |
| Estrés | 100 | 200 | 20,000 |

Para modificar: haz clic en **Concurrent Users** en el panel izquierdo y cambia los valores.

### 11.8 Guardar Resultados

Para guardar los resultados en un archivo:

1. Haz clic en un Listener (ej: Summary Report).
2. En el campo **"Write results to file"**, escribe una ruta como `results.csv`.
3. Ejecuta las pruebas.
4. El archivo CSV contendrá todos los datos para análisis posterior.

---

## 12. Comandos Docker Útiles

### Gestión de Contenedores

```bash
# Ver contenedores activos
docker compose ps

# Ver TODOS los contenedores (incluidos los detenidos)
docker compose ps -a

# Levantar contenedores (sin reconstruir)
docker compose up

# Levantar contenedores (reconstruyendo las imágenes)
docker compose up --build

# Levantar en segundo plano
docker compose up --build -d

# Detener contenedores (sin eliminarlos)
docker compose stop

# Detener y eliminar contenedores, redes y volúmenes
docker compose down

# Reiniciar todos los servicios
docker compose restart

# Reiniciar un servicio específico
docker compose restart backend1
```

### Logs

```bash
# Ver logs de todos los servicios
docker compose logs

# Ver logs en tiempo real
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs frontend
docker compose logs haproxy
docker compose logs backend1

# Ver las últimas 50 líneas de un servicio
docker compose logs --tail 50 backend1
```

### Imágenes

```bash
# Listar imágenes descargadas
docker images

# Eliminar imágenes no utilizadas
docker image prune

# Reconstruir la imagen de un servicio específico
docker compose build backend1
```

### Redes

```bash
# Listar redes de Docker
docker network ls

# Inspeccionar la red del proyecto
docker network inspect docker-haproxy-main_app-net
```

### Acceder a un Contenedor

```bash
# Abrir una terminal dentro de un contenedor
docker compose exec backend1 sh

# Ejecutar un comando dentro de un contenedor
docker compose exec backend1 python --version
docker compose exec frontend node --version
```

---

## 13. Detener y Limpiar Todo

### 13.1 Detener los contenedores

Si los contenedores están corriendo en primer plano (sin `-d`), presiona `Ctrl+C` en la terminal donde ejecutaste `docker compose up`.

Si están en segundo plano:

```bash
docker compose stop
```

### 13.2 Detener y eliminar todo

```bash
docker compose down
```

Esto elimina:
- ✅ Todos los contenedores creados
- ✅ La red `app-net`
- ❌ No elimina las imágenes (para no tener que descargarlas de nuevo)

### 13.3 Eliminar todo incluyendo imágenes

```bash
docker compose down --rmi all
```

### 13.4 Limpieza profunda de Docker

```bash
# Eliminar contenedores detenidos, redes no usadas, imágenes sin referencia y caché
docker system prune -a
```

> **⚠ Cuidado**: Este comando elimina TODOS los recursos Docker no utilizados, no solo los de este proyecto.

---

## 14. Solución de Problemas

### ❌ "Cannot connect to the Docker daemon"

**Causa**: Docker Desktop no está corriendo.
**Solución**: Abre Docker Desktop y espera a que inicie completamente.

### ❌ "port is already allocated" (puerto 80 o 3000)

**Causa**: Otra aplicación está usando el puerto.
**Solución**:

```bash
# Ver qué proceso usa el puerto 80 (Windows)
netstat -ano | findstr ":80"

# Ver qué proceso usa el puerto 80 (Linux/macOS)
lsof -i :80
```

Cierra la aplicación que usa el puerto, o cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8080:80"   # Cambia 80 por 8080
```

### ❌ "no such file or directory" al construir

**Causa**: Estás ejecutando el comando desde la carpeta incorrecta.
**Solución**: Asegúrate de estar en la carpeta `docker-haproxy-main`:
```bash
cd "C:\Users\TU_USUARIO\Desktop\Taller balanceo de carga\docker-haproxy-main"
```

### ❌ El frontend muestra "Fallo en la llamada a la API"

**Causa**: El frontend no puede comunicarse con HAProxy.
**Solución**:
1. Verifica que HAProxy esté corriendo: `docker compose ps`
2. Verifica que los backends estén corriendo: `docker compose logs backend1`
3. Prueba la API directamente: `curl http://localhost/api/hello`

### ❌ JMeter no conecta a localhost:80

**Causa**: Los contenedores no están corriendo o HAProxy no está escuchando en el puerto 80.
**Solución**:
1. Verifica: `docker compose ps`
2. Prueba: `curl http://localhost/api/hello`
3. Si funciona con curl pero no con JMeter, revisa que el host en JMeter sea `localhost` y el puerto `80`.

### ❌ Las imágenes tardan mucho en construirse

**Causa**: Primera ejecución, se descargan las imágenes base.
**Solución**: Es normal la primera vez. Las ejecuciones siguientes serán mucho más rápidas gracias al caché de Docker.

---

> **💡 Tip**: Si tienes algún problema no listado aquí, revisa los logs con `docker compose logs -f` para obtener más información sobre el error.

---
