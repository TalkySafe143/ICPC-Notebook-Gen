import os
from collections import defaultdict

def getAllGitIgnores():
    vis = defaultdict(bool)
    with open(os.getcwd()+"/.gitignore") as file:
        lines = [x.split("\n")[0] for x in file.readlines()]
        for line in lines:
            vis[line]=True
    vis[".git"]=True
    vis[".gitignore"]=True
    #vis[os.getcwd().split("/")[-1]]=True
    return vis
