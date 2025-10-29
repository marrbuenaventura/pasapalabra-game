from menu.menu_principal import menu_principal
from funciones_archivos import *
import pygame
from generales.config_manager_algorithmic import inicializar_configuracion

if __name__ == "__main__":
    pygame.init()
    estado = inicializar_configuracion()
    pantalla = pygame.display.set_mode((estado["ventana"]["ancho"], estado["ventana"]["alto"]))
    pygame.display.set_caption(estado["ventana"]["titulo"])
    icono = pygame.image.load(estado["ventana"]["icono"])
    pygame.display.set_icon(icono)

    lineas_estadisticas = leer_estadisticas("csv/estadisticas.csv")
    menu_principal(pantalla, lineas_estadisticas, estado)
