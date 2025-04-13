# Send data payload to a server

import sys
import socket

if len(sys.argv) != 4:
    print("Usage: fuzzer_bf.py <ip_family> <ip> <port>")  # family = ipv4/ipv6
    sys.exit(1)

ip_family = sys.argv[1].lower()
target_ip = sys.argv[2]

try:
    target_port = int(sys.argv[3])
except ValueError:
    print("Port must be a number")
    sys.exit(1)

bytes_to_send = 100
step = 100


def fuzz_test():
    global bytes_to_send
    global step

    try:
        if ip_family == "ipv6":
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            s.connect((target_ip, target_port, 0, 0))
        elif ip_family == "ipv4":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
        else:
            print("Error: Invalid address family. Only 'ipv4' or 'ipv6' are allowed.")

        try:
            banner = s.recv(1024)
            print(f"Server banner: {banner.decode(errors='ignore')}")
        except:
            pass

        payload = b"A" * bytes_to_send + b"\r\n"
        print(f"Sending {bytes_to_send} bytes...")
        s.send(payload)

        try:
            res = s.recv(1024)
            print(f"Server response: {res.decode(errors='ignore').strip()}")
        except socket.timeout:
            print("No response from server.")
            return True
        except Exception as e:
            print("Error in server response:", str(e))
            return True
    except Exception as e:
        print("Connection error:", str(e))
    finally:
        s.close()
    return False


if __name__ == "__main__":
    while True:
        print(f"Initiating fuzzing against {target_ip}:{target_port}")
        if fuzz_test():
            print(
                f"Crash likely occurred at payload size: {bytes_to_send} bytes")
            break

        bytes_to_send += step

    print("Fuzzing test completed")
