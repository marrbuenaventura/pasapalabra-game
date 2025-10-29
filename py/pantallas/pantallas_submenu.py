from funciones_historial_pygame import *
from generales.generales_pygame import *
from pantallas.pantallas_componentes import *
from pantallas.pantallas_layout import *
from eventos.eventos_generales import *
from musica import *
from funciones_prejuego import *
from pantallas.pantallas_mensajes import *
from funciones_archivos import *

def pantalla_pre_juego(ventana: pygame.Surface, estado_global: dict) -> tuple[str, str, str]:
    """
    Ejecuta la secuencia completa de preparación antes del juego principal.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar las pantallas.
        estado_global (dict): Estado global con configuraciones y recursos.

    Returns:
        tuple[str, str, str]: Tupla con (usuario, dificultad, categoria).
    """
    detener_musica()
    reproducir_musica(estado_global, "MP3/prejuego.mp3")
    
    usuario = obtener_usuario_con_estilo(ventana, estado_global)
    estado_global["usuario_actual"] = usuario
    
    dificultad = elegir_dificultad_con_estilo(ventana, estado_global)
    categoria = elegir_categoria_aleatoria()
    mostrar_categoria_elegida_estilizada(ventana, estado_global, categoria)
    mostrar_resumen_partida(ventana, estado_global, usuario, dificultad, categoria)
    cuenta_regresiva_estilizada(ventana, estado_global)
    
    return usuario, dificultad, categoria

def pantalla_accesibilidad(
    ventana: pygame.Surface,
    estado_global: dict,
    modo_actual: str,
    colores: dict
) -> tuple[str, dict]:
    """
    Muestra la pantalla de configuración de accesibilidad con opciones de modo.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la pantalla.
        estado_global (dict): Estado global con configuraciones.
        modo_actual (str): Modo de accesibilidad actual.
        colores (dict): Diccionario de colores actual.

    Returns:
        tuple[str, dict]: Tupla con (modo_seleccionado, colores_actualizados).
    """
    reloj = pygame.time.Clock()
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]
    alto_ventana = estado_global["config"]["ventana"]["alto"]
    resultado = (modo_actual, colores)

    continuar = True
    while continuar:
        modo_display = estado_global.get("modo", "normal")
        colores_display = estado_global["colores"][modo_display]
        
        ventana.fill(colores_display["GRIS"])
        mostrar_titulo(ventana, "Accesibilidad", estado_global, y_pos=80)

        ancho_boton = 300
        alto_boton = 65
        x_boton = (ancho_ventana - ancho_boton) // 2

        botones = {
            "normal": dibujar_boton(ventana, estado_global, "Modo Normal", x_boton, 260, ancho_boton, alto_boton),
            "daltonico": dibujar_boton(ventana, estado_global, "Modo Daltonico", x_boton, 340, ancho_boton, alto_boton)
        }

        aplicar_brillo(ventana, ancho_ventana, alto_ventana, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        reloj.tick(60)

        modo_seleccionado, salir = manejar_eventos_accesibilidad(pygame.event.get(), botones)

        if modo_seleccionado:
            modo_actual = modo_seleccionado
            colores = estado_global["colores"][modo_actual]
            resultado = (modo_actual, colores)

        if salir:
            continuar = False

    return resultado

def pantalla_estadisticas_general(ventana: pygame.Surface, estado_global: dict):
    """
    Muestra las estadísticas generales obtenidas del ranking JSON.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar las estadísticas.
        estado_global (dict): Estado global con configuraciones.

    Returns:
        None: Esta función no retorna valores.
    """
    lineas_ranking = obtener_ranking_general_json(50)
    if len(lineas_ranking) > 1:
        pantalla_puntajes_scroll(ventana, lineas_ranking, estado_global)
    else:
        mostrar_mensaje(ventana, "No hay estadísticas registradas.", estado_global, ventana.get_height())

def pantalla_historial_usuario(ventana: pygame.Surface, estado_global: dict):
    """
    Muestra el historial de partidas de un usuario específico desde JSON.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el historial.
        estado_global (dict): Estado global con configuraciones.

    Returns:
        None: Esta función no retorna valores.
    """
    usuario = pedir_usuario(estado_global)
    if usuario == None:
        return

    mostrar_cargando(ventana, "Cargando historial...", estado_global, ventana.get_height())

    if not verificar_usuario_existe(usuario):
        mostrar_error(ventana, "Usuario no registrado", estado_global, ventana.get_height())
    else:
        lineas = obtener_historial_usuario_como_lineas(usuario)
        pantalla_puntajes_scroll(ventana, lineas, estado_global)

def pantalla_estadisticas_generales(
    ventana: pygame.Surface,
    estado_global: dict,
    lineas_estadisticas: list
):
    """
    Muestra estadísticas generales calculadas a partir de los datos proporcionados.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar las estadísticas.
        estado_global (dict): Estado global con configuraciones, fuentes y colores.
        lineas_estadisticas (list): Lista de líneas de datos para calcular estadísticas.

    Returns:
        None: Esta función no retorna valores.
    """
    estadisticas = calcular_estadisticas(lineas_estadisticas)
    datos = generar_textos_estadisticas(estadisticas)
    fuente_estadisticas = pygame.font.SysFont("Times New Roman", 36, bold=True)
    reloj = pygame.time.Clock()
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]
    alto_ventana = estado_global["config"]["ventana"]["alto"]

    continuar = True
    while continuar:
        modo_actual = estado_global.get("modo", "normal")
        colores = estado_global["colores"][modo_actual]
        
        ventana.fill(colores.get("GRIS_CLARO", colores["BLANCO"]))
        mostrar_titulo(ventana, "Estadísticas Generales", estado_global, 40)

        contenedor = crear_contenedor(0.85, 320, 130, estado_global)
        dibujar_contenedor_con_sombra(ventana, contenedor, estado_global)

        dibujar_items_estadisticas(
            ventana, estado_global, datos, contenedor,
            fuente_estadisticas,
            padding_vertical=50,
            alto_item=50,
            espacio_entre_items=70
        )

        aplicar_brillo(ventana, ancho_ventana, alto_ventana, estado_global["estado_inicial"]["brillo"])
        pygame.display.flip()
        reloj.tick(30)

        if manejar_eventos_estadisticas():
            continuar = False

