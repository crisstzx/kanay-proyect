from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. Definimos las estructuras de datos que recibirá la API
class ItemPedido(BaseModel):
    opcionMenu: int
    cantidad: int

class PedidoEntrada(BaseModel):
    mesa: int
    productos: List[ItemPedido]
    metodoPago: str  # "1": Efectivo, "2": Tarjeta, "3": Yape

# Diccionario con tu menú original para procesar los precios
MENU = {
    1: {"nombre": "Lomo Saltado", "precio": 25.00},
    2: {"nombre": "Ají de Gallina", "precio": 18.00},
    3: {"nombre": "Pescado frito", "precio": 16.00},
    4: {"nombre": "Alitas BBQ", "precio": 22.00},
    5: {"nombre": "Ceviche", "precio": 20.00},
    6: {"nombre": "Postre del Día", "precio": 12.00},
    7: {"nombre": "Arroz a la cubana", "precio": 15.00},
    8: {"nombre": "Chaufa de pollo", "precio": 21.00},
    9: {"nombre": "Tallarines verdes", "precio": 19.00},
    10: {"nombre": "Pollo a la brasa", "precio": 30.00},
    11: {"nombre": "Causa limeña", "precio": 14.00},
    12: {"nombre": "Arroz con pato", "precio": 25.00},
    13: {"nombre": "Chicha Morada (Jarra)", "precio": 15.00},
    14: {"nombre": "Limonada Frozen", "precio": 10.00},
    15: {"nombre": "Jugo de Maracuyá", "precio": 8.00},
    16: {"nombre": "Gaseosa (Inca Kola/Coca Cola)", "precio": 5.00},
    17: {"nombre": "Cerveza Personal", "precio": 9.00},
    18: {"nombre": "Agua Mineral", "precio": 4.00}
}

METODOS_PAGO = {"1": "Efectivo", "2": "Tarjeta", "3": "Yape"}

@app.get("/")
def inicio():
    return {
        "sistema": "BIENVENIDO AL SISTEMA KANAY",
        "estado": "Servidor activo en la nube",
        "mensaje": "Escanea el QR para enviar tus pedidos a la cocina."
    }

@app.post("/ordenar")
def recibir_pedido(pedido: PedidoEntrada):
    # Validación de la mesa (1-7) tal como en tu código original
    if not (1 <= pedido.mesa <= 7):
        raise HTTPException(status_code=400, detail="Mesa no válida o fuera de rango (1-7).")
    
    subtotal = 0.0
    resumen_productos = []
    
    # Procesamos los productos enviados en el carrito
    for item in pedido.productos:
        if item.opcionMenu not in MENU:
            raise HTTPException(status_code=400, detail=f"Opción de menú {item.opcionMenu} no existe.")
        
        # Validación de cantidad (Máx 10 por pedido)
        if not (1 <= item.cantidad <= 10):
            raise HTTPException(status_code=400, detail=f"Cantidad no permitida para la opción {item.opcionMenu} (Máx. 10).")
            
        prod = MENU[item.opcionMenu]
        costo_item = prod["precio"] * item.cantidad
        subtotal += costo_item
        
        resumen_productos.append({
            "producto": prod["nombre"],
            "cantidad": item.cantidad,
            "precio_unitario": prod["precio"],
            "total_item": costo_item
        })
    
    # Cálculos económicos originales
    igv = subtotal * 0.18
    total = subtotal + igv
    
    nombre_metodo = METODOS_PAGO.get(pedido.metodoPago, "No especificado")
    idPedido = f"KANAY-{pedido.mesa}-2026"
    
    # Devolvemos la respuesta que antes se imprimía en pantalla
    return {
        "id_pedido": idPedido,
        "mesa": pedido.mesa,
        "productos_ordenados": resumen_productos,
        "cuenta": {
            "subtotal": round(subtotal, 2),
            "igv_18": round(igv, 2),
            "total_a_pagar": round(total, 2)
        },
        "pago": f"Validando pago con {nombre_metodo}...",
        "cocina": "Enviando comanda en tiempo real...",
        "estado_final": "¡PEDIDO CONFIRMADO! Su comida llegará pronto."
    }
