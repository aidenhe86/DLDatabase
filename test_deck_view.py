"""Deck View test"""

# run these tests like:
#
#    python -m unittest test_view_model.py

import os
from unittest import TestCase

from models import db, User, Deck
import json

os.environ["DATABASE_URL"] = "postgresql:///duellinks-test"

from app import app, CURR_USER_KEY

db.create_all()


class DeckViewTestCase(TestCase):
    """test view for deck"""

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

    def test_search_page(self):
        """test search card page"""
        with self.client as c:
            resp = c.get("/search")
            self.assertEqual(resp.status_code,200)
            self.assertIn("Card Name",str(resp.data))

    def test_api_search(self):
        """test search card api"""
        with self.client as c:
            resp = c.get("/api/card_search")
            self.assertEqual(resp.status_code,200)
            self.assertIn("Cell Breeding Device",str(resp.data))


    def test_add_deck(self):
        """can user add deck?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            # before add deck should have test-deck in deck page
            resp = c.get("/decks")
            self.assertIn("test-deck",str(resp.data))

            deck = {
                "name" : "test deck 2",
                "md1_id"    : "6850209",
                "md2_id"    : "6850209",
                "md3_id"    : "6850209",
                "md4_id"    : "12644061",
                "md5_id"    : "12644061",
                "md6_id"    : "12644061",
                "md7_id"    : "1475311",
                "md8_id"    : "1475311",
                "md9_id"    : "1475311",
                "md10_id"   : "69831560",
                "md11_id"   : "69831560",
                "md12_id"   : "69831560",
                "md13_id"   : "87112784",
                "md14_id"   : "87112784",
                "md15_id"   : "87112784",
                "md16_id"   : "41925941",
                "md17_id"   : "41925941",
                "md18_id"   : "41925941",
                "md19_id"   : "33731070",
                "md20_id"   : "33731070"
            }
            deckJSON = json.dumps(deck)
            resp = c.post("/decks/add",data = deckJSON,content_type='application/json')

            # should return 204 and empty string
            self.assertEqual(resp.status_code,204)
            self.assertIn("",str(resp.data))

            # after add deck should have test deck 2 in the deck page
            resp = c.get("/decks")
            self.assertIn("test deck 2",str(resp.data))
    
    def test_add_deck_no_session(self):
        """test add deck without log in"""
        with self.client as c:
            deck = {
                "name" : "test deck 2",
                "md1_id"    : "6850209",
                "md2_id"    : "6850209",
                "md3_id"    : "6850209",
                "md4_id"    : "12644061",
                "md5_id"    : "12644061",
                "md6_id"    : "12644061",
                "md7_id"    : "1475311",
                "md8_id"    : "1475311",
                "md9_id"    : "1475311",
                "md10_id"   : "69831560",
                "md11_id"   : "69831560",
                "md12_id"   : "69831560",
                "md13_id"   : "87112784",
                "md14_id"   : "87112784",
                "md15_id"   : "87112784",
                "md16_id"   : "41925941",
                "md17_id"   : "41925941",
                "md18_id"   : "41925941",
                "md19_id"   : "33731070",
                "md20_id"   : "33731070"
            }
            deckJSON = json.dumps(deck)
            resp = c.post("/decks/add",data = deckJSON,content_type='application/json',follow_redirects=True)

            # should return Access unauthorized
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

    
    def test_edit_deck(self):
        """can user edit deck?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            # before add deck should have test-deck in deck page
            resp = c.get("/decks")
            self.assertIn("test-deck",str(resp.data))

            deck = {
                "name" : "test deck 2",
                "md1_id"    : "6850209",
                "md2_id"    : "6850209",
                "md3_id"    : "6850209",
                "md4_id"    : "12644061",
                "md5_id"    : "12644061",
                "md6_id"    : "12644061",
                "md7_id"    : "1475311",
                "md8_id"    : "1475311",
                "md9_id"    : "1475311",
                "md10_id"   : "69831560",
                "md11_id"   : "69831560",
                "md12_id"   : "69831560",
                "md13_id"   : "87112784",
                "md14_id"   : "87112784",
                "md15_id"   : "87112784",
                "md16_id"   : "41925941",
                "md17_id"   : "41925941",
                "md18_id"   : "41925941",
                "md19_id"   : "33731070",
                "md20_id"   : "33731070"
            }
            deckJSON = json.dumps(deck)

            resp = c.post("/decks/1234/edit",data = deckJSON,content_type='application/json')
            # should return 204 and empty string
            self.assertEqual(resp.status_code,204)
            self.assertIn("",str(resp.data))

            # after edit deck should have test deck 2 in the deck page, and only 1 deck in the page
            resp = c.get("/decks")
            self.assertNotIn("test-deck",str(resp.data))
            self.assertIn("test deck 2",str(resp.data))
    
    def test_edit_deck_no_session(self):
        """test edit deck without log in"""
        with self.client as c:
            deck = {
                "name" : "test deck 2",
                "md1_id"    : "6850209",
                "md2_id"    : "6850209",
                "md3_id"    : "6850209",
                "md4_id"    : "12644061",
                "md5_id"    : "12644061",
                "md6_id"    : "12644061",
                "md7_id"    : "1475311",
                "md8_id"    : "1475311",
                "md9_id"    : "1475311",
                "md10_id"   : "69831560",
                "md11_id"   : "69831560",
                "md12_id"   : "69831560",
                "md13_id"   : "87112784",
                "md14_id"   : "87112784",
                "md15_id"   : "87112784",
                "md16_id"   : "41925941",
                "md17_id"   : "41925941",
                "md18_id"   : "41925941",
                "md19_id"   : "33731070",
                "md20_id"   : "33731070"
            }
            deckJSON = json.dumps(deck)
            resp = c.post("/decks/1234/edit",data = deckJSON,content_type='application/json',follow_redirects=True)

            # should return Access unauthorized
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))
    
    def test_delete_deck(self):
        """can user delete deck?"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            # before add deck should have test-deck in deck page
            resp = c.get("/decks")
            self.assertIn("test-deck",str(resp.data))

            resp = c.post("/decks/1234/delete")

            # should return 302 redirect
            self.assertEqual(resp.status_code,302)

            # deck should removed
            self.assertNotIn("test-deck",str(resp.data))
    
    def test_delete_deck_no_session(self):
        """test delete deck without session"""
        with self.client as c:
            resp = c.post("/decks/1234/delete",follow_redirects=True)

            # should return Access unauthorized
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))



