#!/usr/bin/env python

# Adapted from:
# http://wboptimum.com/splitting-gmail-mbox-by-label/

import sys
import getopt
import mailbox

def main(argv):
	in_mbox = "inbox.mbox"
	prefix = "split_"
	try:
		opts, args = getopt.getopt(argv, "i:p:", ["infile=", "prefix="])
	except getopt.GetoptError:
		print("python splitgmail.py -i  -p ")
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--infile"):
			in_mbox = arg
		elif opt in ("-p", "--prefix"):
			prefix = arg
	print("Processing file - " + in_mbox + " with prefix = " + prefix)
	boxes = {"inbox": mailbox.mbox(prefix+"Inbox.mbox", None, True), "sent": mailbox.mbox(prefix+"Sent.mbox", None, True),"archive":mailbox.mbox(prefix+"Archive.mbox", None, True)}

	for message in mailbox.mbox(in_mbox):
		gmail_labels = message["X-Gmail-Labels"]       # Could possibly be None.
		if not gmail_labels:
			boxes["archive"].add(message)
			continue
		gmail_labels = gmail_labels.lower()
		if "spam" in gmail_labels:
			continue
		elif "inbox" in gmail_labels:
			boxes["inbox"].add(message)
		elif "sent" in gmail_labels:
			boxes["sent"].add(message)
		else:
			saved = False
			for label in gmail_labels.split(','):
				if label != "important" and label != "unread" and label != "starred" and label != "newsletters":
					box_name = prefix+label.title()+".mbox"
					if box_name not in boxes:
						boxes[box_name] = mailbox.mbox(box_name, None, True)
					boxes[box_name].add(message)
					saved = True
					break
			if not saved:
				boxes["archive"].add(message)

if __name__ == "__main__":
    main(sys.argv[1:])