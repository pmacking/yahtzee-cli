import unittest
from roll import Roll
from player import Player


class TestRoll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setUpClass :class: `Roll <Roll>`')

    @classmethod
    def tearDownClass(cls):
        print('tearDownClass :class: `Roll <Roll>`')

    def setUp(self):
        print('setUp :obj: rollTest')

        # construct instance of Roll
        self.rollTest = Roll('rollTest')

        # construct instance of Player
        self.playerTest = Player('testPlayer')

    def tearDown(self):
        print('tearDown rollTest')

        # teardown instance of Roll
        self.rollTest.dispose()

        # tear down instance of Player
        self.playerTest.dispose()

    def test_instance_attributes(self):
        self.assertEqual(self.rollTest.name, 'rollTest')
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
