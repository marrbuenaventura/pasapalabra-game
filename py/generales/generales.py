from colorama import *
from generales.bucles_generales import bucle_buscar_maximo, bucle_calcular_promedio, bucle_ordenar_burbuja

init(autoreset=True)

def buscar_maximo(lista: list) -> int | float:
    """
    Devuelve el valor máximo dentro de una lista de números.

    Args:
        lista (list): Lista de valores numéricos.

    Returns:
        int or float: Valor máximo encontrado en la lista.
    """
    return bucle_buscar_maximo(lista)

def calcular_promedio_total(lista: list) -> float:
    """
    Calcula el promedio de una lista de números.

    Args:
        lista (list): Lista de valores numéricos.

    Returns:
        float: Promedio de los valores.
    """
    return bucle_calcular_promedio(lista)

def ordenar_preguntas_por_fallos(lista: list) -> list:
    """
    Ordena una lista de pares [pregunta, fallos] de mayor a menor según la cantidad de fallos.
    Usa el método de burbuja para ordenar.

    Args:
        lista (list): Lista de pares [pregunta, cantidad_fallos].

    Returns:
        list: Lista ordenada de mayor a menor cantidad de fallos.
    """
    return bucle_ordenar_burbuja(lista)

def swap(lista: list, i: int, j: int):
    """
    Ordena con metodo burbuja

    Args:
        lista (list): Lista de lo que se quiera ordenar
        i (str, int): elemento a ordenar
        j (str, int): elemento a ordenar
    """
    auxiliar = lista[i]
    lista[i] = lista[j]
    lista[j] = auxiliar