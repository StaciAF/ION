#!/usr/bin/python3
"""
this module defines unit tests for Skills
testing functionality and documentation
"""
from datetime import datetime
from inspect import getmembers, isfunction
from models.base_model import BaseModel
from models.skills import Skills, __doc__ as skills_doc
import pep8
from time import sleep
from unittest import TestCase, mock


class Test_Skills_Docs(TestCase):
    """
    defines tests to check documentation and style
    for Skills module, class, and methods
    """

    @classmethod
    def setUpClass(self):
        """
        uses inspect to get all methods to test for docstrings
        saves as skills_methods attribute to call later
        """
        self.skills_methods = getmembers(Skills, isfunction)

    def test_pep8_style(self):
        """
        tests that models/skills.py
        and tests/test_models/test_skills.py
        follows pep8 style guidelines
        """
        for path in ['models/skills.py',
                     'tests/test_models/test_skills.py']:
            # tests each path as a subTest for 0 pep8 errors
            with self.subTest(path=path):
                errors = pep8.Checker(path).check_all()
                self.assertEqual(errors, 0,
                                 "pep8 is returning errors for {}".
                                 format(path))

    def test_module_docstring(self):
        """
        tests that models.skills module contains docstring
        """
        # first tests if docstring is not None
        self.assertIsNot(skills_doc, None,
                         "skills module is missing docstring")
        # then tests if there is at least 1 docstring
        self.assertTrue(len(skills_doc) > 1,
                        "skills module is missing docstring")

    def test_class_docstring(self):
        """
        tests that the Skills class contains docstring
        """
        # first tests if docstring is not None
        self.assertIsNot(Skills.__doc__, None,
                         "Skills class is missing docstring")
        # then tests if there is at least 1 docstring
        self.assertTrue(len(Skills.__doc__) > 1,
                        "Skills class is missing docstring")

    def test_method_docstrings(self):
        """
        tests that all methods in Skills have docstrings
        """
        for method in self.skills_methods:
            # tests each method as a subTest for missing docstrings
            with self.subTest(method=method):
                # first tests if docstring is not None
                self.assertIsNot(method[1].__doc__, None,
                                 "{} method is missing docstring".
                                 format(method[0]))
                # then tests if there is at least 1 docstring
                self.assertTrue(len(method[1].__doc__) > 1,
                                "{} method is missing docstring".
                                format(method[0]))


