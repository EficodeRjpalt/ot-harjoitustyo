class Comment():

    def __init__(self, timestamp: str, actor: str, body: str):
        self._timestamp = timestamp
        self._actor = actor
        self._body = body

    def __str__(self) -> str:

        return '; '.join(
            [
                self._timestamp,
                self._actor,
                self._body
            ]
        )

    def __repr__(self) -> str:

        return '; '.join(
            [
                self._timestamp,
                self._actor,
                self._body
            ]
        )

    @property
    def timestamp(self) -> str:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_value) -> None:
        self._timestamp = new_value

    @property
    def actor(self) -> str:
        return self._actor

    @actor.setter
    def actor(self, new_value) -> None:
        self._actor = new_value

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, new_value) -> None:
        self._body = new_value
