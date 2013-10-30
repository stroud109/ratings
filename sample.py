class Ratings(Base): 
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    user = relationship("User")

class Movies(Base):
    __tablename__ = 'left' # parent
    id = Column(Integer, primary_key=True)
    children = relationship("Ratings")

class User(Base):
    __tablename__ = 'right' # child
    id = Column(Integer, primary_key=True)