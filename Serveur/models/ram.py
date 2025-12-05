import os
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Ram(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ram_total: float = Field(default=0)
    ram_use: float = Field(default=0)
    ram_not_use: float = Field(default=0)
    ordinateur_id: Optional[int] = Field(default=None, foreign_key="ordinateur.id")
    ordinateur: Optional["Ordinateur"] = Relationship(back_populates="ram_info")
            
    def init_ram_total_use_not_use(self):
        try:
            cmd = os.popen("free -m").readlines()
            line_un = cmd[1].split()
            self.ram_total = float(line_un[1])
            self.ram_use = float(line_un[2])
            self.ram_not_use = float(line_un[3])
        except:
            self.ram_total = 0.0
            self.ram_use = 0.0
            self.ram_not_use = 0.0

    def __str__(self):
        return f"#{self.id} | Ram total {self.ram_total} Ram use {self.ram_use} Ram not use {self.ram_not_use}"
    
    def __repr__(self):
        return f"<Ram(id='{self.id}', ram_total='{self.ram_total}', ram_use='{self.ram_use}' , ram_not_use='{self.ram_not_use}')>"

def main():
    R1 = Ram(id=50, ram_total=32.1, ram_use=2.1, ram_not_use=5.1)
    print(R1)
    
if __name__ == "__main__":
    main()