class Test_Skills(TestCase):
    """
    defines tests to check functionality
    of Skills class attributes and methods
    """

    def test_class_and_subclass(self):
        """
        tests that instances are of Skills class
        and are a subclass of BaseModel class
        """
        new_obj = Skills()
        # tests that the new instance is of type Skills
        self.assertIs(type(new_obj), Skills)
        # tests that the new instance is a subclass of BaseModel
        self.assertIsInstance(new_obj, BaseModel)

    def test_attribute_types(self):
        """
        tests the class attributes exist and are of correct type
        also tests instantiation of new object
        """
        # creates new instance of Skills
        new_obj = Skills()
        # adds name attribute (inherited requirement from BaseModel)
        # adds optional attributes for testing
        # (id should be set by primary key)
        # (created_at, updated_at should be set by datetime)
        new_obj.name = "test_name"
        # attributes_dict sets up dictionary of attribute names and types
        attributes_dict = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
        }
        # loops through attributes_dict as subTests to check each attribute
        for attr, attr_type in attributes_dict.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                # tests the expected attribute is in the instance's dict
                self.assertIn(attr, new_obj.__dict__)
                # tests the attribute is the expected type
                self.assertIs(type(new_obj.__dict__[attr]), attr_type)

    def test_updated_datetime_attributes(self):
        """
        tests that the datetime attribute updated_at changes
        when the save() method is implemented
        """
        first_time = datetime.now()
        new_obj = Skills()
        second_time = datetime.now()
        # tests if object's created_at time is between timestamps
        self.assertTrue(first_time <= new_obj.created_at <= second_time)
        # tests if object's updated_at is within the same timestamps
        self.assertTrue(first_time <= new_obj.updated_at <= second_time)
        # gets timestamps of current attributes and pauses a moment
        original_created_at = new_obj.created_at
        original_updated_at = new_obj.updated_at
        sleep(1)
        # adds required attributes so the object can be saved; saves object
        new_obj.name = "test_name"
        new_obj.save()
        # tests that the object's updated_at has changed and is later
        self.assertNotEqual(original_updated_at, new_obj.updated_at)
        self.assertTrue(original_updated_at < new_obj.updated_at)
        # tests that only the object's updated_at datetime has changed
        self.assertEqual(original_created_at, new_obj.created_at)

    def test_init_method(self):
        """
        tests the __init__ method for instantiating new objects
        both new and from kwargs
        __init__ method calls on inherited BaseModel with super()
        """
        # creates new instance of Skills
        new_obj1 = Skills()
        # tests that the new object is of type Skills
        self.assertIs(type(new_obj1), Skills)
        # adds all attributes for testing
        # (id should be set by primary key)
        # (created_at, updated_at should be set by datetime)
        new_obj1.name = "test_name"
        # attributes_dict sets up dictionary of attribute names and types
        attributes_dict = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
        }
        # loops through attributes_dict as subTests to check each attribute
        for attr, attr_type in attributes_dict.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                # tests the expected attribute is in the object's dict
                self.assertIn(attr, new_obj1.__dict__)
                # tests the attribute is the expected type
                self.assertIs(type(new_obj1.__dict__[attr]), attr_type)
        # sets kwargs using object's dict and uses to create new object
        kwargs = new_obj1.__dict__
        new_obj2 = Skills(**kwargs)
        # tests that the new object is of type Skills
        self.assertIs(type(new_obj2), Skills)
        # loops through attributes_dict as subTests to check each attribute
        for attr, attr_type in attributes_dict.items():
            with self.subTest(attr=attr, attr_type=attr_type):
                # tests the expected attribute is in the object's dict
                self.assertIn(attr, new_obj2.__dict__)
                # tests the attribute is the expected type
                self.assertIs(type(new_obj2.__dict__[attr]), attr_type)
                # tests the value of name attribute matches the original object
                self.assertEqual(new_obj1.__dict__[attr],
                                 new_obj2.__dict__[attr])

        # tests that __class__ is not set in object 2
        self.assertNotIn('__class__', new_obj2.__dict__)

    def test_str_method(self):
        """
        tests the __str__ method returns the correct format
        this method is inherited from BaseModel, but should show Skills class
        """
        # creates new instance of Skills and saves variables
        new_obj = Skills()
        obj_id = new_obj.id
        obj_dict = new_obj.__dict__
        # tests the string representation of object is formatted correctly
        self.assertEqual(str(new_obj),
                         "[Skills.{}] {}".format(obj_id, obj_dict))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """
        tests that the save() method inherited from BaseModel calls on
        storage.new() to add and commit the object to the database
        """
        # creates new instance of Skills
        new_obj = Skills()
        # adds name as required attribute for database
        # (id should be set by primary key)
        # (created_at, updated_at should be set by datetime)
        new_obj.name = "test_name"
        # saves new instance and tests if storage method new is called
        new_obj.save()
        self.assertTrue(mock_storage.new.called)

    @mock.patch('models.storage')
    def test_delete_method(self, mock_storage):
        """
        tests that the delete() method inherited from BaseModel calls on
        storage.delete() to remove and commit the object from the database
        """
        # creates new instance of Skills
        new_obj = Skills()
        # adds name as required attribute for database
        # (id should be set by primary key)
        # (created_at, updated_at should be set by datetime)
        new_obj.name = "test_name"
        # saves to database before attempting to delete
        new_obj.save()
        self.assertTrue(mock_storage.new.called)
        # deletes new instance and tests if storage method deleted is called
        new_obj.delete()
        self.assertTrue(mock_storage.delete.called)

    # functionality of save() and delete() methods are tested in unit tests
    # for DBStorage as the storage engine is doing the work to actually
    # save or delete the objects from the database
