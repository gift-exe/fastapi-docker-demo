from sqlalchemy import String, Float, Integer, Column


from database import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, default='NULL', nullable=True)
    price = Column(Float)
    tax = Column(Float, default='0.0', nullable=True)