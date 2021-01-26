#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

# Python Standard Library imports

# External imports
import pandas

# Main function to derive metrics from mined data
def get_metrics(mined_data: list) -> dict: 
    """[summary]

    Args:
        mined_data (list): [description]

    Returns:
        dict: A dictionary containing Pandas dataframes
    """

    # Initialise empty lists for each type of data that will later be converted
    # into data frames
    repositories_list: list = []
    branches_list: list = []
    commits_list: list = []
    tickets_list: list = []

    # 
    # Iterate mined data a put information from each type into the lists
    # 

    for repo in mined_data: 
        # Process `Repository`
        repositories_list.append(repo["Repository"])
        # Process `Branches`
        for branch in repo["Branches"]: 
            # Start with columns for repository info
            branch_row: dict = {
                "repo_name": repo["Repository"]["name"],
                # Include `repo_url` so that there's a more unique identifier:
                "repo_url": repo["Repository"]["repo_url"], 
                "branch": branch
            }
            branches_list.append(branch_row)
        # Process `Commits`
        for commit in repo["Commits"]:
            # Start with columns for repository info
            commit_row: dict = {
                "repo_name": repo["Repository"]["name"],
                # Include `repo_url` so that there's a more unique identifier:
                "repo_url": repo["Repository"]["repo_url"]
            }
            # Then add other columns from the commit
            commit_row.update(commit)
            commits_list.append(commit_row)
        # Process `Tickets`
        for ticket in repo["Tickets"]: 
            # Start with columns for repository info
            ticket_row: dict = {
                "repo_name": repo["Repository"]["name"], 
                # Include `repo_url` so that there's a more unique identifier:
                "repo_url": repo["Repository"]["repo_url"]
            }
            # Then add other columns from the ticket
            ticket_row.update(ticket)
            tickets_list.append(ticket_row)

    #
    # Convert lists to Pandas dataframes and process
    #
    
    # Convert each list to a Pandas dataframe
    repositories: pandas.DataFrame = pandas.DataFrame(repositories_list)
    branches: pandas.DataFrame = pandas.DataFrame(branches_list)
    commits: pandas.DataFrame = pandas.DataFrame(commits_list)
    tickets: pandas.DataFrame = pandas.DataFrame(tickets_list)

    # There are multiple `forks` in a `Repository`; `parents` in a `Commit`; 
    # and `participants` in a `Ticket`. `explode()` them so that there is a row
    # for each one. Reference: 
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.explode.html
    # Also explicity cast column data types with `astype()` including all timestamps as UTC.
    repositories = repositories.explode("forks").astype({"name": str, 
                                                         "attributedTo": str, 
                                                         "published": "datetime64[ns, UTC]",
                                                         "project": str, 
                                                         "forkcount": int, 
                                                         "forks": str,
                                                         "license": str, 
                                                         "platform": "category", 
                                                         "repo_url": str,
                                                         "last_mined": "datetime64[ns, UTC]"})
    commits = commits.explode("parents").astype({"repo_name": str, 
                                                 "repo_url": str, 
                                                 "committedBy": str, 
                                                 "committed": "datetime64[ns, UTC]", 
                                                 "hash": str, 
                                                 "summary": str,
                                                 "parents": str,
                                                 "url": str})
    tickets = tickets.explode("participants").astype({"repo_name": str,
                                                      "repo_url": str,
                                                      "attributedTo": str, 
                                                      "summary": str, 
                                                      "published": "datetime64[ns, UTC]",
                                                      "isResolved": bool, 
                                                      "resolved": "datetime64[ns, UTC]",
                                                      "id": str,
                                                      "participants": str,
                                                      "url": str})

    # Convert timestamps to Pandas format
    # repositories["published"] = pandas.to_datetime(repositories["published"], utc=True)
    # commits["committed"] = pandas.to_datetime(commits["committed"], utc=True)
    # tickets["published"] = pandas.to_datetime(tickets["published"], utc=True)
    # tickets["resolved"] = pandas.to_datetime(tickets["resolved"], utc=True)

    # 
    # Create user activity histories
    # 
    
    # User commits
    # Use `drop_duplicates()` to remove extra rows because some commits might 
    # have >1 parents.
    user_commits: pandas.DataFrame = commits[["committedBy", 
                                              "repo_name", 
                                              "repo_url", 
                                              "hash", 
                                              "committed"]].drop_duplicates()
    # Add a column for activity type
    user_commits.insert(3, "activity_type", "commit")
    # Rename columns
    user_commits.rename(columns={"committedBy": "username", 
                                 "hash": "activity_id", 
                                 "committed": "activity_time"}, 
                        inplace=True)
    
    # User tickets
    # For now, this uses the ticket creation time which might not equal the 
    # exact time a user participated in a ticket.
    user_tickets: pandas.DataFrame = tickets[["participants", 
                                              "repo_name", 
                                              "repo_url", 
                                              "id", 
                                              "published"]].drop_duplicates()
    # Add a column for activity type
    user_tickets.insert(3, "activity_type", "ticket")
    # Rename columns
    user_tickets.rename(columns={"participants": "username", 
                                 "id": "activity_id", 
                                 "published": "activity_time"}, 
                        inplace=True)
    
    # Combine into complete user history
    user_history: pandas.DataFrame = pandas.concat([user_commits, user_tickets]).astype({"activity_type": "category"})
    user_history.sort_values(by=["repo_url", 
                                 "username", 
                                 "activity_type", 
                                 "activity_time"], 
                            inplace=True)

    # Put dataframes into a dictionary to return
    processed_data: dict = {
        "Repositories": repositories,
        "Branches": branches,
        "Commits": commits, 
        "Tickets": tickets,
        "Users": user_history
    }

    return processed_data