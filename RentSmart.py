
import csv



class Imovel:
    def __init__(self, tipo, quartos):
        self.tipo = tipo
        self.quartos = quartos

        if tipo == "apartamento":
            self.valor_base = 700

        elif tipo == "casa":
            self.valor_base = 900

        else:
            self.valor_base = 1200

    def adicional_quartos(self):
        if self.quartos == 2:
            if self.tipo == "apartamento":
                return 200
            elif self.tipo == "casa":
                return 250

        return 0



class Locacao:
    TAXA_CONTRATO = 2000

    def __init__(self, imovel, garagem, vagas_extra,
                 sem_criancas, parcelas):
        self.imovel = imovel
        self.garagem = garagem
        self.vagas_extra = vagas_extra
        self.sem_criancas = sem_criancas
        self.parcelas = parcelas

    def calcular_garagem(self):
        if self.imovel.tipo in ["apartamento", "casa"]:
            return 300 if self.garagem else 0

        if self.imovel.tipo == "estudio":
            if self.garagem:
                return 250 + (self.vagas_extra * 60)

        return 0

    def calcular_desconto(self):
        if self.imovel.tipo == "apartamento" and self.sem_criancas:
            valor = self.imovel.valor_base
            valor += self.imovel.adicional_quartos()
            valor += self.calcular_garagem()

            return valor * 0.05

        return 0

    def calcular_aluguel(self):
        valor = self.imovel.valor_base
        valor += self.imovel.adicional_quartos()
        valor += self.calcular_garagem()
        valor -= self.calcular_desconto()

        return round(valor, 2)

    def calcular_parcela_contrato(self):
        return round(self.TAXA_CONTRATO / self.parcelas, 2)

    def apresentar_orcamento(self):
        print("\n========== RENTSMART ==========")
        print(f"Imóvel: {self.imovel.tipo}")
        print(f"Quartos: {self.imovel.quartos}")
        print(f"Aluguel-base: R$ {self.imovel.valor_base:.2f}")
        print(f"Adicional de quartos: R$ {self.imovel.adicional_quartos():.2f}")
        print(f"Garagem/estacionamento: R$ {self.calcular_garagem():.2f}")
        print(f"Desconto: R$ {self.calcular_desconto():.2f}")

        print("-------------------------------")
        print(f"Aluguel mensal: R$ {self.calcular_aluguel():.2f}")
        print(f"Taxa contratual: R$ {self.TAXA_CONTRATO:.2f}")
        print(f"Parcelas do contrato: {self.parcelas}")
        print(f"Valor de cada parcela: R$ {self.calcular_parcela_contrato():.2f}")
        print("===============================")



class Relatorio:
    def __init__(self, locacao):
        self.locacao = locacao

    def gerar_csv(self):
        aluguel = self.locacao.calcular_aluguel()
        parcela = self.locacao.calcular_parcela_contrato()

        with open("projecao_rentsmart.csv", "w",
                  newline="", encoding="utf-8-sig") as arquivo:

            escritor = csv.writer(arquivo, delimiter=";")

            escritor.writerow([
                "Mes",
                "Aluguel",
                "Parcela Contratual",
                "Total Mensal"
            ])

            for mes in range(1, 13):
                taxa = parcela if mes <= self.locacao.parcelas else 0
                total = aluguel + taxa

                escritor.writerow([
                    mes,
                    f"{aluguel:.2f}",
                    f"{taxa:.2f}",
                    f"{total:.2f}"
                ])

        print("\nArquivo CSV gerado com sucesso!")



def solicitar_numero(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))

            if minimo <= valor <= maximo:
                return valor

            print(f"Digite um número entre {minimo} e {maximo}.")

        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")



def main():

    print("===== BEM-VINDO AO RENTSMART =====")

    print("\nTipos de imóveis:")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")

    opcao = solicitar_numero("Escolha o imóvel: ", 1, 3)

    tipos = {
        1: "apartamento",
        2: "casa",
        3: "estudio"
    }

    tipo = tipos[opcao]

    if tipo == "estudio":
        quartos = 0
    else:
        quartos = solicitar_numero(
            "Quantidade de quartos (1 ou 2): ", 1, 2
        )

    imovel = Imovel(tipo, quartos)

    
    garagem = False
    vagas_extra = 0

    if tipo in ["apartamento", "casa"]:
        resposta = solicitar_numero(
            "Deseja uma vaga de garagem? (1-Sim / 0-Não): ", 0, 1
        )
        garagem = resposta == 1

    elif tipo == "estudio":
        resposta = solicitar_numero(
            "Deseja o pacote de estacionamento com 2 vagas? "
            "(1-Sim / 0-Não): ", 0, 1
        )

        garagem = resposta == 1

        if garagem:
            vagas_extra = solicitar_numero(
                "Quantas vagas adicionais deseja? ", 0, 100
            )

    
    sem_criancas = False

    if tipo == "apartamento":
        resposta = solicitar_numero(
            "Não possui crianças? (1-Sim / 0-Não): ", 0, 1
        )
        sem_criancas = resposta == 1

    
    parcelas = solicitar_numero(
        "Em quantas parcelas deseja pagar o contrato (1 a 5)? ",
        1, 5
    )

    
    locacao = Locacao(
        imovel,
        garagem,
        vagas_extra,
        sem_criancas,
        parcelas
    )

    
    locacao.apresentar_orcamento()

    
    relatorio = Relatorio(locacao)
    relatorio.gerar_csv()


if __name__ == "__main__":
    main()
