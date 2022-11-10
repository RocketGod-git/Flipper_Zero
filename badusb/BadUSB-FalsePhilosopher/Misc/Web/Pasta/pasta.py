#!/usr/bin/env python3

try:
    import requests
    import argparse
    import sys
    import string
    import random
    import os
    import re

    from concurrent.futures import ThreadPoolExecutor
    from concurrent.futures.thread import BrokenThreadPool
    from colored import fg, attr
    from bs4 import BeautifulSoup
except ImportError as i:
    print(f"{attr(1)}{fg(1)}[-]{attr(0)} Some libraries are missing !")
    print(f"{attr(1)}{fg(1)}[-]{attr(0)} Python error: {i}")

# Disable insecure SSL warnings
# requests.urllib3.disable_warnings()

def random_ascii():
    files = os.listdir("./misc/art/")
    random_ = random.choice(files)
    try:
        with open(f"./misc/art/{random_}", "r") as asciiart_:
            return asciiart_.read()
    except OSError:
        raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open {fg(134)}{random_}{attr(0)} !")

def ascii():

    art_ = random_ascii()
    printAscii_ = f"""{attr(1)}{fg(45)}
    {art_}{attr(0)}
{fg(179)}ver: {attr(0)}{fg(106)}0.3{attr(0)}

    """
    print(printAscii_)

'''
Class to provide threading to other functions
'''
class Threading:

    def __init__(self, prog, threads):
        self.threads = threads
        self.prog = prog

    def threadit(prog, threads):
        try:
            with ThreadPoolExecutor(max_workers=threads) as executer:
                executer.submit(prog)
        except Exception as e:
            raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Exception hit: [{fg(189)}{e}{attr(0)}]")

'''
Class to search PasteBin with randomly generated
8 character string.

The class can generate number of strings:
 - (Search.randomize_alpha())

The class can send a request for each generated
string:
 - (Search.search_request())
'''
class Search:

    def __init__(self, str_range):
        self.str_range = int(str_range)

    # LA = Length of Alphabet
    # Essentially what string will be send to PasteBin
    def randomize_alpha(LA=8, str_range=0):

        alpha = string.ascii_letters + string.digits
        try:
            if str_range == 0:
                print(f"{attr(1)}{fg(1)}[-]{attr(0)} Number of strings can't be - {fg(13)}0{attr(0)}")
                sys.exit(1)

            elif str_range == 0:
                print(f"{attr(1)}{fg(1)}[-]{attr(0)} No strings to use to search PasteBin !")
                print(f"{attr(1)}{fg(4)}[*]{attr(0)} Generating {fg(119)}100{attr(0)} to use...")
                Search.randomize_alpha(8, 100)

        except Exception as e:
            raise Exception(e)

        # Check if strings.txt exists where random strings will be inserted
        if not os.path.isfile("./strings.txt") and not os.path.exists("./strings.txt"):

            print(f"{attr(1)}{fg(129)}[?]{attr(0)} File {fg(13)}strings.txt{attr(0)} doesn't exist !")
            print(f"{attr(1)}{fg(4)}[*]{attr(0)} Making {fg(13)}strings.txt{attr(0)} !")

            strings_file = open("strings.txt", "w+")
            strings_file.close()

        else:
            print(f"{attr(1)}{fg(2)}[+]{attr(0)} File {fg(13)}strings.txt{attr(0)} exists !")

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Writing {str_range} strings in {fg(13)}strings.txt{attr(0)} !")
        try:
            with open("./strings.txt", "w") as strings_file:
                for strings in range(str_range):
                    strings = ''.join(random.sample(alpha, LA))
                    strings_file.write(strings)
                    # Just need to apend a newline between each string
                    strings_file.write('\n')

                strings_file.close()
        except OSError:
            raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open {fg(134)}strings.txt{attr(0)} !")

    def search_request(threads, str_range=0):

        if str_range != 0:
            Search.randomize_alpha(8, str_range)

        elif str_range == 0:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} No strings to use to search PasteBin !")
            print(f"{attr(1)}{fg(4)}[*]{attr(0)} Generating {fg(119)}100{attr(0)} to use...")
            Search.randomize_alpha(8, 100)

        else:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Something went wrong with generating strings to search PasteBin !")
            sys.exit(1)

        # Safari cuz why not look fancy :P
        user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }
        URL = "https://pastebin.com/raw/"

        # Initiallise GET request
        r = requests.Session()
        search = r.get(URL,
                headers=user_agent,
                # verify=False
                )

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Using {threads} threads !")
        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Requesting the following IDs\r\n")
        # Check each string in the strings.txt file
        try:
            with open("./strings.txt", "r") as strings_file:
                for string in strings_file:

                    s = string.strip()
                    search = r.get(f"{URL}{s}",
                                    headers=user_agent,
                                    # verify=False
                                    )

                    try:
                        try:
                            # Perform GET
                            Threading.threadit(search,
                                               threads)
                        except BrokenThreadPool:
                            raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Threading exception hit !")

                        # Find out what's the response code
                        if search.status_code == 404:
                            print(f"{attr(1)}{fg(3)}[!]{attr(0)} Response {fg(1)}404{attr(0)} for - {fg(1)}{s}{attr(0)}")

                        elif search.status_code == 200:
                            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Response {fg(2)}200{attr(0)} for - {fg(6)}{s}{attr(0)}")
                            print(f"- URL: {URL+s}\r\n")

                        else:
                            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Response is different that 404 or 200 for - {fg(13)}{s}{attr(0)}")
                            sys.exit(1) # Not sure if we should exit here...??

                    except KeyboardInterrupt:
                        raise Exception(f"{attr(1)}{fg(203)}[x]{attr(0)} Killing the script...\r\n")

                strings_file.close()

        except OSError:
            raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open {fg(134)}strings.txt{attr(0)} !")

