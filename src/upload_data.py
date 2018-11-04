import argparse
import boto3
import csv
import re

from datetime import datetime
from decimal import Decimal, InvalidOperation
from pytz import timezone


eastern = timezone('US/Eastern')


def main():
    args = parse_args()
    dynamodb = boto3.resource('dynamodb')

    upload_jump_data(args, dynamodb)
    upload_impacts_data(args, dynamodb)
    upload_summary_data(args, dynamodb)


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


def upload_summary_data(args, dynamodb):
    content = ''
    with open(args.summarycsv) as f:
        is_table = False
        date = ''
        for line in f:
            if "Event Start" in line:
                date = line.split(",")[-1].split(" ")[0]
            if is_table and len(line.strip()) == 0:
                break

            if line.split(',')[0].strip() == "Player Name":
                is_table = True
                content += line.strip() + ",date\n"
            elif is_table:
                content += line.strip() + "," + date + "\n"

    clean_filename = ".".join(args.summarycsv.split(".")[:-1]) + "_clean.csv"
    with open(clean_filename, 'w+') as f:
        f.write(content)

    # write jump records to DynamoDB
    table = dynamodb.Table(args.summarytable)
    count = 0
    with open(clean_filename) as f:
        reader = csv.DictReader(f)

        for line in reader:
            item = dict(line)
            if not item:
                continue

            for key in item:
                val = item[key]
                try:
                    # change str to decimal if possible
                    val = Decimal(val)
                except InvalidOperation:
                    # otherwise, strip trailing and leading whitespace in str
                    val = val.strip()
                item[key] = val

            item['match'] = args.summarycsv.startswith('match')
            table.put_item(Item=item)
            count += 1

    print(f"put {count} items into {args.summarytable}")


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
    parser.add_argument('--summarycsv',
                        required=True,
                        help='path to summary csv file')
    parser.add_argument('--summarytable',
                        default='gtvolleyball-data-summary',
                        help='DynamoDB table name for summary data')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
