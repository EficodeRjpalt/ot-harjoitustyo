class Comment():

    def __init__(self, timestamp: str, actor: str, body: str):
        """_summary_

        Args:
            timestamp (str): _description_
            actor (str): _description_
            body (str): _description_
        """
        self._timestamp = timestamp
        self._actor = actor
        self._body = body

    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """

        return '; '.join(
            [
                self._timestamp,
                self._actor,
                self._body
            ]
        )

    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """

        return '; '.join(
            [
                self._timestamp,
                self._actor,
                self._body
            ]
        )

    @property
    def timestamp(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_value) -> None:
        """_summary_

        Args:
            new_value (_type_): _description_
        """
        self._timestamp = new_value

    @property
    def actor(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self._actor

    @actor.setter
    def actor(self, new_value) -> None:
        self._actor = new_value

    @property
    def body(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self._body

    @body.setter
    def body(self, new_value) -> None:
        """_summary_

        Args:
            new_value (_type_): _description_
        """
        self._body = new_value
