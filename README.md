# searchpwndb2
## Description
This tool uses the widely used migration script `searchreplacedb2.php` which webmasters often forget in their web root to gain control of a WordPress installation.

## Usage
```
$ ./replace_admin.py --help
Usage: ./replace_admin.py -t <target_url> [-u <user>] [-p <password>]

~Mixbo (https://github.com/mixbo)

Options:
  -h, --help          show this help message and exit
  -t TARGET_URL       The target's URL (ex:
                      http://www.exemple.com/searchreplacedb2.php)
  -u TARGET_USER      The target's user you'll use
  -p TARGET_PASSWORD  The new password
```
