#!/bin/bash
python3 -m venv venv
source venv/bin/activate

pip install scapy rich
python3 __main__.py
