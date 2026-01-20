import asyncio
import unittest
import scurrypy
from discord_harness.database import User
from cleancord.api import DiscordAPIInterface, DiscordGatewayInterface
from discord_harness.database import SystemState, UserOperationsService
from cleancord.client import BasicDiscordClient
from cleancord.events import GatewayEventPayload


class FakeDiscordAPIInterface(DiscordAPIInterface):
    def __init__(self, system_state: SystemState):
        self._system_state = system_state
        self._owner_userid = None
        self._own_user_information_requested = False

    def assertOwnUserInformationRequested(self):
        assert self._own_user_information_requested

    def set_own_userid(self, user_id: int):
        self._owner_userid = user_id

    def get_own_user(self) -> scurrypy.UserModel:
        assert self._owner_userid is not None
        matching_user: User = self._system_state.users.find_by_id(self._owner_userid)
        self._own_user_information_requested = True
        return scurrypy.UserModel(
            id=matching_user.id,
            username=matching_user.username,
            discriminator="0000",
            avatar="",
            bot=True,
            mfa_enabled=None,
            global_name=matching_user.username,
            system=None,
            banner=None,
            accent_color=None,
            locale=None)

    def get_other_user(self, userid: int) -> scurrypy.UserModel:
        raise NotImplementedError


class InteractivePayloadQueue:
    def __init__(self):
        self._pending_payloads: list[tuple[GatewayEventPayload, int]] = []

    def set_next_payload_for_opcode(self, payload: GatewayEventPayload, opcode: int) -> None:
        ## FIXME make copies of the payloads or something
        self._pending_payloads.append((payload, opcode))

    def get_next_payload_for_opcode(self, opcode: int) -> GatewayEventPayload | None:
        for payload, target_opcode in self._pending_payloads:
            if target_opcode == opcode:
                return payload
        return None


class FakeDiscordGatewayInterface(DiscordGatewayInterface):
    def __init__(self):
        self._sent_payloads: list[GatewayEventPayload] = []
        self._payload_queue = InteractivePayloadQueue()
        self._last_sent_opcode = None

    @property
    def set_next_payload_for_opcode(self):
        return self._payload_queue.set_next_payload_for_opcode

    @property
    def get_next_payload_for_opcode(self):
        return self._payload_queue.get_next_payload_for_opcode

    @property
    def sent_payloads(self):
        return self._sent_payloads

    def assertPayloadWithOpcodeSent(self, opcode: int):
        found_matching_payload = False
        for payload in self._sent_payloads:
            if payload.opcode == opcode:
                found_matching_payload = True
        assert found_matching_payload

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def send_payload(self, payload: GatewayEventPayload) -> None:
        self._last_sent_opcode = payload.opcode
        self._sent_payloads.append(payload)

    async def recv_payload(self) -> GatewayEventPayload:
        if self._last_sent_opcode is not None:
            return self._payload_queue.get_next_payload_for_opcode(opcode=self._last_sent_opcode)
        else:
            raise EOFError



class ClientTestCase(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self._state = SystemState()
        self._fake_api = FakeDiscordAPIInterface(system_state=self._state)
        self._user_service: UserOperationsService = UserOperationsService(self._state)
        self._mock_gateway = FakeDiscordGatewayInterface()
        self._client = BasicDiscordClient(self._fake_api, self._mock_gateway)

    async def start_client_in_background(self):
        asyncio.create_task(self._client.start())
        await asyncio.sleep(0)

    def make_user_and_set_own_id_for_api(self, username: str) -> None:
        self._user_service.new_user(username)
        user_id = self._state.users.find_id_for_username(username)
        self._fake_api.set_own_userid(user_id)