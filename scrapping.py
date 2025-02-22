import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, sessionmaker
from database import engine, get_db  # utiliza sua configuração atual

Base = declarative_base()

class MenuNav(Base):
    __tablename__ = "menu_nav"
    id = Column(Integer, primary_key=True, nullable=False)
    menuNav = Column(String, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

Base.metadata.create_all(bind=engine)

def scrapping():
    url = "https://www.ufu.br"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Falha ao acessar {url}: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, "html.parser")
    nav = soup.find("nav", id="block-ufu-rodape-2")
    if not nav:
        print("Elemento de navegação não encontrado!")
        return
    links = nav.find_all("a")
    if not links:
        print("Nenhum link encontrado no elemento de navegação!")
        return
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        for a in links:
            texto = a.get_text(strip=True)
            href = a.get("href")
            if href and not href.startswith("http"):
                href = url + href
            menu_item = MenuNav(
                menuNav=texto,
                link=href,
                created_at=datetime.now()
            )
            session.add(menu_item)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()

if __name__ == "__main__":
    scrapping()
