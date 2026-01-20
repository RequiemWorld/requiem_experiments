from dataclasses import dataclass
from scurrypy.models import ChannelModel


@dataclass
class GatewayEventPayload:
    """
    A gateway event payload is what is sent to or from the discord gateway. It has a
    number indicating the purpose of the JSON compatible data contained within.
    """
    opcode: int
    """The operation number indicating the intent/context of the event."""
    event_data: dict
    """The data in the event to be handled by the client application."""
