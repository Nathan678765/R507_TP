import os
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Ordinateur(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hostname: str = Field(default="unknown")
    os_name: str = Field(default="unknown")
    os_version: str = Field(default="unknown")
    ram_info: List["Ram"] = Relationship(back_populates="ordinateur")
    cpu_info: List["Cpu"] = Relationship(back_populates="ordinateur")
    network_interface: List["Ip_address"] = Relationship(back_populates="ordinateur")    
    
    def init_hostname(self):
        try:
            cmd = os.popen("hostname")
            self.hostname = cmd.read().strip()
        except:
            self.hostname = "Error_system"
    
    def init_os_name_version(self):
        try:
            cmd = os.popen("lsb_release -a").read().splitlines()
            line_deux = cmd[2].split()
            line_trois = cmd[3].split()
            self.os_name = line_deux[2] + " " + line_deux[3]
            self.os_version = line_trois[2]
        except:
            self.os_name = "Error_system"
            self.os_version = "Error_system"

    def update_ordinateur(self):
        self.init_hostname()
        self.init_os_name_version()

    def __str__(self):
        return f"#{self.id} | hostname {self.hostname} os_name {self.os_name} os_version {self.os_version}"
    
    def __repr__(self):
        return f"<Ordinateur(id='{self.id}', hostname='{self.hostname}', os_name='{self.os_name}' , os_version='{self.os_version}')>"

def main():
    O1 = Ordinateur(id=50, os_name="Windows 10", os_version="test", hostname="xr")
    print(O1)
    
if __name__ == "__main__":
    main()