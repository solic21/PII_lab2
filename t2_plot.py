import matplotlib.pyplot as plt


def draw_t_1_fuzzy_area(x, mf):
    """
    Draws T1 MF as area
    """
    fig, ax = plt.subplots()
    ax.set_ylabel(r'$\mu$(x)')
    ax.set_xlabel('x')
    ax.set_ylim([0, 1.2])
    ax.plot(x, mf)
    ax.fill_between(x, mf)
    plt.grid(True)
    plt.show()


def draw_t2_fuzzy_set(x, lmf, umf):
    """
    Draws T2 MFs as area
    """
    fig, ax = plt.subplots()
    ax.set_ylabel(r'$\mu$(x)')
    ax.set_xlabel('x')
    ax.set_ylim([0, 1.2])

    ax.fill_between(x, lmf, umf, color="lightblue", edgecolor="b", alpha=.5)
    plt.grid(True)

    plt.show()


def draw_t2_fuzzy_term(x, lmf, umf, title: str):
    """
    Plots the T2 Fuzzy Term.
    """
    pass


def draw_word(x, word: str, word_model):
    """
    Draw the word (term)
    """
    fig, ax = plt.subplots()
    ax.set_ylabel(r'$\mu$(x)')
    ax.set_xlabel('x')
    ax.set_ylim([0, 1.2])
    lmf, umf = word_model['lmf'], word_model['umf']
    ax.fill_between(x, lmf, umf, color="lightblue", edgecolor="b", alpha=.5)

    plt.grid(True)
    plt.show()


def draw_lv(lv, is_word = False):
    """
    Draw the linguistic variable
    """
    fig, ax = plt.subplots()
    ax.set_ylabel(r'$\mu$(x)')
    ax.set_xlabel('x')
    ax.set_ylim([0, 1.2])
    for term in lv['words' if is_word else 'terms'].values():
        x = lv['U']
        lmf, umf = term['lmf'], term['umf']
        ax.set_ylim([0, 1.2])
        ax.fill_between(x, lmf, umf, color="lightblue", edgecolor="b", alpha=.5)

    plt.grid(True)
    plt.title(lv['name'])
    plt.show()

