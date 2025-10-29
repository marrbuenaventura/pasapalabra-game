import os
from funciones_archivos import leer_historial_usuario_json, convertir_json_a_lineas_csv, obtener_ranking_general_json
from bucles_funciones import bucle_migrar_csv_lineas, bucle_obtener_usuarios_con_stats

def procesar_estadisticas(lineas: list) -> tuple:
    """
    Procesa líneas de estadísticas desde un CSV.

    Soporta:
    - lista de strings (líneas crudas con '\n')
    - lista de listas (filas ya separadas por campos)

    Returns:
        tuple: encabezado, datos, indices
    """
    resultado = ([], [], [])
    
    if lineas:
        primer_elemento = lineas[0]

        if isinstance(primer_elemento, str) and ";" in primer_elemento:
            lineas = [linea.strip().split(";") for linea in lineas if linea.strip()]

        if lineas:
            encabezado = lineas[0]
            datos = lineas[1:]
            indices = list(range(len(encabezado)))
            resultado = (encabezado, datos, indices)

    return resultado

def limitar_scroll(estado_global: dict, target_scroll: int, cantidad_filas: int, row_height: int) -> int:
    """
    Limita el scroll para que no se salga de los límites.
    
    Args:
        estado_global: dict con configuración
        target_scroll: posición de scroll objetivo
        cantidad_filas: número de filas de datos
        row_height: altura de cada fila
        
    Returns:
        int: scroll limitado dentro de los bounds válidos
    """
    ventana_alto = estado_global["config"]["ventana"]["alto"]
    max_scroll = cantidad_filas * row_height - (ventana_alto - 140)
    
    if max_scroll < 0:
        max_scroll = 0

    resultado = target_scroll
    if target_scroll < 0:
        resultado = 0
    elif target_scroll > max_scroll:
        resultado = max_scroll
    
    return resultado

def generar_textos_estadisticas(estadisticas: dict) -> list[str]:
    """
    Genera una lista de textos formateados para mostrar estadísticas.
    
    Args:
        estadisticas: dict con claves promedio_aciertos, promedio_errores, etc.
        
    Returns:
        list: lista de strings formateados para mostrar
    """
    return [
        f"Promedio de aciertos: {estadisticas.get('promedio_aciertos', 0):.0f}",
        f"Promedio de errores: {estadisticas.get('promedio_errores', 0):.0f}",
        f"Promedio de tiempo: {estadisticas.get('promedio_tiempo', 0):.2f} seg",
        f"Max errores en una partida: {estadisticas.get('max_errores', 0)}",
    ]

def construir_path_historial(usuario: str) -> str:
    """
    Construye la ruta del archivo de historial para un usuario específico.
    Actualizado para JSON unificado pero mantiene compatibilidad.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        str: ruta completa al archivo JSON unificado
    """
    carpeta = "json"
    
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    return os.path.join(carpeta, "historiales_todos_usuarios.json")

def obtener_historial_usuario_como_lineas(usuario: str) -> list:
    """
    Obtiene el historial de un usuario en formato de líneas CSV.
    Para compatibilidad con pantallas que esperan este formato.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        list: líneas en formato CSV
    """
    return convertir_json_a_lineas_csv(usuario)

def verificar_usuario_existe(usuario: str) -> bool:
    """
    Verifica si un usuario tiene historial registrado.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        bool: True si existe, False si no
    """
    historial = leer_historial_usuario_json(usuario)
    return len(historial) > 0

def cargar_estadisticas() -> list:
    """
    CAMBIADO: Carga todas las estadísticas desde JSON en lugar de CSV.
    
    Returns:
        list: líneas en formato CSV de todas las estadísticas
    """
    return obtener_ranking_general_json(1000)

def cargar_estadisticas_desde_json() -> list:
    """
    Carga todas las estadísticas desde el archivo JSON unificado y las convierte a formato CSV.
    Reemplaza la función anterior que leía desde CSV.
    
    Returns:
        list: líneas en formato CSV de todas las estadísticas
    """
    return obtener_ranking_general_json(1000)

def obtener_estadisticas_completas() -> list:
    """
    Obtiene todas las estadísticas de todos los usuarios desde JSON.
    
    Returns:
        list: líneas en formato CSV con todas las estadísticas
    """
    return cargar_estadisticas_desde_json()

def migrar_csv_a_json():
    """
    Función para migrar datos existentes de CSV a JSON.
    Solo debe ejecutarse una vez durante la transición.
    """
    ruta_csv = "csv/estadisticas.csv"
    
    if os.path.exists(ruta_csv):
        try:
            with open(ruta_csv, "r", encoding="utf-8") as archivo:
                lineas = archivo.readlines()
            
            estadisticas_migradas = bucle_migrar_csv_lineas(lineas)
            
            for estadistica in estadisticas_migradas:
                from funciones_archivos import guardar_en_json_unificado
                guardar_en_json_unificado(estadistica)
        except Exception as e:
            print(f"[Error en migración] {e}")

def calcular_estadisticas_usuario_desde_json(usuario: str) -> dict:
    """
    Calcula estadísticas específicas de un usuario desde el JSON.
    
    Args:
        usuario: nombre del usuario
        
    Returns:
        dict: estadísticas calculadas del usuario
    """
    from funciones_archivos import obtener_estadisticas_usuario_json
    return obtener_estadisticas_usuario_json(usuario)

def obtener_top_usuarios(limite: int = 10) -> list:
    """
    Obtiene los mejores usuarios por puntaje promedio.
    
    Args:
        limite: número máximo de usuarios a retornar
        
    Returns:
        list: lista de usuarios ordenados por mejor promedio
    """
    from funciones_archivos import listar_todos_los_usuarios
    usuarios = listar_todos_los_usuarios()
    
    usuarios_con_stats = bucle_obtener_usuarios_con_stats(usuarios)
    usuarios_con_stats.sort(key=lambda x: x["promedio_puntaje"], reverse=True)
    return usuarios_con_stats[:limite]