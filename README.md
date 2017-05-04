# GMail MBOX to Maildir

How to use these two Python/Perl scripts to migrate a GMail inbox to a cpanel / dovecot / maildir inbox — when you have a lot of emails and other, simpler, imports fail.

You'll need FTP and SSH access to the server; or, if you can't connect over SSH, make sure there's a file manager that permits unzipping in your host's admin interface.

### 1. Download MBOX from Google Takeout

### 2. Split MBOX by labels

```shell
./mbox_split.py --infile google_mbox.mbox --prefix split_
```

You may need to `chmod 755 mbox_split.py` to be able to run.

Alternatively, you can just export by label from Google Takeout directly.

### 3. MBOX to Maildir

```shell
./mb2md.pl -s ~/path/to/split_Inbox.mbox -d ~/path/to/output/Inbox
```

__Notes:__

1. may need `chmod 755 mbox_split.py` to be able to run
2. source and destination need absolute paths

### 4. Zip the `new/` folder for each output mailbox

### 5. Upload Zip to server in appropriate maildir mailbox folder, and expand via SSH:

```shell
unzip -j Inbox.zip
rm Inbox.zip
```

(The `-j` flag will make sure the zipped `new` folder will extract in-place, with no additional folder structure)

### 6. (Optional) Access inbox via webmail and mark everything as read

