class IO:
    def __init__(self):
        self.__init_utility_subclasses()
        self.__init_interface_subclasses()
        self.__init_interface_dict()

    def __init_utility_subclasses(self) -> None:
        self.query = Query()
        self.transform = Transform()

    def __init_interface_subclasses(self) -> None:
        self.json = JSON()
        self.jsonl = JSONL()
        self.csv = CSV()
        self.xlsx = XLSX()
        self.yaml = YAML()
        self.toml = TOML()

    def __init_interface_dict(self) -> None:
        self._id = {
            "json": {"save": self.json.save, "load": self.json.load},
            "jsonl": {"save": self.jsonl.save, "load": self.jsonl.load},
        }

    @property
    def formats(self) -> set[str]:
        return set(self._id.keys())
