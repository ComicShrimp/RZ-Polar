import tkinter as tk
from math import ceil
from tkinter import ttk

import matplotlib
import matplotlib.animation as animation
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import config

matplotlib.use("TkAgg")


janela_principal = tk.Tk()

DPI = janela_principal.winfo_fpixels("1i")

janela_principal.title("RZ - Polar")
janela_principal.resizable(True, True)
janela_principal.config(bg="white")

largura_janela = janela_principal.winfo_screenwidth()
altura_janela = janela_principal.winfo_screenheight()

janela_principal.geometry("%dx%d+0+0" % (largura_janela, altura_janela))

largura_grafico = largura_janela * 0.85
altura_grafico = altura_janela * 0.85
figura = Figure(figsize=(largura_grafico / DPI, altura_grafico / DPI), dpi=DPI)
graficos = figura.subplots(3)

canvas = FigureCanvasTkAgg(figura, janela_principal)
canvas.get_tk_widget().place(x=1, y=1, relx=0.01, rely=0.01)


def meio_periodo(taxa_amostragem: int):
    meio = int(taxa_amostragem / 2)
    pShaping = np.ones((1, taxa_amostragem), dtype=int)
    pShaping[0, meio:] = 0
    return pShaping[0]


def sinal_sequencia_de_bits(numero_amostras: int, taxa_de_simbolo: int):
    numero_de_simbolo = numero_amostras / taxa_de_simbolo

    sinal_senquencia_bits = 2 * (
        np.random.randint(1, 3, size=int(numero_de_simbolo)) - 1.5
    )
    return (sinal_senquencia_bits + 1) / 2


def sinal_digital(pulso_conformador, sequencia_de_bits, numero_simbolos):
    sinal_digital = []
    for s in range(0, int(numero_simbolos)):
        sinal_auxiliar = sequencia_de_bits[s] * pulso_conformador
        for k in range(0, len(sinal_auxiliar)):
            sinal_digital.append(sinal_auxiliar[k])

    return sinal_digital


def funcao_iniciar():
    if config.INICIAR_ANIMACAO:
        config.INICIAR_ANIMACAO = False
        iniciar_butao["text"] = "Iniciar"
        iniciar_butao["bg"] = "#008000"

    else:
        config.INICIAR_ANIMACAO = True
        iniciar_butao["text"] = "Pausar"
        iniciar_butao["bg"] = "#FF0000"


def define_janela_grafico_digital(valor_bit_para_um: int, valor_bit_para_zero: int):

    if abs(valor_bit_para_um) > abs(valor_bit_para_zero):
        config.MAXIMO_EIXO_DIGITAL_Y = ceil(abs(valor_bit_para_um) * 1.2)
        config.MINIMO_EIXO_DIGITAL_Y = -config.MAXIMO_EIXO_DIGITAL_Y
    else:
        config.MAXIMO_EIXO_DIGITAL_Y = ceil(abs(valor_bit_para_zero) * 1.2)
        config.MINIMO_EIXO_DIGITAL_Y = -config.MAXIMO_EIXO_DIGITAL_Y


def mapeamento_de_bits(
    senquencia_bits, valor_bit_para_um: int, valor_bit_para_zero: int, numero_simbolos
):

    for s in range(0, int(numero_simbolos)):
        if senquencia_bits[s] == 1:
            senquencia_bits[s] = valor_bit_para_um
        elif senquencia_bits[s] == 0:
            senquencia_bits[s] = valor_bit_para_zero

    return senquencia_bits


def limpar_graficos():

    # Sinal Sequ??ncia de Bits
    graficos[0].clear()
    graficos[0].set_ylabel("Sequ??ncia de Bits", fontweight="bold")
    graficos[0].set_ylim(config.MINIMO_EIXO_Y, config.MAXIMO_EIXO_Y)
    graficos[0].set_xlim(0, config.NUMERO_DE_SIMBOLO)
    graficos[0].grid(True)

    # Sinal Digital referente a Sequ??ncia de Bits
    graficos[1].clear()
    graficos[1].set_ylabel("Sinal Digital", fontweight="bold")
    graficos[1].set_ylim(config.MINIMO_EIXO_DIGITAL_Y, config.MAXIMO_EIXO_DIGITAL_Y)
    graficos[1].set_xlim(0, config.NUMERO_AMOSTRAS)
    graficos[1].grid(True)

    # Sinal Pulso Conformador
    graficos[2].clear()
    graficos[2].set_ylabel("Pulso Conformador", fontweight="bold")
    graficos[2].set_ylim(config.MINIMO_EIXO_Y, config.MAXIMO_EIXO_Y)
    graficos[2].grid(True)


