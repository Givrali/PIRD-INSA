#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:24:18 2024
Last modified on Thu Dec 05 08:00:13 2024

@author: cghiaus

ELECTRE Tri-B

In ELECTRE Tri-B each category is characterized
by two reference profiles corresponding to the limits of this category.
In ELECTRE Tri-C each category is characterized by one
reference profile only, being representative of the category
[Corente et al; 2016].

References

Almeida-Dias, J., Figueira, J. R., & Roy, B. (2010). Electre Tri-C: A multiple
criteria sorting method based on characteristic reference actions.
European Journal of Operational Research, 204(3), 565-580.
https://doi.org/10.1016/j.ejor.2009.10.018
https://hal.science/hal-00907583v1/document

Mousseau, V., Slowinski, R., & Zielniewicz, P. (1999). ELECTRE TRI 2.0
Methodological guide and user’s manual. Universite Paris Dauphine,
Document du LAMSADE, 111, 263-275.
https://www.lamsade.dauphine.fr/mcda/biblio/PDF/mous3docl99.pdf

Mousseau, V., Slowinski, R., & Zielniewicz, P. (2000). A user-oriented
implementation of the ELECTRE-TRI method integrating preference elicitation
support. Computers & operations research, 27(7-8), 757-777.
https://doi.org/10.1016/S0305-0548(99)00117-3
https://www.lamsade.dauphine.fr/mcda/biblio/PDF/mous3cor00.pdf

J. Almeida-Dias , J. R. Figueira , B. Roy (2010) A multiple criteria sorting
method defining each category by several characteristic reference actions:
The Electre Tri-nC method, Cahier du LAMSADE 294, Université Paris Daufine,
CNRS
https://hal.science/hal-01511223/document

Corrente, S., Greco, S., & Słowiński, R. (2016). Multiple criteria hierarchy
process for ELECTRE Tri methods. European Journal of Operational Research,
252(1), 191-203.
https://doi.org/10.1016/j.ejor.2015.12.053
https://pure.port.ac.uk/ws/portalfiles/portal/5001301/GRECO_Multiple_Criteria_Hierarchy_Process_for_ELECTRE_Tri_methods_Postprint.pdf

Figueira, J. R., Mousseau, V., & Roy, B. (2016). ELECTRE methods. Multiple
criteria decision analysis: State of the art surveys, 155-185.
https://www.lamsade.dauphine.fr/mcda/biblio/PDF/JFVMBR2005.pdf

Corrente, S., Greco, S., & Słowiński, R. (2016). Multiple criteria hierarchy
process for ELECTRE Tri methods. European Journal of Operational Research,
252(1), 191-203.
https://doi.org/10.1016/j.ejor.2015.12.053
https://pure.port.ac.uk/ws/portalfiles/portal/5001301/GRECO_Multiple_Criteria_Hierarchy_Process_for_ELECTRE_Tri_methods_Postprint.pdf

Baseer, M., Ghiaus, C., Viala, R., Gauthier, N., & Daniel, S. (2023).
pELECTRE-Tri: Probabilistic ELECTRE-Tri Method—Application for the
Energy Renovation of Buildings. Energies, 16(14), 5296.
https://doi.org/10.3390/en16145296


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# pd.set_option('future.no_silent_downcasting', True) # Modification


def read_electre_tri_base(filename):
    """Reads the data of the ELECTRE Tri problem.

    Args:
        filename (str): Name of .csv file containing the data of the problem.

    Returns:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        B (DataFrame): Base profiles in ascending order for criteria (columns).

        T (DataFrame): Indifference (q), preference (p) and veto (v) thresholds
        for each criterion (column).

        w (Series): Weight for each criterion.

    Example
    -------

    >>> data_file = './data/simple_example.csv'
    >>> A, B, T, w = read_electre_tri_base(data_file)
    >>> ...

    where `simple_example.csv` is:


    .. code-block:: none

        type, profile, c1, c2
        A,    a1,     8.5, 18
        A,    a2,      14, 16
        A,    a3,       5, 27
        B,    b1,      10, 15
        B,    b2,      15, 20
        T,     q,       1, 2
        T,     p,       2, 4
        T,     v,       4, 8
        w,      ,     0.7, 0.3
    """

    # Read the CSV file
    df = pd.read_csv(filename, header=0)

    # Extract A
    A = df[df.iloc[:, 0] == 'A'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'A'].iloc[:, 1])
    A.index.name = None

    # Extract B
    B = df[df.iloc[:, 0] == 'B'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'B'].iloc[:, 1])
    B.index.name = None

    # Extract T
    T = df[df.iloc[:, 0] == 'T'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'T'].iloc[:, 1])
    T.index.name = None

    # Extract w
    w = pd.Series(df[df.iloc[:, 0] == 'w'].iloc[0, 2:].dropna())
    w.name = None  # Remove the name from the Series

    return A, B, T, w


def read_pelectre_tri_base(filename):
    """Reads the data of the pELECTRE Tri problem.

    Args:
        filename (str): Name of .csv file containing the data of the problem.

    Returns:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        S (DataFrame): Standard deviation of performance matrix
        of alternatives (rows) for criteria (columns).

        B (DataFrame): Base profiles in ascending order for criteria (columns).

        T (DataFrame): Indifference (q), preference (p) and veto (v) thresholds
        for each criterion (column).

        w (Series): Weight for each criterion.

    Example
    -------

    >>> data_file = './data/simple_example_std.csv'
    >>> A, S, B, T, w = read_pelectre_tri_base(data_file)
    >>> ...

    where `simple_example.csv` is:


    .. code-block:: none

        type, profile, c1, c2
        A,    a1,     8.5, 18
        A,    a2,      14, 16
        A,    a3,       5, 27
        S,    a1,    0.85, 1.8
        S,    a2,     1.4, 1.6
        S,    a3,     0.5, 2.7
        B,    b1,      10, 15
        B,    b2,      15, 20
        T,     q,       1, 2
        T,     p,       2, 4
        T,     v,       4, 8
        w,      ,     0.7, 0.3
    """

    # Read the CSV file
    df = pd.read_csv(filename, header=0)

    # Extract A
    A = df[df.iloc[:, 0] == 'A'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'A'].iloc[:, 1])
    A.index.name = None

    # Extract S
    S = df[df.iloc[:, 0] == 'S'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'S'].iloc[:, 1])
    S.index.name = None

    # Extract B
    B = df[df.iloc[:, 0] == 'B'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'B'].iloc[:, 1])
    B.index.name = None

    # Extract T
    T = df[df.iloc[:, 0] == 'T'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'T'].iloc[:, 1])
    T.index.name = None

    # Extract w
    w = pd.Series(df[df.iloc[:, 0] == 'w'].iloc[0, 2:].dropna())
    w.name = None  # Remove the name from the Series

    return A, S, B, T, w


def read_electre_tri_level(filename):
    """ Reads the data for worst and best possible base profiles.

    Args:
        filename (str): Name of .csv file containing the data of the problem.

    Returns:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        L (DataFrame): Worst and best base profiles in ascending order for
        criteria (columns).

        w (Series): Weight for each criterion.

    """

    # Read the CSV file
    df = pd.read_csv(filename, header=0)

    # Extract A
    A = df[df.iloc[:, 0] == 'A'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'A'].iloc[:, 1])
    A.index.name = None

    # Extract L
    L = df[df.iloc[:, 0] == 'L'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'L'].iloc[:, 1])
    L.index.name = None

    # Extract w
    w = pd.Series(df[df.iloc[:, 0] == 'w'].iloc[0, 2:].dropna())
    w.name = None  # Remove the name from the Series

    return A, L, w


def read_pelectre_tri_level(filename):
    """ Reads the data for worst and best possible base profiles.

    Args:
        filename (str): Name of .csv file containing the data of the problem.

    Returns:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        S (DataFrame): Standard deviation of performance matrix
        of alternatives (rows) for criteria (columns).

        L (DataFrame): Worst and best base profiles in ascending order for
        criteria (columns).

        w (Series): Weight for each criterion.

    """

    # Read the CSV file
    df = pd.read_csv(filename, header=0)

    # Extract A
    A = df[df.iloc[:, 0] == 'A'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'A'].iloc[:, 1])
    A.index.name = None

    # Extract S
    S = df[df.iloc[:, 0] == 'S'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'S'].iloc[:, 1])
    S.index.name = None

    # Extract L
    L = df[df.iloc[:, 0] == 'L'].iloc[:, 2:].set_index(
        df[df.iloc[:, 0] == 'L'].iloc[:, 1])
    L.index.name = None

    # Extract w
    w = pd.Series(df[df.iloc[:, 0] == 'w'].iloc[0, 2:].dropna())
    w.name = None  # Remove the name from the Series

    return A, S, L, w