'''
The class is able to get the most recent archive from PasteBin.
It is able to view the contents of a specific PasteBin,
for example: $ pasta.py -c KHK2ndnC
 - CheckBin.get_recent_archive()

The class is able to check the contents of a user-provided ID.
 - CheckBin.view_pastebin(string) // Where string == KHK2ndnC
'''
class CheckBin:

    # def __init__(self, archive):
    #     self.archive = archive

    def get_recent_archive(archive):

        if not archive:

            # Set some variables
            HREF_REGEX = r"<a href=\"\/(.*?)\">(.*?)<\/a>"
            user_agent = {
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }

            ARCHIVE_URL = requests.get('https://pastebin.com/archive',
                                    # verify=False,
                                    headers=user_agent)

            soup = BeautifulSoup(ARCHIVE_URL.content, 'html.parser')
            pastes = soup.find_all('a')

            # prints the necessary values using the HREF_REGEX above
            pastes_findall = re.findall(HREF_REGEX, str(pastes))

            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Grabbing a most recent PasteBin archive !\r\n")

            # Will grab only the title and id of each PasteBin in the recent archive
            try:
                # id = PasteBin ID - KHK2ndnC
                # t = PasteBin Title associated to the ID
                for id, t in pastes_findall:

                    output = f"{t} -> {id}"
                    get_valid = r'(.*?) \-\> ([A-Za-z\d+]{8})'
                    final = re.search(get_valid, output)

                    # Will check if the object type is NoneType
                    # and will skip that object
                    if final is None:
                        pass

                    else:
                        final = final.group(0)
                        print(f"{fg(186)}{attr(1)}{final}{attr(0)}")

            # Again, if there's an IndexError it's skipped
            except IndexError:
                pass

        elif archive:

            ARCHIVE_URL = "https://pastebin.com/archive/"
            HREF_REGEX = r"<a href=\"\/(.*?)\">(.*?)<\/a>"
            user_agent = {
                "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }

            URL_REQUEST = requests.get(f'{ARCHIVE_URL}{archive}',
                                    # verify=False,
                                    headers=user_agent)

            soup = BeautifulSoup(URL_REQUEST.content, 'html.parser')
            pastes = soup.find_all('a')

            # prints the necessary values using the HREF_REGEX above
            pastes_findall = re.findall(HREF_REGEX, str(pastes))

            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Grabbing most recent PasteBin archive of {fg(166)}{archive}{attr(0)}\r\n")

            try:
                for id, t in pastes_findall:

                    output = f"{t} -> {id}"
                    get_valid = r'(.*?) \-\> ([A-Za-z\d+]{8})'
                    final = re.search(get_valid, output)

                    if final is None:
                        pass

                    else:
                        final = final.group(0)
                        print(f"{fg(186)}{attr(1)}{final}{attr(0)}")
            except IndexError:
                pass

    def view_pastebin(string):

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Checking the contents of {fg(12)}{string}{attr(0)}")

        # Simple check if the user-provided string is 8 chars long
        if string == "" or len(string) < 8 or len(string) > 8:
            print(f"{attr(1)}{fg(3)}[!]{attr(0)} An 8 character string has to be provided.")
            print(f"{attr(1)}{fg(3)}[!]{attr(0)} Example: {sys.argv[0]} -c \"KHK2ndnC\"")
            sys.exit(1)

        elif string != "" and len(string) == 8:

            r = requests.Session()
            RAW_URL = f"https://pastebin.com/raw/{string}"
            user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }

            search = r.get(
                RAW_URL,
                headers=user_agent,
                # verify=False
                )

            # If the HTTP response is 200, write the contents of the PasteBin
            if search.status_code == 200:
                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Saving the contents of {fg(12)}{string}{attr(0)} to {fg(3)}output/{string}.pastebin.txt{attr(0)}")
                if not os.path.isdir("output") and not os.path.exists("output"):
                    print(f"{attr(1)}{fg(129)}[?]{attr(0)} Folder 'output' doesn't exist !")
                    print(f"{attr(1)}{fg(4)}[*]{attr(0)} Making folder 'output' !")

                    try:
                        os.mkdir("output")
                    except FileExistsError:
                        raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Directory {fg(13)}output{attr(0)} exists !")

                with open(f"output/{string}.pastebin.txt", "w") as pastebin_entry:
                    pastebin_entry.write(search.text)
                    pastebin_entry.close()

                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Showing the contents of {fg(12)}{string}{attr(0)} PasteBin entry !")
                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Content:")
                print(50 * "-")
                print(search.text)
                sys.exit(0)

            elif search.status_code == 404:
                print(f"{attr(1)}{fg(3)}[!]{attr(0)} Response {fg(1)}404{attr(0)} for - {fg(1)}{string}{attr(0)}")
                sys.exit(1)

            else:
                print(f"{attr(1)}{fg(1)}[-]{attr(0)} Response is different that 404 or 200 for - {fg(13)}{string}{attr(0)}")
                sys.exit(1)

        else:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Something is not right ! Try again !")
            sys.exit(1)

