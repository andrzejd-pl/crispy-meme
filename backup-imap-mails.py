#!/usr/bin/env python3

# source: https://stackoverflow.com/a/28748807
# my changes:
# - .env config
# - SSL login
# - adapt to python 3
# - temporary turn off deleting old messages
# - copy all folders

import imaplib
from dotenv import dotenv_values

def connect_server(server):
    print('Connecting to ' + server['server'] + ':' + str(server['port']))
    conn = imaplib.IMAP4_SSL(server['server'], server['port'])
    conn.login(server['username'], server['password'])
    print('Logged into mail server @ %s' % server['server'])
    return conn

def disconnect_server(server_conn):
    out = server_conn.logout()

if __name__ == '__main__':
    config = dotenv_values('.env')
    from_server = {'server': config['MAIL_FROM_SERVER'],
                   'port': config['MAIL_FROM_PORT'],
                   'username': config['MAIL_FROM_USER'],
                   'password': config['MAIL_FROM_PASSWORD'],
                   'box_names': config['MAIL_FROM_BOX_NAMES'].split(',')}
    to_server = {'server': config['MAIL_TO_SERVER'],
                 'port': config['MAIL_TO_PORT'],
                 'username': config['MAIL_TO_USER'],
                 'password': config['MAIL_TO_PASSWORD'],
                 'box_name': config['MAIL_TO_BOX_NAME'],
                 'folder_prefix': config['MAIL_TO_BOX_PREFIX']}

    From = connect_server(from_server)
    To = connect_server(to_server)

    for folder in From.list()[1]:
        folder_name = folder.decode().split(' "/" ')[1]
        box_select = From.select(folder_name, readonly = False)  #open box which will have its contents copied
        To.create(to_server['folder_prefix'] + folder_name)
        print('Fetching messages from \'%s\'...' % folder_name)
        resp, items = From.search(None, 'ALL')  #get all messages in the box
        msg_nums = items[0].split()
        print('%s messages to archive' % len(msg_nums))

        for msg_num in msg_nums:
            resp, data = From.fetch(msg_num, "(FLAGS INTERNALDATE BODY.PEEK[])") # get email
            message = data[0][1]
            flags = imaplib.ParseFlags(data[0][0]) # get flags
            flag_str = b" ".join(flags)
            date = imaplib.Time2Internaldate(imaplib.Internaldate2tuple(data[0][0])) #get date
            copy_result = To.append(to_server['folder_prefix'] + folder_name, flag_str.decode('utf-8'), date, message) # copy to archive

    # for box in from_server['box_names']:
    #     box_select = From.select(box, readonly = False)  #open box which will have its contents copied
    #     print('Fetching messages from \'%s\'...' % box)
    #     resp, items = From.search(None, 'ALL')  #get all messages in the box
    #     msg_nums = items[0].split()
    #     print('%s messages to archive' % len(msg_nums))
    #     
    #     for msg_num in msg_nums:
    #         resp, data = From.fetch(msg_num, "(FLAGS INTERNALDATE BODY.PEEK[])") # get email
    #         message = data[0][1]
    #         flags = imaplib.ParseFlags(data[0][0]) # get flags
    #         flag_str = b" ".join(flags)
    #         date = imaplib.Time2Internaldate(imaplib.Internaldate2tuple(data[0][0])) #get date
    #         copy_result = To.append(to_server['box_name'], flag_str.decode('utf-8'), date, message) # copy to archive
    #     
    #     #     if copy_result[0] == 'OK':
    #     #         del_msg = From.store(msg_num, '+FLAGS', '\\Deleted') # mark for deletion
    #     
    #     # ex = From.expunge() # delete marked
    #     # print('expunge status: %s' % ex[0])
    #     # if not ex[1][0]: # result can be ['OK', [None]] if no messages need to be deleted
    #     #     print('expunge count: 0')
    #     # else:
    #     #     print('expunge count: %s' % len(ex[1]))

    disconnect_server(From)
    disconnect_server(To)