def base_profile(L, n_base_profile=4):
    """Base profiles for each criterion.

    The range between the best and the worst possible levels `L` is divided
    in equidistant `n_base_profile` resulting in
    `n_base_profile + 1` categories.

    Args:
        L (DataFrame): Worst and best possible base profiles in
        ascending order for criteria (columns).

        n_base_profile (int, optional): Number of base profiles. Defaults to 4.

    Returns:
        B (DataFrame): Base profiles in ascending order for criteria (columns).

    """

    # Calculate the range for each column
    ranges = L.loc['best'] - L.loc['worst']

    # Create the percentages for the profiles
    percentages = np.linspace(0, 1, n_base_profile + 2)[1:-1]

    # Create the base profiles
    B = pd.DataFrame({
        col: [L.loc['worst', col] + p * ranges[col] for p in percentages]
        for col in L.columns
    }, index=[f'b{i+1}' for i in range(len(percentages))])

    return B


def threshold(B, threshold_percent=[0.10, 0.25, 0.50]):
    """
    Indifference (q), preference (p), and veto (v) thresholds as a percentage
    of the range between two consecutive equidistant base profiles.

    Args:
        B (DataFrame): Base profiles in ascending order for criteria (columns).

        threshold_percent (list, optional): Values of indifference (q),
        preference (p) and veto (v) thresholds as a percentage of
        the range between two consecutive equidistant base profiles.
        Defaults to [0.10, 0.25, 0.50].

    Returns:
        T (DataFrame): Indifference (q), preference (p) and veto (v)
        thresholds for each criterion (column).

    """

    T = pd.DataFrame(index=['q', 'p', 'v'], columns=B.columns)

    for col in B.columns:
        # Calculate the differences between consecutive rows in the column
        differences = B[col].diff().dropna()

        # Calculate thresholds for q, p, and v based on the percentages
        T.at['q', col] = threshold_percent[0] * differences.mean()
        T.at['p', col] = threshold_percent[1] * differences.mean()
        T.at['v', col] = threshold_percent[2] * differences.mean()

        T = T.astype(float)

    return T


def partial_concordance(A, B, T):
    """Partial concordance between profiles `a` and `b` for each criterion `c`.

    Truth value (between 0 and 1) of the concordance (i.e. agreement)
    with the statement:
        *a outranks b for criterion c*
    where "outranks" means "is at least as good as".

    In ELECTRE Tri, two partial concordances are calculated:
        - between alternatives a and base profiles b;
        - between base profiles b and alternatives a.


    Args:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        B (DataFrame): Base profiles in ascending order for criteria (columns).

        T (DataFrame): Indifference (q), preference (p) and veto (v) thresholds
        for each criterion (columns).

    Returns:
        con_ab (DataFrame): Partial (or local) concordance between
        alternatives `a` and base profiles `b` for each criterion `c`.
        con_ab has `criteria` and `base` as indexes and
        `alternatives` as columns.

        con_ba (DataFrame):  Partial (or local) concordance between
        base profiles `b` and alternatives `a` for each criterion `c`.
        con_ba has `criteria` and `base` as indexes and
        `alternatives` as columns..

    Let's note:
        - a : value of alternative a for a given criterion c
        - b : value of base b for the same criterion c
        - q : indifference threshold of b for criterion c
        - p : preference threshold of b for criterion c

    Partial concordance between a and b, con_ab, is:
        - = 1, if a >= b - q
        - = 0, if a < b - p
        - = (a - b + p) / (p - q), otherwise

    Partial concordance between b and a, con_ab, is:
        - = 1, if b >= a - q
        - = 0, if b < a - p
        - = (b - a + p) / (p - q), otherwise


    Example
    -------

    For `data_file.csv`:

    +---+----+-----+----+
    |   |    | c1  | c2 |
    +===+====+=====+====+
    | A | a1 | 8.5 | 18 |
    +---+----+-----+----+
    | A | a2 | 14  | 16 |
    +---+----+-----+----+
    | A | a3 |  5  | 27 |
    +---+----+-----+----+
    | B | b1 | 10  | 15 |
    +---+----+-----+----+
    | B | b2 | 15  | 20 |
    +---+----+-----+----+
    | T | q  |  1  |  2 |
    +---+----+-----+----+
    | T | p  |  2  |  4 |
    +---+----+-----+----+
    | T | v  |  4  |  8 |
    +---+----+-----+----+
    | w |    | 0.7 | 0.3|
    +---+----+-----+----+

    .. code-block:: none

        type, profile, c1, c2
        A,    a1,     8.5, 18
        A,    a2,      14, 16
        A,    a3,       5, 27
        B,    b1,      10, 15
        B,    b2,      15, 20
        T,     q,       1, 2
        T,     p,       2, 4
        T,     v,       4, 8
        w,      ,     0.7, 0.3

    Partial concordance between alternatives and base profiles, `con_ab`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 0.5 |  1  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  1  | 0   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 1   |  1  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 1   |  0  | 1   |
    +----------+------+-----+-----+-----+

    Consider column a1:

    con_ab[(c1, b1), a1] = 0.5 means that it is partly true that a1 outranks b1
    on criterion c1, i.e., on c1, a1 is between indifference (b1 - q ) and
    preference (b1 - p) boundaries of b1.

    con_ab[(c1, b2), a1] = 0 means that it not true that a1 outranks b2
    on criterion c1, i.e., on c1, a1 is bellow preference
    boundary of b1, b1 - p.

    con_ab[(c2, b2), a1] = 1 means that it true that a1 outranks b1
    on criterion c2, i.e., on c2, a1 is above indifference
    boundary of b1, b1 - q.


    Partial concordance between base profiles and alternatives, `con_ba`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 1   |  0  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 1   |  1  | 1   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 0.5 |  1  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 1   |  1  | 0   |
    +----------+------+-----+-----+-----+

    Consider row (c2, b1):

    con_ab[(c2, b1), a1] = 0.5 means that it is partly true that b1 outranks a1
    on criterion c2, i.e., on c1, b1 is between indifference (a1 - q ) and
    preference (a1 - p) boundaries of a1.

    con_ab[(c2, b1), a2] = 1 means that it true that b1 outranks a2
    on criterion c2, i.e., on c2, b1 is above indifference
    boundary of a1, a1 - q.

    con_ab[(c2, b1), a3] = 0 means that it not true that b1 outranks a3
    on criterion c2, i.e., on c2, b1 is bellow preference
    boundary of a3, a3 - p.

    """

    # Initialize the result DataFrame
    index = pd.MultiIndex.from_product([A.columns, B.index],
                                       names=['criteria', 'base'])
    con_ab = pd.DataFrame(index=index, columns=A.index)
    con_ba = pd.DataFrame(index=index, columns=A.index)

    for criterion in A.columns:
        for base in B.index:
            for alternative in A.index:
                a = A.loc[alternative, criterion]
                b = B.loc[base, criterion]
                q = T.loc['q', criterion]
                p = T.loc['p', criterion]

                # partial concordance (a_i, b_k) for c_j
                if a >= b - q:
                    con = 1
                elif a < b - p:
                    con = 0
                else:
                    con = (a - b + p) / (p - q)

                con_ab.loc[(criterion, base), alternative] = con

                # partial concordance (b_k, a_i) for c_j
                if b >= a - q:
                    con = 1
                elif b < a - p:
                    con = 0
                else:
                    con = (b - a + p) / (p - q)

                con_ba.loc[(criterion, base), alternative] = con

    # Replace NaN with 0 and round to 3 decimal places
    con_ab = con_ab.fillna(0).round(3)
    con_ba = con_ba.fillna(0).round(3)

    return con_ab, con_ba


