from vr900connector.api import ApiConnector
import pprint

pp = pprint.PrettyPrinter(indent=4)

connector = ApiConnector('Guardway', 'Hopelijkluktditwel!')
pprint.pprint(connector.get_facilities())
