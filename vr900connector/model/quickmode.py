from enum import Enum

from . import Constants


class QuickMode(Enum):
    """
    Quick modes are mode you can quickly set with the app. Most of the times, quick modes have system wise impact.
    Example: for 'ONE_DAY_AWAY', the quick mode will prevent zones, rooms and water heater from heating.

    This is different from quick veto, which will only impact one component.

    Quick mode are taking precedence in case of simultaneous quick veto and quick mode.

    This class is a helper to check what is impacted by a quick mode.

    Note that there is a default duration for quick modes (which can't be changed) but the API always returns '0' as
    remaining duration, so there is no way to know when quick mode will end

    Vaillant documentation link:
    http://elearning.vaillant.com/vrc700/ci/en/documents/uk/infopool/Operating_instructions.pdf

    Args:
        name: Name of the quick mode, directly coming from the API
        for_zone: does the quick mode apply to a zone ?
        for_room: does the quick mode apply to a room ?
        for_hot_water: does the quick mode apply to the hot_water ?
        for_circulation: does the quick mode apply to the circulation ?
    """

    def __init__(self, mode_name, for_zone: bool, for_room: bool, for_hot_water: bool, for_circulation: bool):
        self.mode_name = mode_name
        self.for_zone = for_zone
        self.for_room = for_room
        self.for_hot_water = for_hot_water
        self.for_circulation = for_circulation

    QM_HOTWATER_BOOST = (Constants.QM_HOTWATER_BOOST, False, False, True, True)
    """
    The advanced function heats the water in the domestic hot water cylinder once until the desired DHW circuit 
    temperature set is reached or until you cancel the advanced function early. The heating installation will then 
    return to the pre-set mode
    """

    QM_VENTILATION_BOOST = (Constants.QM_VENTILATION_BOOST, True, True, False, False)
    """
    This advanced function switches the zone off for 30 minutes. The frost protection function is activated, and hot 
    water  generation and circulation remain active. Ventilation is activated and works at the highest ventilation 
    level.
    The advanced function is automatically deactivated after 30 minutes or if you cancel the advanced function early. 
    The heating installation will then return to the pre-set mode
    """

    QM_ONE_DAY_AWAY = (Constants.QM_ONE_DAY_AWAY, True, False, True, True)
    """
    Hot water generation and circulation are switched off and the frost protection is activated. The advanced function 
    is automatically deactivated after 24:00 hours or if you cancel the advanced function first. The heating 
    installation will then return to the pre-set mode. Ventilation is activated and works at the lowest ventilation 
    level.
    """

    QM_SYSTEM_OFF = (Constants.QM_SYSTEM_OFF, True, True, True, True)
    """
    The heating function, hot water circuit and cooling are switched off. The frost protection function is activated.
    The circulation is switched off. Ventilation is activated and works at the lowest ventilation level.
    """

    QM_ONE_DAY_AT_HOME = (Constants.QM_ONE_DAY_AT_HOME, True, False, False, False)
    """
    This advanced function activates Automatic mode for one day with the settings for Sunday, as set using the Time 
    programmes function. The advanced function is automatically deactivated after 24:00 hours or if you cancel the 
    advanced function first. The heating installation will then return to the pre-set mode.
    """

    QM_PARTY = (Constants.QM_PARTY, True, False, False, False)
    """
    The advanced function brings the room temperature to the set desired Day temperature, in accordance with the set 
    time periods. The advanced function is deactivated after six hours or if you cancel it before the six hours is up. 
    The heating installation will then return to the pre-set mode.
    """

    @staticmethod
    def from_name(name):
        """

        :param name: Name of the quick mode
        :return: QuickMode instance based one the name of the quick mode
        """

        return QuickMode[name]

    @staticmethod
    def for_zone() -> list:
        sub_list = []

        for quickMode in QuickMode:
            if quickMode.for_zone:
                sub_list.append(quickMode)

        return sub_list

    @staticmethod
    def for_room() -> []:
        sub_list = []

        for quickMode in QuickMode:
            if quickMode.for_room:
                sub_list.append(quickMode)

        return sub_list

    @staticmethod
    def for_hot_water() -> []:
        sub_list = []

        for quickMode in QuickMode:
            if quickMode.for_hot_water:
                sub_list.append(quickMode)

        return sub_list

    @staticmethod
    def for_circulation() -> []:
        sub_list = []

        for quickMode in QuickMode:
            if quickMode.for_circulation:
                sub_list.append(quickMode)

        return sub_list
