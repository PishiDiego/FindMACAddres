# Universidad Politecnica de Durango

## Ing. en Redes y Telecomunicaciones
## By: Diego Alonso González Gándara

# README

## Introducción

Este proyecto utiliza la biblioteca `Netmiko` para conectarse a una red de switches Cisco y buscar una dirección MAC específica. El algoritmo implementado permite encontrar la ubicación de una dirección MAC en la red, determinar si está conectada directamente al switch o si se encuentra en otro switch a través de un puerto trunk. Además, el programa explora switches vecinos utilizando CDP (Cisco Discovery Protocol) de manera recursiva.

---

## Descripción del Código

El código se conecta a un switch Cisco mediante SSH utilizando las credenciales proporcionadas por el usuario. Posteriormente, busca la dirección MAC en la tabla de direcciones del switch, analiza los resultados para determinar el puerto asociado y, si es necesario, explora switches vecinos para continuar la búsqueda.

---

## Funcionalidad Principal

### Etapas del Algoritmo

1. **Conversión de la dirección MAC:**
   - El usuario proporciona una dirección MAC en formato estándar (como `C8-4D-44-20-CD-C0`), que es convertida al formato esperado por los comandos de Cisco (`c84d.4420.cdc0`).

2. **Búsqueda en el switch inicial:**
   - Se conecta al switch inicial usando `Netmiko`.
   - Se ejecuta el comando `show mac address-table | include {MAC}` para buscar la dirección MAC en la tabla de direcciones.

3. **Análisis del puerto asociado:**
   - Si la dirección MAC se encuentra en el switch, se extrae el puerto asociado.
   - Se verifica si el puerto es un trunk mediante el comando `show interfaces trunk`.
   - Si no es un trunk, la MAC está conectada directamente al switch; de lo contrario, se continúa explorando vecinos.

4. **Exploración de switches vecinos:**
   - Se utiliza el comando `show cdp neighbors detail` para obtener la lista de switches vecinos y sus direcciones IP.
   - Los switches vecinos no visitados son analizados recursivamente para buscar la dirección MAC.

5. **Finalización:**
   - Si la dirección MAC se encuentra, el programa imprime los resultados detallados y finaliza la búsqueda.
   - Si no se encuentra, se notifica al usuario.

### Funciones Principales

- `convertir_mac(mac)`: Convierte una dirección MAC al formato compatible con los comandos de Cisco.
- `buscar_mac(switch_ip)`: Busca recursivamente la dirección MAC en el switch actual y sus vecinos.

### Conexión y Resultados

- **Conexión a switches:**
  Utiliza la clase `ConnectHandler` de Netmiko para establecer una conexión SSH segura.

- **Resultados:**
  - Imprime la ubicación de la MAC (switch y puerto).
  - Indica si la MAC está conectada directamente o si debe buscarse en otro switch.
  - Documenta cualquier error durante la conexión o la ejecución de comandos.

---

## Requisitos

1. **Hardware:**
   - Switches Cisco con CDP habilitado.

2. **Software:**
   - Python 3.x
   - Biblioteca `Netmiko` instalada.

3. **Credenciales:**
   - Nombre de usuario y contraseña válidos para los switches de la red.

---

## Instalación de Dependencias

1. **Clonar el repositorio:**
   ```bash
   git clone <URL del repositorio>
   cd <nombre del repositorio>
   ```

2. **Crear un entorno virtual (opcional):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install netmiko
   ```

4. **Ejecutar el programa:**
   ```bash
   python buscar_mac.py
   ```

---