def pantalla_config_visual(ventana: pygame.Surface, estado_global: dict):
    """
    Muestra la pantalla de configuración visual que guarda preferencias por usuario en JSON.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la configuración.
        estado_global (dict): Estado global con configuraciones y fuentes.

    Returns:
        tuple[float, float]: Tupla con (volumen_final, brillo_final).
    """
    usuario_actual = estado_global.get("usuario_actual", "invitado")
    preferencias = cargar_preferencias_usuario(usuario_actual)
    
    slider_ancho = 400
    ancho_ventana = estado_global["config"]["ventana"]["ancho"]
    slider_x = (ancho_ventana - slider_ancho) // 2

    estado_local = {
        "volumen": preferencias["volumen"],
        "brillo": preferencias["brillo"],
        "slider_volumen": pygame.Rect(slider_x, 220, slider_ancho, 10),
        "slider_brillo": pygame.Rect(slider_x, 320, slider_ancho, 10),
        "dragging_vol": False,
        "dragging_bri": False,
    }

    estado_local["selector_vol"] = crear_selector(estado_local["slider_volumen"], estado_local["volumen"])
    estado_local["selector_bri"] = crear_selector(estado_local["slider_brillo"], estado_local["brillo"])

    reloj = pygame.time.Clock()
    resultado = (estado_local["volumen"], estado_local["brillo"])

    continuar = True
    while continuar:
        modo_actual = estado_global.get("modo", "normal")
        colores = estado_global["colores"][modo_actual]
        
        ventana.fill(colores["GRIS"])
        mostrar_titulo(ventana, "Visual y sonido", estado_global, 80)

        dibujar_slider(
            ventana, 
            estado_global, 
            "Volumen", 
            estado_global["fuentes"]["boton"], 
            estado_local["slider_volumen"], 
            estado_local["selector_vol"], 
            180, 
            estado_local["volumen"]
        )

        estado_local["brillo"] = dibujar_slider(
            ventana, 
            estado_global, 
            "Brillo", 
            estado_global["fuentes"]["boton"],
            estado_local["slider_brillo"], 
            estado_local["selector_bri"],
            280, 
            estado_local["brillo"]
        )

        aplicar_brillo(ventana, ancho_ventana, estado_global["config"]["ventana"]["alto"], estado_local["brillo"])

        pygame.display.flip()
        reloj.tick(60)

        salir = manejar_eventos_config(estado_local)
        if salir:
            continuar = False
            resultado = (estado_local["volumen"], estado_local["brillo"])
            
            preferencias_actualizadas = {
                "volumen": estado_local["volumen"],
                "brillo": estado_local["brillo"],
                "modo_accesibilidad": preferencias.get("modo_accesibilidad", "neurotipico"),
                "dificultad_preferida": preferencias.get("dificultad_preferida", "facil"),
                "tiempo_partida": preferencias.get("tiempo_partida", 120)
            }
            guardar_preferencias_usuario(usuario_actual, preferencias_actualizadas)

    return resultado

