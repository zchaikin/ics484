import pandas as pd
import numpy as np
import re


def sep_by_brands(df):
    amd = df[df['ALL VIDEO CARDS'].str.contains('^AMD.*') == True]
    intel = df[df['ALL VIDEO CARDS'].str.contains('^Intel.*') == True]
    nvidia = df[df['ALL VIDEO CARDS'].str.contains('^NVIDIA.*') == True]
    return amd, intel, nvidia


if __name__ == '__main__':
    data = pd.read_csv('data/Steam Hardware & Software Survey_ October 2022 - Sheet1.csv')
    amd, intel, nvidia = sep_by_brands(data)