'''
The class can check the contents of the PasteBins
 - CheckAllBin.contents_of_pastes(id) // Where id == ID of PasteBin

The class can check for sensitive data such as emails, usernames & IP addresses
 - CheckAllBin.search_sensitive_data()
'''
class CheckAllBin:

    def __init__(self, threads):
        self.threads = threads

    def contents_of_pastes(id, threads):

        ARCHIVE_URL = "https://pastebin.com/archive"
        RAW_URL = "https://pastebin.com/raw/"

        HREF_REGEX = r"<a href=\"\/(.*?)\">(.*?)<\/a>"
        get_valid_id = r'\(\'([A-Za-z\d+]{8})\''
        user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
        }

        URL_ARCHIVE = requests.get(ARCHIVE_URL,
                                    # verify=False,
                                    headers=user_agent)

        soup = BeautifulSoup(URL_ARCHIVE.content, 'html.parser')
        pastes = soup.find_all('a')

        # Prints the necessary values using the regex above
        pastes_findall = re.findall(HREF_REGEX, str(pastes))
        pastes_id = re.findall(get_valid_id, str(pastes_findall))

        if not os.path.isdir("output") and not os.path.exists("output"):
            print(f"{attr(1)}{fg(129)}[?]{attr(0)} Folder {fg(13)}output{attr(0)} doesn't exist !")
            print(f"{attr(1)}{fg(4)}[*]{attr(0)} Making folder {fg(13)}output{attr(0)} !")

            try:
                os.mkdir("output")
            except FileExistsError:
                raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Directory {fg(13)}output{attr(0)} exists !")

        # Directory 'pastebins' will be created
        if os.path.exists('output/pastebins') and os.path.isdir('output/pastebins'):
            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Directory {fg(13)}pastebins{attr(0)} exists !")

        else:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Directory {fg(13)}pastebins{attr(0)} doesn't exist, making it !")
            try:
                os.mkdir('output/pastebins')
            except NotADirectoryError or FileExistsError:
                raise Exception(f"{attr(1)}{fg(3)}[-]{attr(0)} Directory creation of {fg(13)}pastebins{attr(0)} failed !")

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Using {threads} threads !")
        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Grabbing most recent PasteBin archive !\r\n")
        try:
            # A for loop to check the contents of each ID.
            for id in pastes_id:
                URL_RAW = requests.get(f"{RAW_URL}{id}",
                                        # verify=False,
                                        headers=user_agent)

                try:
                    with open(f"output/pastebins/Pastebin-{id}.txt", "w") as pastebin:
                        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Saving the contents of {fg(12)}{id}{attr(0)} to {fg(3)}output/pastebins/Pastebin-{id}.txt{attr(0)}")
                        try:
                            Threading.threadit(pastebin.write(URL_RAW.text), threads)
                            Threading.threadit(pastebin.close(), threads)
                        except Exception as e:
                            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Threading exception hit: [{fg(189)}{e}{attr(0)}]")
                except OSError:
                    pastebin.close()
                    raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open ./output/pastebins/Pastebin-{fg(134)}{id}{attr(0)} !")

        except KeyboardInterrupt:
            raise Exception(f"{attr(1)}{fg(203)}[x]{attr(0)} Killing the script...\r\n")

    def search_sensitive_data(f):

        # Some regex variables
        USERNAME_REGEX = r"^[a-z0-9_-]{3,15}$"
        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        IP_REGEX = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"

        if not f:
            for file in os.listdir("./output/pastebins/"):
                # For each file check if it's a directory instead of file
                # If yes, exit
                try:
                    if os.path.isdir(f"./output/pastebins/{file}"):
                        print(f"{attr(1)}{fg(1)}[-]{attr(0)} {fg(134)}{attr(1)}{file}{attr(0)} is a directory not a file !")
                        sys.exit(0)
                except Exception as e:
                    raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Something went wrong [{fg(187)}{e}{attr(0)}]")

                try:
                    # Read each file and search for emails, usernames, IP addresses
                    with open(f"./output/pastebins/{file}", "r") as pastebin:

                        # For each of the read files, look for the matching regex
                        for line in pastebin.readlines():

                            email_search = re.search(EMAIL_REGEX, str(line))
                            if email_search:
                                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found emails in {fg(3)}output/pastebins/{file}{attr(0)}")
                                print(f"{email_search.group(0)}\r\n")

                            ip_search = re.search(IP_REGEX, str(line))
                            if ip_search:
                                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found IP addresses in {fg(3)}output/pastebins/{file}{attr(0)}")
                                print(f"{ip_search.group(0)}\r\n")

                            username_search = re.search(USERNAME_REGEX, str(line))
                            if username_search:
                                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found username in {fg(3)}output/pastebins/{file}{attr(0)}")
                                print(f"{username_search.group(0)}\r\n")

                        pastebin.close()
                except OSError:
                    pastebin.close()
                    raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open ./output/pastebins/{fg(134)}{file}{attr(0)} !")

        # Choose a file in ./output/ and check for sensitive info
        # using regex above
        else:
            try:
                if os.path.isdir(f"./output/{f}"):
                    print(f"{attr(1)}{fg(1)}[-]{attr(0)} {fg(134)}{attr(1)}{f}{attr(0)} is a directory not a file !")
                    sys.exit(0)
            except Exception as e:
                raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Something went wrong [{fg(187)}{e}{attr(0)}]")

            try:
                with open(f"./output/{f}", "r") as file_to_read:

                    print(f"{attr(1)}{fg(2)}[+]{attr(0)} Searching for sensitive info in {fg(3)}output/{f}{attr(0)}")
                    file = file_to_read.readlines()

                    for line in file:
                        email_search = re.search(EMAIL_REGEX, str(line))
                        if email_search:
                            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found emails in {fg(3)}output/{f}{attr(0)}")
                            print(f"{email_search.group(0)}\r\n")

                        ip_search = re.search(IP_REGEX, str(line))
                        if ip_search:
                            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found IP addresses in {fg(3)}output/{f}{attr(0)}")
                            print(f"{ip_search.group(0)}\r\n")

                        username_search = re.search(USERNAME_REGEX, str(line))
                        if username_search:
                            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Found username in {fg(3)}output/{f}{attr(0)}")
                            print(f"{username_search.group(0)}\r\n")

                    file_to_read.close()
            except OSError:
                raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open ./output/{fg(134)}{f}{attr(0)} !")


