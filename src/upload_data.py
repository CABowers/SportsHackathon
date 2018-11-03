import argparse
import boto3
import csv
import re

from datetime import datetime
from decimal import Decimal, InvalidOperation


def upload_data(args):
    dynamodb = boto3.resource('dynamodb')

    #upload_jump_data(args, dynamodb)
    #upload_impacts_data(args, dynamodb)


def upload_jump_data(args, dynamodb):
    # write jump records to DynamoDB
    table = dynamodb.Table(args.jumptable)

    with open(args.jumpcsv, newline='') as csv_file:
        reader = csv.reader(csv_file)

        headers = ['datetime', 'date', 'time', 'session_type', 'player_name', 'height']
        bad_headers = [headers[1], headers[2]]
        next(reader)  # throw away the header line

        for row in reader:
            item = {}
            for i, val in enumerate(row):
                if not val:
                    continue

                try:
                    # change str to decimal if possible
                    val = Decimal(val)
                except InvalidOperation:
                    # otherwise, strip trailing and leading whitespace in str
                    val = val.strip()

                item[headers[i]] = val

            if item:
                for bad_key in bad_headers:
                    del item[bad_key]
                table.put_item(Item=item)


def upload_impacts_data(args, dynamodb):
    # write impact records to DynamoDB
    table = dynamodb.Table(args.impactstable)

    with open(args.impactscsv, newline='') as csv_file:
        reader = csv.reader(csv_file)

        headers = ['datetime', 'time', 'session_type', 'player_name', 'height']
        bad_headers = [headers[1]]
        next(reader)  # throw away the header line

        for row in reader:
            item = {}
            try:
                dt = datetime.strptime(f"{row[0].strip()} {row[1]}", '%m/%d/%Y %H:%M:%S.%f (%z)')
            except ValueError:  # not valid date
                continue

            stamp = dt.strftime('%Y-%m-%dT%H:%M:%S.%f %z')
            print(stamp)
            #   2018-10-27T14:24:24.212-04:00

            # for i, val in enumerate(row[2:]):
            #     if not val:
            #         continue

            #     try:
            #         # change str to decimal if possible
            #         val = Decimal(val)
            #     except InvalidOperation:
            #         # otherwise, strip trailing and leading whitespace in str
            #         val = val.strip()

            #     item[headers[i]] = val

            # if item:
            #     for bad_key in bad_headers:
            #         del item[bad_key]
            #     table.put_item(Item=item)

def parse_args():
    parser = argparse.ArgumentParser(description='Upload GT Volleyball Data')
    parser.add_argument('--jumpcsv',
                        required=True,
                        help='path to jump csv file')
    parser.add_argument('--jumptable',
                        default='gtvolleyball-data-jump',
                        help='DynamoDB table name for jump data')
    parser.add_argument('--impactscsv',
                        required=True,
                        help='path to impacts csv file')
    parser.add_argument('--impactstable',
                        default='gtvolleyball-data-impacts',
                        help='DynamoDB table name for impacts data')
    # parser.add_argument('--summarycsv',
    #                     required=True,
    #                     help='path to summary csv file')
    # parser.add_argument('--summarytable',
    #                     default='gtvolleyball-data-summary',
    #                     help='DynamoDB table name for summary data')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

    upload_data(args)
