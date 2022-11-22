class Comment():

    def __init__(self, timestamp: str, actor: str, body: str):
        self.timestamp = timestamp
        self.actor = actor
        self.body = body

    def __str__(self) -> str:
        
        return '; '.join(
            [
                self.timestamp,
                self.actor,
                self.body
            ]
        )