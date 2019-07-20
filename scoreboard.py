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
    rank_filepath = "../../Halite-III/tools/manager/ranks/current.log"
    ranks = parse_rank_file(rank_filepath)
    return render_template("index.html", ranks=ranks)

def parse_rank_file(filepath):
    rank_file = open(filepath, 'r')
    rank_lines = rank_file.readlines()
    rank_file.close()

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
