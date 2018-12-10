import io
import pandas
import requests
from bs4 import BeautifulSoup
import warnings

def scrape_data(formula, column_names=None):
    """
    Download X-ray form factor table for a given element or compound from the
    NIST website and return it as a pandas dataframe.
    """
    table_text = _get_table_text(_make_nist_url(formula))
    header_rows,data_rows = _split_header_and_data(table_text)

    try:
        df = _rows_to_dataframe(data_rows, column_names)
    except Exception as exc:
        warnings.warn("Header is" + ("\n".join(header_rows)))
        raise
    return df

def _make_nist_url(formula):
    url = f"https://physics.nist.gov/cgi-bin/ffast/ffast.pl?Z=1&Formula={formula}&gtype=4&range=U&frames=no"
    return url

def _get_table_text(query_url):
    page = requests.get(query_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tabledata = soup.find_all("pre")
    table_text = tabledata[-1].text
    return table_text

def _split_header_and_data(table_text, num_header_lines=3):
    table_lines = table_text.splitlines()
    return table_lines[:num_header_lines], table_lines[num_header_lines:]

def _rows_to_dataframe(table_rows, column_names):

    if column_names is None:
        num_columns = len(table_rows[0].split())
        if num_columns == 4:
            column_names = ["energy_keV", "f2_e_atom", "mu_rho_cm2_g", "mu_rho_tot_cm2_g"]
        elif num_columns == 8:
            column_names = ["energy_keV", "f1_e_atom", "f2_e_atom", "mu_rho_cm2_g", "sigma_rho_cm2_g", "mu_rho_tot_cm2_g", "mu_rho_K_cm2_g", "lambda_nm"]
        else:
            raise Exception(f"Got {num_columns} columns, expected 4 or 6")

    df = pandas.read_table(io.StringIO("\n".join(table_rows)), names=column_names, sep=r"\s+")
    return df


