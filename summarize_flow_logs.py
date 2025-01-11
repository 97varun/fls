import argparse

from file_handler import writeStats
from flow_logs_summarizer import FlowLogsSummarizer

def handleOutput(flowLogSummarizer: FlowLogsSummarizer, args):
    matchesByProtocolByPort = flowLogSummarizer.getMatchesByProtocolByPort()
    writeStats(matchesByProtocolByPort, args.protocol_port_matches_summary_file)

    matchesByTag = flowLogSummarizer.getMatchesByTag()
    writeStats(matchesByTag, args.tag_matches_summary_file)

def main():
    argsParser = argparse.ArgumentParser(description='Parse VPC Flow Logs.')
    argsParser.add_argument('--flow-log-file', type=str, required=True, help='Path to the input flow log file.')
    argsParser.add_argument('--tag-lookup-file', type=str, required=True, help='Path to the tag lookup table file.')
    argsParser.add_argument('--tag-matches-summary-file', type=str, default='tag-matches.csv', help='Path to the output file (default: tag-matches.csv).')
    argsParser.add_argument('--protocol-port-matches-summary-file', type=str, default='protocol-port-matches.csv', help='Path to the output file (default: protocol-port-matches.csv).')

    args = argsParser.parse_args()

    flowLogSummarizer = FlowLogsSummarizer(args.tag_lookup_file)
    flowLogSummarizer.processFlowLogFile(args.flow_log_file)

    handleOutput(flowLogSummarizer, args)

if __name__ == '__main__':
    main()