from sqlalchemy import create_engine, Column, Integer, String, or_, text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite:///./bdd/chatbot_metadata.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    titre = Column(String(200))
    url = Column(String(300))
    tags = Column(String(200))

    @staticmethod
    def load_tags_keywords_from_db(db: Session):
        rows = db.execute(text("SELECT tag, keyword FROM tags_keywords")).fetchall()
        tags_keywords = {}
        for tag, keyword in rows:
            tags_keywords.setdefault(tag, []).append(keyword)
        return tags_keywords

    @staticmethod
    def extract_tags_from_question(question: str, tags_keywords: dict):
        question = question.lower()
        tags = set()
        for tag, keywords in tags_keywords.items():
            for kw in keywords:
                if kw in question:
                    tags.add(tag)
                    break
        return list(tags)
    # def extract_tags_from_question(question: str):
    #     question = question.lower()
    #     tags = []
    #     if "inscription" in question:
    #         tags.append("Inscription")
    #     if "perceptron" in question:
    #         tags.append("Deep Learning")
    #     if "deep learning" in question:
    #         tags.append("Deep Learning")
    #     if "pyspark" in question:
    #         tags.append("PySpark")
    #     if "ml" in question or "machine learning" in question:
    #         tags.append("Machine Learning")
    #     return tags

    @staticmethod
    def get_additional_resources(db: Session, context_tags: list):
        if not context_tags:
            return []
        filters = [Resource.tags.ilike(f"%{tag}%") for tag in context_tags]
        return db.query(Resource).filter(or_(*filters)).all()

class ResourceCreate(BaseModel):
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

class ResourceOut(BaseModel):
    id: int
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

    class Config: # <-- Ajoutez cette classe Config
        from_attributes = True # <-- C'est la ligne magique !

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    chat_message_id = Column(Integer) 
    sentiment = Column(String(400), nullable=False) 
    timestamp = Column(DateTime, default=func.now())
    user_id = Column(Integer) # Si vous avez une table users
    

    

# Pydantic model pour la requête de feedback
class FeedbackRequest(BaseModel):
    chat_message_id: int
    sentiment: str # 'satisfied' ou 'dissatisfied'
    user_id: Optional[int] = None
    

class FeedbackResponse(BaseModel):
    message: str
    status: str