#!/usr/bin/env python3

# Adapted from:
# http://wboptimum.com/splitting-gmail-mbox-by-label/

import getopt
import mailbox
import os
import sys
from email.header import decode_header
from email.errors import HeaderParseError


def decode_rfc2822(header_value):
    """Returns the value of the rfc2822 decoded header, or the header_value as-is if it's not encoded."""
    result = []
    for binary_value, charset in decode_header(header_value):
        decoded_value = None
        if isinstance(binary_value, str):
            result.append(binary_value)
            continue

        if charset is not None:
            try:
                decoded_value = binary_value.decode(charset, errors='ignore')
            except Exception as e:
                pass

        if decoded_value is None:
            try:
                decoded_value = binary_value.decode('utf8', errors='ignore')
            except Exception as e:
                decoded_value = 'HEX({})'.format(binary_value.hex())

        result.append(decoded_value)

    return ''.join(result)


def main(argv):
    in_mbox = "inbox.mbox"
    prefix = "split_"
    try:
        opts, args = getopt.getopt(argv, "i:p:", ["infile=", "prefix="])
    except getopt.GetoptError:
        print("Usage:", sys.argv[0], "-i <input_file.mbox> -p <prefix>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--infile"):
            in_mbox = arg
        elif opt in ("-p", "--prefix"):
            prefix = arg
    print("Processing file - " + in_mbox + " with prefix = " + prefix)
    boxes = {
        "inbox": mailbox.mbox(prefix+"Inbox.mbox", None, True),
        "sent": mailbox.mbox(prefix+"Sent.mbox", None, True),
        "archive": mailbox.mbox(prefix+"Archive.mbox", None, True),
    }

    for message in mailbox.mbox(in_mbox):
        target = "archive"
        gmail_labels = message["X-Gmail-Labels"] or ""      # Could possibly be None.
        if gmail_labels != "":
            gmail_labels = decode_rfc2822(gmail_labels).lower()
        if "inbox" in gmail_labels:
            target = "inbox"
        elif "sent" in gmail_labels:
            target = "sent"
        else:
            for label in gmail_labels.split(','):
                if label != "important" and label != "unread" and label != "starred" and label != "newsletters":
                    target = prefix + label.title().replace(os.pathsep, '.') + ".mbox"
                    if target not in boxes:
                        boxes[target] = mailbox.mbox(target, None, True)
                    break
        try:
            boxes[target].add(message)
        except HeaderParseError as e:
            pass  # there's nothing we can do, so just skip this message


if __name__ == "__main__":
    main(sys.argv[1:])
