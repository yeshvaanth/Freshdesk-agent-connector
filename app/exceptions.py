class TicketNotFoundError(Exception):
    pass


class FreshdeskAuthenticationError(Exception):
    pass


class FreshdeskRateLimitError(Exception):
    pass


class FreshdeskAPIError(Exception):
    pass