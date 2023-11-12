from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    conversation_id = Column(Integer(), ForeignKey("conversations.id"))
    content = Column(Text())
    role = Column(Text())


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    email = Column(Text())
    name = Column(Text())
