import numpy as np
import pandas as pd

def asia_pop_life(df, year: int = 2007) -> pd.DataFrame:
    '''Selects Asia based on the selected year, Creates a separate table, and Rank the life Expectancy'''
    asia_sel = df.loc[(df['continent'] == 'Asia') & (df['year'] == year)].copy()

    asia_sel['pop_millions'] = asia_sel['pop']/1000000

    lifeExp_rank = asia_sel['lifeExp'].rank(ascending = False, method = 'min')
    asia_sel['lifeExp_rank'] = lifeExp_rank.astype(int)

    final_part1 = asia_sel.sort_values(by = ['lifeExp_rank', 'country'], ascending = [True, True]) 
    return final_part1
    
def phil_pop_life(df, country: str = 'Philippines') -> pd.DataFrame:
    '''Selects Philippines from the table, Sorts by year, and Adds pop_millions & lifeExp_change'''
    phil_sel = df.loc[(df['country'] == country)].copy()

    phil_sel['pop_millions'] = phil_sel['pop']/1000000

    phil_sel = phil_sel.sort_values(by = 'year', ascending = True)

    life_num = phil_sel['lifeExp'].iloc[0]
    phil_sel['lifeExp_change'] = phil_sel['lifeExp'] - life_num
    return phil_sel
    
def build_population_matrix(df, countries: list, years: list) -> np.ndarray:
    '''Creating a Matrix based on population from the selected countries and years'''
    numpy_asia = df.loc[df['country'].isin(countries) & df['year'].isin(years)]
    pop_list = []

    for c in countries:
        country_nump = numpy_asia.loc[numpy_asia['country'] == c]
        country_order = country_nump.sort_values(by = 'year', ascending = True)
        country_pop = country_order['pop']
        pop_list.append(np.array(country_pop))

    converted = np.vstack(pop_list)
    return converted
    
def population_index(matrix: np.ndarray) -> np.ndarray:
    '''Calculate the population index of the matrix'''
    sliced_select = matrix[:, [0]]
    divide = matrix / sliced_select
    result_product = divide * 100

    return result_product
    
def asia_pop_total(df, cont_arr: str = 'Asia', year_arr: int = 2007) -> tuple:
    '''Takes continent from original data and Returns a sum of population and counts of matching rows'''
    continent = df['continent'].to_numpy()
    year = df['year'].to_numpy()
    pop = df['pop'].to_numpy()

    mask = (continent == cont_arr) & (year == year_arr)
    val = pop[mask].sum()
    counts = mask.sum()

    return int(val), int(counts)
    
def pop_ind(matrix: np.ndarray) -> np.ndarray:
    '''Rebuilds the index with plain loops and Returns the result'''
    rows, cols = matrix.shape
    store = np.zeros((rows, cols))
    
    for i in range(rows):
        for j in range(cols):
            store[i, j] = (matrix[i, j] / matrix[i, 0]) * 100

    return store
    
def population_index_table(index_matrix: np.ndarray, countries: list[str], years: list[int]) -> pd.DataFrame:
    """Labels an index matrix with country names and string year column headers."""
    if index_matrix.shape != (len(countries), len(years)):
        raise ValueError(
            f"Matrix shape {index_matrix.shape} does not match "
            f"{len(countries)} countries x {len(years)} years"
        )
    table = pd.DataFrame(index_matrix, columns=[str(y) for y in years])
    table.insert(0, "country", countries)
    return table

def generate_validation_rows(case_week, countries, years, year: int = 2007,
                             country: str = "Philippines") -> list:
    """Generates the 5 validation dictionaries for the configured year."""
    results = []

    var1 = asia_pop_life(case_week, year)
    var2, var3 = asia_pop_total(case_week, year_arr=year)
    actual_total = int(var1["pop"].sum())
    length1 = len(var1)

    results.append({
        "check": f"Asia total {year}",
        "expected": var2,
        "actual": actual_total,
        "tolerance": 0,
        "pass": bool(var2 == actual_total),
    })
    results.append({
        "check": f"Asia row count {year}",
        "expected": int(var3),
        "actual": int(length1),
        "tolerance": 0,
        "pass": bool(length1 == var3),
    })

    pop_matrix = build_population_matrix(case_week, countries, years)
    pop_idx = population_index(pop_matrix)
    stored = pop_ind(pop_matrix)
    maxi = np.abs(stored - pop_idx).max()
    results.append({
        "check": "Broadcast Result versus Loop Result",
        "expected": 0.0,
        "actual": float(maxi),
        "tolerance": 1e-8,
        "pass": bool(np.allclose(stored, pop_idx, atol=1e-8, rtol=0)),
    })

    first_col = pop_idx[:, 0]
    results.append({
        "check": "First-year column equals 100 (max deviation)",
        "expected": 0.0,
        "actual": float(np.abs(first_col - 100).max()),
        "tolerance": 1e-8,
        "pass": bool(np.allclose(first_col, 100, atol=1e-8, rtol=0)),
    })

    names = case_week["country"].to_numpy()
    yrs = case_week["year"].to_numpy()
    pops = case_week["pop"].to_numpy()
    expected_pop = int(pops[(names == country) & (yrs == year)].sum())
    history = phil_pop_life(case_week, country)
    actual_pop = int(history.loc[history["year"] == year, "pop"].sum())
    results.append({
        "check": f"{country} population {year}",
        "expected": expected_pop,
        "actual": actual_pop,
        "tolerance": 0,
        "pass": bool(expected_pop == actual_pop),
    })
    return results

