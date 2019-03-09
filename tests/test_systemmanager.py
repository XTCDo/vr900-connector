import json
import unittest

import responses

from tests.testutil import TestUtil
from vr900connector.api import Urls
from vr900connector.systemmanager import SystemManager


class SystemManagerTest(unittest.TestCase):

    @responses.activate
    def test_system(self):
        serial = TestUtil.mock_full_auth_success()

        with open(TestUtil.path('files/responses/livereport'), 'r') as file:
            livereport_data = json.loads(file.read())

        with open(TestUtil.path('files/responses/rooms'), 'r') as file:
            rooms_data = json.loads(file.read())

        with open(TestUtil.path('files/responses/systemcontrol'), 'r') as file:
            system_data = json.loads(file.read())

        with open(TestUtil.path('files/responses/hvacstate'), 'r') as file:
            hvacstate_data = json.loads(file.read())

        self._mock_urls(hvacstate_data, livereport_data, rooms_data, serial, system_data)

        manager = SystemManager("user", "pass", "test", TestUtil.temp_path())
        system = manager.get_system()

        self.assertIsNotNone(system)

        self.assertEqual(2, len(system.zones))
        self.assertEqual(4, len(system.rooms))

    # @responses.activate
    # def test_active_mode_hot_water_boost(self):
    #     serial = TestUtil.mock_full_auth_success()
    #
    #     with open(TestUtil.path('files/responses/livereport'), 'r') as file:
    #         livereport_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/rooms'), 'r') as file:
    #         rooms_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/systemcontrol_hotwater_boost'), 'r') as file:
    #         system_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/hvacstate'), 'r') as file:
    #         hvacstate_data = json.loads(file.read())
    #
    #     self._mock_urls(hvacstate_data, livereport_data, rooms_data, serial, system_data)
    #
    #     manager = SystemManager("user", "pass", "test", TestUtil.temp_path())
    #     system = manager.get_system()
    #
    #     self.assertIsNotNone(system)
    #
    #     active_mode = system.get_active_mode_hot_water()
    #     self.assertEqual(Constants.QM_HOTWATER_BOOST, active_mode.current_mode)
    #     self.assertEqual(51, active_mode.target_temperature)
    #
    # @responses.activate
    # def test_active_mode_system_off(self):
    #     serial = TestUtil.mock_full_auth_success()
    #
    #     with open(TestUtil.path('files/responses/livereport'), 'r') as file:
    #         livereport_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/rooms'), 'r') as file:
    #         rooms_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/systemcontrol_off'), 'r') as file:
    #         system_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/hvacstate'), 'r') as file:
    #         hvacstate_data = json.loads(file.read())
    #
    #     self._mock_urls(hvacstate_data, livereport_data, rooms_data, serial, system_data)
    #
    #     manager = SystemManager("user", "pass", "test", TestUtil.temp_path())
    #     system = manager.get_system()
    #
    #     self.assertIsNotNone(system)
    #
    #     active_mode = system.get_active_mode_hot_water()
    #     self.assertEqual(QuickMode.QM_SYSTEM_OFF.name, active_mode.current_mode)
    #     self.assertEqual(HotWater.MIN_TEMP, active_mode.target_temperature)
    #
    #     active_mode = system.get_active_mode_circulation()
    #     self.assertEqual(QuickMode.QM_SYSTEM_OFF.name, active_mode.current_mode)
    #     self.assertIsNone(active_mode.target_temperature)
    #
    #     for room in system.rooms:
    #         active_mode = system.get_active_mode_room(room)
    #         self.assertEqual(QuickMode.QM_SYSTEM_OFF.name, active_mode.current_mode)
    #         self.assertEqual(Constants.FROST_PROTECTION_TEMP, active_mode.target_temperature)
    #
    #     for zone in system.zones:
    #         if not zone.rbr:
    #             active_mode = system.get_active_mode_zone(zone)
    #             self.assertEqual(QuickMode.QM_SYSTEM_OFF.name, active_mode.current_mode)
    #             self.assertEqual(Constants.FROST_PROTECTION_TEMP, active_mode.target_temperature)
    #
    # @responses.activate
    # def test_active_mode_zone_quick_veto(self):
    #     serial = TestUtil.mock_full_auth_success()
    #
    #     with open(TestUtil.path('files/responses/livereport'), 'r') as file:
    #         livereport_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/rooms'), 'r') as file:
    #         rooms_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/systemcontrol_quick_veto'), 'r') as file:
    #         system_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/hvacstate'), 'r') as file:
    #         hvacstate_data = json.loads(file.read())
    #
    #     self._mock_urls(hvacstate_data, livereport_data, rooms_data, serial, system_data)
    #
    #     manager = SystemManager("user", "pass", "test", TestUtil.temp_path())
    #     system = manager.get_system()
    #
    #     self.assertIsNotNone(system)
    #
    #     zone = system.get_zone("Control_ZO2")
    #     active_mode = system.get_active_mode_zone(zone)
    #     self.assertEqual(Constants.QUICK_VETO, active_mode.current_mode)
    #     self.assertEqual(18.5, active_mode.target_temperature)
    #
    # @responses.activate
    # def test_active_mode_room_quick_veto(self):
    #     serial = TestUtil.mock_full_auth_success()
    #
    #     with open(TestUtil.path('files/responses/livereport'), 'r') as file:
    #         livereport_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/rooms_quick_veto'), 'r') as file:
    #         rooms_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/systemcontrol'), 'r') as file:
    #         system_data = json.loads(file.read())
    #
    #     with open(TestUtil.path('files/responses/hvacstate'), 'r') as file:
    #         hvacstate_data = json.loads(file.read())
    #
    #     self._mock_urls(hvacstate_data, livereport_data, rooms_data, serial, system_data)
    #
    #     manager = SystemManager("user", "pass", "test", TestUtil.temp_path())
    #     system = manager.get_system()
    #
    #     self.assertIsNotNone(system)
    #
    #     room = system.get_room(0)
    #     active_mode = system.get_active_mode_room(room)
    #     self.assertEqual(Constants.QUICK_VETO, active_mode.current_mode)
    #     self.assertEqual(20.0, active_mode.target_temperature)

    def _mock_urls(self, hvacstate_data, livereport_data, rooms_data, serial, system_data):
        responses.add(responses.GET, Urls.live_report().format(serial_number=serial), json=livereport_data,
                      status=200)
        responses.add(responses.GET, Urls.rooms().format(serial_number=serial), json=rooms_data, status=200)
        responses.add(responses.GET, Urls.system().format(serial_number=serial), json=system_data, status=200)
        responses.add(responses.GET, Urls.hvac().format(serial_number=serial), json=hvacstate_data, status=200)


if __name__ == '__main__':
    unittest.main()
