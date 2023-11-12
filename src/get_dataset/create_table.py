from sqlalchemy import create_engine, Column, Integer, String, Sequence, URL, Text, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

urll = URL.create(
        drivername="postgresql",
        username="smarthack",
        password="12345",
        host="123.45.67.890",
        port="12345",
        database="smarthack"
    )

engine = create_engine(url)


# Create a base class for declarative class definitions
Base = declarative_base()


# Define the User class, representing the "users" table
class Tender_procedures(Base):
    __tablename__ = 'tender_procedures'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    tender_id = Column(String, unique=True)
    url = Column(String, unique=True)
    institution_name = Column(String)
    institution_type = Column(String)
    activity_type = Column(String)
    tender_name = Column(String)
    CPV_code = Column(String)
    contract_type = Column(String)
    short_desc = Column(String)
    long_desc = Column(Text)
    criteria_signing = Column(String)
    activity_capacity = Column(Text)
    technical_capacity = Column(Text)
    min_estimated_value = Column(String)
    max_estimated_value = Column(String)
    currency = Column(String)
    raw_estimated_value = Column(String)


class Tender_documents(Base):
    __tablename__ = 'tender_documents'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    doc_name = Column(String)
    down_link = Column(String)
    doc_content = Column(LargeBinary)

    tender_id = Column(String, ForeignKey('tender_procedures.tender_id'))


# Create the table in the database
# Base = declarative_base()
Base.metadata.create_all(engine)

# # Create a session to interact with the database
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Add a new user to the "users" table
# new_user = User(username='john_doe', email='john.doe@example.com')
# session.add(new_user)
# session.commit()
#
# # Query the "users" table
# queried_user = session.query(User).filter_by(username='john_doe').first()
# print("Queried User:", queried_user.username, queried_user.email)
