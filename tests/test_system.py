import datetime
import unittest

from vr900connector.model import System, TimeProgram, TimeProgramDaySetting, TimeProgramDay, QuickMode, QuickVeto, \
    HolidayMode, Room, HotWater, Zone, Constants, Circulation


class SystemTest(unittest.TestCase):

    def test_get_active_mode_room(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, None)
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

        room = Room(1, 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, False, False, [])
        system = System(None, None, [], [room], None, None, 5, None)

        active_mode = system.get_active_mode_room(room)

        self.assertEqual(active_mode.current_mode, Constants.MODE_AUTO)
        self.assertIsNone(active_mode.sub_mode)
        self.assertEqual(active_mode.target_temperature, timeprogram_day_setting.target_temperature)

    def test_get_active_mode_room_quick_veto(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, None)
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
        quick_veto = QuickVeto(0, 22)

        room = Room(1, 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, quick_veto, False, False, [])
        system = System(None, None, [], [room], None, None, 5, None)

        active_mode = system.get_active_mode_room(room)

        self.assertEqual(active_mode.current_mode, Constants.QUICK_VETO)
        self.assertEqual(active_mode.target_temperature, quick_veto.target_temperature)

    def test_get_active_mode_room_holiday_mode(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, None)
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

        room = Room(1, 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, False, False, [])
        system = System(holiday_mode, None, [], [room], None, None, 5, None)

        active_mode = system.get_active_mode_room(room)

        self.assertEqual(active_mode.current_mode, Constants.HOLIDAY_MODE)
        self.assertEqual(active_mode.target_temperature, holiday_mode.target_temperature)

    def test_get_active_mode_room_system_off(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 20, None)
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

        room = Room(1, 'Test', timeprogram, 20, 20, Constants.MODE_AUTO, None, False, False, [])
        system = System(None, None, [], [room], None, None, 5, QuickMode.QM_SYSTEM_OFF)

        active_mode = system.get_active_mode_room(room)

        self.assertEqual(active_mode.current_mode, QuickMode.QM_SYSTEM_OFF.name)
        self.assertEqual(active_mode.target_temperature, Room.MIN_TEMP)

    def test_get_active_mode_hot_water(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 55, Constants.MODE_ON)
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

        hot_water = HotWater('test', 'name', timeprogram, 50, 55, Constants.MODE_AUTO)
        system = System(None, None, [], [], hot_water, None, 5, None)

        active_mode = system.get_active_mode_hot_water()

        self.assertEqual(active_mode.current_mode, Constants.MODE_AUTO)
        self.assertEqual(active_mode.sub_mode, Constants.MODE_ON)
        self.assertEqual(active_mode.target_temperature, 55)

    def test_get_active_mode_hot_water_system_off(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 55, Constants.MODE_ON)
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

        hot_water = HotWater('test', 'name', timeprogram, 50, 55, Constants.MODE_AUTO)
        system = System(None, None, [], [], hot_water, None, 5, QuickMode.QM_SYSTEM_OFF)

        active_mode = system.get_active_mode_hot_water()

        self.assertEqual(active_mode.current_mode, QuickMode.QM_SYSTEM_OFF.name)
        self.assertEqual(active_mode.target_temperature, HotWater.MIN_TEMP)

    def test_get_active_mode_hot_water_hot_water_boost(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 55, Constants.MODE_ON)
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

        hot_water = HotWater('test', 'name', timeprogram, 50, 55, Constants.MODE_ON)
        system = System(None, None, [], [], hot_water, None, 5, QuickMode.QM_HOTWATER_BOOST)

        active_mode = system.get_active_mode_hot_water()

        self.assertEqual(active_mode.current_mode, QuickMode.QM_HOTWATER_BOOST.name)
        self.assertEqual(active_mode.target_temperature, 55)

    def test_get_active_mode_hot_water_holiday_mode(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', 55, Constants.MODE_ON)
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

        hot_water = HotWater('test', 'name', timeprogram, 50, 55, Constants.MODE_AUTO)
        system = System(holiday_mode, None, [], [], hot_water, None, 5, None)

        active_mode = system.get_active_mode_hot_water()

        self.assertEqual(active_mode.current_mode, Constants.HOLIDAY_MODE)
        self.assertEqual(active_mode.target_temperature, HotWater.MIN_TEMP)

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

    def test_get_active_mode_zone_quick_mode_one_day_away(self):
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
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_ONE_DAY_AWAY)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(QuickMode.QM_ONE_DAY_AWAY.name, active_mode.current_mode)
        self.assertEqual(zone.target_min_temperature, active_mode.target_temperature)

    def test_get_active_mode_zone_quick_mode_party(self):
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
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_PARTY)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(QuickMode.QM_PARTY.name, active_mode.current_mode)
        self.assertEqual(zone.target_temperature, active_mode.target_temperature)

    def test_get_active_mode_zone_quick_mode_ventilation(self):
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
        system = System(None, None, [zone], None, None, None, 5, QuickMode.QM_VENTILATION_BOOST)

        active_mode = system.get_active_mode_zone(zone)

        self.assertEqual(QuickMode.QM_VENTILATION_BOOST.name, active_mode.current_mode)
        self.assertEqual(Zone.MIN_TEMP, active_mode.target_temperature)

    def test_get_active_mode_circulation_hot_water_boost(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', None, Constants.MODE_ON)
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

        circulation = Circulation('id', 'name', timeprogram, Constants.MODE_AUTO)
        system = System(None, None, [], None, None, circulation, 5, QuickMode.QM_HOTWATER_BOOST)

        active_mode = system.get_active_mode_circulation()

        self.assertEqual(QuickMode.QM_HOTWATER_BOOST.name, active_mode.current_mode)
        self.assertIsNone(active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_circulation_off(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', None, Constants.MODE_ON)
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

        circulation = Circulation('id', 'name', timeprogram, Constants.MODE_AUTO)
        system = System(None, None, [], None, None, circulation, 5, QuickMode.QM_SYSTEM_OFF)

        active_mode = system.get_active_mode_circulation()

        self.assertEqual(QuickMode.QM_SYSTEM_OFF.name, active_mode.current_mode)
        self.assertIsNone(active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_circulation_holiday(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', None, Constants.MODE_ON)
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

        circulation = Circulation('id', 'name', timeprogram, Constants.MODE_AUTO)
        holiday_mode = HolidayMode(True, datetime.date.today(), datetime.date.today(), 10)
        system = System(holiday_mode, None, [], None, None, circulation, 5, None)

        active_mode = system.get_active_mode_circulation()

        self.assertEqual(Constants.HOLIDAY_MODE, active_mode.current_mode)
        self.assertIsNone(active_mode.target_temperature)
        self.assertIsNone(active_mode.sub_mode)

    def test_get_active_mode_circulation_auto(self):
        timeprogram_day_setting = TimeProgramDaySetting('00:00', None, Constants.MODE_ON)
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

        circulation = Circulation('id', 'name', timeprogram, Constants.MODE_AUTO)
        system = System(None, None, [], None, None, circulation, 5, None)

        active_mode = system.get_active_mode_circulation()

        self.assertEqual(Constants.MODE_AUTO, active_mode.current_mode)
        self.assertIsNone(active_mode.target_temperature)
        self.assertEqual(Constants.MODE_ON, active_mode.sub_mode)


if __name__ == '__main__':
    unittest.main()
