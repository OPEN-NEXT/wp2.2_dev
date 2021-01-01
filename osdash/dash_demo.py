#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import json

# BEGIN: Import dash-related libraries

import dash
import pandas
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

# END: Import dash-related libraries

"""

Import and prepare data for a demo dashboard

"""

# Load commit history
commits: list = []
import_file = open(file="commit_history.json", mode="r")
commits = json.load(import_file)
import_file.close()

# Load issues
issues: list = []
import_file = open(file="issues.json", mode="r")
issues = json.load(import_file)
import_file.close()

print("Files loaded.")

# Convert data to Pandas dataframes

commits_df = pandas.DataFrame(commits)
issues_df = pandas.DataFrame(issues)

# Get number of open and closed isses
# Using method here: 
# https://thispointer.com/pandas-count-rows-in-a-dataframe-all-or-those-only-that-satisfy-a-condition/
issues_open_df = issues_df.apply(lambda x: True if x["closed"] == False else False, axis=1)
n_open_issues = len(issues_open_df[issues_open_df == True].index)
n_closed_issues = len(issues_df) - n_open_issues

# Get number of commits
n_commits = len(commits_df)

# Get number of unique committers
# Method: 
# https://www.geeksforgeeks.org/how-to-count-distinct-values-of-a-pandas-dataframe-column/
n_committers = len(pandas.unique(commits_df["committer_email"]))

# Make sure timestamps are in Pandas format
# Method: 
# https://stackoverflow.com/q/29626543/186904
commits_df["commit_date"] = pandas.to_datetime(commits_df["commit_date"])
issues_df["createdAt"] = pandas.to_datetime(issues_df["createdAt"])

# Add year columns to dataframes
# Method: 
# https://stackoverflow.com/a/25149272/186904
commits_df["commit_date_year"] = pandas.DatetimeIndex(commits_df["commit_date"]).year
issues_df["createdAt_year"] = pandas.DatetimeIndex(issues_df["createdAt"]).year



# exit(0)

"""

Create basic Dash webview

"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# App layout

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Metrics for GitHub repository Safecast/bGeigieNanoKit")
            ]
        ),
        html.Br(),
        html.H2(id="chosen-year"),
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Select a year:"),
                        dcc.Slider(
                            id="year-slider",
                            min=min(commits_df["commit_date_year"]),
                            max=max(commits_df["commit_date_year"]),
                            value=min(commits_df["commit_date_year"]),
                            marks={str(year): str(year) for year in commits_df["commit_date_year"].unique()},
                            step=None
                        )
                    ],
                    className="pretty_container four columns"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Commits"),
                                html.H6(id="n-commits")
                            ],
                            className="mini_container"
                        ),
                        html.Div(
                            [
                                html.H3("Issues"),
                                html.H6(id="n-issues")
                            ],
                            className="mini_container"
                        ),
                        html.Div(
                            [
                                html.H3("Committers"),
                                html.H6(id="n-committers")
                            ],
                            className="mini_container"
                        )
                    ],
                    id="info-container",
                    className="row container-display"
                )
            ],
            className="row flex-display"
        )
    ]
)

# Dash callbacks

# Show chosen year
@app.callback(
    Output(component_id="chosen-year", component_property="children"),
    [Input("year-slider", "value")]
)
def show_chosen_year(selected_year):
    return f"As of {selected_year}"

# Show cumulative number of commits until a given year
@app.callback(
    Output(component_id="n-commits", component_property="children"),
    [Input("year-slider", "value")]
)
def show_n_commits(selected_year):
    filtered_commits = commits_df[commits_df["commit_date_year"] <= selected_year]
    filtered_n_commits = len(filtered_commits)
    return f"{filtered_n_commits}"

# Show cumulative number of issues until a given year
@app.callback(
    Output(component_id="n-issues", component_property="children"),
    [Input("year-slider", "value")]
)
def show_n_issues(selected_year):
    filtered_issues = issues_df[issues_df["createdAt_year"] <= selected_year]
    n_filtered_open_issues = len(filtered_issues[filtered_issues["closed"] == False])
    n_filtered_closed_issues = len(filtered_issues[filtered_issues["closed"] == True])
    return f"{n_filtered_open_issues}/{n_filtered_closed_issues} open/closed"

# Show cumulative number of committers until a given year
@app.callback(
    Output(component_id="n-committers", component_property="children"),
    [Input("year-slider", "value")]
)
def show_n_commiters(selected_year):
    filtered_commits = commits_df[commits_df["commit_date_year"] <= selected_year]
    n_committers = len(pandas.unique(filtered_commits["committer_email"]))
    return f"{n_committers}"

# Start Dash app server
if __name__ == "__main__":
    app.run_server(port=21110, debug=True)