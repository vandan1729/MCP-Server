from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List


engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)


Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NoteRepository:

    @staticmethod
    def get_notes_by_user_id(user_id: str) -> List[Note]:
        db = SessionLocal()
        try:
            return db.query(Note).filter(Note.user_id == user_id).all()
        finally:
            db.close()

    @staticmethod
    def create_note(user_id: str, content: str) -> Note:
        db = SessionLocal()
        try:
            note = Note(user_id=user_id, content=content)
            db.add(note)
            db.commit()
            db.refresh(note)
            return note
        finally:
            db.close()

    @staticmethod
    def delete_note_by_user_id_note_id(user_id: str, note_id: int):
        db = SessionLocal()
        try:
            note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
            if note:
                db.delete(note)
                db.commit()
        finally:
            db.close()
