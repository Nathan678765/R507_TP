import os
import re
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import JSON, Column

ip_address_regex = re.compile(r"\b(?P<ip>(?:(?:[1-9]?\d|1\d{2}|2(?:[0-4][0-9]|5[0-4]))\.){3}(?:[1-9]?\d|1\d{2}|2(?:[0-4][0-9]|5[0-4])))\b/(?P<mask>\d{1,2})")
mac_address_regex = re.compile(r"link/ether (?P<mac>(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})")
interfaces_regex = re.compile(r"^\d+: ([^:\s]+):")

class Ip_address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip_addresses: List[str] = Field(default=[], sa_column=Column(JSON))
    mac_addresses: List[str] = Field(default=[], sa_column=Column(JSON))
    interfaces: List[str] = Field(default=[], sa_column=Column(JSON))
    ordinateur_id: Optional[int] = Field(default=None, foreign_key="ordinateur.id")
    ordinateur: Optional["Ordinateur"] = Relationship(back_populates="network_interface")
    
    def init_ip_addresses(self):
        try:
            out = os.popen("ip a").read()
            match = ip_address_regex.search(out)
            if match:
                ip = match.group("ip")
                mask = match.group("mask")
                self.ip_addresses = [f"{ip}/{mask}"]
            else:
                self.ip_addresses = []
        except Exception:
            self.ip_addresses = ["error"]

    def init_mac_addresses(self):
        try:
            out = os.popen("ip a").read()
            match = mac_address_regex.search(out)
            if match:
                self.mac_addresses = [match.group("mac")]
            else:
                self.mac_addresses = []
        except Exception:
            self.mac_addresses = ["error"]
        
    def init_interfaces(self):       
        try:
            out = os.popen("ip a").read()
            self.interfaces = interfaces_regex.findall(out)
        except:
                self.mac_addresses = ["error"]
    
    def update_ip(self):
        self.init_ip_addresses()
        self.init_mac_addresses()
        self.init_interfaces()
        
    def __str__(self):
        return f"#{self.id} |  interfaces {self.interfaces} ip_addresses {self.ip_addresses} mac_addresses {self.mac_addresses}"

    def __repr__(self):
        return (f"<Ip_address(id='{self.id}', interfaces={self.interfaces}, "
                f"ip_addresses={self.ip_addresses}, mac_addresses={self.mac_addresses})>")

def main():
    I1 = Ip_address(id=51, ip_addresses=["192.168.1.10/24"], mac_addresses=["aa:bb:cc:dd:ee:ff"],  interfaces=["eth0"])
    I1.update_ip()
    print(I1)
    
if __name__ == "__main__":
    main()