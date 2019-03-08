import json


class Payloads:
    """
    This is meant to be used with :mod: `vr900connector.api.urls` to allow user to easily obtain the payload for a
    request.
    Payload are always json formatted
    """

    @classmethod
    def set_temperature_setpoint(cls, temperature: float):
        """
        Payload used to set target temperature for a component
        """
        return json.dumps({'temperature_setpoint': str(temperature)})

    @classmethod
    def set_operation_mode(cls, mode: str):
        """
        Payload to set operation mode for a component
        """
        return json.dumps({'operation_mode': mode})

    @classmethod
    def quickmode(cls, quick_mode: str, duration: int = None):
        """
        Payload to set quick mode for the system
        """
        return json.dumps({
            "quickmode":
                {
                    "quickmode": quick_mode,
                    "duration": duration if duration is not None else 0
                }
        })
