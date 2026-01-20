from cleancord.client.errors import SessionError
from . import ClientTestCase
from cleancord.events import GatewayEventPayload

_IDENTIFY_OPCODE = 2


class TestClientIdentificationOnStart(ClientTestCase):
    async def test_should_send_payload_with_identify_opcode_on_startup(self):
        self.make_user_and_set_own_id_for_api("Username123")
        await self.start_client_in_background()
        self._mock_gateway.assertPayloadWithOpcodeSent(_IDENTIFY_OPCODE)


class TestClientIdentificationErrorOnStart(ClientTestCase):

    async def test_should_raise_invalid_session_when_opcode_9_encountered(self):
        response_payload = GatewayEventPayload(opcode=9, event_data={})
        self._mock_gateway.set_next_payload_for_opcode(response_payload, _IDENTIFY_OPCODE)
        self.make_user_and_set_own_id_for_api("SomeName123")
        with self.assertRaises(SessionError):
            await self._client.start()

