# ForgeFed field mappings

Highest level is a Python dictionary with the following keys (those with "*" are not part of or deviate from ForgeFed model): 

* Repository (dictionary)
  * name (string) - GitHub repository name i.e. the name part of owner/name in URL; Wikifactory project name from URL project name slug
  * attributedTo (string) - GitHub owner name in owner/namer in URL; Wikifactory project creator username (* because ForgeFed wants this to be URI or mailtoURI as email address)
  * published (ISO 8601 string) - GitHub repository's dateCreated; Wikifactory project's dateCreated
  * project* (string) - The project that this repository belongs to, e.g. multiple GitHub repositories belong to the Pocket Science Lab project
  * forkcount* (integer) - GitHub provides this number directly; Wikifactory 0 for now
  * forks* (list?) - GitHub list of forks URLs; Wikifactory null for now
  * license* (SPDX string) - GitHub provides this directly; Wikifactory might need mapping to SPDX string, need to check
  * platform* (string) - "GitHub" or "Wikifactory"
  * repo_url* (string) - This string should match what's in the repository list URLs
  * last_mined* (ISO 8601 string) - this is saved each time the repository is successfully mined
* Branches (list)
  * Branch (dictionary)
    * name (string) - Straightforward for GitHub, null for Wikifactory for now
* Commits (list)
  * Commit (dictionary)
    * committedBy (string) - GitHub author user name and Wikifactory creator user name (* because ForgeFed wants this to be URI or mailtoURI as email address)
    * committed (ISO 8601 string) - GitHub authored time and Wikifactory dateCreated
    * hash (string) - GitHub commit hash; Wikifactory contribution id
    * summary (string) - GitHub one-line title; Wikifactory contribution title
    * parents* (list) - GitHub normally one or two hashes; Wikifactory always seems to be one id since there are no branches to merge for now
    * url* (string) - GitHub and Wikifactory URLs to commit. GitHub gives this directly; for Wikifactory you need to construct this from project URL and contribution slug.
* Tickets (list)
  * Ticket (dictionary)
    * attributedTo (string) - GitHub and Wikifactory user name (* because ForgeFed wants this to be URI or mailtoURI as email address)
    * summary (string) - GitHub title and Wikifactory title
    * published (ISO 8601 string) - GitHub publishedAt and Wikifactory dateCreated
    * isResolved (boolean) - True/False from GitHub closed and Wikifactory
    * resolved (ISO 8601 string) - GitHub closedAt and Wikifactory empty string if not resolved, lastActivityAt if resolved (need to check if lastActivityAt matches actual resolve timestamp)
    * id* (string) - GitHub issue number and Wikifactory issue id
    * participants* (list) - List of strings of user names of anyone who has participated in this issue. Right now this probably means just commentors plus the original creator. (e.g. `creator` and `commentor` `username`s in Wikifactory API)
    * url* (string) - URL to issue. GitHub's API gives this directly, for Wikifactory will need project URL plus issue slug.
