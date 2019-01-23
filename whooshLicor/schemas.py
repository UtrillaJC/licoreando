from whoosh import fields

from decimal import Decimal

def crear_esquema():
    licorSchema = fields.Schema(
    id = fields.NUMERIC(stored=True),
    titulo = fields.TEXT(sortable = True,field_boost=1.5),
    descripcion = fields.TEXT,
    categoria = fields.TEXT(sortable = True),
    precio = fields.NUMERIC(Decimal, decimal_places=2,sortable= True),
    precioGroup = fields.NUMERIC(sortable= True),
    origen = fields.TEXT(sortable= True),
    graduacion = fields.NUMERIC(sortable = True),
    enStock = fields.BOOLEAN(stored = True),
    urlProducto = fields.TEXT(field_boost=0.5),)
    
    return licorSchema