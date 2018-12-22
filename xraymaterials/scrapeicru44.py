import io
import pandas
import requests
import urllib
from bs4 import BeautifulSoup

def scrape_icru44_tables(main_url=None):
    """
    Download ICRU-44 xray absorption tables from the NIST website and return
    all of them as pandas dataframes.
    """
    if main_url is None:
        main_url = _main_url

    links = _get_icru44_links(main_url)

    icru44_tables = {}

    for link in links:
        url = urllib.parse.urljoin(main_url, link["href"])
        df = _scrape_icru44_page(url)
        icru44_tables[link.text] = df
    
    return icru44_tables

def scrape_icru44_composition():
    """
    Download ICRU-44 material composition table from the NIST website and
    return it in a list of dicts.
    """
    tab2_url = "https://physics.nist.gov/PhysRefData/XrayMassCoef/tab2.html"

    page = requests.get(tab2_url)
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup("tr")[3:]

    composition_pattern = re.compile(r"(.*):(.*)")
    density_pattern = re.compile(".*E.[0-9]{2}")

    material_data = []

    for row in rows:
        material = row("td")[0]

        density_g_cc = row.find("td", text=density_pattern)
        composition = row.find_all("td")[-1]
        z_fractions = composition_pattern.findall(composition.text)

        zs = [int(token[0].strip()) for token in z_fractions]
        fractions = [float(token[1].strip()) for token in z_fractions]

        material_data.append( {"material":material.text, "density_g_cc": float(density_g_cc.text), "z":zs, "fraction":fractions} )

    return material_data

_main_url = "https://physics.nist.gov/PhysRefData/XrayMassCoef/tab4.html"

def _get_icru44_links(main_url):

    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table")
    linx = table.findAll("a")
    
    return linx

def _scrape_icru44_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    table_text = soup("pre")[0].text
    table_rows = table_text.splitlines()[6:]
    last_three_tokens = [" ".join(row.split()[-3:]) for row in table_rows]
    
    cleaned_table_txt = "\n".join(last_three_tokens)
    
    df = pandas.read_table(io.StringIO(cleaned_table_txt), names=["energy_MeV", "mu_rho_cm2_g", "muen_rho_cm2_g"], delimiter="\s+")
    return df

