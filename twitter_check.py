#!/usr/bin/python

import sys
import re
from datetime import datetime
import requests

if len(sys.argv) != 3:
    sys.exit("Usage: ./%s <list_of_accounts> <year>" % sys.argv[0])

proxies = {
    'http':'socks5://USER:PASSWORD@SERVER',
    'https':'socks5://USER:PASSWORD@SERVER'
}


def fillfound():

    msg = sys.argv[2] + "&quot;"
    url = "https://twitter.com/"
    acc_list = open(sys.argv[1], 'r', encoding="ISO-8859-1")
    acc_found = open(sys.argv[2] + ".txt", "a", encoding="ISO-8859-1")
    acc_nb = 0
    retry = 0
    max_retry = 10

    for line in acc_list:
        splitted = line.split(':')
        acc_name = splitted[0]
        acc_pass = splitted[1]
        print("[.] Checking Availability Of '%s'..." % acc_name)
        if len(splitted) != 2:
            print("[$]\tError: Wrong format!")
            continue
        while True:
            try:
                ret = requests.get(url + acc_name, proxies=proxies)
                retry = 0
                find = re.search(msg, str(ret.content))
                if find and len(acc_name) > 0:
                    acc_found.write(acc_name + ":" + acc_pass)
                    print("[+]\t%s\'s Account Has Been Created In %s!" %
                          (acc_name, sys.argv[2]))
                    acc_nb += 1
                break
            except IOError:
                print("[x] Connection error, reconnecting... %s of %s" %
                      (retry+1, max_retry))
                retry += 1
                if retry == max_retry:
                    print("[x] Too many retries, program interrupted...")
                    return acc_nb
                continue
            except (KeyboardInterrupt, SystemExit):
                print("\n[x] Program Interrupted...")
                return acc_nb

    acc_list.close()
    acc_found.close()

    return acc_nb


def main():
    actual_time = datetime.now()
    acc_nb = fillfound()
    print("\n[*] Scanning completed, %s account(s) found, elapsed time: %s." %
          (acc_nb, datetime.now() - actual_time))


if __name__ == "__main__":
    main()
    sys.exit()
