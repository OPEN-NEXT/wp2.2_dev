#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021 Pen-Yuan Hsing
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Define layout and functions of dashboard
"""

# Python Standard Library imports
import calendar
import datetime
import pathlib

# External imports
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.express
import plotly.graph_objects
from dash.dependencies import Input, Output

# Some constants
EXTERNAL_CSS: list = [str(pathlib.Path(__file__).parent / pathlib.Path("assets/css/bootstrap.min.css"))]
# EXTERNAL_CSS: list = [dbc.themes.BOOTSTRAP]

# Generate a table
def generate_table(df: pandas.DataFrame, max_rows: int=20) -> html.Table:
    """[summary]
    Reference: 
    https://dash.plotly.com/layout

    Args:
        df (pandas.DataFrame): [description]
        max_rows (int, optional): [description]. Defaults to 10.

    Returns:
        html.Table: [description]
    """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])

# Function to add an arbitrary number of months to a given year-month-day date
def add_months(startdate: datetime.date, inc: int) -> datetime.date:
    """Add any number of months to a date

    In this implementation, one month after the input date will not end up
    being two months later. For example, one month after January 31 wouldn't
    be February 31 or March 1, this function would return (for better or worse)
    February 28. Based on this solution by Dave Webb (2010-11-09 CC BY-SA 3.0): 
    https://stackoverflow.com/a/4131114/186904

    Args:
        timestamp (datetime.date): [description]
        inc (int): Number of months to add

    Returns:
        datetime.date: [description]
    """
    # Do this to the month first to deal with overflow months (e.g. 13):
    month: int = startdate.month - 1 + inc
    year: int = startdate.year + (month // 12) # Increment as many years as needed
    # Now get the actual resulting month
    month = month % 12 + 1
    # The following line makes sure we don't get results like February 31 or 
    # "one month" after January 31 being 1 March:
    # (`monthrange()` returns te number of days for given a year-month as its
    # second return value)
    day: int = min(startdate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

# Get the number of months between two dates
def month_diff(date1: datetime.date, date2: datetime.date) -> int: 
    """Return absolute number of months between two dates

    Rounded to full months, so difference between February 29 and March 1 of 
    the same year is still one month.

    Based on snippet by John La Rooy (2010-10-28 CC BY-SA 3.0): 
    https://stackoverflow.com/a/4040338/186904

    Args:
        startdate (datetime.date): [description]
        enddate (datetime.date): [description]

    Returns:
        int: [description]
    """
    return abs((date1.year - date2.year) * 12 + date1.month - date2.month)

# Given two Pandas timestamps, iterate through each month within to get marks
# for Dash Core Component RangeSlider
def get_time_range_slider_marks(mintime, maxtime) -> dict:
    """[summary]

    Each quarter (i.e. every three months) gets a mark (e.g. Q2) while the 
    first quarter is labelled as the year (e.g. 2020). Based on Dash app 
    `dash-nlp` in `dash-sample-apps` by Vildly (2019 MIT license): 
    https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-nlp

    Args:
        mintime ([type]): [description]
        maxtime ([type]): [description]
        range ([type]): [description]

    Returns:
        dict: For use in RangeSlider's `marks` argument
    """
    # Get the number of months between the two dates
    mindate: datetime.date = datetime.date(mintime.year, mintime.month, 1)
    maxdate: datetime.date = datetime.date(maxtime.year, maxtime.month, maxtime.day)
    n_months: int = month_diff(mindate, maxdate)
    # Get the first mark at a quarter
    marks: dict = {}
    current_date: datetime.date = mindate
    for m in range(0, n_months): 
        current_date: datetime.date = add_months(current_date, 1)
        if current_date.month == 1: 
            marks[m] = {
                "label": str(current_date.year),
                "style": {"font-weight": "bold"}
            }
        elif current_date.month == 4:
            marks[m] = {
                "label": "Q2",
                "style": {"font-weight": "lighter", "font-size": 7}
            }
        elif current_date.month == 7:
            marks[m] = {
                "label": "Q3",
                "style": {"font-weight": "lighter", "font-size": 7}
            }
        elif current_date.month == 10:
            marks[m] = {
                "label": "Q4",
                "style": {"font-weight": "lighter", "font-size": 7}
            }
        else: 
            pass
    return marks

#
# Main function for creating app
#

def create_app(data: dict) -> dash.Dash:
    """
    docstring
    """
    # Initialise a Dash app
    app: dash.Dash = dash.Dash(__name__, external_stylesheets=EXTERNAL_CSS)

    #
    # Prepare base data
    #

    repositories: pandas.DataFrame = data["Repositories"]
    # branches: pandas.DataFrame = data["Branches"] # Nothing implemented yet
    commits: pandas.DataFrame = data["Commits"]
    tickets: pandas.DataFrame = data["Tickets"]
    users: pandas.DataFrame = data["Users"]

    #
    # Define page layout
    #

    TOP_BAR = dbc.Navbar(
        children=[
            html.A(
                dbc.Row(
                    [
                        dbc.NavbarBrand("Open!Next WP2.2 dashboard")
                    ], 
                    no_gutters=True
                )
            )
        ], 
        color="dark", 
        dark=True, 
        sticky="top"
    )

    LEFT_COLUMN = dbc.Jumbotron(
        children=[
            html.H2("Choose repository"),
            html.Label("1. Select a project: "),
            dcc.Dropdown(
                id="project-menu",
                options=[
                    {"label": p, "value": p} for p in repositories["project"].unique()
                ],
                # Default to project in first row of repositories dataframe
                value=repositories.iloc[0]["project"],
                clearable=False, 
                style={"marginBottom": 30}
            ),
            html.Label(id="repo-menu-label"),
            dcc.Dropdown(
                id="repo-menu",
                clearable=False, 
                style={"marginBottom": 30},
            ),
            html.Label("3. Customise timeframe to view: "), 
            dcc.RangeSlider(
                id="time-range-slider",
                updatemode = "mouseup", # Don't refresh until mouse button released!
            ),
            html.P(
                "(draggable in 1-month increments)", 
                style={"fontSize": 10, "font-weight": "light"}
            )
        ], 
        style={"columnCount": 1}
    )

    COMMITS_CARD = dbc.Card(
        dbc.CardBody(
            [
                html.H4(id="commits-card", className="card-title"), 
                html.P("Commits")
            ]
        )
    )

    TICKETS_CARD = dbc.Card(
        dbc.CardBody(
            [
                html.H4(id="tickets-card", className="card-title"), 
                html.P("Tickets opened/closed")
            ]
        )
    )

    CONTRIBUTORS_CARD = dbc.Card(
        dbc.CardBody(
            [
                html.H4(id="contributors-card", className="card-title"), 
                html.P("Contributors")
            ]
        )
    )

    RIGHT_COLUMN = html.Div(children=[
        html.H1(id="repo-title"),

        html.Div(children=f'''
            Information about this repository during specified timeframe.
        '''),

        dbc.CardGroup(
            [
                COMMITS_CARD,
                TICKETS_CARD,
                CONTRIBUTORS_CARD
            ],
            style={"marginTop": 30}
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.H4("Commits over time", className="card-title")),
                dbc.CardBody(
                    [
                        dcc.Graph(
                            id="commits-plot"
                        )
                    ]
                )
            ],
            style={"marginTop": 30}
        ),

        html.H3("User activities", style={"marginTop": 30}), 
        html.P("Total commits and tickets by username during specified timeframe."),
        html.Div(
            id="user-activity-table"
        )
    ])

    BODY: dbc.Container = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(LEFT_COLUMN, md=4),
                    dbc.Col(RIGHT_COLUMN, md=8)
                ], 
                style={"marginTop": 30}
            )
        ],
        className="mt-12"
    )

    app.layout = html.Div(children=[
        TOP_BAR, 
        BODY
    ])

    #
    # Dash callbacks
    #

    # Label for project selection menu
    @app.callback(
        Output(component_id="repo-menu-label", component_property="children"),
        Input(component_id="project-menu", component_property="value")
    )
    def update_repo_selector_label(project_name): 
        return html.P(f"2. Select a repository from {project_name}: ")
    
    # Options in repository selection menu
    @app.callback(
        [
            Output(component_id="repo-menu", component_property="options"),
            Output(component_id="repo-menu", component_property="value")
        ],
        Input(component_id="project-menu", component_property="value")
    )
    def update_repo_menu(project_name): 
        # Populate a project's repository selection menu
        project_repo_names = repositories[repositories["project"] == project_name]["name"]
        repo_menu_list: list = [{"label": name, "value": name} for name in project_repo_names]
        # This menu defaults to the first repository
        default_menu_item: str = repo_menu_list[0]["value"]
        return repo_menu_list, default_menu_item

    # Parameterise time range slider based on repository activity timeline    
    @app.callback(
        [
            Output("time-range-slider", "marks"),
            Output("time-range-slider", "min"),
            Output("time-range-slider", "max"),
            Output("time-range-slider", "step"),
            Output("time-range-slider", "value")
        ],
        Input(component_id="repo-menu", component_property="value")
    )
    def update_repo_time_slider(repo_name): 
        # Get full range of timestamps from commits and tickets
        repo_commits: pandas.DataFrame = commits[commits["repo_name"] == repo_name]
        repo_tickets: pandas.DataFrame = tickets[tickets["repo_name"] == repo_name]
        all_activities = pandas.concat([repo_commits["committed"], repo_tickets["published"]]).unique()
        start_time = all_activities.min()
        end_time = all_activities.max()

        # Get labelled marks in slider where beginning of years and each 
        # quarter will be labelled
        slider_marks: dict = get_time_range_slider_marks(start_time, end_time)

        # Get min and max values in slider
        start_date: datetime.date = datetime.date(start_time.year, start_time.month, start_time.day)
        end_date: datetime.date = datetime.date(end_time.year, end_time.month, end_time.day)
        # This will create a list from 0 to x, where x is the number of months
        # the end timestamp is after the beginning:
        if month_diff(start_date, end_date) < 1:
            # Handle situation when the repository has less than a month of activity
            months: list = list(range(0, 2))
        else:
            months: list = list(range(0, month_diff(start_date, end_date)))

        slider_min: int = months[0]
        slider_max: int = months[-1] # I.e. the last item in `months`

        # The slider can be dragged in 1-month increments
        slider_step: int = 1

        # Use full timespan for default time slider start/end dates
        slider_value: list = [slider_min, slider_max]

        return slider_marks, slider_min, slider_max, slider_step, slider_value
        
    # Set title to show repository name
    @app.callback(
        Output("repo-title", "children"),
        Input("repo-menu", "value")
    )
    def update_repo_title(repo_name): 
        repo_info: pandas.DataFrame = repositories[
            repositories["name"] == repo_name
        ].reset_index(
            drop=True # This resets the row index to start from 0 which allows
                      # referring to index `[0]` below for `href`
        )
        title: list = html.P(
            [
                dcc.Link(
                    children=str(repo_name),
                    href=str(repo_info["repo_url"][0])
                ),
                str(f" on {repo_info['platform'][0]}")
            ]
        )
        return title

    # Compute: 
    # 1. Number of commits within time slider timespan
    # 2. Commits history plot based on time slider constraints
    @app.callback(
        [
            Output("commits-card", "children"),
            Output("commits-plot", "figure")
        ],
        [
            Input("repo-menu", "value"), 
            Input("time-range-slider", "value")
        ]        
    )
    def draw_commits_plot(repo_name, slider_values): 
        # Get commits for just the specified repository
        repo_commits: pandas.DataFrame = commits[commits["repo_name"] == repo_name]
        # Get the earliest committed timestamp
        repo_start_time = repo_commits["committed"].min()
        # Set start date to the first day of the month of that timestamp
        start_date: datetime.date = datetime.date(repo_start_time.year, repo_start_time.month, 1)
        # Set end date to the number of months after that start date as specified
        # by the time slider
        end_date: datetime.date = add_months(start_date, slider_values[-1] + 1)
        end_date = datetime.date(
            end_date.year,
            end_date.month,
            calendar.monthrange(end_date.year, end_date.month)[1]
        )
        # Change start date to that specified by time slider
        start_date = add_months(start_date, slider_values[0])

        #
        # 1. Get number of commits within timespan
        #

        # Get number of commits within slider-defined timespan
        start_time: datetime.datetime = datetime.datetime(
            start_date.year, 
            start_date.month, 
            1,
            0, 0, 0, 
            tzinfo=datetime.timezone.utc
        )
        end_time: datetime.datetime = datetime.datetime(
            end_date.year, 
            end_date.month, 
            calendar.monthrange(end_date.year, end_date.month)[1],
            23, 59, 59, 
            tzinfo=datetime.timezone.utc
        ) # Set `end_time` to the last day of its month at 23:59:59 UTC
        # Get all commits between `start_time` and `end_time` (inclusive)
        n_commits_df: pandas.DataFrame = repo_commits[
            (repo_commits["committed"] >= start_time) & (repo_commits["committed"] <= end_time)
        ].drop_duplicates(subset="committed") # Drop due to multiple parent commits
        n_commits: int = len(n_commits_df["hash"])

        #
        # 2. Plot monthly commits during timespan
        #

        # Count number of rows per month. The resulting dataframe would have the
        # same values in each row so any one of them could be used in the plot.
        # `drop_duplicates()` because some commits have >1 parents.
        # `freq="1M"` groups `committed` timestamps by month: 
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Grouper.html
        repo_commits_monthly = repo_commits[
            (repo_commits["committed"] >= start_time) & (repo_commits["committed"] <= end_time)
        ].drop_duplicates(
            subset="committed"
        ).groupby(
            pandas.Grouper(key="committed", freq="1M")
        ).count()

        commits_fig = plotly.graph_objects.Figure()
        commits_fig.add_trace(plotly.graph_objects.Bar(
            name="Commits bar plot", 
            x=repo_commits_monthly.index, 
            y=repo_commits_monthly["hash"], 
            xperiod="M1", 
            xperiodalignment="middle"
        ))
        commits_fig.update_layout(
            xaxis_title="Date", 
            yaxis_title="Number of commits"
        )
        # TODO: Making the plot rangeslider default to time slider values is
        # not working.
        # commits_fig.update_xaxes(
        #     rangeslider_visible=True, 
        #     rangeslider_autorange=False,
        #     rangeslider_range=[str(start_date), str(end_date)],
        #     ticklabelmode="period"
        # )
        return str(n_commits), commits_fig
    
    # Compute number of tickets are open/closed during time slider timespan
    @app.callback(
        Output("tickets-card", "children"),
        [
            Input("repo-menu", "value"),
            Input("time-range-slider", "value")
        ]
    )
    def get_n_tickets(repo_name, slider_values):
        # Get tickets for specified repository
        repo_tickets: pandas.DataFrame = tickets[tickets["repo_name"] == repo_name]
        # If there are no tickets, just return 0
        if repo_tickets.empty:
            return str("0/0")
        else: 
            pass
        # Initialise start time to first ticket that was published
        start_time = repo_tickets["published"].min()
        # Initialise start date to the first day of its month
        start_date: datetime.date = datetime.date(
            start_time.year, 
            start_time.month, 
            1
        )
        # Set end date to number of months after start date set by time slider
        end_date: datetime.date = add_months(start_date, slider_values[-1] + 1)
        # Set end time to the final UTC day and moment of its month
        end_time: datetime.datetime = datetime.datetime(
            end_date.year, 
            end_date.month, 
            calendar.monthrange(end_date.year, end_date.month)[1],
            23, 59, 59, 
            tzinfo=datetime.timezone.utc
        )
        # Change start date/time to that specified by time slider
        start_date = add_months(start_date, slider_values[0])
        start_time: datetime.datetime = datetime.datetime(
            start_date.year, 
            start_date.month, 
            1,
            0, 0, 0, 
            tzinfo=datetime.timezone.utc
        )

        # Constrain tickets to within slider-set timespan
        repo_tickets_opened = repo_tickets[
            (repo_tickets["published"] >= start_time) & (repo_tickets["published"] <= end_time)
        ].drop_duplicates(subset="id")
        repo_tickets_resolved = repo_tickets[
            (repo_tickets["resolved"] >= start_time) & (repo_tickets["resolved"] <= end_time)
        ].drop_duplicates(subset="id")
        # Calculate number of tickets opened and resolved during this time
        n_tickets_opened: int = len(repo_tickets_opened["id"])
        n_tickets_resolved: int = len(repo_tickets_resolved["id"])

        # Construct string to show in card
        n_tickets: str = f"{n_tickets_opened}/{n_tickets_resolved}"

        return n_tickets

    # Compute: 
    # 1. Number of users during time slider timespan
    # 2. User activity table based on time slider constraints
    @app.callback(
        [
            Output("contributors-card", "children"), 
            Output("user-activity-table", "children")
        ], 
        [
            Input("repo-menu", "value"), 
            Input("time-range-slider", "value")
        ]
    )
    def make_user_table(repo_name, slider_values): 
        repo_users: pandas.DataFrame = users[users["repo_name"] == repo_name]
        start_time = repo_users["activity_time"].min()
        start_date: datetime.date = datetime.date(
            start_time.year, 
            start_time.month, 
            1
        )
        end_date: datetime.date = add_months(start_date, slider_values[-1] + 1)
        end_time: datetime.datetime = datetime.datetime(
            end_date.year, 
            end_date.month, 
            calendar.monthrange(end_date.year, end_date.month)[1],
            23, 59, 59, 
            tzinfo=datetime.timezone.utc
        )
        # Change start date/time to that specified by time slider
        start_date = add_months(start_date, slider_values[0])
        start_time: datetime.datetime = datetime.datetime(
            start_date.year, 
            start_date.month, 
            1,
            0, 0, 0, 
            tzinfo=datetime.timezone.utc
        )
        
        repo_users = repo_users[
            (repo_users["activity_time"] >= start_time) & (repo_users["activity_time"] <= end_time)
        ]
        
        #
        # 1. Number of users during time slider timespan
        # 

        n_users_df: pandas.DataFrame = repo_users.drop_duplicates(subset="username", inplace=False)
        n_users: int = len(n_users_df["username"])

        #
        # 2. User activity table based on time slider constraints
        # 

        user_commits: pandas.DataFrame = repo_users[
            repo_users["activity_type"] == "commit"
        ].groupby(
            "username", 
            as_index=False
        )["activity_id"].count().sort_values(
            by="activity_id", 
            ascending=False
        )
        user_commits.rename(columns={"activity_id": "commits"}, inplace=True)

        user_tickets: pandas.DataFrame = repo_users[
            repo_users["activity_type"] == "ticket"
        ].groupby(
            "username", 
            as_index=False
        )["activity_id"].count().sort_values(
            by="activity_id", 
            ascending=False
        )
        user_tickets.rename(columns={"activity_id": "tickets"}, inplace=True)

        user_activities: pandas.DataFrame = pandas.merge(
            user_commits, 
            user_tickets, 
            how="outer", 
            on="username"
        ).fillna("0")

        return str(n_users), generate_table(user_activities)
    
    return app