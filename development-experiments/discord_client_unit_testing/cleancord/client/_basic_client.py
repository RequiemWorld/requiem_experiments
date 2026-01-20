from dataclasses import dataclass
from cleancord.api import DiscordAPIInterface
from cleancord.api import DiscordGatewayInterface
from cleancord.events import GatewayEventPayload


@dataclass
class ClientIdentity:
    userid: int
    username: str


class BasicDiscordClient:
    def __init__(self,
                 api: DiscordAPIInterface,
                 gateway: DiscordGatewayInterface):
        self._discord_api = api
        self.gateway = gateway
        self._client_identity = None

    @property
    def client_identity(self) -> ClientIdentity | None:
        return self._client_identity

    async def start(self):
        user = self._discord_api.get_own_user()
        self._client_identity = ClientIdentity(user.id, user.username)
        await self.gateway.connect()
        identify_payload = GatewayEventPayload(2, {})
        await self.gateway.send_payload(identify_payload)
        response = await self.gateway.recv_payload()
        if response.opcode == 9:
            from .errors import SessionError
            raise SessionError()
