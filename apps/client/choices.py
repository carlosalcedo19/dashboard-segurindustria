from django.db.models import TextChoices


class DocumentTypeChoices(TextChoices):
    DNI = 'Dni', 'Dni'
    CE = 'Carnet extranjeria', 'Carnet extranjeria'
    PASSPORT = 'Pasaporte', 'Pasaporte'
    EMPTY = '', ''


class PersonTypeChoices(TextChoices):
    N = 'Natural', 'Natural'
    E = 'Empresa', 'Empresa'

class IndustryTypeChoices(TextChoices):
    AI = "Agroindustrial",  "Agroindustrial"
    AB = "Alimentos y bebidas", "Alimentos y bebidas"
    CO = "Construccion", "Construccion"
    CN = "Contratistas", "Contratistas"
    DB = "Distribuidrores", "Distribuidrores"
    ELI= "Empresas de limpieza industrial","Empresas de limpieza industrial"
    E= "Energía", "Energía"
    FM = "Forestal / madereras", "Forestal / madereras"
    FR = "Frigoríficos", "Frigoríficos"
    II = "Imprentas industriales",  "Imprentas industriales"
    LA = "Laboratorios", "Laboratorios"
    LO = "Logística y almacenes", "Logística y almacenes"
    MID = "Mantenimiento industrial", "Mantenimiento industrial"
    MA = "Manufactura", "Manufactura"
    ME = "Metalurgía", "Metalurgía"
    MI = "Minería", "Minería"
    SP = "Sector Público", "Sector Público"
    OG = "Oil & Gas", "Oil & Gas"
    PI = "Pesca industrial", "Pesca industrial"
    PTAR= "Plantas de tratamiento de aguas residuales","Plantas de tratamiento de aguas residuales"
    QI= "Químico", "Químico"
    RET= "Retail", "Retail"
    SGRPR = "Saneamiento / gestión de residuos / plantas de reciclaje", "Saneamiento / gestión de residuos / plantas de reciclaje"
    TEL = "Telecomunicaciones", "Telecomunicaciones"
    TEX= "Textil", "Textil"
    TRA = "Transporte", "Transporte"
    OT = "Otros", "Otros"


class OficioTypeChoices(TextChoices):
    AD= "Administrativos", "Administrativos"
    AG= "Agricultor", "Agricultor"
    AB= "Albañil", "Albañil"
    AL= "Almacenero", "Almacenero"
    CA= "Carpintero", "Carpintero"
    CH="Chofer", "Chofer"
    CM= "Comerciante", "Comerciante"
    EL = "Electricista", "Electricista"
    ES = "Estudiante", "Estudiante"
    GAS = "Gasfitero", "Gasfitero"
    ING = "Ingeniero", "Ingeniero"
    MOB= "Maestro de obra", "Maestro de obra"
    OP= "Operario", "Operario"
    PL = "Pesonal de limpieza", "Personal de limpieza"
    PS= "Personal de seguridad", "Personal de seguridad"
    PA= "Pescador artesanal", "Personal artesanal"
    PI= "Pintor", "Pintor"
    SOL= "Soldador", "Soldador"
    OT= "Otros", "Otros"