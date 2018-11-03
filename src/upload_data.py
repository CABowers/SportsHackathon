import argparse
import boto3
import csv
import re

from datetime import datetime
from decimal import Decimal, InvalidOperation
from pytz import timezone


eastern = timezone('US/Eastern')


def upload_data(args):
    dynamodb = boto3.resource('dynamodb')

    upload_jump_data(args, dynamodb)
    upload_impacts_data(args, dynamodb)


def upload_jump_data(args, dynamodb):
    # write jump records to DynamoDB
    table = dynamodb.Table(args.jumptable)

    count = 0
    with open(args.jumpcsv, newline='') as csv_file:
        reader = csv.reader(csv_file)

        headers = ['datetime', 'date', 'time', 'session_type', 'player_name', 'height']
        bad_headers = [headers[1], headers[2], headers[3]]
        next(reader)  # throw away the header line

        for row in reader:
            item = {}
            try:
                dt = datetime.strptime(f"{row[0].strip()[:-3] + row[0][-2:]}", '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:  # not valid date
                continue

            item['datetime'] = str(dt.astimezone(eastern))
            for i, val in enumerate(row[1:], start=1):
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
                item['match'] = args.jumpcsv.startswith('match')
                table.put_item(Item=item)
                count += 1
    print(f"put {count} items into {args.jumptable}")


def upload_impacts_data(args, dynamodb):
    # write impact records to DynamoDB
    table = dynamodb.Table(args.impactstable)

    count = 0
    with open(args.impactscsv, newline='') as csv_file:
        reader = csv.reader(csv_file)

        headers = ['datetime', 'time', 'session_type', 'gforce', 'player_name']
        bad_headers = [headers[1], headers[2]]
        next(reader)  # throw away the header line

        for row in reader:
            item = {}
            try:
                dt = datetime.strptime(f"{row[0].strip()} {row[1]}", '%m/%d/%Y %H:%M:%S.%f (%z)')
            except ValueError:  # not valid date
                continue

            item['datetime'] = str(dt.astimezone(eastern))
            for i, val in enumerate(row[1:], start=1):
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
                item['match'] = args.impactscsv.startswith('match')
                table.put_item(Item=item)
                count += 1

    print(f"put {count} items into {args.impactstable}")


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