'''
The class is capable of going through all PasteBins of
a user and grabbing all PasteBins posted by that person
 - search_person()
'''
# Users to use for debugging:
# - 7d2dlauncher (short list)
# - desislava_topuzakova (long list)
class Pastebiner:

    def pastebiner(u, p, threads):

        RAW_URL = "https://pastebin.com/raw/"
        USER_URL = "https://pastebin.com/u/"

        HREF_REGEX = r"<a href=\"\/(.*?)\">(.*?)<\/a>"
        get_valid_id = r"\(\'([A-Za-z\d+]{8})\'"

        r = requests.Session()
        user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
        }

        request_user = r.get(
            USER_URL+u,
            headers=user_agent,
            # verify=False
            )

        # Is the user parameter empty ?
        if not u:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} User cannot be empty !")

        # Directory 'users' will be created if not existing
        if os.path.exists(f'output/users') and os.path.isdir(f'output/users'):
            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Directory {fg(13)}users{attr(0)} exists !")

        else:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Directory {fg(13)}users{attr(0)} doesn't exist, making it !")
            try:
                os.mkdir('output/users')
            except NotADirectoryError or FileExistsError:
                raise Exception(f"{attr(1)}{fg(3)}[-]{attr(0)} Directory creation of {fg(13)}users{attr(0)} failed or already exists !")

        # Check if user exists in PasteBin
        if request_user.status_code == 404:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} User {fg(134)}{attr(1)}{u}{attr(0)} doesn't exist")
            sys.exit(0)

        # When user is present make a dir with their name
        if request_user.status_code == 200:
            if os.path.exists(f'output/users/{u}') and os.path.isdir(f'output/users/{u}'):
                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Directory of user {fg(13)}{u}{attr(0)} exists !")

            else:
                print(f"{attr(1)}{fg(1)}[-]{attr(0)} Directory of user {fg(134)}{u}{attr(0)} doesn't exist, making it !")
                try:
                    os.mkdir(f'output/users/{u}')
                except NotADirectoryError or FileExistsError:
                    raise Exception(f"{attr(1)}{fg(3)}[-]{attr(0)} Directory creation of user {fg(134)}{u}{attr(0)} failed or already exists !")

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Requesting page {fg(44)}{attr(1)}{p}{attr(0)}")
        try:
            get_page = r.get(
                f"{USER_URL}{u}/{p}",
                headers=user_agent,
                # verify=False
            )

            soup = BeautifulSoup(get_page.content, 'html.parser')
            pastes = soup.find_all('a')

            # Prints the necessary values using the regex above
            pastes_findall = re.findall(HREF_REGEX, str(pastes))
            pastes_id = re.findall(get_valid_id, str(pastes_findall))

            print(f"{attr(1)}{fg(2)}[+]{attr(0)} Using {threads} threads !\r\n")
            for id in pastes_id:
                URL_RAW = requests.get(f"{RAW_URL}{id}",
                                    # verify=False,
                                    headers=user_agent)
                try:
                    with open(f"output/users/{u}/Pastebin-{id}.txt", "w") as pastebin:
                        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Saving the contents of {fg(12)}{id}{attr(0)} to {fg(3)}output/users/{fg(134)}{u}{attr(0)}{fg(3)}/Pastebin-{id}.txt{attr(0)}")
                        try:
                            Threading.threadit(pastebin.write(URL_RAW.text), threads)
                            Threading.threadit(pastebin.close(), threads)
                        except Exception as e:
                            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Threading exception hit: [{fg(189)}{e}{attr(0)}]")
                            sys.exit(0)
                except OSError:
                    raise Exception(f"{attr(1)}{fg(1)}[-]{attr(0)} Cannot read/open ./output/users/{fg(134)}{u}{attr(0)}")

        except Exception as e:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Exception hit: [{fg(189)}{e}{attr(0)}]")

