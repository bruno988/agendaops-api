"""
reativar.py
===========
Reativa os usuarios desativados incorretamente no Activesoft.
"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

ACTIVESOFT_BASE_URL = "https://siga.activesoft.com.br"
TOKENS = {
    "OVM":          os.getenv("ACTIVESOFT_TOKEN_OVM"),
    "APS":          os.getenv("ACTIVESOFT_TOKEN_APS"),
    "MARILLAC":     os.getenv("ACTIVESOFT_TOKEN_MARILLAC"),
    "TUTOR":        os.getenv("ACTIVESOFT_TOKEN_TUTOR"),
    "DOMHENRIQUE":  os.getenv("ACTIVESOFT_TOKEN_DH1"),
    "DOMHENRIQUE2": os.getenv("ACTIVESOFT_TOKEN_DH2"),
}

# Lista exata de unidade + login para reativar
PARA_REATIVAR = [
    ("OVM",          "Beatriz.freitas"),
    ("OVM",          "anna.fernandes"),
    ("OVM",          "sara.dias"),
    ("OVM",          "mateus.silva"),
    ("OVM",          "janaina.silva"),
    ("OVM",          "fabiola.dias"),
    ("OVM",          "lais.scicco"),
    ("OVM",          "adriana.fernandes"),
    ("APS",          "mateus.silva"),
    ("APS",          "beatriz.freitas"),
    ("APS",          "fabiola.dias"),
    ("APS",          "adriana.fernandes"),
    ("MARILLAC",     "beatriz.freitas"),
    ("MARILLAC",     "jose.teiga"),
    ("MARILLAC",     "mateus.silva"),
    ("MARILLAC",     "anna.fernandes"),
    ("MARILLAC",     "ana.claudia"),
    ("MARILLAC",     "Lais.Scicco"),
    ("MARILLAC",     "geisse.peixoto"),
    ("MARILLAC",     "fabiola.dias"),
    ("MARILLAC",     "adriana.fernandes"),
    ("TUTOR",        "beatriz.freitas"),
    ("TUTOR",        "jose.teiga"),
    ("TUTOR",        "anna.fernandes"),
    ("TUTOR",        "mateus.silva"),
    ("TUTOR",        "Karen.Cristine"),
    ("TUTOR",        "fabiola.dias"),
    ("TUTOR",        "lais.scicco"),
    ("TUTOR",        "adriana.fernandes"),
    ("DOMHENRIQUE",  "beatriz.freitas"),
    ("DOMHENRIQUE",  "jose.teiga"),
    ("DOMHENRIQUE",  "marcela.almeida"),
    ("DOMHENRIQUE",  "soraia.thomazi"),
    ("DOMHENRIQUE",  "anna.fernandes"),
    ("DOMHENRIQUE",  "LARA.DINIZ"),
    ("DOMHENRIQUE",  "mateus.silva"),
    ("DOMHENRIQUE",  "sandra.kishimoto"),
    ("DOMHENRIQUE",  "pamela.cunha"),
    ("DOMHENRIQUE",  "312.713.488-61"),
    ("DOMHENRIQUE",  "marjorie.pauloconhis"),
    ("DOMHENRIQUE",  "lais.scicco"),
    ("DOMHENRIQUE",  "fabiola.dias"),
    ("DOMHENRIQUE",  "juliana.aparecida"),
    ("DOMHENRIQUE",  "analia.lima"),
    ("DOMHENRIQUE",  "cristiane.silva"),
    ("DOMHENRIQUE",  "alenilda.santos"),
    ("DOMHENRIQUE",  "adriana.fernandes"),
    ("DOMHENRIQUE2", "leticia.dario"),
    ("DOMHENRIQUE2", "jose.teiga"),
    ("DOMHENRIQUE2", "beatriz.freitas"),
    ("DOMHENRIQUE2", "jackeline.santos"),
    ("DOMHENRIQUE2", "anna.fernandes"),
    ("DOMHENRIQUE2", "mateus.silva"),
    ("DOMHENRIQUE2", "rafaela.costa"),
    ("DOMHENRIQUE2", "valter.pereira"),
    ("DOMHENRIQUE2", "fabiola.dias"),
    ("DOMHENRIQUE2", "adriana.fernandes"),
]

def _headers(unidade):
    return {
        "Authorization": f"Bearer {TOKENS[unidade]}",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
    }

def reativar(unidade, login):
    # Tenta endpoint reativar
    r = requests.post(
        f"{ACTIVESOFT_BASE_URL}/api/v0/usuario/{login}/reativar/",
        headers=_headers(unidade), timeout=15
    )
    if r.status_code == 404:
        # Fallback: PATCH ativo=True
        r = requests.patch(
            f"{ACTIVESOFT_BASE_URL}/api/v0/usuario/{login}/",
            headers=_headers(unidade),
            json={"ativo": True}, timeout=15
        )
    return r.status_code in (200, 201, 204), r.status_code

print("=" * 55)
print("  REATIVACAO DE USUARIOS — Rede Apice de Ensino")
print("=" * 55)

ok_count = 0
falha_count = 0
for unidade, login in PARA_REATIVAR:
    sucesso, code = reativar(unidade, login)
    status = "OK" if sucesso else f"FALHA ({code})"
    print(f"  [{unidade:<12}] {login:<30} -> {status}")
    if sucesso:
        ok_count += 1
    else:
        falha_count += 1

print(f"\nReativados: {ok_count} | Falhas: {falha_count}")
