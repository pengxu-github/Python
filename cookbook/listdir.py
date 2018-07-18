import os

path = '/mnt/freemeos-code/6763o/prod_debug'
names = os.listdir(path)


def bad_str(msg):
    return repr(msg)[1:-1]


def my_print(comment, msg):
    try:
        print('{}: {}'.format(comment, msg))
    except UnicodeEncodeError:
        print('{}: {}'.format(comment, bad_str(msg)))


for name in names:
    '''
    print names in path
    '''
    full_name = os.path.join(path, name)
    if os.path.isdir(full_name):
        my_print('dir', full_name)
    elif os.path.isfile(full_name):
        my_print('file', full_name)
    else:
        my_print('other', full_name)

ndis_dir = b'udce4'
ndis_file = b'udce4.txt'
if not os.path.exists(ndis_dir):
    os.mkdir(ndis_dir)
with open(os.path.join(ndis_dir, ndis_file), 'w') as f:
    f.write('hello world')
f.close()
