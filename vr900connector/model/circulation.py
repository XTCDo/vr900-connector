from . import Component, TimeProgram, ActiveMode, Constants


class Circulation(Component):
    """
    Circulation is quite a special component since there is no temperature nor quick veto involved.
    This class only exists to have a clean hierarchy
    """

    MODES = [Constants.MODE_ON, Constants.MODE_OFF, Constants.MODE_AUTO]
    """
    List of mode available for circulation
    """

    def __init__(self, component_id: any, name: str, time_program: TimeProgram, operation_mode: str):
        super().__init__(component_id, name, time_program, None, None, operation_mode, None)

    def _get_specific_active_mode(self) -> ActiveMode:
        return ActiveMode(None, self.operation_mode)