def gerar_grafico(i):

    if config.INICIAR_ANIMACAO:

        define_janela_grafico_digital(
            config.VALOR_DE_BITS_PARA_UM, config.VALOR_DE_BITS_PARA_ZERO
        )

        limpar_graficos()

        sinal_pulso_conformador = meio_periodo(config.TAXA_DE_SIMBOLO)

        sequencia_de_bits = sinal_sequencia_de_bits(
            config.NUMERO_AMOSTRAS, config.TAXA_DE_SIMBOLO
        )

        # Fun????o do Sinal de sequ??ncia de Bits
        graficos[0].stem(
            sequencia_de_bits,
            use_line_collection=True,
        )

        # Fun????o do Sinal Digital referente a Sequ??ncia de Bits
        graficos[1].plot(
            sinal_digital(
                sinal_pulso_conformador,
                mapeamento_de_bits(
                    sequencia_de_bits,
                    config.VALOR_DE_BITS_PARA_UM,
                    config.VALOR_DE_BITS_PARA_ZERO,
                    config.NUMERO_DE_SIMBOLO,
                ),
                config.NUMERO_DE_SIMBOLO,
            ),
            "r",
        )
        # Sinal Pulso Conformador
        graficos[2].plot(range(0, config.TAXA_DE_SIMBOLO), sinal_pulso_conformador)


def set_taxa_simbolo(event):
    taxa_de_simbolo_digitada = int(input_taxa_simbolo.get().replace(",", "."))
    if (
        taxa_de_simbolo_digitada >= 0
        and taxa_de_simbolo_digitada <= config.NUMERO_AMOSTRAS
    ):
        config.TAXA_DE_SIMBOLO = taxa_de_simbolo_digitada
        config.NUMERO_DE_SIMBOLO = config.NUMERO_AMOSTRAS / config.TAXA_DE_SIMBOLO
        taxa_simbolo_InfoLabel["text"] = taxa_de_simbolo_digitada
    else:
        tk.messagebox.showerror("Erro", "Taxa de s??mbolos inv??lida")

    input_taxa_simbolo.delete(0, tk.END)


def set_numero_amostras(event):
    numero_amostras_digitada = int(numero_amostras_entrada.get().replace(",", "."))
    if (
        numero_amostras_digitada >= 0
        and numero_amostras_digitada >= config.TAXA_DE_SIMBOLO
    ):
        config.NUMERO_AMOSTRAS = numero_amostras_digitada
        config.NUMERO_DE_SIMBOLO = config.NUMERO_AMOSTRAS / config.TAXA_DE_SIMBOLO
        numero_amostras_infoframe["text"] = numero_amostras_digitada
    else:
        tk.messagebox.showerror("Erro", "N??mero de amostras inv??lida")

    numero_amostras_entrada.delete(0, tk.END)


ani = animation.FuncAnimation(
    figura,
    gerar_grafico,
    interval=1500,
)

# Atribuindo padr??es para a labelframe de n??mero de amostras
numero_amostras_frame = tk.LabelFrame(
    janela_principal,
    text="Taxa de Amostragem",
    width=180,
    height=75,
    borderwidth=0,
)

# Definindo a posi????o da labelframe
numero_amostras_frame.place(
    in_=janela_principal, relx=0.87, rely=0.18, anchor=tk.CENTER
)


numero_amostras_infoframe = tk.Label(
    numero_amostras_frame,
    text=str(config.NUMERO_AMOSTRAS),
)
numero_amostras_infoframe.place(relx=0.5, rely=0.15, anchor=tk.N)
numero_amostras_entrada = tk.Entry(numero_amostras_frame, width=12)
numero_amostras_entrada.place(relx=0.5, rely=0.55, anchor=tk.N)
numero_amostras_entrada.bind("<Return>", set_numero_amostras)


# Atribuindo padr??es para a labelframe da taxa de s??mbolos
taxa_simbolo_Frame = tk.LabelFrame(
    janela_principal,
    text="Taxa de S??mbolos",
    width=180,
    height=75,
    borderwidth=0,
)

# Definindo a posi????o da labelframe
taxa_simbolo_Frame.place(in_=janela_principal, relx=0.87, rely=0.3, anchor=tk.CENTER)


taxa_simbolo_InfoLabel = tk.Label(
    taxa_simbolo_Frame,
    text=str(config.TAXA_DE_SIMBOLO),
)
taxa_simbolo_InfoLabel.place(relx=0.5, rely=0.15, anchor=tk.N)
input_taxa_simbolo = tk.Entry(taxa_simbolo_Frame, width=12)
input_taxa_simbolo.place(relx=0.5, rely=0.55, anchor=tk.N)
input_taxa_simbolo.bind("<Return>", set_taxa_simbolo)


# Atribuindo padr??es para a labelframe do N??mero de Simbolos
numero_simbolo_Frame = tk.LabelFrame(
    janela_principal,
    text="\n\nMapeamento de bit: \n\n1  ???  1 \n 0  ??? -1 \n\n Pulso Conformador:\n Retangular de meio per??odo",
    width=180,
    height=150,
    borderwidth=0,
)

# Definindo a posi????o da labelframe
numero_simbolo_Frame.place(in_=janela_principal, relx=0.87, rely=0.42, anchor=tk.CENTER)


# Atribuindo padr??es para o combobox do pulso conformador
pulso_conformador_frame = tk.LabelFrame(
    janela_principal,
    text="Pulso Conformador",
    width=180,
    height=150,
    borderwidth=0,
)

# Atribuindo os padr??es do bot??o iniciar
iniciar_butao = tk.Button(
    janela_principal,
    width=6,
    height=1,
    font=14,
    bg="#008000",
    fg="#000000",
    text="Iniciar",
    command=funcao_iniciar,
)
# Definindo a posi????o do bot??o iniciar
iniciar_butao.place(relx=0.87, rely=0.835, anchor=tk.N)

tk.mainloop()