def discordance(A, B, T):
    """Partial discordance between profiles `a` and `b` for each criterion `c`.

    Truth value (between 0 and 1) of the discordance (i.e. disagreement)
    with the statement:
        *a outranks b for criterion c*
    where "outranks" means "is at least as good as".


    Args:
        A (DataFrame): Performance matrix of alternatives (rows) for
        criteria (columns).

        B (DataFrame): Base profiles in ascending order for criteria (columns).

        T (DataFrame): Indifference (q), preference (p) and veto (v) thresholds
        for each criterion (columns).

    Returns:
        dis_ab (DataFrame): Partial (or local) discordance between
        alternatives `a` and base profiles `b` for each criterion `c`. d_ab
        has `criteria` and `base` as indexes and `alternatives` as columns.

        dis_ba (DataFrame): Partial (or local) discordance between
        base profiles `b` and alternatives `a` for each criterion `c`. d_ba
        has `criteria` and `base` as indexes and `alternatives` as columns.

    Let's note:
        - a : value of alternative a for a given criterion c
        - b : value of base b for the same criterion c
        - q : indifference threshold of b for criterion c
        - p : preference threshold of b for criterion c

    Partial concordance between a and b, con_ab, is:
        - = 1, if a >= b - q
        - = 0, if a < b - p
        - = (a - b + p) / (p - q), otherwise

    Partial concordance between b and a, con_ab, is:
        - = 1, if b >= a - q
        - = 0, if b < a - p
        - = (b - a + p) / (p - q), otherwise

    Example
    -------

    For `data_file.csv`:

    +---+----+-----+----+
    |   |    | c1  | c2 |
    +===+====+=====+====+
    | A | a1 | 8.5 | 18 |
    +---+----+-----+----+
    | A | a2 | 14  | 16 |
    +---+----+-----+----+
    | A | a3 |  5  | 25 |
    +---+----+-----+----+
    | B | b1 | 10  | 15 |
    +---+----+-----+----+
    | B | b2 | 15  | 20 |
    +---+----+-----+----+
    | T | q  |  1  |  2 |
    +---+----+-----+----+
    | T | p  |  2  |  4 |
    +---+----+-----+----+
    | T | v  |  4  |  8 |
    +---+----+-----+----+
    | w |    | 0.7 | 0.3|
    +---+----+-----+----+

    .. code-block:: none

        type, profile, c1, c2
        A,    a1,     8.5, 18
        A,    a2,      14, 16
        A,    a3,       5, 27
        B,    b1,      10, 15
        B,    b2,      15, 20
        T,     q,       1, 2
        T,     p,       2, 4
        T,     v,       4, 8
        w,      ,     0.7, 0.3

    Partial discordance between alternatives and base profiles, `dis_ab`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 0   |  0  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 1   |  0  | 1   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 0   |  0  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  0  | 0   |
    +----------+------+-----+-----+-----+

    Consider column a1:

    dis_ab[(c1, b1), a1] = 0 means that it not true that a1 is worse than b1
    on criterion c1, i.e., on c1, a1 is above preference
    boundary of b1, b1 - p.

    con_ab[(c1, b2), a1] = 1 means that it true that a1 is worse that b2
    on criterion c1, i.e., on c1, a1 is bellow indifference
    boundary of b1, b1 - v

    Partial discordance between base profiles and alternatives, `dis_ba`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 0   |  1  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  0  | 0   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 0   |  0  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  0  | 0.75|
    +----------+------+-----+-----+-----+

    Consider row (c2, b2):

    dis_ba[(c2, b2), a3] = 0 means that it not true that b2 is worse than a3
    on criterion c2, i.e., on c2, b2 is above preference
    boundary of a3, a3 - p.

    dis_ba[(c2, b2), a3] = 0.25 means that it is partly true that b2
    is worse than a1 on criterion c2,
    i.e., on c2, b2 is between preferrence (a1 - p ) and
    veto (a1 - v) boundaries of a1.

    """

    # Initialize the result DataFrame
    index = pd.MultiIndex.from_product([A.columns, B.index],
                                       names=['criteria', 'base'])
    dis_ab = pd.DataFrame(index=index, columns=A.index)
    dis_ba = pd.DataFrame(index=index, columns=A.index)

    for criterion in A.columns:
        for base in B.index:
            for alternative in A.index:
                a = A.loc[alternative, criterion]
                b = B.loc[base, criterion]
                p = T.loc['p', criterion]
                v = T.loc['v', criterion]

                # Calculate d_j(a_i, b_k)
                # partial discordance (a_i, b_k) for c_j
                if a >= b - p:
                    dis = 0
                elif a < b - v:
                    dis = 1
                else:
                    dis = (p - b + a) / (p - v)

                dis_ab.loc[(criterion, base), alternative] = dis

                # partial concordance (b_k, a_i) for c_j
                if b >= a - p:
                    dis = 0
                elif b <= a - v:
                    dis = 1
                else:
                    dis = (p - a + b) / (p - v)

                dis_ba.loc[(criterion, base), alternative] = dis

    # Replace NaN with 0 and round to 3 decimal places
    dis_ab = dis_ab.fillna(0).round(3)
    dis_ba = dis_ba.fillna(0).round(3)

    return dis_ab, dis_ba


def global_concordance(c, w):
    """Global concordance between profiles `a` and `b`.

    Truth value (berween 0 and 1) of the statement:
        *a outranks b globlly, i.e. for all criteria*
    where "outranks" means "is at least as good as".


    Args:
        c (DataFrame): Partial (or local) concordance between
        two profiles (a, b) for all criteria.

        w (Series): Weights of criteria.

    Returns:
        C (DataFrame): Global concordance between two profiles.

    The global concordance index is the sum of weighted partial concordances
    divided by the sum of the weights.

    Example
    -------
    Given partial concordance between alternatives and base profiles, `c_ab`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 0.5 |  1  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  1  | 0   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 1   |  1  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 1   |  0  | 1   |
    +----------+------+-----+-----+-----+

    and the weights w:

    +---+----+-----+----+
    |   |    | c1  | c2 |
    +===+====+=====+====+
    | w |    | 0.7 | 0.3|
    +---+----+-----+----+

    the global concordance C_ab is:

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    | 0.65 | 1.0  | 0.3  |
    +---------+------+------+------+
    |   b2    | 0.3  | 0.7  | 0.3  |
    +---------+------+------+------+

    C[b1, a1] = (0.7 * 0.5 + 0.3 * 1) = 0.65

    """
    # Normalize weights
    w_normalized = w / w.sum()

    # Get unique base values
    base_values = c.index.get_level_values('base').unique()

    # Initialize the result DataFrame
    C = pd.DataFrame(index=base_values, columns=c.columns)

    for base in base_values:
        # Step 1: Calculate weighted concordance for each base
        c_base = c.xs(base, level='base')
        weighted_c = c_base.mul(w_normalized, axis=0)

        # Step 2: Sum the columns to get global concordance
        global_c = weighted_c.sum(axis=0)

        # Assign the results to the corresponding row in C
        C.loc[base] = global_c
    return C


