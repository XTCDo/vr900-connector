import unittest

from vr900connector.model import Component, Constants, QuickVeto, TimeProgramDaySetting, TimeProgramDay, TimeProgram


class ComponentTest(unittest.TestCase):

    def test_get_active_mode_quick_veto(self):
        comp = Component('Id', 'Name', None, 1.0, 5.0, Constants.MODE_AUTO, QuickVeto(300, 10.0))

        active_mode = comp.active_mode
        self.assertEqual(Constants.QUICK_VETO, active_mode.current_mode)
        self.assertEqual(10.0, active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_auto(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 25, Constants.MODE_ON)
        timeprogram_day = TimeProgramDay([timeprogram_day_setting])
        timeprogram_days = {
            'monday': timeprogram_day,
            'tuesday': timeprogram_day,
            'wednesday': timeprogram_day,
            'thursday': timeprogram_day,
            'friday': timeprogram_day,
            'saturday': timeprogram_day,
            'sunday': timeprogram_day,
        }
        timeprogram = TimeProgram(timeprogram_days)

        comp = Component('Id', 'Name', timeprogram, 1.0, 5.0, Constants.MODE_AUTO, None)

        active_mode = comp.active_mode
        self.assertEqual(Constants.MODE_AUTO, active_mode.current_mode)
        self.assertEqual(25, active_mode.target_temperature)
        self.assertEqual(Constants.MODE_ON, active_mode.sub_mode)


if __name__ == '__main__':
    unittest.main()
