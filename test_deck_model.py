"""Deck Model test"""

# run these tests like:
#
#    python -m unittest test_deck_model.py

import os
from unittest import TestCase

from models import db, User, Deck

os.environ["DATABASE_URL"] = "postgresql:///duellinks-test"

from app import app

db.create_all()

class DeckModelTestCase(TestCase):
    """ test models for decks"""

    def setUp(self):
        """Create test client and add sample data."""
        # delete data
        User.query.delete()
        Deck.query.delete()

        # insert default user
        self.testuser = User.signup("test1","password",None)
        self.testuser_id = 1111
        self.testuser.id = self.testuser_id

        # create default deck
        testdeck = Deck(
            name = "test-deck",
            user_id = self.testuser_id,
            id = 1234,
            md1_id    = 6850209,
            md2_id    = 6850209,
            md3_id    = 6850209,
            md4_id    = 12644061,
            md5_id    = 12644061,
            md6_id    = 12644061,
            md7_id    = 1475311,
            md8_id    = 1475311,
            md9_id    = 1475311,
            md10_id   = 69831560,
            md11_id   = 69831560,
            md12_id   = 69831560,
            md13_id   = 87112784,
            md14_id   = 87112784,
            md15_id   = 87112784,
            md16_id   = 41925941,
            md17_id   = 41925941,
            md18_id   = 41925941,
            md19_id   = 33731070,
            md20_id   = 33731070
        )
        db.session.add(testdeck)
        db.session.commit()

        # create test client
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    def test_add_deck_model(self):
        """check if the add deck model works correctly"""

        # should have default deck 1
        self.assertEqual(len(self.testuser.decks),1)
        self.assertEqual(self.testuser.decks[0].name,"test-deck")

        deck = Deck(
            name = "test deck 2",
            user_id = self.testuser_id,
            md1_id    = 6850209,
            md2_id    = 6850209,
            md3_id    = 6850209,
            md4_id    = 12644061,
            md5_id    = 12644061,
            md6_id    = 12644061,
            md7_id    = 1475311,
            md8_id    = 1475311,
            md9_id    = 1475311,
            md10_id   = 69831560,
            md11_id   = 69831560,
            md12_id   = 69831560,
            md13_id   = 87112784,
            md14_id   = 87112784,
            md15_id   = 87112784,
            md16_id   = 41925941,
            md17_id   = 41925941,
            md18_id   = 41925941,
            md19_id   = 33731070,
            md20_id   = 33731070
        )
        db.session.add(deck)
        db.session.commit()

        # testuser should have 2 deck
        self.assertEqual(len(self.testuser.decks),2)
        self.assertEqual(self.testuser.decks[1].name,"test deck 2")
    
    def test_edit_deck_model(self):
        """check if the edit deck model works correctly"""
        deck = Deck.query.get(1234)
        deck.name = "test deck rename"
        deck.md20_id = 86198326
        deck.md21_id = 86198326

        db.session.commit()

        # test deck should renamed, have card 21, and card 20 have changed
        self.assertIsNotNone(deck.md21_id)
        self.assertNotEqual(deck.name,"test-deck")
        self.assertNotEqual(deck.md20_id,33731070)