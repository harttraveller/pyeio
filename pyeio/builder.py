class IO:
    def __init__(self):
        self.__init_interfaces()
        self.__init_methods()

    def __init_interfaces(self) -> None:
        pass

    def __init_methods(self) -> None:
        self._id = {
            "json": {"save": self.json.save, "load": self.json.load},
            "jsonl": {"save": self.jsonl.save, "load": self.jsonl.load},
        }

    @property
    def formats(self) -> set[str]:
        return set(self._id.keys())
