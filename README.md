# crispy-meme - Python SCRIPTS

useful scriprts

## Copy mails/`backup-imap-mails.py`

1. Create `.env` file
2. ```pip install python-dotenv```
3. Fill
    ```ini
    MAIL_FROM_SERVER=
    MAIL_FROM_PORT=
    MAIL_FROM_USER=
    MAIL_FROM_PASSWORD=
    MAIL_FROM_BOX_NAMES=

    MAIL_TO_SERVER=
    MAIL_TO_PORT=
    MAIL_TO_USER=
    MAIL_TO_PASSWORD=
    MAIL_TO_BOX_NAME=
    ```
    e.g. for iCloud
    ```ini
    MAIL_FROM_SERVER=imap.mail.me.com
    MAIL_FROM_PORT=993
    MAIL_FROM_USER=xyz@abc.com
    MAIL_FROM_PASSWORD=super-strong-password-for-app
    MAIL_FROM_BOX_NAMES=Sent,Inbox
    ```
    or
    ```ini
    MAIL_TO_SERVER=imap.mail.me.com
    MAIL_TO_PORT=993
    MAIL_TO_USER=xyz@abc.com
    MAIL_TO_PASSWORD=super-strong-password-for-app
    MAIL_TO_BOX_NAME=Backup-folder
    ```
4. Run ```./backup-imap-mails.py```
