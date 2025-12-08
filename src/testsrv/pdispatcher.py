import os
import socket
import struct
import time
import random
from testsrv.tlogger import TLogger

class PDispatcher:
        
    ICMP_ECHO_REQUEST = 8  # ICMP type code for echo request

    def __init__(self, address: str, timeout: float = 1.0):
        self.pending = False
        self.address = address
        self.timeout = timeout
        self.logger = TLogger.create_logger(f"PDispatcher-{self.address}")

    @classmethod
    @staticmethod
    def checksum(source: bytes) -> int:
        if len(source) % 2:
            source += b"\x00"

        s = 0
        for i in range(0, len(source), 2):
            w = source[i] << 8 | source[i + 1]
            s = (s + w) & 0xffffffff

        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff

    @classmethod
    @staticmethod
    def create_icmp_packet(ident: int, seq: int, payload: bytes = b"PING") -> bytes:
        header = struct.pack("!BBHHH", PDispatcher.ICMP_ECHO_REQUEST, 0, 0, ident, seq)
        data = payload
        chksum = PDispatcher.checksum(header + data)
        header = struct.pack("!BBHHH", PDispatcher.ICMP_ECHO_REQUEST, 0, chksum, ident, seq)
        return header + data

    def send_icmp_packet(self) -> float | None:
        self.pending = True
        
        dest_addr = socket.gethostbyname(self.address)
        #ident = os.getpid() & 0xFFFF
        ident = random.randint(0, 65535)
        seq = 1

        # Raw ICMP socket (requires root/admin on most systems)
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            sock.settimeout(self.timeout)
            packet = PDispatcher.create_icmp_packet(ident, seq)
            recv_packet = b""
            send_time = time.time()
            recv_time = send_time
            sock.sendto(packet, (dest_addr, 0))

            #self.logger.info(f"Waiting for reply from {self.address} [{ident}]")
            sock.settimeout(0.1)
            while self.pending :
                try:
                    recv_data, _ = sock.recvfrom(1024)
                    recv_packet += recv_data
                    recv_time = time.time()
                    #self.logger.info(f"D: "+str(len(recv_data)))
                except socket.timeout:
                    recv_time = time.time()
                    if((recv_time - send_time) >= self.timeout):
                        return None
                
                # Check timeout
                if(len(recv_packet) == 0):
                    if((recv_time - send_time) >= self.timeout):
                        return None
                    else:                    
                        continue

                # IP header is first 20 bytes (without options)
                ip_header = recv_packet[:20]
                icmp_header = recv_packet[20:28]
                _type, code, chksum, r_ident, r_seq = struct.unpack("!BBHHH", icmp_header)
                #self.logger.info(f"Received ICMP packet: type={_type}, code={code}, id={r_ident}, seq={r_seq}")

                if (_type == 0 or _type == 8) and r_ident == ident and r_seq == seq:
                    return (recv_time - send_time) * 1000.0  #ms
                
    def init_stop(self):
        self.pending = False
        self.logger.info(f"Stop signal sent to dispatcher at {self.address}")