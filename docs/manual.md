# Installation

 - check `../requirements.txt` for required python libraries.
 - the library [perceval](https://github.com/chaoss/grimoirelab-perceval ) requires Python >= 3.4

# Execution

`start.py` is the main script. It requires arguments that can either be passed as command line arguments or from a json configuration file.

| short argument code | long argument code | type | meaning |
| ------------------- | ------------------ | ---- | ------- |
|`-c`|`--config_file`|string| Path to configuration file. Will override corresponding --auth and --repolist options.|
|`-a`|`--auth_token`|string|Path to GitHub personal authentication token file. |
|`-d`|`--data_dir`|string| Output directory for storing downloaded data.|
|`-r`|`--repo_list`|string| Path to CSV file containing list of repositories to mine.|
|`-l`|`-log_level`|string| Valid options: debug, info, warning, error (default), critical.|
| - |`--create_data_dir`|bool| If data output directory doesn't exist, create it.|

Example:

Command line: `python3 start.py -c config.json`

Configuration file `config.json`:
```
{
    "auth_token": "token",
    "data_dir": "__DATA__",
    "repo_list": "repolist_example.csv",
    "create_data_dir": true,
    "log_level": "DEBUG",
}
```

# Input data

`--repo_list` should be a valid CSV file in the following format:
 - line separator: carriage return
 - column separator: comma
 - the table has headings ("owner,repo")
 - column 1 contains valid GitHub user logins
 - column 2 contains valid Github repository name
 - the combination of the user login and the repository name at the same line yield a valid GitHub repository identifier ("OPEN-NEXT/WP2.2_dev")

Example:

```
owner,repo
OPEN-NEXT,wp2.2_reference
jbon,github-mining
```