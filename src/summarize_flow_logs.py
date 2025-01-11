import argparse
import os

from file_handler import writeStats
from flow_logs_summarizer import FlowLogsSummarizer
from flow_log_constants import INPUT_DIR, OUTPUT_DIR


def handleOutput(flowLogSummarizer: FlowLogsSummarizer, args):
    protocolPortMatchesSummaryFile = os.path.join(OUTPUT_DIR, args.protocol_port_matches_summary_file)
    tagMatchesSummaryFile = os.path.join(OUTPUT_DIR, args.tag_matches_summary_file)

    matchesByProtocolByPort = flowLogSummarizer.getMatchesByProtocolByPort()
    writeStats(matchesByProtocolByPort, protocolPortMatchesSummaryFile)

    matchesByTag = flowLogSummarizer.getMatchesByTag()
    writeStats(matchesByTag, tagMatchesSummaryFile)

def main():
    argsParser = argparse.ArgumentParser(description='Parse VPC Flow Logs.')
    argsParser.add_argument('--flow-log-file', type=str, required=True, help='Path to the input flow log file.')
    argsParser.add_argument('--tag-lookup-file', type=str, required=True, help='Path to the tag lookup table file.')
    argsParser.add_argument('--tag-matches-summary-file', type=str, default='tag-matches.csv', help='Path to the output file (default: tag-matches.csv).')
    argsParser.add_argument('--protocol-port-matches-summary-file', type=str, default='protocol-port-matches.csv', help='Path to the output file (default: protocol-port-matches.csv).')

    args = argsParser.parse_args()

    tagLookupFile = os.path.join(INPUT_DIR, args.tag_lookup_file)
    flowLogFile = os.path.join(INPUT_DIR, args.flow_log_file)

    flowLogSummarizer = FlowLogsSummarizer(tagLookupFile)
    flowLogSummarizer.processFlowLogFile(flowLogFile)

    handleOutput(flowLogSummarizer, args)

if __name__ == '__main__':
    main()