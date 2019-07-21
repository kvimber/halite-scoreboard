from flask import Flask, escape, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/scores')
def score():
    import os
    print("cwd: %s" % os.getcwd())

    # rank_filepath = "../../Halite-III/tools/manager/ranks/current.log"
    # rank_lines = rank_file_local(rank_filepath)

    rank_url = "https://raw.githubusercontent.com/kvimber/halite-scores/master/report.txt"
    rank_lines = rank_file_http(rank_url)

    ranks = parse_rank_file(rank_lines)
    return render_template("index.html", ranks=ranks)

def rank_file_local(filepath):
    rank_file = open(filepath, 'r')
    rank_lines = rank_file.readlines()
    rank_file.close()
    return rank_lines

def rank_file_http(file_url):
    import requests
    response = requests.get(file_url)
    if response.status_code != 200:
        msg = "scoreboard.py rank_file_url could not get rank file:"
        msg += ("\n- URL: %s" % file_url)
        msg += ("\n- status: %d" % response.status_code)
        msg += ("\n- response: %d" % response)
        raise RuntimeError(msg)
    rank_lines = response.text.split("\n")
    print("rank lines from URL: %s" % file_url)
    print(response.text)
    return rank_lines

def parse_rank_file(rank_lines):

    ranks = []
    for line in rank_lines:
        if line.startswith("Using") or line.strip() == "" or line.startswith("name"):
            continue

        line_parts = line.split()
        print("parse_rank_file:line_parts:%s" % line_parts)
        last_seen = "%s %s" % (line_parts[1], line_parts[2])
        ranks.append({
            "name":      line_parts[0],
            "last_seen": last_seen,
            "rank":      line_parts[3],
            "skill":     line_parts[4],
            "mu":        line_parts[5],
            "sigma":     line_parts[6],
            "ngames":    line_parts[7],
            "active":    line_parts[8],
            "path":      line_parts[9],
        })
    return ranks
