def mostrar_torres(torres):
    print()
    for nombre, torre in torres.items():
        print(f"{nombre}: {torre}")
    print("-" * 20)

def mover_disco(torres, origen, destino):
    if not torres[origen]:
        print(f"No hay discos en {origen}")
        return False
    if torres[destino] and torres[origen][-1] > torres[destino][-1]:
        print("Movimiento inválido: no puedes poner un disco grande sobre uno pequeño")
        return False
    disco = torres[origen].pop()
    torres[destino].append(disco)
    return True

def juego_torre_hanoi(n=3):
    torres = {
        "A": list(range(n, 0, -1)),  # [n, n-1, ..., 1]
        "B": [],
        "C": []
    }

    print("🎮 Torre de Hanói - Juego interactivo 🎮")
    print(f"Objetivo: mover los {n} discos de A hasta C")
    mostrar_torres(torres)

    while len(torres["C"]) != n:
        origen = input("Mover desde (A/B/C): ").strip().upper()
        destino = input("Mover hacia (A/B/C): ").strip().upper()

        if origen not in torres or destino not in torres:
            print("Entrada inválida. Usa A, B o C.")
            continue

        mover_disco(torres, origen, destino)
        mostrar_torres(torres)

    print("🎉 ¡Felicidades! Has completado la Torre de Hanói 🎉")

if __name__ == "__main__":
    juego_torre_hanoi(3)  # Puedes cambiar 3 por 4 o 5 discos
