def movimiento_a_estimulo(movimiento):
    def H1F1():
        return 3
    def H1F2():
        return 4
    def H1F3():
        return 5
    def H1F4():
        return 6
    def H0F1():
        return 7
    def H0F2():
        return 8
    def H0F3():
        return 9
    def H0F4():
        return 10
    def H2F1():
        return 11
    def H2F2():
        return 12
    def H2F3():
        return 13
    def H2F4():
        return 14
    def default():
        return "Opcion no valida"
    
    pos_mano = {
        "H0F1":H0F1,
        "H0F2":H0F2,
        "H0F3":H0F3,
        "H0F4":H0F4,
        "H1F1":H1F1,
        "H1F2":H1F2,
        "H1F3":H1F3,
        "H1F4":H1F4,
        "H2F1":H2F1,
        "H2F2":H2F2,
        "H2F3":H2F3,
        "H2F4":H2F4,
    }

    return pos_mano.get(movimiento,default)()