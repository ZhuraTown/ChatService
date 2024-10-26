from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./test.db"  # или другой URL для вашей базы данных

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

