# searchdestroydb2
## Description
This tool uses the widely used migration script `searchreplacedb2.php` which webmasters often forget in their web root to gain control of a WordPress installation.
## Warning!
`single_user.py` is meant for the installations with only one user. Any collision will destroy the table. You can use it anyway on a multi-user wordpress, but having two hashes with the same first character following `$P$B` will fuck shit up.
## Usage
```
Usage: ./single_user.py <url>
```

## To Do
- Using multiple filling characters instead of always using `*` to mitigate collisions
