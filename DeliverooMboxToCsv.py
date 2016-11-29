import sys
import mailbox
import re

mbox_filename = ''
csv_filename = ''
if len(sys.argv) == 3:
    mbox_filename = sys.argv[1]
    csv_filename = sys.argv[2]
elif len(sys.argv) == 2:
    mbox_filename = sys.argv[1]
    csv_filename = sys.argv[1][:sys.argv[1].index('.')] + '.csv'
else:
    raise ValueError('Invalid parameters')

mbox = mailbox.mbox(mbox_filename)

delivery_csv = open(csv_filename, 'w')
delivery_csv.write('Order #,Date,Time,Delivery Time,Restaurant,Credit Card Tip\n')

for message in mbox:
    body = message.get_payload().split('\r\n')
    order_number = re.findall('\d+', body[1])[0]
    date = body[4].split()[2]
    time = body[4].split()[3]
    delivery_time = int(re.findall('\d+', body[5].split()[2])[0])*60\
                    + int(re.findall('\d+', body[5].split()[3])[0])
    restaurant = ' '.join(body[7].split()[1:])
    tip = float(body[11].split()[-1])
    delivery_csv.write('{},{},{},{},{},{}\n'.format(order_number, date, time, delivery_time, restaurant, tip))

delivery_csv.close()