from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlmodel import Session, select, SQLModel
from database import configure_db, get_session, engine
from models.ordinateur import Ordinateur
from models.ram import Ram
from models.cpu import Cpu
from models.ip_address import Ip_address

class OrdinateurRead(SQLModel):
    id: int
    hostname: str
    os_name: str
    os_version: str
    ram_info: List[Ram] = []
    cpu_info: List[Cpu] = []
    network_interface: List[Ip_address] = []
    
async def on_start_up():
    configure_db()
    
    with Session(engine) as session:
        if not session.get(Ordinateur, 51):
            pc_static = Ordinateur(id=51, hostname="xr", os_name="Windows 10", os_version="test")
            session.add(pc_static)
            ram_static = Ram(id=51, ordinateur_id=51, ram_total=32.1, ram_use=2.1, ram_not_use=5.1)
            session.add(ram_static)
            cpu_static = Cpu(id=51, ordinateur_id=51, cpu_model="intel i5", cpu_utilisation="51.0%")
            session.add(cpu_static)
            network_static = Ip_address(id=51, ordinateur_id=51, ip_addresses=["192.168.1.10/24"], mac_addresses=["aa:bb:cc:dd:ee:ff"],  interfaces=["eth0"])
            session.add(network_static)
            session.commit()


app = FastAPI(on_startup=[on_start_up])

@app.post("/ordinateur/setup", response_model=OrdinateurRead)
def create_current_machine(session: Session = Depends(get_session)):
    pc = Ordinateur()
    pc.update_ordinateur()
    session.add(pc)
    session.commit()
    session.refresh(pc)
    ram = Ram(ordinateur_id=pc.id)
    ram.init_ram_total_use_not_use()
    session.add(ram)
    cpu = Cpu(ordinateur_id=pc.id)
    cpu.update_cpu()
    session.add(cpu)
    net = Ip_address(ordinateur_id=pc.id)
    net.update_ip()
    session.add(net)
    session.commit()
    session.refresh(pc)
    return pc

@app.get("/ordinateurs", response_model=List[OrdinateurRead])
def read_ordinateurs(session: Session = Depends(get_session)):
    ordinateurs = session.exec(select(Ordinateur)).all()
    return ordinateurs

@app.post("/ordinateur/{pc_id}/update")
def update_stats(pc_id: int, session: Session = Depends(get_session)):
    pc = session.get(Ordinateur, pc_id)
    if not pc:
        raise HTTPException(status_code=404, detail="PC introuvable")
    pc.update_ordinateur()
    session.add(pc)
    for ram in pc.ram_info:
        ram.init_ram_total_use_not_use()
        session.add(ram)
    for cpu in pc.cpu_info:
        cpu.update_cpu()
        session.add(cpu)
    for net in pc.network_interface:
        net.update_ip()
        session.add(net)
    session.commit()
    return {"status": "Updated", "hostname": pc.hostname}


#suppression un ordinateur et ses objets

#suppression d'un objets d'un ordinateur

#Ajout manuel d'un ordinateur 

#Ajout manuel d'un objets d'un ordinateur

#Affichage d'un ordinateur unique