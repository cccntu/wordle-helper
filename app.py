# %%
import inspect
import random

import gradio as gr
import pandas as pd

url = "words.txt"
# "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
df = pd.read_table(url, header=None)
words = df[0].astype(str).tolist()
words = [x.lower() for x in words if len(x) == 5 and x.isalpha()]


def filter_one_word(
    w,
    no="",
    yes="",
    no1="",
    no2="",
    no3="",
    no4="",
    no5="",
    yes1="",
    yes2="",
    yes3="",
    yes4="",
    yes5="",
):
    for c in w:
        if c in no:
            return False
    for c in yes:
        if c not in w:
            return False
    nos = [no1, no2, no3, no4, no5]
    for c, n in zip(w, nos):
        if c in n:
            return False
    yeses = [yes1, yes2, yes3, yes4, yes5]
    for c, n in zip(w, yeses):
        if n and c != n:
            return False
    return True


def process_args(chars):
    cs = set([c for c in chars.lower() if c.isalpha()])
    return "".join(list(cs))


def main(
    no="",
    yes="",
    no1="",
    no2="",
    no3="",
    no4="",
    no5="",
    yes1="",
    yes2="",
    yes3="",
    yes4="",
    yes5="",
):
    no, yes, no1, no2, no3, no4, no5, yes1, yes2, yes3, yes4, yes5 = map(
        process_args, [no, yes, no1, no2, no3, no4, no5, yes1, yes2, yes3, yes4, yes5]
    )
    candidates = [
        w
        for w in words
        if filter_one_word(
            w, no, yes, no1, no2, no3, no4, no5, yes1, yes2, yes3, yes4, yes5
        )
    ]
    return str(len(candidates)), "\n".join(
        random.sample(candidates, (min(10, len(candidates))))
    )


args = inspect.getfullargspec(main)
iface = gr.Interface(
    fn=main,
    inputs=[gr.inputs.Textbox(label=n) for n in args.args],
    outputs=["text", "text"],
).launch()
