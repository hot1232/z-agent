#!/usr/bin/env python
import os

def get():
    return os.uname()[0]

if __name__ == "__main__":
    print os.uname()[0]