def write_analysis_report_html(path, year: int, country: str, asia: pd.DataFrame,
                               history: pd.DataFrame, index_table: pd.DataFrame,
                               checks: list) -> None:
    """Writes report.html: a self-contained summary of the Member 4 analysis outputs."""
    from html import escape
    total, count = int(asia["pop"].sum()), len(asia)

    def table(df, digits=2):
        return df.to_html(index=False, border=0, classes="t", float_format=lambda v: f"{v:,.{digits}f}")

    # Inline SVG line chart of the population index (no plotting library needed).
    year_cols = [c for c in index_table.columns if c != "country"]
    w, h, pad = 640, 300, 45
    lo = min(100.0, float(index_table[year_cols].to_numpy().min()))
    hi = float(index_table[year_cols].to_numpy().max())
    x = lambda i: pad + i * (w - pad - 120) / max(len(year_cols) - 1, 1)
    y = lambda v: h - pad - (v - lo) * (h - 2 * pad) / max(hi - lo, 1e-9)
    colors = ["#1b6ca8", "#d9822b", "#2e8b57", "#8e44ad"]
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Population index, first year = 100">']
    parts.append(f'<line x1="{pad}" y1="{y(100):.1f}" x2="{w - 120}" y2="{y(100):.1f}" stroke="#999" stroke-dasharray="4"/>')
    for i, c in enumerate(year_cols):
        parts.append(f'<text x="{x(i):.1f}" y="{h - pad + 18}" font-size="12" text-anchor="middle">{escape(c)}</text>')
    for k, (_, row) in enumerate(index_table.iterrows()):
        col = colors[k % len(colors)]
        pts = " ".join(f"{x(i):.1f},{y(float(row[c])):.1f}" for i, c in enumerate(year_cols))
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>')
        parts.append(f'<text x="{w - 114}" y="{y(float(row[year_cols[-1]])) + 4:.1f}" font-size="12" fill="{col}">{escape(str(row["country"]))}</text>')
    parts.append("</svg>")

    check_rows = "".join(
        f"<tr><td>{escape(str(c['check']))}</td><td>{escape(str(c['expected']))}</td>"
        f"<td>{escape(str(c['actual']))}</td><td>{escape(str(c['tolerance']))}</td>"
        f"<td class=\"{'ok' if c['pass'] else 'bad'}\">{'PASS' if c['pass'] else 'FAIL'}</td></tr>"
        for c in checks)
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Population analysis report</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;color:#1d2530}}
h1{{font-size:1.6rem}} h2{{margin-top:2rem;border-bottom:1px solid #d8dde3;padding-bottom:.2rem}}
table.t,table.c{{border-collapse:collapse;width:100%;font-size:.9rem}}
.t th,.t td,.c th,.c td{{padding:.3rem .5rem;border-bottom:1px solid #e4e8ec;text-align:right}}
.t th:first-child,.t td:first-child,.c td:first-child,.c th:first-child{{text-align:left}}
.ok{{color:#1a7f37;font-weight:600}} .bad{{color:#c62828;font-weight:600}}
.scroll{{overflow-x:auto}} svg{{width:100%;height:auto}}
</style></head><body>
<h1>Population analysis report</h1>
<p>Generated by the pipeline from the clean canonical table. Reporting year: {year}.</p>
<h2>Asia, {year}</h2>
<p>{count} countries, total population {total:,}. Ranked by life expectancy (descending, ties share the lowest rank).</p>
<div class="scroll">{table(asia)}</div>
<h2>{escape(country)} history</h2>
<div class="scroll">{table(history)}</div>
<h2>Population index (first year = 100)</h2>
{"".join(parts)}
<div class="scroll">{table(index_table)}</div>
<h2>Calculation checks</h2>
<div class="scroll"><table class="c"><tr><th>check</th><th>expected</th><th>actual</th><th>tolerance</th><th>result</th></tr>{check_rows}</table></div>
</body></html>"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
