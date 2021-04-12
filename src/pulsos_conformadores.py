import numpy as np


def periodo_completo(taxa_amostragem: int):
    pShaping = np.ones((1, taxa_amostragem), dtype=int)

    return pShaping[0]


def meio_periodo(taxa_amostragem: int):
    meio = int(taxa_amostragem / 2)
    pShaping = np.ones((1, taxa_amostragem), dtype=int)
    pShaping[0, meio:] = 0
    return pShaping[0]


dicionario_pulso_conformador = {
    "Retangular: Meio Período": meio_periodo,
    "Retangular: Período Completo": periodo_completo,
}