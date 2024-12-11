from netmiko import ConnectHandler
import getpass
import re

# Función para convertir la MAC al formato f430.b9a0.c3e8
def convertir_mac(mac):
    mac = mac.replace("-", "").replace(":", "").replace(".", "")  # Eliminar separadores
    if len(mac) != 12 or not re.match(r"^[0-9a-fA-F]+$", mac):
        raise ValueError("Formato de MAC inválido. Use C8-4D-44-20-CD-C0 o similar.")
    return mac[:4].lower() + "." + mac[4:8].lower() + "." + mac[8:].lower()

# Pedir información del switch inicial
host = input("Ingrese la IP del switch inicial: ")
username = input("Ingrese el nombre de usuario: ")
password = input("Ingrese su contraseña: ")
mac_address_input = input("Ingrese la MAC (en formato C8-4D-44-20-CD-C0): ")

try:
    mac_address = convertir_mac(mac_address_input)
except ValueError as e:
    print(e)
    exit()

# Configuración base del switch
base_config = {
    "device_type": "cisco_ios",
    "username": username,
    "password": password,
}

# Lista de switches visitados para evitar bucles
visited_switches = set()

def buscar_mac(switch_ip):
    """Busca la dirección MAC en un switch y explora vecinos si es necesario."""
    global visited_switches
    visited_switches.add(switch_ip)

    switch_config = base_config.copy()
    switch_config["host"] = switch_ip

    try:
        # Conectarse al switch
        connection = ConnectHandler(**switch_config)
        print(f"\nConectado al switch {switch_ip}")

        # Buscar la MAC en la tabla de direcciones
        command_mac = f"show mac address-table | include {mac_address}"
        mac_output = connection.send_command(command_mac)

        if mac_address in mac_output:
            print("#"*100, '\n')
            print(f"MAC {mac_address} encontrada en el switch {switch_ip}:")
            print(mac_output)

            # Extraer el puerto asociado
            port = mac_output.split()[-1]
            print(f"Puerto asociado: {port}", '\n')

            # Verificar si el puerto es un trunk
            trunk_command = "show interfaces trunk"
            trunk_output = connection.send_command(trunk_command)
            if port in trunk_output:
                print(f"La MAC {mac_address} está en otro switch, a través del puerto {port}.")
            else:
                print("="*100, '\n')
                print(f"La MAC {mac_address} está conectada directamente al puerto {port}.")
                print("=" * 100, '\n')
                print("*"*100, '\n')
                print("Fin.,\npaseme profe")
                connection.disconnect()
                return True  # Detener la búsqueda

        else:
            print(f"MAC {mac_address} no encontrada en el switch {switch_ip}.")

        # Descubrir switches vecinos
        print("Buscando vecinos con CDP...")
        cdp_output = connection.send_command("show cdp neighbors detail")
        for line in cdp_output.split("\n"):
            if "IP address" in line:
                neighbor_ip = line.split()[-1]
                if neighbor_ip not in visited_switches:
                    print(f"Vecino encontrado: {neighbor_ip}")
                    if buscar_mac(neighbor_ip):  # Llamada recursiva
                        connection.disconnect()
                        return True

        # Cerrar conexión
        connection.disconnect()

    except Exception as e:
        print(f"Error al conectar con {switch_ip}: {e}")
        return False

# Iniciar la búsqueda desde el switch inicial
if not buscar_mac(host):
    print(f"\nLa MAC {mac_address} no fue encontrada en la red.")

