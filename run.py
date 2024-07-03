## Add all required imports here ##
## Eg. 
# import cv2
# import streamlit as st
# import pandas
##
import subprocess
import os
from openai import OpenAI
from pypdf import PdfReader
import streamlit as st

if __name__ == '__main__':
    subprocess.run(["streamlit", "run", "./main.py"])