def pantalla_puntajes_scroll(ventana: pygame.Surface, lineas_estadisticas: list, estado_global: dict):
    """
    Muestra una tabla de puntajes con scroll vertical para navegación.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la tabla.
        lineas_estadisticas (list): Lista de líneas de datos estadísticos.
        estado_global (dict): Estado global con fuentes y configuraciones.

    Returns:
        None: Esta función no retorna valores.
    """
    if len(lineas_estadisticas) <= 1:
        mostrar_mensaje(ventana, "No hay estadísticas registradas.", estado_global, ventana.get_height())
        return

    encabezado, datos, indices = procesar_estadisticas(lineas_estadisticas)
    ancho_ventana = ventana.get_width()
    col_width = ancho_ventana // len(indices)
    row_height = 40
    scroll, target_scroll, scroll_speed = 0, 0, 20

    clock = pygame.time.Clock()

    continuar = True
    while continuar:
        dt = clock.tick(60) / 1000
        ventana.fill((240, 240, 240))

        dibujar_titulo_puntajes(ventana, estado_global["fuentes"]["titulo"], estado_global)
        
        dibujar_encabezado(
            ventana, 
            estado_global["fuentes"]["pequena"], 
            estado_global, 
            encabezado, 
            indices, 
            col_width, 
            row_height
        )

        scroll += (target_scroll - scroll) * 0.2
        mouse_y = pygame.mouse.get_pos()[1]

        dibujar_filas(
            ventana, 
            estado_global["fuentes"]["pequena"], 
            estado_global, 
            datos, 
            indices, 
            col_width, 
            row_height, 
            scroll, 
            mouse_y
        )

        pygame.display.flip()

        accion = manejar_eventos_scroll()
        if accion == "salir":
            continuar = False
        elif accion == "abajo":
            target_scroll += scroll_speed
        elif accion == "arriba":
            target_scroll -= scroll_speed
        elif accion.startswith("scroll:"):
            cantidad = int(accion.split(":")[1])
            target_scroll -= cantidad * scroll_speed * 3

        target_scroll = limitar_scroll(estado_global, target_scroll, len(datos), row_height)

def pantalla_ranking_json(ventana: pygame.Surface, estado_global: dict):
    """
    Muestra el ranking de jugadores obtenido desde el archivo JSON unificado.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar el ranking.
        estado_global (dict): Estado global con configuraciones.

    Returns:
        None: Esta función no retorna valores.
    """
    mostrar_cargando(ventana, "Cargando ranking...", estado_global, ventana.get_height())
    
    lineas_ranking = obtener_ranking_general_json(20)
    
    if len(lineas_ranking) <= 1:
        mostrar_mensaje(ventana, "No hay datos de ranking disponibles.", estado_global, ventana.get_height())
    else:
        pantalla_puntajes_scroll(ventana, lineas_ranking, estado_global)

def pantalla_lista_usuarios(ventana: pygame.Surface, estado_global: dict):
    """
    Muestra una lista completa de todos los usuarios registrados en el sistema.

    Args:
        ventana (pygame.Surface): Superficie donde mostrar la lista.
        estado_global (dict): Estado global con configuraciones.

    Returns:
        None: Esta función no retorna valores.
    """
    usuarios = listar_todos_los_usuarios()
    
    if not usuarios:
        mostrar_mensaje(ventana, "No hay usuarios registrados.", estado_global, ventana.get_height())
    else:
        lineas_usuarios = ["usuario\n"]
        for usuario in usuarios:
            lineas_usuarios.append(f"{usuario}\n")
        
        pantalla_puntajes_scroll(ventana, lineas_usuarios, estado_global)