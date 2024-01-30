from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.repository.config.database import Base, get_db


def setup_test_db(app):
    SQLALCHEMY_DATABASE_URL = "postgresql://surveyuser:admin@localhost/surveydbtest"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