def credibility_index(C, d):
    """Credibility of the assertion "a outranks b".

    Credibility index σ(a,b) corresponds to the concordance
    index C(a,b) weakened by discorcdances d(a, b):

        When no criterion shows strong opposition (discordance) to the
        outranking relation, the credibility index is equal to the global
        concordance.

        When a discordant criterion opposes a veto to the assertion
        ”a outranks b" (i.e. discordance is 1), then credibility index σ(a,b)
        becomes null (the assertion ”a outranks b" is not credible at all).

        When one or more criteria strongly oppose the outranking relation
        (i.e., their discordance exceeds the global concordance),
        the credibility index is reduced by multiplying the global concordance
        by a factor derived from the discordances that exceed the global
        concordance.
        The formula for this correction involves a product of terms,
        each representing the effect of a discordant criterion.

    This approach ensures that strong opposition on even a single criterion
    can significantly reduce the credibility of the outranking relation,
    reflecting the non-compensatory nature of ELECTRE methods.

    The credibility index provides a nuanced measure of
    the strength of the outranking relation by taking into account
    performance on both supporting and opposing criteria.

    Args:
        C (DataFrame): Global concordance.

        d (DataFrame): Discordance.

    Returns:
        sigma (DataFrame): Credibility index.

    Example
    -------

    Global concordance `C_ba`:

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    | 0.85 | 0.3  | 0.7  |
    +---------+------+------+------+
    |   b2    | 1.0  | 1.0  | 0.7  |
    +---------+------+------+------+

    Discordance between base profiles and alternatives, `d_ba`:

    +----------+------+-----+-----+-----+
    |          |      | a1  | a2  | a3  |
    +==========+======+=====+=====+=====+
    | criteria | base |     |     |     |
    +----------+------+-----+-----+-----+
    | c1       | b1   | 0   |  1  | 0   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  0  | 0   |
    +----------+------+-----+-----+-----+
    | c2       | b1   | 0   |  0  | 1   |
    +----------+------+-----+-----+-----+
    |          | b2   | 0   |  0  | 0.75|
    +----------+------+-----+-----+-----+

    Obtained credibility index `sigma_ba`:

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    | 0.85 |  0   |  0   |
    +---------+------+------+------+
    |   b2    |  1   |  1   | 0.583|
    +---------+------+------+------+

    sigma_ba[b1, a1] = C_ba[b1, a1] because d_ba[b1, a1] = 0.

    sigma_ba[b1, a2] = C_ba[b1, a2] because d_ba[b1, a1] = 1.

    sigma_ba[b2, a3] =

    C_ba[b2, a3] * (1 - d_ba[(c2, b2), a3]) /  (1 - C_ba[b2, a3]) =

    0.7 * (1 - 0.75)/(1 - 0.7) = 0.583

    because d_ba[(c2, b2), a3] = 0.8 > C_ba[b2, a3] = 0.7

    and the other dscordances are 0 or smaller than the global concordances.

    """

    # Initialize the result DataFrame with the same structure as C
    sigma = pd.DataFrame(index=C.index, columns=C.columns)

    for base in C.index:
        for alternative in C.columns:
            C_value = C.loc[base, alternative]

            # Get discordance values for this base and alternative
            d_values = d.loc[(slice(None), base), alternative]

            # Identify criteria where discordance exceeds global concordance
            F = d_values[d_values > C_value].index.get_level_values('criteria')

            if len(F) == 0:
                # If no discordance exceeds global concordance,
                # credibility equals global concordance
                sigma.loc[base, alternative] = C_value
            else:
                # Calculate the product term for discordance that exceeds
                # the gobal concordance
                product_term = np.prod(
                    [(1 - d.loc[(criterion, base), alternative]
                      ) / (1 - C_value)
                     for criterion in F])

                # Calculate credibility index as corrected concordance
                sigma.loc[base, alternative] = C_value * product_term

    sigma = sigma.round(4)  # Round to 4 decimal places for readability
    return sigma


def outrank(sigma_ab, sigma_ba, credibility_threshold):
    """Preference relation between alternatives and base profiles.

    Four outranking (preference) relations are defined:

    - σ(a,b) < λ and σ(b,a) ≥ λ  ⇒ a I b, "a is indifferent to b"
    - σ(a,b) ≥ λ and σ(b,a) ≥ λ  ⇒ a ≻ b, "a is preferred to b"
    - σ(a,b) < λ and σ(b,a) < λ  ⇒ a ≺ b, "a is not preferred to b"
    - σ(a,b) ≥ λ and σ(b,a) < λ  ⇒ a R b, "a is incomparable with b"

        where λ is a cutting level, i.e. the smallest value  of the
        credibility index compatible with the
        assertion ”a outranks b", i.e., σ(a, b) ≥ λ ⇒ a > b.

    a ≻ b, "a outranks b", i.e. "a is as least as good as b", means that a is
    preferred to b.

    a ≺ b, "a is not preferred to b", i.e. "a is not as least as good as b",
    means that a is not preferred to b.

    a I b, "a is indifferent to b" means that the performances of
    the alternative a and of the base profile b are considered equivalent
    or close enough that no clear preference can be established between them.

    a R b, "a is incomparable with b" means that there is not enough evidence
    to estabish preference or indifference between profiles. This is typically
    the case when an alternative a outranks the base profile b on some criteria
    and the base profile b outranks the alternative a on other criteria.

    Args:
        sigma_ab (DataFrame): Credibility index that alternative a outranks
        base profile b.

        sigma_ba (DataFrame): Credibility index that base profile b ouranks
        alternative a.

        credibility_threshold (float): Credibility threshold is a
        minimum degree of credibility index that is considered necessary
        to validate the statement "alternative a outranks base profile b".
        It takes a value within the range [0.5, 1], typically 0.75.

    Returns:
        outranking (DataFrame): Preference relations: ≻, ≺, I, R between
        base profiles (rows) and alternatives (columns).

    Example
    -------

    credibility index `sigma_ab`:

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    | 0.65 |  1   |  0   |
    +---------+------+------+------+
    |   b2    |  0   |  0.7 | 0    |
    +---------+------+------+------+

    credibility index `sigma_ba`:

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    | 0.85 |  0   |  0   |
    +---------+------+------+------+
    |   b2    |  1   |  1   | 0.583|
    +---------+------+------+------+

    credibility_threshold = 0.7

    outranking

    +---------+------+------+------+
    |         |  a1  |  a2  |  a3  |
    +=========+======+======+======+
    |  base   |      |      |      |
    +---------+------+------+------+
    |   b1    |   ≻  |  ≺   |  R   |
    +---------+------+------+------+
    |   b2    |  ≻   |  I   |  R   |
    +---------+------+------+------+

    """

    # Initialize the result DataFrame with the same structure as sigma_ab
    outranking = pd.DataFrame(index=sigma_ab.index, columns=sigma_ab.columns)

    for base in sigma_ab.index:
        for alternative in sigma_ab.columns:
            s_ab = sigma_ab.loc[base, alternative]
            s_ba = sigma_ba.loc[base, alternative]
            ct = credibility_threshold

            if s_ab >= ct and s_ba >= ct:
                outranking.loc[base, alternative] = 'I'  # a indifferent to b
            elif (s_ab >= ct and s_ba < ct):
                outranking.loc[base, alternative] = '≺'  # a preferred to b
            elif s_ab < ct and s_ba >= ct:
                outranking.loc[base, alternative] = '≻'  # a not preferred to b
            else:
                outranking.loc[base, alternative] = 'R'  # a incomparable to b

    return outranking


