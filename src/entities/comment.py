class Comment():

    def __init__(self, timestamp: str, actor: str, body: str):
        self._timestamp = timestamp
        self._actor = actor
        self._body = body

    def __str__(self) -> str:

        return '; '.join(
            [
                self.timestamp,
                self.actor,
                self.body
            ]
        )

    def __repr__(self) -> str:

        return '; '.join(
            [
                self.timestamp,
                self.actor,
                self.body
            ]
        )

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @property
    def actor(self) -> str:
        return self._actor

    @property
    def body(self) -> str:
        return self._body
