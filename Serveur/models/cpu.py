import os
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Cpu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cpu_model: str = Field(default="Unknown")
    cpu_utilisation: str = Field(default="50.0%")
    
    ordinateur_id: Optional[int] = Field(default=None, foreign_key="ordinateur.id")
    ordinateur: Optional["Ordinateur"] = Relationship(back_populates="cpu_info")
            
    def init_cpu_name(self):
        try:
            cmd = os.popen("cat /proc/cpuinfo | grep 'model name' | uniq").readlines()
            line_un = cmd[0].split()
            self.cpu_model = line_un[2]
        except:
            self.cpu_model = "Error_system"

    def init_cpu_utilisation(self):
        try:
            cmd = os.popen("LC_ALL=C top -b -n 1 | grep ^%Cpu")
            output = cmd.read()
            if output:
                idle = output.split()[7]
                self.cpu_utilisation = f"{100 - float(idle):.1f}%"
        except:
            self.cpu_utilisation = "0%"

    def update_cpu(self):
        self.init_cpu_name()
        self.init_cpu_utilisation()
        
    def __str__(self):
        return f"#{self.id} | Cpu {self.cpu_model} utilisation {self.cpu_utilisation}"
    
    def __repr__(self):
        return f"<Cpu(id='{self.id}', cpu_model='{self.cpu_model}', cpu_utilisation='{self.cpu_utilisation}')>"

def main():
    C1 = Cpu(id=50, cpu_model="intel i5",  cpu_utilisation="50 %")
    print(C1)
    
if __name__ == "__main__":
    main()