from dataclasses import dataclass

@dataclass
class FlowLogRecord:
    version: int
    accountId: str
    interfaceId: str
    srcAddr: str
    dstAddr: str
    srcPort: int
    dstPort: int
    protocol: int
    packets: int
    bytes: int
    start: int
    end: int
    action: str
    logStatus: str

    def __post_init__(self):
        self.version = int(self.version)
        self.srcPort = int(self.srcPort)
        self.dstPort = int(self.dstPort)
        self.protocol = int(self.protocol)
        self.packets = int(self.packets)
        self.bytes = int(self.bytes)
        self.start = int(self.start)
        self.end = int(self.end)