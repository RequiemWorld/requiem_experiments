import abc
from cleancord.events import GatewayEventPayload


class DiscordGatewayInterface(abc.ABC):

    @abc.abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send_payload(self, payload: GatewayEventPayload) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def recv_payload(self) -> GatewayEventPayload:
        """
        :raises EOFError: When there it is no longer possible to read any more payloads/connection closed.
        """
        raise NotImplementedError