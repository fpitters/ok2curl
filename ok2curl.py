import sys
import argparse
import re
import fileinput
from dataclasses import dataclass, field
from typing import List, ClassVar


@dataclass
class Header:
    """Header model"""
    key: str
    value: str


@dataclass
class Request:
    """Request model"""
    method: str
    url: str
    is_data: bool
    data: str = None
    headers: list = field(default_factory=list)

    EXCLUDED_HEADERS: ClassVar[list] = ['Accept-Encoding', 'Cookie'] #['Cookie', 'Accept-Encoding']

    def curl(self):
        h = ' '.join([f'-H "{header.key}: {header.value}"' for header in self.headers if header.key not in Request.EXCLUDED_HEADERS])
        if not self.is_data:
            return f'curl -X {self.method} {h} "{self.url}"'
        else:
            return f'curl -X {self.method} --data \'{self.data}\' {h} "{self.url}"'


def parseFile(file):
    request = None
    pattern_json = '^[{\[].*[}\]]$'
    for line in fileinput.input(file):
        logs = re.split('okhttp\\.OkHttpClient.*I\\s\\s', line) # line.split('OkHttpClient : ')
        if len(logs) > 1:
            log = logs[1].strip()
            if log.startswith('-->'):
                url_params = log.split()
                command = url_params[1]
                if command == 'END':
                    if request == None:
                        print('Invalid end of request reached without any request')
                    else:
                        print('>>> Curl command:')
                        print(request.curl())
                        request = None
                else:
                    is_data = command == 'POST' or command == 'PUT'
                    request = Request(command, url_params[2], is_data) 
            else:
                if not request:
                    # print('Invalid header or data without any request')
                    pass
                else:
                    # it's either a header or json body
                    if request.is_data and re.search(pattern_json, log):
                        request.data = log
                    else:
                        header_str = log.split(':')
                        header = Header(header_str[0].strip(), header_str[1].strip())
                        request.headers.append(header)
    if request:
        print('>>> Incomplete request:')
        print(request.curl())
        request = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse OkHttp logs')
    parser.add_argument('-f', '--file', action='store',
            help='file with the OkHttp logs to be parsed')
    args = parser.parse_args()
    
    if(args.file):
        parseFile(args.file)
    else:
        parseFile(None)

