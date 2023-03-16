class IO:
    def __init__(self):
        self.__init_interface_dict()

    def __init_interface_dict(self) -> None:
        self._id = {
            "json": {"save": self.json.save, "load": self.json.load},
            "jsonl": {"save": self.jsonl.save, "load": self.jsonl.load},
        }

    @property
    def formats(self) -> set[str]:
        return set(self._id.keys())
