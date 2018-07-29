def plotdata():
    import seaborn as sns
    from bokeh.plotting import figure
    from bokeh.embed import components

    data = sns.load_dataset('tips')
    data2 = data.groupby(['smoker', 'sex']).mean().tip

    p = figure(x_range=['Smoking & Male', 'Smoking & Female', 'Non-Smoking & Male', 'Non-Smoking & Female'], plot_width=800, plot_height=600)
    p.vbar(x=['Smoking & Male', 'Smoking & Female', 'Non-Smoking & Male', 'Non-Smoking & Female'], width=0.01, bottom=0, top=data2, legend='팁')

    return components(p)