def classify(outranking):
    """Optimistic and pessimistic classification.

    These classification procedures are used to assign
    alternatives to ordered categories separated by base profiles.
    They utilize outranking relations:
         - preferred "≻"
         - not preferred "≺"
         - indifferent "I"
         - incomparable "R"

    between the alternatives and the base profiles:

        -The optimistic procedure increases the level of base profiles till
        the lowest base profile which is "preferred" to alternative (b ≻ a)
        is found.
        The alternative is assigned to the category having this base as upper
        bound. If no base is "preferred", the alternative is assigned to
        the category above the highest base profile.

        -The pesimestic procedure decreases the level of base profiles till
        a base profile which is "not preferred" to alternative (b ≺ a)
        is found.
        The alternative is assigned to the category having this base as lower
        bound. If no base is "not preferred", the alternative is assigned to
        the category below the lowest base profile

    When the outranking relation between base and alternative is only of
    "preferrence" ("b ≻ a" or "b ≺ a"), the classification of the alternative
    gives the same result with optimistic and pessimistic procedure.
    For example, consider the outranking relation
    b = ["≺", "≺", "≻", "≻", "≻", "≻"] for an alternative a.
    Both classifications (optimistic and pessimistic) classify alternative a
    in (b1, b2), a ∈ (b1, b2).

    When the outranking relation between alternative and base is of
    "indifference" ("I") or "incomparable" ("R"), the pessimmistic procedure
    assigns the alternative in a lower category than the optimistic procedure.
    For example, consider the outranking relation
    b = ["≺", "≺", "I", "R", "≻", "≻"] for an alternative a.
    Optimistic classification starts from b[0] = "≺" and increases the index
    of b till b[4] = "≻". The alternative is classified in (b3, b4),
    a ∈ (b3, b4).
    Pessimstic classification starts from b[-1] = "≻" and decreases the index
    of b till b[1] = "≺". The alternative is classified in (b1, b2),
    a ∈ (b1, b2).

    Args:
        outranking (DataFrame): Preference relations: ≻, ≺, I, R between
        base profiles (index) and alternatives (columns).

    Returns:
        opti (DataFrame): Optimistic classification matrix.

        pessi (DataFrame): Pessimistic classification matrix.

    Called Functions
    ----------------
    create(outranking) :
        Creates the categories (separated by base profiles) and an empty
        matrix of classification.
    optimistic_classification(outranking) :
        Optimistic classification (ascending rule).
    pessimistic_classification(outranking):
        Pessimistic classification (descending rule).

    """

    def create(outranking):
        """Empty classification matrix and category list.

        Based on outranking matrix (of alternatives on columns and
        base profiles on rows), construct empty matrix for clasificatioin of
        alternatives in ranges defined by base profiles, and a list of
        categories.

        Args:
            outranking (DataFrame): Preference relations: ≻, ≺, I, R
            between base profiles (index) and alternatives (columns).

        Returns:
            classification (DataFrame): Empty DataFrame of classification of
            alternatives in categories (delimited by base profiles).

            categories (list): categories obtained from base profiles.
            For n profiles, there are n + 1 categories:
            "b0 ≻", "(b0, b1)", ... , "bn ≺" for
            b0 preferred, between b0 and b1, ... , bn not preferred,
            respectively.

        Example
        -------

        Given outranking matrix

        +---------+------+------+------+
        |         |  a1  |  a2  |  a3  |
        +=========+======+======+======+
        |  base   |      |      |      |
        +---------+------+------+------+
        |   b1    |   >  |  <   |  R   |
        +---------+------+------+------+
        |   b2    |  >   |  I   |  R   |
        +---------+------+------+------+

        obtain categories

        ['b1 >', '(b1, b2)', 'b2 <']


        and classification (empty matrix)

        +----------+------+------+------+
        |          |  a1  |  a2  |  a3  |
        +==========+======+======+======+
        |  base    |      |      |      |
        +----------+------+------+------+
        | b1 >     | nan  | nan  | nan  |
        +----------+------+------+------+
        | (b1, b2) | nan  | nan  | nan  |
        +----------+------+------+------+
        | b2 <     | nan  | nan  | nan  |
        +----------+------+------+------+

        """
        n = len(outranking.index)
        categories = [f"{outranking.index[0]} ≻"] + [
            f"({outranking.index[i]}, {outranking.index[i+1]})"
            for i in range(n - 1)
        ] + [f"{outranking.index[-1]} ≺"]

        classification = pd.DataFrame(
            index=categories,
            columns=outranking.columns,
            data=np.nan
        )
        return classification, categories

    def optimistic_classification(outranking):
        """Optimistic classification (ascending rule).

        Optimistic classification procedure:

            -Initialize a classification matrix where rows represent categories
            and columns represent alternatives.

            -For each alternative 'altern' in the outranking matrix:

                a.Start from the lowest category (represented by the first
                base profile) and move upwards.

                b.For each base profile 'base', if the outranking relation
                between 'base' and 'altern' is "≻" (i.e., 'base' is preferred
                to 'altern'), then assign the alternative to the
                category below the base profile.
                Stop the process for this alternative and move to
                the next one.

                c.If no preference relation "≻" is found for any base profile,
                assign the alternative to the highest category, i.e. higher
                than the highest base profile.

        The result is a classification matrix where each alternative is
        assigned to exactly one category, represented by a '1'
        in the corresponding cell.

        Args:
            outranking (DataFrame): Preference relations: >, <, I, R
            between base profiles (index) and alternatives (columns).

        Returns:
            classification (DataFrame): Matrix of categories (with
            base profiles as boundaries) and alternatives. The values are 1
            if the alternative belongs to the category and NaN otherwise..

        Example
        -------

        outranking

        +---------+------+------+------+
        |         |  a1  |  a2  |  a3  |
        +=========+======+======+======+
        |  base   |      |      |      |
        +---------+------+------+------+
        |   b1    |  >   |  <   |  R   |
        +---------+------+------+------+
        |   b2    |  >   |  I   |  R   |
        +---------+------+------+------+


        optimistic classification

        +----------+------+------+------+
        |          |  a1  |  a2  |  a3  |
        +==========+======+======+======+
        |  base    |      |      |      |
        +----------+------+------+------+
        | b1 >     |  1   | nan  | nan  |
        +----------+------+------+------+
        | (b1, b2) | nan  | nan  | nan  |
        +----------+------+------+------+
        | b2 <     | nan  |  1   |  1   |
        +----------+------+------+------+

        For a1:
            - outranking(b1, a1) = "≻" (b1 preferred to a1) --> a1 ∈ (b1 >)

        For a2:
            - outranking(b1, a2) = "≺" (b1 not preferred to a1) --> increase b
            - outranking(b2, a2) = "I" (b2 indifferent to a1) --> increase b
            - no base "≻" preferred to a2, a2 ∈ (b2 <),
            i.e. a2 preferred to highest b.

        For a3:
            - outranking(b1, a3) = "R" (b1 incomparable to a1) --> increase b
            - outranking(b2, a3) = "R" (b1 incomparable to a1) --> increase b
            - no base "≻" than a2, a2 ∈ (b2 <), i.e. a2 preferred to highest b.

        """

        classification, categories = create(outranking)

        for altern in outranking.columns:
            for i, base in enumerate(outranking.index):
                if outranking.loc[base, altern] == "≻":
                    classification.loc[categories[i], altern] = 1
                    break
            else:
                classification.loc[categories[-1], altern] = 1
        return classification

    def pessimistic_classification(outranking):
        """Pessimistic classification (descending rule).

        Pessimistic classification procedure:

            -Initialize a classification matrix where rows represent categories
            and columns represent alternatives.

            -For each alternative 'altern' in the outranking matrix:

                a.Start from the highest category (represented by the last
                base profile) and move downwards.

                b.For each base profile 'base', if the outranking relation
                between 'base' and 'altern' is "≺" (i.e., 'base' is not
                preferred to 'altern'), then assign the alternative to the
                category above the base profile.
                Stop the process for this alternative and move to
                the next one.

                c.If no preference relation "<" is found for any base profile,
                assign the alternative to the lowest category, i.e. lower
                than the lowest base profile.

        The result is a classification matrix where each alternative is
        assigned to exactly one category, represented by a '1'
        in the corresponding cell.

        Args:
            outranking (DataFrame): Preference relations: >, <, I, R
            between base profiles (index) and alternatives (columns)..

        Returns:
            classification (DataFrame): Matrix of categories (with base
            profiles as boundaries) and alternatives. The values are 1
            if the alternative belongs to the category and NaN otherwise.

        Example
        -------

        outranking

        +---------+------+------+------+
        |         |  a1  |  a2  |  a3  |
        +=========+======+======+======+
        |  base   |      |      |      |
        +---------+------+------+------+
        |   b1    |  ≻   |  ≺   |  R   |
        +---------+------+------+------+
        |   b2    |  ≻   |  I   |  R   |
        +---------+------+------+------+


        pessimistic classification

        +----------+------+------+------+
        |          |  a1  |  a2  |  a3  |
        +==========+======+======+======+
        |  base    |      |      |      |
        +----------+------+------+------+
        | b1 ≻     |  1   | nan  |  1   |
        +----------+------+------+------+
        | (b1, b2) | nan  |  1   | nan  |
        +----------+------+------+------+
        | b2 ≺     | nan  | nan  | nan  |
        +----------+------+------+------+

        For a1:
            - outranking(b2, a1) = "≻" (b2 preferred to a1) -> decrease b
            - outranking(b1, a1) = "≻" (b1 preferred to a1) -> decrease b
            - no base "≺" than a1, a1 ∈ (b1 ≻), a1 not preferred to lowest b

        For a2:
            - outranking(b2, a2) = "I" (b2 not preferred to a2) -> decrease b
            - outranking(b1, a2) = "≺" (b1 not preferred to a1) -> a2 ∈ (b1,b2)

        For a3:
            - outranking(b2, a3) = "R" (b1 incomparable to a1) -> decrease b
            - outranking(b1, a3) = "R" (b1 incomparable to a1) -> decrease b
            - a2 ∈ (b1 ≻), i.e. a3 not preferred to lowest b

        """
        classification, categories = create(outranking)

        n = len(outranking.index)
        for altern in outranking.columns:
            for i in range(n - 1, -1, -1):
                base = outranking.index[i]
                if outranking.loc[base, altern] == "≺":
                    classification.loc[categories[i + 1], altern] = 1
                    break
            else:
                classification.loc[categories[0], altern] = 1

        return classification

    opti = optimistic_classification(outranking)
    pessi = pessimistic_classification(outranking)
    return opti, pessi


