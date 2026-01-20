import unittest
from . import ClientTestCase
from cleancord.client import BasicDiscordClient
from discord_harness.database import UserOperationsService


class TestClientStartupIdentification(ClientTestCase):

    async def test_should_request_own_user_information_on_startup(self):
        self.make_user_and_set_own_id_for_api("Username")
        await self.start_client_in_background()
        self._fake_api.assertOwnUserInformationRequested()

    async def test_should_have_client_identity_with_right_username_after_startup(self):
        self.make_user_and_set_own_id_for_api("Someone123")
        await self.start_client_in_background()
        self.assertEqual("Someone123", self._client.client_identity.username)
