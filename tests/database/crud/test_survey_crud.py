import unittest
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.crud import survey_crud
from app.database.models import models
from uuid import uuid4, UUID
from testing.postgresql import Postgresql

from app.database.schemas import schemas


class TestSurveyCrud(unittest.TestCase):

    def setUp(self):
        self.postgresql = Postgresql()
        dsn = self.postgresql.dsn(dialect="postgresql")
        engine = create_engine(
            f"postgresql://{dsn['user']}@{dsn['host']}:{dsn['port']}/{dsn['database']}")
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = Session()
        models.Base.metadata.create_all(bind=engine)

    def tearDown(self):
        self.db.close()
        self.postgresql.stop()

    @patch('app.database.crud.survey_crud.get_survey',
           return_value=models.Survey(
               id="10000000-0000-0000-0000-000000000000",
               creator_id="20000000-0000-0000-0000-000000000000"
           ))
    def test_get_survey(self, mock_get_survey):
        survey_id = "10000000-0000-0000-0000-000000000000"

        result = survey_crud.get_survey(self.db, survey_id)
        self.assertEqual(result.id, survey_id)

        mock_get_survey.assert_called_once_with(self.db, survey_id)

    @patch('app.database.crud.survey_crud.get_surveys_by_creator_id',
           return_value=[
               models.Survey(
                   id="10000000-0000-0000-0000-000000000000",
                   creator_id="20000000-0000-0000-0000-000000000000"
               ),
               models.Survey(
                   id="11111111-0000-0000-0000-000000000000",
                   creator_id="20000000-0000-0000-0000-000000000000"
               )
           ])
    def test_get_surveys_by_creator(self, mock_get_surveys_by_creator_id):
        creator_id = "20000000-0000-0000-0000-000000000000"
        survey_id_1 = "10000000-0000-0000-0000-000000000000"
        survey_id_2 = "11111111-0000-0000-0000-000000000000"

        result = survey_crud.get_surveys_by_creator_id(self.db, creator_id)

        self.assertTrue(2, len(result))
        self.assertEqual(survey_id_1, result[0].id)
        self.assertEqual(survey_id_2, result[1].id)
        mock_get_surveys_by_creator_id.assert_called_once_with(self.db, creator_id)

    def test_create_survey(self):
        title = "good survey"
        description = "this is a good survey"
        survey_data = {
            "creator_id": str(uuid4()),
            "title": title,
            "description": description
        }
        survey_create = schemas.SurveyCreate(**survey_data)

        result = survey_crud.create_survey(self.db, survey_create)

        self.assertIsInstance(result.id, UUID)
        self.assertIsInstance(result.creator_id, UUID)
        self.assertEqual(title, result.title)
        self.assertEqual(description, result.description)

    def test_delete_survey(self):
        title = "good survey"
        description = "this is a good survey"
        survey_data = {
            "creator_id": str(uuid4()),
            "title": title,
            "description": description
        }
        survey_create = schemas.SurveyCreate(**survey_data)
        created_survey = survey_crud.create_survey(self.db, survey_create)

        result = survey_crud.delete_survey(self.db, created_survey.id)

        self.assertEqual(created_survey.id, result.id)
        self.assertEqual(created_survey.creator_id, result.creator_id)
        self.assertEqual(created_survey.title, result.title)
        self.assertEqual(created_survey.description, result.description)

        db_content = self.db.query(models.Survey).all()
        self.assertFalse(db_content)

    def test_delete_surveys_by_creator_id(self):
        creator_id = str(uuid4())
        survey_data_1 = {
            "creator_id": creator_id,
            "title": "Survey 1",
            "description": "Description 1"
        }
        survey_create_1 = schemas.SurveyCreate(**survey_data_1)
        survey_crud.create_survey(self.db, survey_create_1)
        survey_data_2 = {
            "creator_id": creator_id,
            "title": "Survey 2",
            "description": "Description 2"
        }
        survey_create_2 = schemas.SurveyCreate(**survey_data_2)
        survey_crud.create_survey(self.db, survey_create_2)

        result = survey_crud.delete_surveys_by_creator_id(self.db, creator_id)

        self.assertEqual(2, len(result))
        self.assertEqual(UUID(creator_id), result[0].creator_id)
        self.assertEqual(UUID(creator_id), result[1].creator_id)
        db_content = self.db.query(models.Survey).all()
        self.assertFalse(db_content)
