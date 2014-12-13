#!/usr/bin/env python3

from argparse import ArgumentParser
import os
from random import randint

participants_path = "participants"
output_dir_path = "tickets"

message = "You are Secret Santa for:"

def raffle(participants):
    output = {}
    recipients = list(participants)
    for participant in participants:
        index = randint(0, len(recipients)-1)
        recipient = recipients[index]
        output[participant] = recipient
        recipients.remove(recipient)
    return output

def check_collisions(ticket_dict):
    for g,r in ticket_dict.items():
        if g == r:
            return False
    return True

def checked_raffle(participants):
    while True :
        output = raffle(participants)
        if check_collisions(output):
            return output

participants = []

parser = ArgumentParser()
parser.add_argument('-m', '--message')
parser.add_argument('-f', '--participants-file')
parser.add_argument('-o', '--output-dir')
args = parser.parse_args()

if args.message:
    message = args.message

if args.participants_file:
    participants_path = args.participants_file

if args.output_dir:
    output_dir_path = args.output_dir

if not os.path.isfile(participants_path):
    print("no participants file found -- aborting.")
    sys.exit(1)

if not os.path.exists(output_dir_path):
    os.mkdir(output_dir_path)

if not os.path.isdir(output_dir_path):
    print("{} is not a directory -- aborting.".format(output_dir_path))

with open(participants_path) as participants_file:
    for participant in participants_file.read().split('\n'):
        if participant.strip(' ') != '':
            participants.append(participant.strip(' '))



tickets = checked_raffle(participants)

for santa, recipient in tickets.items():
    ticket_path = output_dir_path + '/' + santa + '.txt'
    with open(ticket_path, 'w') as ticket:
        ticket.write(message)
        ticket.write(recipient)



