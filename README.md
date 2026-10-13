# Taller de Balanceo de Carga con HAProxy y Docker

Implementación de una arquitectura de microservicios con balanceo de carga HTTP utilizando HAProxy como proxy inverso y balanceador de carga, distribuyendo el tráfico entre múltiples instancias de backend en FastAPI y sirviendo un frontend en React con Vite. Todo el entorno está orquestado mediante Docker Compose.

## Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Tecnologías](#tecnologías)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Componentes y Configuración](#componentes-y-configuración)
  - [HAProxy](#haproxy)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (React + Vite)](#frontend-react--vite)
- [Instrucciones de Ejecución](#instrucciones-de-ejecución)
- [Verificación del Balanceo](#verificación-del-balanceo)
- [Pruebas de Carga con JMeter](#pruebas-de-carga-con-jmeter)
- [Puertos y URLs](#puertos-y-urls)

## Arquitectura

```
                           +---------------------+
                           |       Usuario       |
                           |   (Navegador Web)   |
                           +----------+----------+
                                      |
                                      v
                           +---------------------+
                           |  HAProxy (puerto 80)|
                           |    Load Balancer    |
                           +----------+----------+
                                      |
                    +-----------------+-----------------+
                    |                 |                 |
             /api/* |          /api/* |          /api/* |      default
                    v                 v                 v         |
          +--------------+  +--------------+  +--------------+    |
          |  Backend 1   |  |  Backend 2   |  |  Backend 3   |    |
          |  FastAPI     |  |  FastAPI     |  |  FastAPI     |    |
          |  puerto 8000 |  |  puerto 8000 |  |  puerto 8000 |    |
          +--------------+  +--------------+  +--------------+    |
                                                                  v
                                                        +--------------+
                                                        |   Frontend   |
                                                        |  React + Vite|
                                                        |  puerto 3000 |
                                                        +--------------+
```

### Flujo de Tráfico

1. El cliente se conecta a `http://localhost` (puerto 80).
2. HAProxy evalúa las reglas ACL definidas:
   - Si la ruta inicia con `/api/`, se redirige hacia el pool `api_servers` usando el algoritmo round-robin entre las tres instancias de backend.
   - Si la ruta es `/stats`, se expone la consola de administración y métricas de HAProxy.
   - Cualquier otra ruta se enruta hacia el servicio de frontend.
3. El frontend consume el endpoint `/api/hello`, el cual a su vez es balanceado equitativamente entre `backend1`, `backend2` y `backend3`.

## Tecnologías

- **HAProxy 2.8**: Balanceador de carga y reverse proxy HTTP.
- **Docker & Docker Compose**: Contenedorización y orquestación de la red y los servicios.
- **Python 3.11 & FastAPI**: API REST para atender las peticiones en el backend.
- **Uvicorn**: Servidor ASGI para las instancias de FastAPI.
- **Node.js 18 & React 18**: Interfaz de usuario empaquetada con Vite.
- **Apache JMeter 5.6+**: Herramienta de pruebas de rendimiento y concurrencia.

## Estructura del Repositorio

```
.
|-- backend/
|   |-- Dockerfile            # Construcción de la imagen del backend
|   `-- main.py               # Servicio FastAPI con endpoint /api/hello
|-- frontend/
|   |-- src/
|   |   |-- App.jsx           # Vista principal que consume el backend
|   |   `-- main.jsx          # Punto de entrada de la aplicación React
|   |-- Dockerfile            # Construcción de la imagen del frontend
|   |-- index.html            # Plantilla HTML
|   |-- package.json          # Dependencias y scripts de Vite
|   `-- vite.config.js        # Configuración de proxy y puerto
|-- haproxy/
|   `-- haproxy.cfg           # Reglas de enrutamiento y balanceo
|-- jmeter/
|   `-- haproxy_load_test.jmx # Plan de pruebas de carga
|-- docs/
|   `-- architecture.png      # Diagrama conceptual
|-- docker-compose.yml        # Definición de servicios, volúmenes y red
|-- INSTRUCCIONES.md          # Guía detallada de despliegue y solución de problemas
`-- README.md                 # Documentación general
```

## Componentes y Configuración

### HAProxy

El archivo `haproxy/haproxy.cfg` define:

- **Frontend `http-in`**: Escucha en el puerto 80 para tráfico entrante.
- **Backend `api_servers`**: Balancea mediante `balance roundrobin` entre `backend1`, `backend2` y `backend3`. Incorpora health checks periódicos (`option httpchk GET /api/hello`).
- **Backend `front_servers`**: Dirige al contenedor del frontend en el puerto 3000.
- **Backend `stats_backend`**: Dashboard en `/stats` con refresco automático cada 5 segundos.

### Backend (FastAPI)

Tres réplicas idénticas construidas a partir de `python:3.11-slim`:
- Cada contenedor recibe por variable de entorno `INSTANCE_NAME` (`backend1`, `backend2`, `backend3`).
- Endpoint: `GET /api/hello`, retornando el nombre de instancia y el hostname del contenedor.
- Los contenedores se comunican internamente en la red `app-net` sin exponer puertos directos al host por motivos de aislamiento.

### Frontend (React + Vite)

- SPA sencilla que consulta `/api/hello` al montarse y renderiza el mensaje junto con la instancia que contestó.
- Proxy configurado en `vite.config.js` para reenviar llamadas de `/api` al host interno de HAProxy dentro de Docker.

## Instrucciones de Ejecución

### Requisitos Previos

- Docker Engine y Docker Compose instalados (Docker Desktop en Windows/macOS o Docker CE en Linux).
- Puertos `80` y `3000` libres en el sistema host.

### Iniciar los Servicios

Para construir las imágenes e iniciar la infraestructura:

```bash
docker compose up --build
```

Para ejecutar en segundo plano:

```bash
docker compose up --build -d
```

### Consultar Estado y Logs

```bash
# Ver estado de los contenedores
docker compose ps

# Ver logs consolidados en tiempo real
docker compose logs -f

# Ver logs de un servicio específico
docker compose logs haproxy
```

### Detener los Servicios

```bash
docker compose down
```

## Verificación del Balanceo

Para validar que el balanceo round-robin distribuye las solicitudes equitativamente:

### Linux / macOS (Bash)

```bash
for i in {1..9}; do curl -s http://localhost/api/hello; echo ""; done
```

### Windows (PowerShell)

```powershell
1..9 | ForEach-Object { (Invoke-RestMethod http://localhost/api/hello).instance }
```

La salida alternará consecutivamente entre `backend1`, `backend2` y `backend3`.

## Pruebas de Carga con JMeter

El archivo `jmeter/haproxy_load_test.jmx` contiene el plan de pruebas preconfigurado con:

- **Hilos concurrentes**: 20 usuarios.
- **Ramp-up**: 10 segundos.
- **Iteraciones (Loop Count)**: 50 ciclos por usuario (1000 solicitudes en total).
- **Objetivo**: `GET http://localhost:80/api/hello`.

### Ejecución

1. Abrir JMeter y cargar `jmeter/haproxy_load_test.jmx`.
2. Ejecutar la prueba (`Run -> Start` o `Ctrl+R`).
3. Analizar métricas en los listeners incluidos:
   - **Summary Report**: Tiempo de respuesta promedio, mínimo, máximo, throughput y tasa de error.
   - **View Results Tree**: Detalle individual de respuestas HTTP.
   - **Response Time Graph**: Evolución de latencia en el tiempo.

## Puertos y URLs

| Servicio | URL | Descripción |
|---|---|---|
| Frontend | http://localhost:3000 | Interfaz web |
| API (balanceada) | http://localhost/api/hello | Endpoint de prueba a través de HAProxy |
| HAProxy Stats | http://localhost/stats | Panel de estadísticas y estado de nodos |
