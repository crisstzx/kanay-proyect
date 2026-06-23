from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Configuración completa de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ItemPedido(BaseModel):
    opcionMenu: int
    cantidad: int

class PedidoEntrada(BaseModel):
    mesa: int
    platos: List[ItemPedido]
    metodoPago: str
    nombre: str

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
    return {"sistema": "BIENVENIDO AL SISTEMA KANAY", "estado": "Servidor activo"}

@app.post("/ordenar")
def recibir_pedido(pedido: PedidoEntrada):
    if not (1 <= pedido.mesa <= 7):
        raise HTTPException(status_code=400, detail="Mesa no válida.")
    
    subtotal = 0.0
    resumen_platos = []
    
    for item in pedido.platos:
        if item.opcionMenu not in MENU:
            raise HTTPException(status_code=400, detail=f"Opción {item.opcionMenu} no existe.")
        if not (1 <= item.cantidad <= 10):
            raise HTTPException(status_code=400, detail="Cantidad no permitida.")
            
        plat = MENU[item.opcionMenu]
        costo_item = plat["precio"] * item.cantidad
        subtotal += costo_item
        
        resumen_productos.append({
            "plato": plat["nombre"],
            "cantidad": item.cantidad,
            "precio_unitario": plat["precio"],
            "total_item": costo_item
        })
    
    igv = subtotal * 0.18
    total = subtotal + igv
    
    pago_recibido = pedido.metodoPago.strip()
    nombre_metodo = "No especificado"
    if pago_recibido in METODOS_PAGO:
        nombre_metodo = METODOS_PAGO[pago_recibido]
    elif "efectivo" in pago_recibido.lower():
        nombre_metodo = "Efectivo"
    elif "tarjeta" in pago_recibido.lower():
        nombre_metodo = "Tarjeta"
    elif "yape" in pago_recibido.lower() or "plin" in pago_recibido.lower():
        nombre_metodo = "Yape"
    
    idPedido = f"KANAY-{pedido.mesa}-2026"
    nombre_cliente = pedido.nombre.strip() if pedido.nombre.strip() else "Cliente"
    
    # --- NUEVO: GUARDAR EN ARCHIVO JSON ---
    registro_venta = {
        "id_pedido": idPedido,
        "cliente": nombre_cliente,
        "mesa": pedido.mesa,
        "total": round(total, 2),
        "metodo_pago": nombre_metodo,
        "platos": resumen_platos
    }
    
    historial = []
    if os.path.exists("pedidos.json"):
        with open("pedidos.json", "r", encoding="utf-8") as f:
            try:
                historial = json.load(f)
            except:
                historial = []
                
    historial.append(registro_venta)
    with open("pedidos.json", "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)
    # ----------------------------------------

    return {
        "id_plato": idPlato,
        "mesa": pedido.mesa,
        "cliente": nombre_cliente,
        "platos_ordenados": resumen_platos,
        "cuenta": {
            "subtotal": round(subtotal, 2),
            "igv_18": round(igv, 2),
            "total_a_pagar": round(total, 2)
        },
        "pago": f"Validando pago con {nombre_metodo}...",
        "cocina": "Enviando comanda en tiempo real...",
        "estado_final": "¡PEDIDO CONFIRMADO! Su comida llegará pronto."
    }

# NUEVA RUTA: Entrega el historial guardado en formato JSON
@app.get("/historial")
def ver_historial():
    if os.path.exists("pedidos.json"):
        with open("pedidos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# NUEVA RUTA: Por si quieres limpiar el historial y empezar desde cero
@app.delete("/historial/limpiar")
def limpiar_historial():
    if os.path.exists("pedidos.json"):
        os.remove("pedidos.json")
        return {"mensaje": "Historial borrado con éxito."}
    return {"mensaje": "No hay historial que borrar."}