def sort(class_matrix):
    """Classes (in ascending order) and alternatives that are in each class.

    Args:
        class_matrix (DataFrame): Matrix of (optimistic or pessimesitc)
        classification obtained by using classify().

    Returns:
        Series: classes (categories) with boundaries the base profiles (index);
        list of alternatives in each class (values).
    """
    result = {}
    for index, row in class_matrix.iterrows():
        columns_with_one = row[row == 1].index.tolist()
        result[index] = columns_with_one

    return pd.Series(result)


def rank(class_matrix):
    """Alternative and the class to which it belongs.

    Args:
        class_matrix (DataFrame): Matrix of (optimistic or pessimesitc)
        classification obtained by using classify().

    Returns:
        Series: Alternaitves, e.g. 'a1', 'a2' (index) and
        the class (category) to which the alternative bellongs,
        e.g. '< b1', '∈ (b1, b2)' (values).

    """

    def modify_result(result):
        """Ranking result to be printed as a ≻ b, a ≺ b or a ∈ (b1, b2)

        Makes the result more readable.

        Args:
            result (dict): Keys are strings, e.g. 'a1', 'a2', 'a3'.
            Values are strings e.g. 'b1 >', '(b1, b2)', 'b1 >',
            e.g. {'a1': 'b1 >', 'a2': '(b1, b2)', 'a3': 'b1 >'}.

        Returns:
            modified_result (dict): Keys are strings, e.g. 'a1', 'a2', 'a3'.
            Values are strings e.g. '≺ b1', '∈ (b1, b2)', '≻ b1'.
            e.g. {'a1': '≺ b1', 'a2': '∈ (b1, b2)', 'a3': '≻ b1'}.

        """
        modified_result = {}
        for key, value in result.items():
            if '≺' not in value and '>' not in value:
                modified_result[key] = f'∈ {value}'
            elif value.endswith('≺'):
                modified_result[key] = f'> {value[:-2]}'
            elif value.endswith('>'):
                modified_result[key] = f'< {value[:-2]}'
            else:
                modified_result[key] = value
        return modified_result

    result = {}
    for column in class_matrix.columns:
        row_with_one = class_matrix[class_matrix[column] == 1].index
        if not row_with_one.empty:
            result[column] = row_with_one[0]
        else:
            result[column] = None

    result = modify_result(result)
    return pd.Series(result)


def electre_tri_b(A, B, T, w, credibility_threshold):
    """ELECTRE Tri-B workflow.

    All criteria are in ascending order, i.e., higher values are better
    (e.g. efficiency). For criterian that need to be minimised (e.g. cost):
        - use sign inversion for values of alternatives and base profiles.
        - do not use sign inversion for thresholds and weights.

    The base profiles need to be in ascending order.

    The steps of ELECTRE Tri-B method are:
        - Calculate partial concordance, discordance, and global concordance.
        - Assess the credibility for the outranking between:
            - alternatives `a` and base profiles `b`;
            - base profiles `b` and alternatives `a`.
        - Outrank the alternatives.
        - Classify the alternatives.

    Args:
        A (DataFrame): Matrix of performance of alternatives (on rows)
        for criteria (on columns).
        Multiply by -1 for citeria to be minimised.

        B (DataFrame): Matrix of base profiles organized in ascending order.
        Base profiles are on rows and criteria on columns.
        Multiply by -1 for citeria to be minimised.

        T (DataFrame): Matrix of thresholds:
            - q : indifference,
            - p : preference,
            - v  :veto.
        The thresholds are for each criterion.
        Do not multiply by -1 for citeria to be minimised.

        w (DataFrame): Vector of weights for each criterion.
        Do not multiply by -1 for citeria to be minimised.

        credibility_threshold (float): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.

    Returns:
        optimistic (DataFrame): Optimistic ranking DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which is an
        alternative. There is only one value of 1 per row and per colum, i.e.
        an alternative belongs to one and only one category.

        pessimistic (DataFrame): Pessimistic ranking DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which is an
        alternative. There is only one value of 1 per row and per colum, i.e.
        an alternative belongs to one and only one category.

    Tha data of the problem can be read from a data file using
    read_electre_tri_base(filename).
    The `filename = "data_file.csv"` contains the follwong matrices and vector
    with columns representing criteria:
        - A : matrix of performance of alternatives.
        - B : matrix of base profiles organized n ascending order.
        - T : matrix of thresholds:
            - q : indifference,
            - p : preference,
            - v  :veto.
        - w : vector of weights for each criterion.

    >>> A, B, T, w = read_electre_tri_base(data_file)
    >>> opti, pessi = electre_tri(A, B, T, w,
    ...                           credibility_threshold=0.7)


    where `data_file.csv` is:


    .. code-block:: none

        type, profile, c1, c2
        A,    a1,     8.5, 18
        A,    a2,      14, 16
        A,    a3,       5, 27
        B,    b1,      10, 15
        B,    b2,      15, 20
        T,     q,       1, 2
        T,     p,       2, 4
        T,     v,       4, 8
        w,      ,     0.7, 0.3

    """
    # A, B, T, w = read_electre_tri_base(data_file)
    c_ab, c_ba = partial_concordance(A, B, T)
    d_ab, d_ba = discordance(A, B, T)
    C_ab = global_concordance(c_ab, w)
    C_ba = global_concordance(c_ba, w)
    sigma_ab = credibility_index(C_ab, d_ab)
    sigma_ba = credibility_index(C_ba, d_ba)
    outranking = outrank(sigma_ab, sigma_ba, credibility_threshold)
    optimistic, pessimistic = classify(outranking)
    return optimistic, pessimistic


def pelectre_tri_b(A, S, B, T, w,
                   credibility_threshold,
                   n_simulations=100,
                   seed=123):
    """pETECTRE Tri-B: probabilistic ELECTRE Tri-B

    Monte Carlo simulation of the ELECTRE Tri-B method with
    normally distributed performance values.`

    Steps:
        - Generate random samples from normal distributions for each value
        in the performance matrix A.
        - Run the ELECTRE Tri-B method on each sample of A.
        - Aggregate the results to get probabilities of assignment
        to each category

`
    Args:
        A (DataFrame): Matrix of performance of alternatives (on rows)
        for criteria (on columns).
        Multiply by -1 for citeria to be minimised.

        S (DataFrame): Matrix with standard deviations of each value of
        the performance matrix A.

        B (DataFrame): Matrix of base profiles organized in ascending order.
        Base profiles are on rows and criteria on columns.
        Multiply by -1 for citeria to be minimised.

        T (DataFrame): Matrix of thresholds:
            - q : indifference,
            - p : preference,
            - v  :veto.
        The thresholds are for each criterion.
        Do not multiply by -1 for citeria to be minimised.

        w (DataFrame): Vector of weights for each criterion.
        Do not multiply by -1 for citeria to be minimised.

        credibility_threshold (float): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.

        n_simulations (int, optional): Number of simulations.
        Default to 100.

        seed (int, optonal): Seed for the reproducibility of random number
        generator. Use `seed=None` for truely random numbers.
        Default to 123.

    Returns:
        p_opti (DataFrame): Optimistic ranking DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which is an
        alternative. There is only one value of 1 per row and per colum, i.e.
        an alternative belongs to one and only one category.

        p_pessi (DataFrame): Pessimistic ranking DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which is an
        alternative. There is only one value of 1 per row and per colum, i.e.
        an alternative belongs to one and only one category.

    """
    opti, pessi = electre_tri_b(A, B, T, w,
                                credibility_threshold=0.7)

    # Initialize result dataframe
    p_opti = pd.DataFrame(0, index=opti.index, columns=opti.columns)
    p_pessi = pd.DataFrame(0, index=pessi.index, columns=pessi.columns)

    # Set up random number generator
    rng = np.random.default_rng(seed)

    # Create sample_A once, outside the loop
    sample_A = pd.DataFrame(index=A.index, columns=A.columns)

    for _ in range(n_simulations):
        # Generate new random values for sample_A
        sample_A[:] = A + rng.normal(loc=0, scale=S)

        # Run ELECTRE Tri-B on the sample
        opti, pessi = electre_tri_b(sample_A,
                                    B, T, w,
                                    credibility_threshold)

        # Aggregate results
        p_opti += opti.fillna(0)
        p_pessi += pessi.fillna(0)

    # Convert counts to probabilities
    p_opti /= n_simulations
    p_pessi /= n_simulations

    # Replace zero probabilities with NaN for better readability
    p_opti = p_opti.replace(0, np.nan)
    p_pessi = p_pessi.replace(0, np.nan)

    return p_opti, p_pessi


