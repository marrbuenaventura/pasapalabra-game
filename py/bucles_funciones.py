import pygame
import sys
import os
import json

def bucle_recorrer_lista_con_archivo(lista: list, archivo, funcion):
    """Bucle para recorrer una lista y aplicar función con archivo"""
    for elemento in lista:
        funcion(elemento, archivo)

def bucle_calcular_estadisticas_usuario(historial: list) -> tuple:
    """Bucle para calcular estadísticas de usuario desde historial JSON"""
    if not historial:
        return 0, 0, 0, 0, 0, 0
    
    total_aciertos = 0
    total_errores = 0
    total_tiempo = 0
    total_puntaje = 0
    mejor_puntaje = 0
    
    for partida in historial:
        total_aciertos += partida["aciertos"]
        total_errores += partida["errores"]
        total_tiempo += partida["tiempo"]
        total_puntaje += partida["puntaje"]
        if partida["puntaje"] > mejor_puntaje:
            mejor_puntaje = partida["puntaje"]
    
    return total_aciertos, total_errores, total_tiempo, total_puntaje, mejor_puntaje, len(historial)

def bucle_procesar_ranking_general(todos_los_datos: dict) -> list:
    """Bucle para procesar ranking general desde JSON"""
    ranking = []
    
    for usuario, partidas in todos_los_datos.items():
        for partida in partidas:
            ranking.append({
                "usuario": usuario,
                "puntaje": partida["puntaje"],
                "aciertos": partida["aciertos"],
                "errores": partida["errores"],
                "tiempo": partida["tiempo"]
            })
    
    return ranking

def bucle_generar_lineas_ranking(ranking: list, limite: int) -> list:
    """Bucle para generar líneas CSV desde ranking ordenado"""
    lineas = ["usuario;aciertos;errores;tiempo;puntaje\n"]
    
    for entrada in ranking[:limite]:
        linea = f'{entrada["usuario"]};{entrada["aciertos"]};{entrada["errores"]};{entrada["tiempo"]};{entrada["puntaje"]}\n'
        lineas.append(linea)
    
    return lineas

def bucle_convertir_historial_a_csv(historial_json: list, usuario: str) -> list:
    """Bucle para convertir historial JSON a líneas CSV"""
    lineas = ["usuario;aciertos;errores;tiempo;puntaje\n"]
    
    if historial_json:
        for partida in historial_json:
            linea = f'{usuario};{partida["aciertos"]};{partida["errores"]};{partida["tiempo"]};{partida["puntaje"]}\n'
            lineas.append(linea)
    
    return lineas

def bucle_migrar_csv_lineas(lineas: list) -> list:
    """Bucle para migrar líneas CSV a formato JSON"""
    estadisticas_migradas = []
    
    for linea in lineas[1:]: 
        campos = linea.strip().split(";")
        if len(campos) >= 5:
            estadistica = {
                "usuario": campos[0],
                "aciertos": int(campos[1]),
                "errores": int(campos[2]),
                "tiempo": float(campos[3]),
                "puntaje": int(campos[4])
            }
            estadisticas_migradas.append(estadistica)
    
    return estadisticas_migradas

def bucle_obtener_usuarios_con_stats(usuarios: list) -> list:
    """Bucle para obtener usuarios con sus estadísticas"""
    from funciones_historial_pygame import calcular_estadisticas_usuario_desde_json
    
    usuarios_con_stats = []
    for usuario in usuarios:
        stats = calcular_estadisticas_usuario_desde_json(usuario)
        if stats["partidas_jugadas"] > 0:
            usuarios_con_stats.append({
                "usuario": usuario,
                "promedio_puntaje": stats["promedio_puntaje"],
                "partidas": stats["partidas_jugadas"]
            })
    
    return usuarios_con_stats

def bucle_animacion_fade_in(ventana: pygame.Surface, estado_global: dict, titulo: str, colores: dict, ancho: int, alto: int):
    """Bucle para animación de fade in de texto"""
    for alpha in range(0, 256, 15):
        ventana.fill(colores["BLANCO"])
        
        titulo_render = estado_global["fuentes"]["titulo"].render(titulo, True, colores["AZUL"])
        titulo_surface = titulo_render.copy()
        titulo_surface.set_alpha(alpha)
        titulo_rect = titulo_render.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo_surface, titulo_rect)
        
        from pantallas.pantallas_juego import aplicar_brillo
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        pygame.time.delay(50)