#Initilize parser for arguments
def argparser():

    parser = argparse.ArgumentParser(description='Pasta - A PasteBin Scraper')
    parser.add_argument("-s",
            "--search",
            help="Search PasteBin with a set of strings",
            action="store_true",
            required=False
            )

    parser.add_argument("-r",
            "--range_str",
            help="How many strings to generate",
            type=int,
            required=False
            # default=5
            )

    parser.add_argument("-c",
            "--check",
            help="Check contents of a specific PasteBin entry",
            type=str,
            required=False
            )

    parser.add_argument("-g",
            "--get_archive",
            help="Get most recent PasteBin archive",
            required=False,
            #action='store_true'
            nargs="?"
            )

    parser.add_argument("-d",
            "--scrape",
            help="Scrape the most recent archive and save each Pastebin",
            required=False,
            action='store_true'
            )

    parser.add_argument("-e",
            "--sensitive",
            help="Search for sensitive info from downloaded Pastebins",
            required=False,
            action='store_true'
            )

    parser.add_argument("-u",
            "--userbin",
            help="Retrieve the PasteBin posts of a user",
            required=False,
            type=str
            )

    parser.add_argument("-p",
            "--page",
            help="Page number of user's PasteBins",
            required=False,
            type=str
            )

    parser.add_argument("-f",
            "--file",
            help="Search PasteBin with a set of strings",
            required=False,
            type=str
            )

    parser.add_argument("-t",
            "--threads",
            help="How many threads to use",
            required=False,
            type=int
            )

    #Show help menu if no arguments provided
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h'])

    if args.search:

        if args.threads:
            threads = args.threads
        else:
            threads = 5

        if args.range_str:
            str_range = args.range_str
        else:
            str_range = 0

        Search.search_request(threads, str_range)

    if args.range_str and not args.search:
        str_range = args.range_str
        Search.randomize_alpha(8, str_range)

    if args.check:
        string = args.check
        CheckBin.view_pastebin(string)

    if args.get_archive is not None:
        archive = args.get_archive
        CheckBin.get_recent_archive(archive)
    else:
        CheckBin.get_recent_archive(None)

    if args.scrape:
        if args.threads:
            threads = args.threads
        else:
            threads = 5

        CheckAllBin.contents_of_pastes(id, threads)

    # These go together ############################
    if args.sensitive and not args.file:
        f = None
        CheckAllBin.search_sensitive_data(f)
    elif args.sensitive and args.file:
        CheckAllBin.search_sensitive_data(args.file)
    ################################################

    # These go together ####################
    if args.userbin and not args.page:
        u = args.userbin
        p = 0

        if args.threads:
            threads = args.threads
        else:
            threads = 5
        Pastebiner.pastebiner(u, p, threads)

    if args.userbin and args.page:
        u = args.userbin
        p = args.page

        if args.threads:
            threads = args.threads
        else:
            threads = 5
        Pastebiner.pastebiner(u, p, threads)
    ########################################

    # Checks for parameters used alone which shouldn't be
    # -p parameter (user page)
    if args.page:
        print(f"{attr(1)}{fg(4)}[*]{attr(0)} Parameter {fg(155)}-p{attr(0)} cannot be used alone !")
        print("Usage in combination with: \r\n")
        print("-u/--userbin USER - Retrieve the PasteBin posts of a user")
        # print("-t/--threads THREADS - How many threads to use")
        sys.exit(0)

    # -t threads
    if args.threads:
        print(f"{attr(1)}{fg(4)}[*]{attr(0)} Parameter {fg(155)}-t{attr(0)} cannot be used alone !")
        print("Usage in combination with: \r\n")
        print("-u/--userbin USER - Retrieve the PasteBin posts of a user")
        # print("-t/--threads THREADS - How many threads to use")
        print("-d/--scrape - Scrape the most recent archive and save each Pastebin")
        print("-s/--search - Search PasteBin with a set of strings")
        sys.exit(0)

if __name__ == "__main__":
    ascii()
    argparser()
