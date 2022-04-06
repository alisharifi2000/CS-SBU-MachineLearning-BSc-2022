preprocess = []

def apply_process(df):
    for p in preprocess:
        df[p[0]] = df[p[0]].apply(lambda x: p[1](x, p[2]))