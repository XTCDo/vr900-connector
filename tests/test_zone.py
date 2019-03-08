import unittest
import datetime

from vr900connector.model import TimeProgramDaySetting, TimeProgramDay, TimeProgram, Zone, System, QuickVeto, \
    Constants, HolidayMode, QuickMode


class ZoneTest(unittest.TestCase):

    def test_get_active_mode_zone(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
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

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, 18, 'STANDBY', False)
        system = System(None, None, [zone], None, None, None, 5, None)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, Constants.MODE_AUTO)
        self.assertEqual(active_mode.sub_mode, timeprogram_day_setting.mode)
        self.assertEqual(active_mode.target_temperature, timeprogram_day_setting.target_temperature)

    def test_get_active_mode_zone_quick_veto(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
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
        quickveto = QuickVeto(0, 55)

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, quickveto, 18, 'STANDBY', False)
        system = System(None, None, [zone], None, None, None, 5, None)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, Constants.QUICK_VETO)
        self.assertEqual(active_mode.target_temperature, quickveto.target_temperature)

    def test_get_active_mode_zone_holiday_mode(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
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
        holiday_mode = HolidayMode(True, datetime.date.today(), datetime.date.today(), 10)

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, 18, 'STANDBY', False)
        system = System(holiday_mode, None, [zone], None, None, None, 5, None)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, Constants.HOLIDAY_MODE)
        self.assertEqual(active_mode.target_temperature, holiday_mode.target_temperature)

    def test_get_active_mode_zone_quick_mode_water_boost(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
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

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, 18, 'STANDBY', False)
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_HOTWATER_BOOST)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, Constants.MODE_AUTO)
        self.assertEqual(active_mode.sub_mode, timeprogram_day_setting.mode)
        self.assertEqual(active_mode.target_temperature, timeprogram_day_setting.target_temperature)

    def test_get_active_mode_zone_quick_mode_system_off(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
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

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, 18, 'STANDBY', False)
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_SYSTEM_OFF)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, QuickMode.QM_SYSTEM_OFF.name)
        self.assertEqual(active_mode.target_temperature, Zone.MIN_TEMP)

    def test_get_active_mode_zone_quick_mode_one_day_home(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, Constants.MODE_DAY)
        timeprogram_day_setting_sunday = TimeProgramDaySetting('00:00', 25, Constants.MODE_DAY)
        timeprogram_day = TimeProgramDay([timeprogram_day_setting])
        timeprogram_days = {
            'monday': timeprogram_day,
            'tuesday': timeprogram_day,
            'wednesday': timeprogram_day,
            'thursday': timeprogram_day,
            'friday': timeprogram_day,
            'saturday': timeprogram_day,
            'sunday': TimeProgramDay([timeprogram_day_setting_sunday]),
        }
        timeprogram = TimeProgram(timeprogram_days)

        zone = Zone('1', 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, 18, 'STANDBY', False)
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_ONE_DAY_AT_HOME)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(active_mode.current_mode, QuickMode.QM_ONE_DAY_AT_HOME.name)
        self.assertEqual(active_mode.target_temperature, timeprogram_day_setting_sunday.target_temperature)
