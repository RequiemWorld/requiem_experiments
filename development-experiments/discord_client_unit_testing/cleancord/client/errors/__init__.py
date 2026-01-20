

class SessionError(Exception):
    pass

class GatewayConnectionClosed(Exception):
    pass


class GatewayConnectionClosedForInvalidSession(GatewayConnectionClosed):
    pass

class GatewayConnectionClosedForInvalidIntents(GatewayConnectionClosed):
    pass
