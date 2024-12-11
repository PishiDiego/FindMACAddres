from netmiko import ConnectHandler

R1 = ConnectHandler(host = '192.168.1.1',
                    username = 'cisco',
                    password = 'cisco',
                    device_type = 'cisco_xe'
                    )
Heartbeat = R1.is_alive()
print(Heartbeat)

