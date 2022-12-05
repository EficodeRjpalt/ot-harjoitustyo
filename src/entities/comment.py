class Comment():

    def __init__(self, timestamp: str, actor: str, body: str):
        """Constructor for Comment object.

        Args:
            timestamp (str): Timestamp of when the comment was made.
            actor (str): The name of the person who made the comment.
            body (str): The actual body of the comment or description of the
            action that was performed.
        """
        self._timestamp = timestamp
        self._actor = actor
        self._body = body

    def __str__(self) -> str:
        """String method to turn the Comment object into string.

        Returns:
            str: Returns the Comment as a string formatted as 'timestamp;
            actor; body'.
        """

        return '; '.join(
            [
                self._timestamp,
                self._actor,
                self._body
            ]
        )

    def __repr__(self) -> str:
        """Repr method for allowing understansable printing of the issue.

        Returns:
            str: Returns a string format representation of the object in the
            following format: 'timestamp; actor; body'.
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
        """Getter method for timestamp attribute.

        Returns:
            str: returns timestamp attribute.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_value) -> None:
        """Setter method for timestamp attribute.

        Args:
            new_value (_type_): new value for the timestamp attribute.
        """
        self._timestamp = new_value

    @property
    def actor(self) -> str:
        """Getter method for actor attribute.

        Returns:
            str: returns actor attribute of the Comment.
        """
        return self._actor

    @actor.setter
    def actor(self, new_value) -> None:
        """Setter method for actor attribute.

        Args:
            new_value (_type_): Sets a new value for the actor attribute
            of the Comment object.
        """
        self._actor = new_value

    @property
    def body(self) -> str:
        """Getter method for body attribute.

        Returns:
            str: Returns the body attribute of a Comment object.
        """
        return self._body

    @body.setter
    def body(self, new_value) -> None:
        """Setter method for body attribute.

        Args:
            new_value (_type_): Sets a new value for the Comment objects'
            body attribute.
        """
        self._body = new_value
