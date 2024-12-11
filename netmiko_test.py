from netmiko import ConnectHandler

SW1 = ConnectHandler(host = '192.168.1.1',
                    username = 'cisco',
                    password = 'cisco',
                    device_type = 'cisco_xe'
                    )
Heartbeat = SW1.is_alive()
print(Heartbeat)

