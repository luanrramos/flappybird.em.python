#BIBLIOTECAS UTILIZADAS
import pygame
import os
import random

#NÃO SE CONFUNDIR O NOME DAS CLASSES:
#PASSARO = BOLA DE FUTEBOL DO BRASIL
#CANO = TAÇA DA COPA DO MUNDO

#INSTRUÇÕES:
#1. CRIAÇÃO DO BACKGROUND + IMAGENS
#2. PONTUAÇÃO DO JOGO
#3. TODAS AS ANIMAÇÕES DA BOLA + COLISÃO
#4. MOVIMENTAÇÃO DOS CANOS + COLISÃO
#5. MOVIMENTAÇÃO DO CHÃO
#6. INTERAÇÃO DO USUÁRIO COM A INTERFACE
#7. DINÂMICA E VALIDAÇÃO DOS CANOS
#8. EXECUÇÃO DO JOGO (MAIN FUNCTION)

#TAMANHO DA TELA DO G
TELA_LARGURA = 500
TELA_ALTURA = 800

#CONSTANTES UTILIZADAS + INTEGRAÇÃO DAS IMAGENS
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
IMAGENS_PASSARO = [
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bola1.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bola2.png"))),
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bola3.png")))
]

#PONTUAÇÃO DO GAME (TEXTO)
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont("arial", 30)

#CLASSES E OS MÉTODOS (INIT)

class Passaro:
    IMGS = IMAGENS_PASSARO
    # ANIMAÇÕES DA ROTAÇÃO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    #MÉTODO INIT (DEFININDO VARIÁVEIS DA BOLA)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5 # DESLOCAMENTO APENAS NO EIXO Y
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # CALCULAR O DESLOCAMENTO DA BOLA
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo #FÓRMULA FÍSICA UTILIZADA PARA OBTER A POSIÇÃO DA BOLA
        if deslocamento > 16:
            # RESTRINGIR O DESLOCAMENTO (FACILITAR A JOGATINA)
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento
        #ANGULO DA BOLA NA TELA
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -360:  #ANIMAÇÃO 360 ENQUANTO A BOLA ESTIVER CAINDO
                self.angulo -= self.VELOCIDADE_ROTACAO
    def desenhar(self, tela):
        self.contagem_imagem +=1   #ANIMAÇÃO DA BOLA

        # DEFINIR QUAL IMAGEM DA BOLA SERÁ USADA EM CADA ANIMAÇÃO
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO *2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 +1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # SE A BOLA ESTIVER CAINDO, NÃO VOU GIRAR ELA
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # DESENHAR A IMAGEM E EXIBIR NA TELA
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # COLISÃO --> BOLA
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
class Cano:
    # DIMENSÕES DO CANO
    DISTANCIA = 200
    VELOCIDADE = 5

    #MÉTODO INIT (ANIMAÇÃO DO CANO)
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # MOVIMENTAÇÃO DO CANO (NO EIXO)
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    # DESENHO DO CANO
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    # COLISÃO --> CANO
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        #VERIFICAR SE COLIDIU (TRUE OR FALSE)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        if base_ponto or topo_ponto:
            return True
        else:
            return False
class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    # MÉTODO INIT (ANIMAÇÃO DO CHÃO)
    #X1 = CHÃO 1 (APÓS SAIR DA INTERFACE DA TELA)
    #X2 = CHÃO 2 (CHÃO QUE O PÁSSARO AINDA PASSARÁ)

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    #MOVIMENTAÇÃO DO CHÃO
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA <0:
            self.x2 = self.x1 + self.LARGURA

    #DESENHO DO CHÃO
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

#FUNÇÃO AUXILIAR QUE VAI FAZER A TELA DO GAME
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255)) #INTEGRAÇÃO DO TEXTO NA TELA
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


#FUNÇÃO QUE EXECUTA O JOGO (INTERFACE) + DINÂMICA DOS CANOS
def main():
    #Posição onde o passáro aparece na tela
    # Valores ajustáveis
    passaros = [Passaro(230, 350)]
    chao = Chao(730) #Posição Y
    canos = [Cano(700)] #Posição X
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA)) #Criação da tela
    pontos = 0
    relogio = pygame.time.Clock() #Atualização da tela (JÁ EMBUTIDO NO PYGAME)


    #ESTRUTURA DE REPETIÇÃO RESPONSÁVEL PELO CONTROLE DE FINALIZAÇÃO DO PROGRAMA
    rodando = True
    while rodando:
        relogio.tick(30) #QUANTOS QUADROS POR SEGUNDOS ELE VAI ATUALIZAR A TELA

        #INTERAÇÃO DO USUÁRIO COM A INTERFACE
        for evento in pygame.event.get(): #RECONHECIMENTO DAS TECLAS DO TECLADO PELO PYGAME
            if evento.type == pygame.QUIT:  #SE O USUARIO CLICAR NO Xzinho PARA FECHAR A ABA
                rodando = False #Loop desativo
                pygame.quit() #(Encerramento do jogo)
                quit()
            if evento.type == pygame.KEYDOWN: #SE O USUARIO APERTA EM ALGUMA TECLA
                if evento.key == pygame.K_SPACE: #SE O USUARIO APERTA NA TECLA ESPAÇO
                    for passaro in passaros:
                        passaro.pular()
        #MOVIMENTAÇÃO DO PÁSSARO NA TELA
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        #Validar se o pássaro já passou do cano seguinte
        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros): # i = POSIÇÃO DO PÁSSARO DENTRO DA LISTA
                if cano.colidir(passaro): #SE A BOLA BATER NO CANO
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x: #SE A BOLA JÁ PASSOU DO CANO SEGUINTE, CRIE O PROXIMO CANO
                    cano.passou = True
                    adicionar_cano = True
            #EXCLUIR O CANO, APOS A BOLA PASSAR DELE, SAIR DA TELA
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600)) #VALOR AJUSTÁVEL
        for cano in remover_canos:
            canos.remove(cano)
        #DEFINIR "MORTE DO BOLA" SE ELE SUBIR PRO TETO OU CAIR NO CHÃO
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)


        desenhar_tela(tela, passaros, canos, chao, pontos)


#EXECUTAR FUNÇÃO MAIN
if __name__ == '__main__':
    main()
