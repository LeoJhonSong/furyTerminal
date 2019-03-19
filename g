#! /bin/sh

# a script to automatically do git add all, git commit and git push

git add .
git commit -m $1
git push