def electre_tri_base(
        data_file,
        credibility_threshold=0.75):
    """ELECTRE Tri-B workflow for base profiles defined explicitly.

    Workflow
    --------

    Given data file with:
        - performance matrix, A
        - base profiles, B
        - indifference q, preferrence p, veto v thresholds, T
        - weights of criteria, w

    and:
        - credibility threshold for the validation of an outranking relation

    Perform: electre_tri_b(A, B, T, w,
                           credibility_threshold)

    Args:
        data_file (str): Name of .csv file containing the data of the problem
        (performance of alternatives A, base profiles B, thersholds T,
         and weights w).

        credibility_threshold (float, optional): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.
        Defaults to 0.75.

    Returns:
        optimistic (DataFrame): Optimistic classification DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which an
        alternative is classified. There is only one value of 1 per row and
        per column, i.e. an alternative belongs to one and only one category.

        pessimistic (DataFrame): Optimistic classification DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which an
        alternative is classified. There is only one value of 1 per row and
        per column, i.e. an alternative belongs to one and only one category.

    Example
    -------

    >>> opti, pessi = electre_tri_base(
    ...     data_file="bldg_retrofit_base.csv",
    ...     credibility_threshold=0.75)


    where `bldg_retrofit_base.csv` is:


    .. code-block:: none

        type, profile,      Saving/(kWh/m²/year), Cost/(€/m²)
        A,    a1: Basic,                      50, -100
        A,    a2: Moderate,                   80, -200
        A,    a3: Extensive,                 120, -350
        B,    bad,                            50, -300
        B,    good,                          100, -100
        T,    q,                               5,   10
        T,    p,                              10,   25
        T,    v,                              20,   50
        w,   ,                                 0.7,  0.3

   """

    A, B, T, w = read_electre_tri_base(data_file)
    optimistic, pessimistic = electre_tri_b(A, B, T, w,
                                            credibility_threshold)

    return optimistic, pessimistic


def electre_tri_level(
        data_file,
        n_base_profile=4,
        threshold_percent=[0.10, 0.25, 0.50],
        credibility_threshold=0.75):
    """ELECTRE Tri-B workflow for base profiles from worst & best levels.

    Workflow
    --------

    Given data file with:
        - performance matrix, A
        - level of worst and best possible base profiles, L
        - weights of criteria, w

    and:
        - number of base profiles
        - thresholds (q, p, v) as a percentage
        of the range between two consecutive equidistant base profiles
        - credibility threshold for the validation of an outranking relation

    Calculate:
        - base profiles, B
        - theresholds, T

    Perform: electre_tri_b(A, B, T, w, credibility_threshold)

    Args:
        data_file (str): Name of .csv file containing the data of the problem
        (performance of alternatives A, worst/best possible base levels L, and
        weights w).

        n_base_profile (int, optional): Number of equidistant base profiles
        between worst and best possible.
        Defaults to 4.

        threshold_percent (list, optional): Percentage of the range
        between base profiles for
        veto v, preferrence p, and indifference p thresholds.
        Defaults to [0.10, 0.25, 0.50].

        credibility_threshold (float, optional): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.
        Defaults to 0.75.

    Returns:
        optimistic (DataFrame): Optimistic classification DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which an
        alternative is classified. There is only one value of 1 per row and
        per column, i.e. an alternative belongs to one and only one category.

        pessimistic (DataFrame): Optimistic classification DataFrame with
        index for categories and columns for alternatives.
        Values are NaN or 1. Value 1 indicates the category in which an
        alternative is classified. There is only one value of 1 per row and
        per column, i.e. an alternative belongs to one and only one category.

    Example
    -------

    >>> opti, pessi = electre_tri_level(
    ...     data_file="bldg_retrofit_level.csv",
    ...     n_base_profile=2,
    ...     threshold_percent=[0.10, 0.25, 0.50],
    ...     credibility_threshold=0.75)

    where `bldg_retrofit_level.csv` is:

    .. code-block:: none

        type, profile,                 Saving/(kWh/m²/year), Cost/(€/m²)
        A,    a1: Basic,                      50, -100
        A,    a2: Moderate,                   80, -200
        A,    a3: Extensive,                 120, -350
        L,    worst,                           0, -400
        L,    best,                          150,  -50
        w,   ,                                 0.7,  0.3

   """

    A, L, w = read_electre_tri_level(data_file)
    B = base_profile(L, n_base_profile)
    T = threshold(B, threshold_percent)

    optimistic, pessimistic = electre_tri_b(A, B, T, w,
                                            credibility_threshold)

    return optimistic, pessimistic


def pelectre_tri_base(
        data_file,
        credibility_threshold=0.75,
        n_simulations=100,
        seed=123):
    """Probabilistic ELECTRE Tri-B workflow for base profiles defined
    explicitly.

    Workflow
    --------

    Given data file with:
        - performance matrix, A
        - standard deviations of values of performance matrix, S
        - base profiles, B
        - indifference q, preferrence p, veto v thresholds, T
        - weights of criteria, w

    and:
        - credibility threshold for the validation of an outranking relation
        - number of Monte Carlo simulations
        - seed for random numbers

    Perform: electre_tri_b(A, B, T, w,
                           credibility_threshold)

    Args:
        data_file (str): Name of .csv file containing the data of the problem
        (performance of alternatives A, base profiles B, thersholds T,
         and weights w).

        credibility_threshold (float, optional): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.
        Defaults to 0.75.

    Returns:
        p_opti (DataFrame): Probabilistic optimistic classification
        DataFrame with index for categories and columns for alternatives.
        Values are NaN or floats from 0 to 1 indicating the probability of
        membership of an altenative to a category. The sum of values on a
        columns is 1.

        p_pessi (DataFrame): Probabilistic pessimistic classification
        DataFrame with index for categories and columns for alternatives.
        Values are NaN or floats from 0 to 1 indicating the probability of
        membership of an altenative to a category. The sum of values on a
        columns is 1.

    Example
    -------

    >>> opti, pessi = pelectre_tri_base(
    ...     data_file="bldg_retrofit_base_std.csv",
    ...     credibility_threshold=0.75,
    ...     n_simulations=100,
    ...     seed=123)

    where `bldg_retrofit_base_std.csv` is:


    .. code-block:: none

        type, profile,      Saving/(kWh/m²/year), Cost/(€/m²)
        A,    a1: Basic,                      50, -100
        A,    a2: Moderate,                   80, -200
        A,    a3: Extensive,                 120, -350
        S,    a1: Basic,                       5,   10
        S,    a2: Moderate,                    8,   20
        S,    a3: Extensive,                  12,   35
        B,    bad,                            50, -300
        B,    good,                          100, -100
        T,    q,                               5,   10
        T,    p,                              10,   25
        T,    v,                              20,   50
        w,   ,                                 0.7,  0.3

   """

    A, S, B, T, w = read_pelectre_tri_base(data_file)
    p_opti, p_pessi = pelectre_tri_b(A, S, B, T, w,
                                     credibility_threshold)
    return p_opti, p_pessi


