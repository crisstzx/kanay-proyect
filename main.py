def sistema_pedidos_kanay():
    # CICLO DE REPETICIÓN: Control de acceso por QR / Mesa
    while True:
        print("===========================================")
        print("       BIENVENIDO AL SISTEMA KANAY         ")
        print("===========================================")
        print("[Sistema] Escaneo de Código QR detectado...")
        
        # Validación con try-except para evitar errores si el usuario ingresa texto
        try:
            numMesa = int(input("Por favor, ingrese su número de mesa (1-7): "))
        except ValueError:
            numMesa = 0 # Asignamos 0 para que caiga en el 'else' de mesa inválida
            
        # ESTRUCTURA CONDICIONAL: Validación de mesa (1-7)
        if 1 <= numMesa <= 7:
            print(f"[OK] Mesa {numMesa} validada. Cargando Menú...")
            subtotal = 0.0
            
            # CICLO DE REPETICIÓN: Selección de productos (Carrito)
            while True:
                print("\n---- MENÚ DIGITAL DISPONIBLE ----")
                print("1. Lomo Saltado - S/. 25.00")
                print("2. Ají de Gallina - S/. 18.00")
                print("3. Pescado frito - S/. 16.00")
                print("4. Alitas BBQ - S/. 22.00")
                print("5. Ceviche - S/. 20.00")
                print("6. Postre del Día - S/. 12.00")
                print("7. Arroz a la cubana - S/. 15.00")
                print("8. Chaufa de pollo - S/. 21.00")
                print("9. Tallarines verdes - S/. 19.00")
                print("10. Pollo a la brasa - S/. 30.00")
                print("11. Causa limeña - S/. 14.00")
                print("12. Arroz con pato - S/. 25.00")
                print("---------------------------------")
                print("\n>>> BEBIDAS <<<")
                print("13. Chicha Morada (Jarra) - S/. 15.00")
                print("14. Limonada Frozen - S/. 10.00")
                print("15. Jugo de Maracuyá - S/. 8.00")
                print("16. Gaseosa (Inca Kola/Coca Cola) - S/. 5.00")
                print("17. Cerveza Personal - S/. 9.00")
                print("18. Agua Mineral - S/. 4.00")
                print("---------------------------------")
                
                try:
                    opcionMenu = int(input("Seleccione una opción (1-18): "))
                except ValueError:
                    opcionMenu = 0
                
                # Variables temporales para el producto actual
                precioUnitario = 0.0
                productoSeleccionado = ""
                
                # Estructura de decisión para asignar producto y precio
                if opcionMenu == 1:
                    productoSeleccionado = "Lomo Saltado"
                    precioUnitario = 25.00
                elif opcionMenu == 2:
                    productoSeleccionado = "Ají de Gallina"
                    precioUnitario = 18.00
                elif opcionMenu == 3:
                    productoSeleccionado = "Pescado frito"
                    precioUnitario = 16.00
                elif opcionMenu == 4:
                    productoSeleccionado = "Alitas BBQ"
                    precioUnitario = 22.00
                elif opcionMenu == 5:
                    productoSeleccionado = "Ceviche"
                    precioUnitario = 20.00
                elif opcionMenu == 6:
                    productoSeleccionado = "Postre del Día"
                    precioUnitario = 12.00
                elif opcionMenu == 7:
                    productoSeleccionado = "Arroz a la cubana"
                    precioUnitario = 15.00
                elif opcionMenu == 8:
                    productoSeleccionado = "Chaufa de pollo"
                    precioUnitario = 21.00
                elif opcionMenu == 9:
                    productoSeleccionado = "Tallarines verdes"
                    precioUnitario = 19.00
                elif opcionMenu == 10:
                    productoSeleccionado = "Pollo a la brasa"
                    precioUnitario = 30.00
                elif opcionMenu == 11:
                    productoSeleccionado = "Causa limeña"
                    precioUnitario = 14.00
                elif opcionMenu == 12:
                    productoSeleccionado = "Arroz con pato"
                    precioUnitario = 25.00
                elif opcionMenu == 13:
                    productoSeleccionado = "Chicha Morada (Jarra)"
                    precioUnitario = 15.00
                elif opcionMenu == 14:
                    productoSeleccionado = "Limonada Frozen"
                    precioUnitario = 10.00
                elif opcionMenu == 15:
                    productoSeleccionado = "Jugo de Maracuyá"
                    precioUnitario = 8.00
                elif opcionMenu == 16:
                    productoSeleccionado = "Gaseosa (Inca Kola/Coca Cola)"
                    precioUnitario = 5.00
                elif opcionMenu == 17:
                    productoSeleccionado = "Cerveza Personal"
                    precioUnitario = 9.00
                elif opcionMenu == 18:
                    productoSeleccionado = "Agua Mineral"
                    precioUnitario = 4.00
                else:
                    print("Opción no válida.")
                
                if precioUnitario > 0:
                    try:
                        cantidad = int(input(f"Ingrese la cantidad para {productoSeleccionado}: "))
                    except ValueError:
                        cantidad = 0
                        
                    # CONDICIONAL: Validación de cantidad permitida
                    if 1 <= cantidad <= 10:
                        subtotal += (precioUnitario * cantidad)
                        print(f"[Carrito] Añadido: {cantidad} x {productoSeleccionado}")
                    else:
                        print("Error: Cantidad no permitida (Máx. 10 por pedido).")
                
                agregarOtro = input("¿Desea agregar otro producto al pedido? (S/N): ").strip().upper()
                if agregarOtro == "N":
                    break # Rompe el ciclo del menú y pasa al pago
            
            # ESTRUCTURA DE SECUENCIA: Proceso de Pago
            print("\n--- RESUMEN DE CUENTA ---")
            igv = subtotal * 0.18
            total = subtotal + igv
            
            # Formateamos a 2 decimales (.2f) para que parezca moneda
            print(f"Subtotal: S/. {subtotal:.2f}")
            print(f"IGV (18%): S/. {igv:.2f}")
            print(f"TOTAL A PAGAR: S/. {total:.2f}")
            
            metodoPago = input("Seleccione Método de Pago (1: Efectivo / 2: Tarjeta / 3: Yape): ").strip()
            # Diccionario para completar la experiencia mostrando el método elegido
            metodos = {"1": "Efectivo", "2": "Tarjeta", "3": "Yape"}
            nombre_metodo = metodos.get(metodoPago, "No especificado")
            
            confirmar = input("¿Confirmar envío del pedido a cocina? (S/N): ").strip().upper()
            
            # Condicional final de registro
            if confirmar == "S":
                idPedido = f"KANAY-{numMesa}-2026"
                print(f"\n[Procesando] Generando ID de Pedido: {idPedido}")
                print("[DB] Registrando pedido en Base de Datos...")
                print(f"[Pago] Validando pago con {nombre_metodo}...")
                print("[Cocina] Enviando comanda en tiempo real...")
                print("=============================================")
                print("¡PEDIDO CONFIRMADO! Su comida llegará pronto.")
                print("=============================================")
                intentarDeNuevo = "N"
            else:
                print("Pedido cancelado. Puede volver a empezar.\n")
                intentarDeNuevo = "S"
                
        else:
            # Manejo de flujo en caso de error en mesa
            print("\n--- ERROR DE ACCESO ---")
            print("Mesa no válida o fuera de rango.")
            intentarDeNuevo = input("¿Desea intentar escanear de nuevo? (S/N): ").strip().upper()
        
        # Condición de salida del ciclo principal
        if intentarDeNuevo == "N":
            break

    print("\nGracias por usar el Sistema de Pedidos Kanay. ¡Buen provecho!")

# Punto de entrada del script
if __name__ == "__main__":
    sistema_pedidos_kanay()
