import abc
import discord
import scurrypy


class DiscordAPIInterface(abc.ABC):
    """
    A clean interface to the discord api driven by intent.
    """
    @abc.abstractmethod
    def get_own_user(self) -> scurrypy.UserModel:
        """
        Reaches out to the discord API to get the @me user.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_other_user(self, userid: int) -> scurrypy.UserModel:
        raise NotImplementedError()