def pelectre_tri_level(
        data_file,
        n_base_profile=4,
        threshold_percent=[0.10, 0.25, 0.50],
        credibility_threshold=0.75,
        n_simulations=100,
        seed=123):
    """Probabilistic ELECTRE Tri-B workflow for base profiles from
    worst & best levels.

    Workflow
    --------

    Given data file with:
        - performance matrix, A
        - standard deviations of values of performance matrix, S
        - level of worst and best possible base profiles, L
        - weights of criteria, w

    and:
        - number of base profiles
        - thresholds (q, p, v) as a percentage
        of the range between two consecutive equidistant base profiles
        - credibility threshold for the validation of an outranking relation
        - number of Monte Carlo simulations
        - seed for random numbers

    Calculate:
        - base profiles, B
        - theresholds, T

    Perform: electre_tri_b(A, B, T, w, credibility_threshold)

    Args:
        data_file (str): Name of .csv file containing the data of the problem
        (performance of alternatives A, worst/best possible base levels L, and
        weights w).

        n_base_profile (int, optional): Number of equidistant base profiles
        between worst and best possible.
        Defaults to 4.

        threshold_percent (list, optional): Percentage of the range
        between base profiles for
        veto v, preferrence p, and indifference p thresholds.
        Defaults to [0.10, 0.25, 0.50].

        credibility_threshold (float, optional): Thershold between 0.5 and 1
        (typically 0.75) to be used for the credibility of outranking.
        Defaults to 0.75.

    Returns:
        p_opti (DataFrame): Probabilistic optimistic classification
        DataFrame with index for categories and columns for alternatives.
        Values are NaN or floats from 0 to 1 indicating the probability of
        membership of an altenative to a category. The sum of values on a
        columns is 1.

        p_pessi (DataFrame): Probabilistic pessimistic classification
        DataFrame with index for categories and columns for alternatives.
        Values are NaN or floats from 0 to 1 indicating the probability of
        membership of an altenative to a category. The sum of values on a
        columns is 1.

    Example
    -------

    >>> opti, pessi = pelectre_tri_level(
    ...     data_file="bldg_retrofit_level_std.csv",
    ...     n_base_profile=2,
    ...     threshold_percent=[0.10, 0.25, 0.50],
    ...     credibility_threshold=0.75,
    ...     n_simulations=100,
    ...     seed=123)

    where `bldg_retrofit_level_std.csv` is:

    .. code-block:: none

        type, profile,                 Saving/(kWh/m²/year), Cost/(€/m²)
        A,    a1: Basic,                      50, -100
        A,    a2: Moderate,                   80, -200
        A,    a3: Extensive,                 120, -350
        S,    a1: Basic,                       5,   10
        S,    a2: Moderate,                    8,   20
        S,    a3: Extensive,                  12,   35
        L,    worst,                           0, -400
        L,    best,                          150,  -50
        w,   ,                                 0.7,  0.3

   """

    A, S, L, w = read_pelectre_tri_level(data_file)
    B = base_profile(L, n_base_profile)
    T = threshold(B, threshold_percent)

    optimistic, pessimistic = pelectre_tri_b(A, S, B, T, w,
                                             credibility_threshold)

    return optimistic, pessimistic


def plot_alternatives_vs_base_profile(A, B_row, T):
    """Plots alternatives as lines and one base profile with
    ranges of indifference, preference and veto.

    Args:
        A (DataFrame): Performance matrix of alternatives (rows)
        for criteria (columns).

        B_row (DataFrame): One Base profile.

        T (DataFrame): Indifference (q), preference (p) and veto (v) thresholds
        for each criterion (columns).

    Returns:
        None.

    Example
    -------

    >>> plot_alternatives_vs_base_profile(A, B.iloc[0], T)

    """

    # Create a new figure
    # plt.figure(figsize=(12, 7))
    plt.figure(figsize=(10, 6))

    # Plot lines for each alternative in A
    for idx, row in A.iterrows():
        plt.plot(A.columns, row.values,
                 marker='o', linewidth=6, label=f'Alternative {idx}')

    # Plot the base profile
    plt.plot(B_row.index, B_row.values,
             color='blue', marker='s', linestyle='-',
             linewidth=2, label=f'Base profile {B_row.name}')

    # Plot the indifference threshold
    indifference = B_row.copy() # Modification
    indifference[B_row > 0] = B_row[B_row > 0] - T.loc['q']
    indifference[B_row <= 0] = B_row[B_row <= 0] + T.loc['q']
    plt.plot(indifference.index, indifference.values,
             color='blue', marker='^',
             linestyle='--', label='Indifference')

    # Plot the preference threshold
    preference = B_row.copy()
    preference[B_row > 0] = B_row[B_row > 0] - T.loc['p']
    preference[B_row <= 0] = B_row[B_row <= 0] + T.loc['p']
    plt.plot(preference.index, preference.values,
             color='green', marker='v',
             linestyle='--', label='Preference')

    # Plot the veto threshold
    veto = B_row.copy()
    veto[B_row > 0] = B_row[B_row > 0] - T.loc['v']
    veto[B_row <= 0] = B_row[B_row <= 0] + T.loc['v']
    plt.plot(veto.index, veto.values,
             color='black', marker='x',
             linestyle='--', label='Veto')

    # Fill the space between Base profile and Indifference
    plt.fill_between(B_row.index, B_row.values, indifference.values,
                     color='blue', alpha=0.1)
    plt.fill_between(B_row.index, B_row.values, preference.values,
                     color='green', alpha=0.1)
    plt.fill_between(B_row.index, B_row.values, veto.values,
                     color='black', alpha=0.1)

    # Customize the plot
    plt.xlabel('Criteria')
    plt.ylabel('Values')
    plt.title(f'Comparison between alternatives and base profile {B_row.name}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1), ncol=3) # Modification

    # Show the plot
    plt.show()


def plot_base_profiles_vs_alternative(B, A_row, T):
    """ Plots base profiles as lines and one alternative with
    ranges of indifference, preference and veto.

    Args:
        B (DataFrame): Base profiles in ascending order for criteria (columns).

        A_row (DataFrame): One alternative from the performance matrix.

        T (DataFrame): Indifference (q), preference (p) and veto (v)
        thresholds for each criterion (columns).

    Returns:
        None.

    Example
    -------
    >>> plot_base_profiles_vs_alternative(B, A.iloc[0], T)
    """

    # Create a new figure
    # plt.figure(figsize=(12, 7))
    plt.figure(figsize=(10, 6))

    # Plot lines for each alternative in A
    for idx, row in B.iterrows():
        plt.plot(B.columns, row.values,
                 marker='o', linewidth=6, label=f'Base profile {idx}')

    # Plot the base profile
    plt.plot(A_row.index, A_row.values,
             color='blue', marker='s', linestyle='-',
             linewidth=2, label=f'Alternative {A_row.name}')

    # Plot the indifference threshold
    indifference = A_row.copy() # Modification
    indifference[A_row > 0] = A_row[A_row > 0] - T.loc['q']
    indifference[A_row <= 0] = A_row[A_row <= 0] + T.loc['q']
    plt.plot(indifference.index, indifference.values,
             color='blue', marker='^',
             linestyle='--', label='Indifference')

    # Plot the preference threshold
    preference = A_row.copy()
    preference[A_row > 0] = A_row[A_row > 0] - T.loc['p']
    preference[A_row <= 0] = A_row[A_row <= 0] + T.loc['p']
    plt.plot(preference.index, preference.values,
             color='green', marker='v',
             linestyle='--', label='Preference')

    # Plot the veto threshold
    veto = A_row.copy()
    veto[A_row > 0] = A_row[A_row > 0] - T.loc['v']
    veto[A_row <= 0] = A_row[A_row <= 0] + T.loc['v']
    plt.plot(veto.index, veto.values,
             color='black', marker='x',
             linestyle='--', label='Veto')

    # Fill the space between Base profile and Indifference
    plt.fill_between(A_row.index, A_row.values, indifference.values,
                     color='blue', alpha=0.1)
    plt.fill_between(A_row.index, A_row.values, preference.values,
                     color='green', alpha=0.1)
    plt.fill_between(A_row.index, A_row.values, veto.values,
                     color='black', alpha=0.1)

    # Customize the plot
    plt.xlabel('Criteria')
    plt.ylabel('Values')
    plt.title(f'Comparison between base profile and alternatives {A_row.name}')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
   # plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # plt.legend(loc='upper left', bbox_to_anchor=(0.5, -0.1), ncol=3)

    # Show the plot
    plt.show()
