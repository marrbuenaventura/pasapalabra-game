from generales.generales import *
from eventos.eventos_menu import *
from pantallas.pantallas_juego import aplicar_brillo
import pygame
import random
from funciones_archivos import verificar_usuario_existe, inicializar_usuario_en_juego
from bucles_funciones import *

def obtener_usuario_con_estilo(ventana: pygame.Surface, estado_global: dict) -> str:
    """Pantalla estilizada para obtener el usuario"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    bucle_animacion_fade_in(ventana, estado_global, "¡BIENVENIDO A PASAPALABRA!", colores, ancho, alto)
    
    resultado = ""
    while not resultado:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("¡BIENVENIDO A PASAPALABRA!", True, colores["AZUL"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)
        
        subtitulo = estado_global["fuentes"]["boton"].render("Prepárate para el desafío definitivo", True, colores["NEGRO"])
        subtitulo_rect = subtitulo.get_rect(center=(ancho // 2, alto // 4 + 80))
        ventana.blit(subtitulo, subtitulo_rect)
        
        instruccion = estado_global["fuentes"]["pequena"].render("Ingresa tu nombre de usuario para comenzar:", True, colores["NEGRO"])
        instruccion_rect = instruccion.get_rect(center=(ancho // 2, alto // 2))
        ventana.blit(instruccion, instruccion_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        usuario = pedir_texto_estilizado(ventana, estado_global, "")
        
        if usuario:
            if verificar_usuario_existe(usuario):
                if preguntar_si_ya_jugo_estilizado(ventana, estado_global, usuario):
                    estado_global, mensaje_bienvenida = inicializar_usuario_en_juego(usuario, estado_global)
                    mostrar_mensaje_estilizado(ventana, estado_global, "¡Bienvenido de nuevo!", mensaje_bienvenida, 3)
                    resultado = usuario
                else:
                    mostrar_mensaje_estilizado(ventana, estado_global, "Usuario ya existe", "Prueba con otro nombre", 2)
            else:
                estado_global, mensaje_bienvenida = inicializar_usuario_en_juego(usuario, estado_global)
                mostrar_mensaje_estilizado(ventana, estado_global, "¡Nuevo jugador!", mensaje_bienvenida, 3)
                resultado = usuario
    
    return resultado

def elegir_dificultad_con_estilo(ventana: pygame.Surface, estado_global: dict) -> str:
    """Pantalla estilizada para elegir dificultad"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    opciones = ["facil", "dificil"]
    seleccion = 0
    reloj = pygame.time.Clock()
    
    bucle_animacion_slide_down(ventana, estado_global, "ELIGE TU DESAFÍO", colores, ancho, alto)
    
    resultado = ""
    while not resultado:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("ELIGE TU DESAFÍO", True, colores["AZUL"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)
        
        desc = estado_global["fuentes"]["pequena"].render("Usa ↑↓ para navegar, ENTER para seleccionar", True, colores["NEGRO"])
        desc_rect = desc.get_rect(center=(ancho // 2, alto // 3))
        ventana.blit(desc, desc_rect)
        
        bucle_dibujar_opciones_estilizadas(ventana, estado_global, opciones, seleccion, colores, ancho, alto, "vertical")
        
        # Agregar descripciones
        descripciones = ["Perfecto para principiantes", "Para expertos del juego"]
        for i, desc_dif in enumerate(descripciones):
            y_pos = alto // 2 + i * 100
            if i == seleccion:
                desc_texto = estado_global["fuentes"]["pequena"].render(desc_dif, True, colores["AZUL"])
            else:
                desc_texto = estado_global["fuentes"]["pequena"].render(desc_dif, True, colores["NEGRO"])
            desc_rect = desc_texto.get_rect(center=(ancho // 2, y_pos + 25))
            ventana.blit(desc_texto, desc_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        accion, evento = bucle_eventos_prejuego_basico()
        if accion == "arriba":
            seleccion = (seleccion - 1) % len(opciones)
        elif accion == "abajo":
            seleccion = (seleccion + 1) % len(opciones)
        elif accion == "enter":
            resultado = opciones[seleccion]
        
        reloj.tick(60)
    
    return resultado

def mostrar_resumen_partida(ventana: pygame.Surface, estado_global: dict, usuario: str, dificultad: str, categoria: str):
    """Muestra un resumen bonito de la configuración de partida"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    reloj = pygame.time.Clock()
    tiempo_inicio = pygame.time.get_ticks()
    duracion = 3000
    
    while pygame.time.get_ticks() - tiempo_inicio < duracion:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("¡LISTOS PARA JUGAR!", True, colores["VERDE"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)
        
        contenedor_ancho = 500
        contenedor_alto = 300
        contenedor_x = (ancho - contenedor_ancho) // 2
        contenedor_y = alto // 2 - contenedor_alto // 2
        
        pygame.draw.rect(ventana, (0, 0, 0, 30), (contenedor_x + 5, contenedor_y + 5, contenedor_ancho, contenedor_alto), border_radius=20)
        
        pygame.draw.rect(ventana, colores["AZUL"], (contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto), border_radius=20)
        pygame.draw.rect(ventana, colores["BLANCO"], (contenedor_x + 5, contenedor_y + 5, contenedor_ancho - 10, contenedor_alto - 10), border_radius=15)
        
        info_items = [
            f"Jugador: {usuario.upper()}",
            f"Dificultad: {dificultad.upper()}",
            f"Categoría: {categoria.upper()}",
            f"Tiempo: 3 minutos"
        ]
        
        bucle_mostrar_items_info(ventana, estado_global, info_items, contenedor_y, ancho)
        
        prep_texto = estado_global["fuentes"]["pequena"].render("¡Prepárate para el desafío!", True, colores["VERDE"])
        prep_rect = prep_texto.get_rect(center=(ancho // 2, alto - 100))
        ventana.blit(prep_texto, prep_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        accion, evento = bucle_eventos_prejuego_basico()
        # Solo salir en caso de quit (manejado dentro del bucle)
        
        reloj.tick(60)

def cuenta_regresiva_estilizada(ventana: pygame.Surface, estado_global: dict):
    """Cuenta regresiva con efectos visuales"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    bucle_cuenta_regresiva_animada(ventana, estado_global, colores, ancho, alto)
    bucle_fade_in_final(ventana, estado_global, "¡COMIENZA!", colores, ancho, alto)
    
    pygame.time.delay(800)

def pedir_texto_estilizado(ventana: pygame.Surface, estado_global: dict, prompt: str, max_len: int = 15) -> str:
    """Versión estilizada de pedir texto"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    texto = ""
    cursor_visible = True
    tiempo_cursor = pygame.time.get_ticks()
    resultado = ""
    
    while not resultado:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("¡BIENVENIDO A PASAPALABRA!", True, colores["AZUL"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)
        
        campo_ancho = 400
        campo_alto = 60
        campo_x = (ancho - campo_ancho) // 2
        campo_y = alto // 2
        
        pygame.draw.rect(ventana, colores["GRIS"], (campo_x - 2, campo_y - 2, campo_ancho + 4, campo_alto + 4), border_radius=12)
        pygame.draw.rect(ventana, colores["BLANCO"], (campo_x, campo_y, campo_ancho, campo_alto), border_radius=10)
        
        texto_mostrar = texto
        if pygame.time.get_ticks() - tiempo_cursor > 500:
            cursor_visible = not cursor_visible
            tiempo_cursor = pygame.time.get_ticks()
        
        if cursor_visible:
            texto_mostrar += "|"
        
        texto_render = estado_global["fuentes"]["boton"].render(texto_mostrar, True, colores["NEGRO"])
        ventana.blit(texto_render, (campo_x + 15, campo_y + 15))
        
        instruccion = estado_global["fuentes"]["pequena"].render("Presiona ENTER para continuar", True, colores["AZUL"])
        instruccion_rect = instruccion.get_rect(center=(ancho // 2, campo_y + 100))
        ventana.blit(instruccion, instruccion_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        accion, evento = bucle_eventos_prejuego_basico()
        if accion == "backspace":
            texto = texto[:-1]
        elif accion == "enter" and len(texto.strip()) > 0:
            resultado = texto.strip()
        elif accion == "caracter" and len(texto) < max_len:
            texto += evento.unicode
    
    return resultado

def preguntar_si_ya_jugo_estilizado(ventana: pygame.Surface, estado_global: dict, usuario: str) -> bool:
    """Pregunta estilizada si ya jugó antes"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    opciones = ["si", "no"]
    seleccion = 0
    reloj = pygame.time.Clock()
    resultado = None
    
    while resultado is None:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("¡USUARIO ENCONTRADO!", True, colores["VERDE"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)
        
        pregunta = estado_global["fuentes"]["boton"].render(f"Hola {usuario.upper()}, ¿ya jugaste antes?", True, colores["NEGRO"])
        pregunta_rect = pregunta.get_rect(center=(ancho // 2, alto // 3))
        ventana.blit(pregunta, pregunta_rect)
        
        instruccion = estado_global["fuentes"]["pequena"].render("Usa ←→ para navegar, ENTER para seleccionar", True, colores["NEGRO"])
        instruccion_rect = instruccion.get_rect(center=(ancho // 2, alto // 3 + 50))
        ventana.blit(instruccion, instruccion_rect)
        
        bucle_dibujar_opciones_estilizadas(ventana, estado_global, opciones, seleccion, colores, ancho, alto, "horizontal")
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        accion, evento = bucle_eventos_prejuego_basico()
        if accion == "izquierda":
            seleccion = (seleccion - 1) % len(opciones)
        elif accion == "derecha":
            seleccion = (seleccion + 1) % len(opciones)
        elif accion == "enter":
            resultado = opciones[seleccion] == "si"
        
        reloj.tick(60)
    
    return resultado

def mostrar_mensaje_estilizado(ventana: pygame.Surface, estado_global: dict, titulo: str, mensaje: str, segundos: int):
    """Muestra un mensaje con estilo"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    tiempo_inicio = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - tiempo_inicio < segundos * 1000:
        ventana.fill(colores["BLANCO"])
        
        titulo_render = estado_global["fuentes"]["boton"].render(titulo, True, colores["ROJO"])
        titulo_rect = titulo_render.get_rect(center=(ancho // 2, alto // 2 - 30))
        ventana.blit(titulo_render, titulo_rect)
        
        mensaje_render = estado_global["fuentes"]["pequena"].render(mensaje, True, colores["NEGRO"])
        mensaje_rect = mensaje_render.get_rect(center=(ancho // 2, alto // 2 + 20))
        ventana.blit(mensaje_render, mensaje_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        
        accion, evento = bucle_eventos_prejuego_basico()
        # Solo salir en caso de quit (manejado dentro del bucle)

def elegir_categoria_aleatoria() -> str:
    """Elige una categoría aleatoria"""
    categorias = ["cine", "musica"]
    return random.choice(categorias)

def mostrar_categoria_elegida_estilizada(ventana: pygame.Surface, estado_global: dict, categoria: str):
    """Muestra la categoría elegida con animación bonita"""
    modo_actual = estado_global.get("modo", "normal")
    colores = estado_global["colores"][modo_actual]
    ancho = estado_global["config"]["ventana"]["ancho"]
    alto = estado_global["config"]["ventana"]["alto"]
    
    categoria_texto = categoria.upper()
    tiempo_letra = 150
    pausa_final = 1500
    reloj = pygame.time.Clock()
    
    # Usar bucle para animación letra por letra
    letras_mostradas, terminado = bucle_animacion_categoria_letra_por_letra(
        ventana, estado_global, categoria_texto, colores, ancho, alto, tiempo_letra
    )
    
    # Pausa final
    tiempo_pausa_inicio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - tiempo_pausa_inicio < pausa_final:
        ventana.fill(colores["BLANCO"])
        
        titulo = estado_global["fuentes"]["titulo"].render("¡CATEGORÍA ELEGIDA!", True, colores["AZUL"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)

        base_render = estado_global["fuentes"]["boton"].render("Categoría seleccionada:", True, colores["NEGRO"])
        base_rect = base_render.get_rect(center=(ancho // 2, alto // 2 - 40))
        ventana.blit(base_render, base_rect)

        # Contenedor final
        contenedor_ancho = 300
        contenedor_alto = 80
        contenedor_x = (ancho - contenedor_ancho) // 2
        contenedor_y = alto // 2 - 10
        
        pygame.draw.rect(ventana, colores["VERDE"], (contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto), border_radius=15)
        pygame.draw.rect(ventana, colores["BLANCO"], (contenedor_x + 3, contenedor_y + 3, contenedor_ancho - 6, contenedor_alto - 6), border_radius=12)
        
        categoria_render = estado_global["fuentes"]["titulo"].render(categoria_texto, True, colores["VERDE"])
        categoria_rect = categoria_render.get_rect(center=(ancho // 2, alto // 2 + 30))
        ventana.blit(categoria_render, categoria_rect)

        if categoria == "cine":
            descripcion = "🎬 Películas, actores y directores"
        else:
            descripcion = "🎵 Cantantes, bandas y canciones"
        
        desc_render = estado_global["fuentes"]["pequena"].render(descripcion, True, colores["NEGRO"])
        desc_rect = desc_render.get_rect(center=(ancho // 2, alto // 2 + 100))
        ventana.blit(desc_render, desc_rect)

        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()

        accion, evento = bucle_eventos_prejuego_basico()
        # Solo salir en caso de quit (manejado dentro del bucle)
        
        reloj.tick(60)