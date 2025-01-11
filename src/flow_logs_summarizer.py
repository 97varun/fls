import socket
from collections import defaultdict

from file_handler import readFlowLogs, readLookupTable
from flow_log_constants import UNTAGGED, LookupTableFields, StatsFields
from flow_log_record import FlowLogRecord


class FlowLogsSummarizer:
    def __init__(self, tagLookupFile: str):
        self.loadTagLookupTable(tagLookupFile)
        self.matchesByProtocolByPort = defaultdict(lambda: defaultdict(int))

    def loadTagLookupTable(self, tagLookupFile: str):
        self.tagByProtocolByPort = defaultdict(lambda: defaultdict(str))
        self.protocolNameByNumber = defaultdict(str)
        for row in readLookupTable(tagLookupFile):
            protocolNumber = socket.getprotobyname(row[LookupTableFields.PROTOCOL])
            port = int(row[LookupTableFields.DSTPORT])
            self.protocolNameByNumber[protocolNumber] = row[LookupTableFields.PROTOCOL]
            self.tagByProtocolByPort[protocolNumber][port] = row[LookupTableFields.TAG]

    def getFlowLogRecord(self, flowLogLine: str):
        fields = flowLogLine.split()
        fields = map(str.strip, fields)
        return FlowLogRecord(*fields)

    def processFlowLogRecord(self, flowLogLine: str):
        flowLogRecord = self.getFlowLogRecord(flowLogLine)
        self.matchesByProtocolByPort[flowLogRecord.protocol][flowLogRecord.dstPort] += 1

    def processFlowLogFile(self, flowLogFilePath: str):
        for flowLogLine in readFlowLogs(flowLogFilePath):
            self.processFlowLogRecord(flowLogLine)

    def getMatchesByProtocolByPort(self):
        matchesByProtocolByPort = []
        for protocol, portMatches in self.matchesByProtocolByPort.items():
            for port, matches in portMatches.items():
                matchesByProtocolByPort.append({
                    StatsFields.PORT: port,
                    StatsFields.PROTOCOL: self.protocolNameByNumber[protocol],
                    StatsFields.COUNT: matches
                })
        
        return matchesByProtocolByPort
    
    def getMatchesByTag(self):
        matchesByTag = defaultdict(int)
        for protocol, portMatches in self.matchesByProtocolByPort.items():
            for port, matches in portMatches.items():
                tag = self.tagByProtocolByPort.get(protocol, {}).get(port, UNTAGGED)
                matchesByTag[tag] += matches

        return [
            {
                StatsFields.TAG: tag,
                StatsFields.COUNT: count
            }
            for tag, count in matchesByTag.items()
        ]