def bucle_animacion_slide_down(ventana: pygame.Surface, estado_global: dict, titulo: str, colores: dict, ancho: int, alto: int) -> bool:
    """Bucle para animación de deslizamiento hacia abajo"""
    from pantallas.pantallas_juego import aplicar_brillo
    reloj = pygame.time.Clock()
    
    offset_y = alto
    target_y = 0
    
    while offset_y > target_y:
        offset_y -= 30
        if offset_y < target_y:
            offset_y = target_y
            
        ventana.fill(colores["BLANCO"])
        
        titulo_render = estado_global["fuentes"]["titulo"].render(titulo, True, colores["AZUL"])
        titulo_rect = titulo_render.get_rect(center=(ancho // 2, alto // 4 + offset_y))
        ventana.blit(titulo_render, titulo_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        reloj.tick(60)
    
    return True

def bucle_eventos_prejuego_basico() -> tuple:
    """Bucle básico de eventos para prejuego"""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                return "arriba", evento
            elif evento.key == pygame.K_DOWN:
                return "abajo", evento
            elif evento.key == pygame.K_LEFT:
                return "izquierda", evento
            elif evento.key == pygame.K_RIGHT:
                return "derecha", evento
            elif evento.key == pygame.K_RETURN:
                return "enter", evento
            elif evento.key == pygame.K_BACKSPACE:
                return "backspace", evento
            elif evento.unicode.isprintable():
                return "caracter", evento
    
    return "nada", None

def bucle_cuenta_regresiva_animada(ventana: pygame.Surface, estado_global: dict, colores: dict, ancho: int, alto: int):
    """Bucle para cuenta regresiva con animación"""
    from pantallas.pantallas_juego import aplicar_brillo
    
    for numero in [3, 2, 1]:

        for escala in range(50, 151, 10):
            ventana.fill(colores["BLANCO"])
            
            radio_circulo = int(escala * 1.5)
            pygame.draw.circle(ventana, colores["AZUL"], (ancho // 2, alto // 2), radio_circulo, 5)
            
            fuente_grande = pygame.font.SysFont("arial", escala, bold=True)
            texto = fuente_grande.render(str(numero), True, colores["AZUL"])
            texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
            ventana.blit(texto, texto_rect)
            
            aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
            pygame.display.flip()
            pygame.time.delay(50)

        for _ in range(20):
            ventana.fill(colores["BLANCO"])
            
            pygame.draw.circle(ventana, colores["AZUL"], (ancho // 2, alto // 2), 150, 5)
            
            fuente_final = pygame.font.SysFont("arial", 150, bold=True)
            texto = fuente_final.render(str(numero), True, colores["AZUL"])
            texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
            ventana.blit(texto, texto_rect)
            
            aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
            pygame.display.flip()
            pygame.time.delay(50)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

def bucle_fade_in_final(ventana: pygame.Surface, estado_global: dict, texto: str, colores: dict, ancho: int, alto: int):
    """Bucle para fade in del texto final"""
    from pantallas.pantallas_juego import aplicar_brillo
    
    for alpha in range(0, 256, 20):
        ventana.fill(colores["BLANCO"])
        
        texto_final = estado_global["fuentes"]["titulo"].render(texto, True, colores["VERDE"])
        texto_surface = texto_final.copy()
        texto_surface.set_alpha(alpha)
        texto_rect = texto_final.get_rect(center=(ancho // 2, alto // 2))
        ventana.blit(texto_surface, texto_rect)
        
        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        pygame.time.delay(50)

def bucle_dibujar_opciones_estilizadas(ventana: pygame.Surface, estado_global: dict, opciones: list, 
                                      seleccion: int, colores: dict, ancho: int, alto: int, tipo: str = "vertical"):
    """Bucle para dibujar opciones de menú estilizadas"""
    if tipo == "vertical":
        for i, opcion in enumerate(opciones):
            y_pos = alto // 2 + i * 100
            
            rect_ancho = 300
            rect_alto = 70
            rect_x = (ancho - rect_ancho) // 2
            rect_y = y_pos - rect_alto // 2
            
            if i == seleccion:
                pygame.draw.rect(ventana, colores["AZUL"], (rect_x, rect_y, rect_ancho, rect_alto), border_radius=15)
                pygame.draw.rect(ventana, colores["BLANCO"], (rect_x + 3, rect_y + 3, rect_ancho - 6, rect_alto - 6), border_radius=12)
                color_texto = colores["AZUL"]
            else:
                pygame.draw.rect(ventana, colores["NEGRO"], (rect_x, rect_y, rect_ancho, rect_alto), border_radius=15)
                pygame.draw.rect(ventana, colores["BLANCO"], (rect_x + 2, rect_y + 2, rect_ancho - 4, rect_alto - 4), border_radius=13)
                color_texto = colores["NEGRO"]
            
            texto_opcion = estado_global["fuentes"]["boton"].render(opcion.upper(), True, color_texto)
            texto_rect = texto_opcion.get_rect(center=(ancho // 2, y_pos))
            ventana.blit(texto_opcion, texto_rect)
    
    elif tipo == "horizontal":
        for i, opcion in enumerate(opciones):
            x_pos = ancho // 2 + (i - 0.5) * 200
            y_pos = alto // 2 + 50
            
            rect_ancho = 150
            rect_alto = 60
            rect_x = int(x_pos - rect_ancho // 2)
            rect_y = y_pos - rect_alto // 2
            
            if i == seleccion:
                pygame.draw.rect(ventana, colores["VERDE"], (rect_x, rect_y, rect_ancho, rect_alto), border_radius=15)
                pygame.draw.rect(ventana, colores["BLANCO"], (rect_x + 3, rect_y + 3, rect_ancho - 6, rect_alto - 6), border_radius=12)
                color_texto = colores["VERDE"]
            else:
                pygame.draw.rect(ventana, colores["NEGRO"], (rect_x, rect_y, rect_ancho, rect_alto), border_radius=15)
                pygame.draw.rect(ventana, colores["BLANCO"], (rect_x + 2, rect_y + 2, rect_ancho - 4, rect_alto - 4), border_radius=13)
                color_texto = colores["NEGRO"]
            
            texto_opcion = estado_global["fuentes"]["boton"].render(opcion.upper(), True, color_texto)
            texto_rect = texto_opcion.get_rect(center=(int(x_pos), y_pos))
            ventana.blit(texto_opcion, texto_rect)

def bucle_mostrar_items_info(ventana: pygame.Surface, estado_global: dict, items: list, contenedor_y: int, ancho: int):
    """Bucle para mostrar items de información estilizados"""
    y_pos = contenedor_y + 50
    
    for item in items:
        texto = estado_global["fuentes"]["boton"].render(item, True, estado_global["colores"][estado_global.get("modo", "normal")]["AZUL"])
        texto_rect = texto.get_rect(center=(ancho // 2, y_pos))
        ventana.blit(texto, texto_rect)
        y_pos += 50

def bucle_animacion_categoria_letra_por_letra(ventana: pygame.Surface, estado_global: dict, categoria_texto: str, 
                                            colores: dict, ancho: int, alto: int, tiempo_letra: int) -> tuple:
    """Bucle para mostrar texto letra por letra con animación"""
    from pantallas.pantallas_juego import aplicar_brillo
    
    letras_mostradas = 0
    tiempo_ultimo = pygame.time.get_ticks()
    terminado = False
    
    while not terminado and letras_mostradas <= len(categoria_texto):
        ventana.fill(colores["BLANCO"])

        titulo = estado_global["fuentes"]["titulo"].render("¡CATEGORÍA ELEGIDA!", True, colores["AZUL"])
        titulo_rect = titulo.get_rect(center=(ancho // 2, alto // 4))
        ventana.blit(titulo, titulo_rect)

        base_render = estado_global["fuentes"]["boton"].render("Categoría seleccionada:", True, colores["NEGRO"])
        base_rect = base_render.get_rect(center=(ancho // 2, alto // 2 - 40))
        ventana.blit(base_render, base_rect)

        parcial = categoria_texto[:letras_mostradas]
        
        contenedor_ancho = 300
        contenedor_alto = 80
        contenedor_x = (ancho - contenedor_ancho) // 2
        contenedor_y = alto // 2 - 10
        
        pygame.draw.rect(ventana, colores["VERDE"], (contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto), border_radius=15)
        pygame.draw.rect(ventana, colores["BLANCO"], (contenedor_x + 3, contenedor_y + 3, contenedor_ancho - 6, contenedor_alto - 6), border_radius=12)
        
        categoria_render = estado_global["fuentes"]["titulo"].render(parcial, True, colores["VERDE"])
        categoria_rect = categoria_render.get_rect(center=(ancho // 2, alto // 2 + 30))
        ventana.blit(categoria_render, categoria_rect)

        aplicar_brillo(ventana, ancho, alto, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()

        ahora = pygame.time.get_ticks()
        if ahora - tiempo_ultimo > tiempo_letra:
            letras_mostradas += 1
            tiempo_ultimo = ahora
            if letras_mostradas > len(categoria_texto):
                terminado = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    return letras_mostradas, terminado