# TEE PELI TÄHÄN
"""#############################################################################################
Ohjelma:    Robottipeli

Tiedostot:    main.py, robo.pgn
    
Kuvaus:    Robotti liikkuu ruudukossa hiirellä vetämällä kuten ratsu shakkipelissä. 
            Pelin tarkoitus on käydä kaikissa ruuduissa mahdollisimman vähillä siirroilla.

Tekijä:    Pekka Paldánius (PP)


Huomautus:        Tämä on MOOC-ohjelmoinnin jatkokurssin viimeinen harjoitus

Päivitykset:    0.1 2.5.2022 (PP)
 
################################################################################################"""


import pygame

class Ruutu:
    def __init__(self, i: int, j: int):
        self.i = i
        self.j = j
        self.x = 5 + i * 75
        self.y = 10 + j * 105
        self.vari = (0, 255, 0)

class Robotti:
    def __init__(self):
        self.kuva = pygame.image.load("robo.png")
        self.x = 0
        self.y = 0   
        self.on_liikkeessa = False

    def osui(self, x: int, y: int):
        if x >= self.x and x <= self.x + self.kuva.get_width() and y >= self.y and y <= self.y + self.kuva.get_height():
            return True
        else:
            return False

    def palaa(self, ruutu: Ruutu):
        if self.x > ruutu.x + 10:
            self.x -= 2
        if self.x < ruutu.x + 10:
            self.x += 2
        if self.y >  ruutu.y + 10:
            self.y -= 2
        if self.y <  ruutu.y + 10:
            self.y += 2

    def oikea_siirto(self, nykyinen_ruutu: Ruutu, ij: tuple):
        ylos_alas = False
        sivulle = False
        ylos_alas = abs(ij[0] - nykyinen_ruutu.i) == 1 and abs(ij[1] - nykyinen_ruutu.j) == 2
        sivulle = abs(ij[0] - nykyinen_ruutu.i) == 2 and abs(ij[1] - nykyinen_ruutu.j) == 1
        if ylos_alas or sivulle:
            return True
        else:
            return False

    def aseta_ruutuun(self, ruutu: Ruutu):
        self.x = ruutu.x + 10
        self.y = ruutu.y + 10

    def katso_ruutu(self):
        i = -1
        j = -1
        if self.x >= 5 and self.x < 80:
            i = 0
        elif self.x >= 80 and self.x < 135:
            i = 1
        elif self.x >= 135 and self.x < 210:
            i = 2
        elif self.x >= 210 and self.x < 285:
            i = 3
        elif self.x >= 285 and self.x < 360:
            i = 4    
        elif self.x >= 360 and self.x < 435:
            i = 5
        elif self.x >= 435 and self.x < 510:
            i = 6
        elif self.x >= 510 and self.x <= 580:
            i = 7

        if self.y >= 10 and self.y < 120:
            j = 0
        elif self.y >= 120 and self.y < 230:
            j = 1
        elif self.y >= 230 and self.y < 340:
            j = 2
        elif self.y >= 340 and self.y <= 440:
            j = 3
        return (i, j)

class RobottiPeli:
    def __init__(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.naytto = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Robottipeli")
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.siirrot = 0
        self.siirto_oikein = True
        self.ruudut = dict()
        for i in range(8):
            for j in range(4):
                self.ruudut[(i, j)] = Ruutu(i, j)
        self.nykyinen_ruutu = Ruutu(5, 2)
        self.robotti = Robotti()
        self.robotti.aseta_ruutuun(self.nykyinen_ruutu)
        self.ruudut[(5, 2)].vari = (135,206,250)
        self.silmukka()

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.kello.tick(60)

    def tutki_tapahtumat(self):
        offset_x = 0
        offset_y = 0
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()
            elif tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                if tapahtuma.button == 1:
                    if self.robotti.osui(tapahtuma.pos[0], tapahtuma.pos[1]):
                        self.robotti.on_liikkeessa = True
                        self.siirto_oikein = False
                        mouse_x, mouse_y = tapahtuma.pos
                        offset_x = self.robotti.x - mouse_x
                        offset_y = self.robotti.y - mouse_y
            elif tapahtuma.type == pygame.MOUSEBUTTONUP:
                if tapahtuma.button == 1:            
                    self.robotti.on_liikkeessa = False
                    ij = self.robotti.katso_ruutu()
                    if self.robotti.oikea_siirto(self.nykyinen_ruutu, ij):
                        self.siirto_oikein = True
                        self.robotti.aseta_ruutuun(self.ruudut[ij])
                        self.ruudut[ij].vari = (135,206,250)
                        self.siirrot += 1
                        self.nykyinen_ruutu =  self.ruudut[ij]
            elif tapahtuma.type == pygame.MOUSEMOTION:
                if self.robotti.on_liikkeessa:
                    mouse_x, mouse_y = tapahtuma.pos
                    self.robotti.x = mouse_x + offset_x
                    self.robotti.y = mouse_y + offset_y
            elif tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_F2:
                    RobottiPeli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
        
    def piirra_naytto(self):
        if not self.siirto_oikein:
            self.robotti.palaa(self.nykyinen_ruutu)
        self.naytto.fill((0, 0, 0))
        for i in range(8):
            for j in range(4):
                pygame.draw.rect(self.naytto, self.ruudut[(i, j)].vari, (self.ruudut[(i, j)].x, self.ruudut[(i, j)].y, 70, 100))
        self.naytto.blit(self.robotti.kuva, (self.robotti.x, self.robotti.y))
        if self.peli_lapi():
            teksti = self.fontti.render("Onnittelut, läpäisit pelin!", True, (255, 0, 0))
            self.naytto.blit(teksti, (25, 430))
        else:
            teksti = self.fontti.render("Käy kaikissa ruuduissa mahdollisimman vähillä siirroilla", True, (255, 0, 0))
            self.naytto.blit(teksti, (25, 430))
        teksti = self.fontti.render("Siirrot: " + str(self.siirrot), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, 450))
        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (200, 450))
        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (400, 450))
        pygame.display.flip()

    def peli_lapi(self):
        for avain in self.ruudut:
            if self.ruudut[avain].vari == (0, 255, 0):
                return False
        return True

if __name__ == "__main__":
    RobottiPeli()