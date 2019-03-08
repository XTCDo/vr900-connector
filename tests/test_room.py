import unittest

from vr900connector.model import Room, Constants


class RoomTest(unittest.TestCase):

    def test_get_active_mode_manual(self):
        room = Room('id', 'Test', None, 5.0, 7.0, Constants.MODE_MANUAL, None, True, False, [])

        active_mode = room.active_mode

        self.assertEqual(Constants.MODE_MANUAL, active_mode.current_mode)
        self.assertEqual(7.0, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_off(self):
        hot_water = Room('id', 'Test', None, 5.0, 7.0, Constants.MODE_OFF, None, True, False, [])

        active_mode = hot_water.active_mode

        self.assertEqual(Constants.MODE_OFF, active_mode.current_mode)
        self.assertEqual(Room.MIN_TEMP, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)


if __name__ == '__main__':
    unittest.main()
