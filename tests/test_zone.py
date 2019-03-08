import unittest

from vr900connector.model import Zone, Constants


class ZoneTest(unittest.TestCase):

    def test_get_active_mode_night(self):
        zone = Zone('id', 'Test', None, 10.0, 7.0, Constants.MODE_NIGHT, None, 6.0, 'Heating', False)

        active_mode = zone.active_mode

        self.assertEqual(Constants.MODE_NIGHT, active_mode.current_mode)
        self.assertEqual(6.0, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_day(self):
        zone = Zone('id', 'Test', None, 10.0, 7.0, Constants.MODE_DAY, None, 6.0, 'Heating', False)

        active_mode = zone.active_mode

        self.assertEqual(Constants.MODE_DAY, active_mode.current_mode)
        self.assertEqual(7.0, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_off(self):
        zone = Zone('id', 'Test', None, 10.0, 7.0, Constants.MODE_OFF, None, 6.0, 'Heating', False)

        active_mode = zone.active_mode

        self.assertEqual(Constants.MODE_OFF, active_mode.current_mode)
        self.assertEqual(Zone.MIN_TEMP, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)


if __name__ == '__main__':
    unittest.main()
