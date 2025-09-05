import sys,os,getpass,requests,time,csv,logging
from datetime import datetime

logging.basicConfig( 
    filename="registro.log", 
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s" 
) 
if len(sys.argv) != 2: 
    print("Uso: python verificar_correo.py correo@example.com") 
    sys.exit(1) 
correo = sys.argv[1] 
api_key_path="apikey.txt"
if not os.path.exists("apikey.txt"): 
    print("No se encontró el archivo apikey.txt.") 
    clave = getpass.getpass("Ingresa tu API key: ") 
    try:
        with open("apikey.txt", "w") as archivo: 
            archivo.write(clave.strip()) 
    except Exception as e:
        logging.error(f"No se pudo guardar la API key: {e}")
        sys.exit(1)
try: 
    with open("apikey.txt", "r") as archivo: 
        api_key = archivo.read().strip() 
except FileNotFoundError: 
    print("Error al leer la API key")
    logging.error(f"Error al leer apikey.txt {e}") 
    sys.exit(1) 
url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{correo}" 
headers = { 
    "hibp-api-key": api_key, 
    "user-agent": "PythonScript" 
} 
try:
    response = requests.get(url, headers=headers) 
except Exception as e:
    print("Error al conectar con la API")
    logging.error(f"Error de conexión: {e}")
    sys.exit(1)
if response.status_code == 200: 
    brechas = response.json() 
    logging.info(f"Consulta exitosa para {correo}. Brechas encontradas: {len(brechas)}")
    try:
        with open("reporte.csv","w",newline='',encoding="utf-8") as archivo_csv:
            with open("reporte.csv", "w", newline='', encoding="utf-8") as archivo_csv: 
                writer = csv.writer(archivo_csv)
                writer.writerow(["Título","Dominio","Fecha de Brecha",
                             "Datos Comprometidos", "Verificada","Sensible"]) 
                for i,brecha in enumerate(brechas[:3]):
                    nombre=brecha['Name']
                    detalle_url=f"https://haveibeenpwned.com/api/v3/breach/{nombre}"
                    try:
                        detalle_resp=requests.get(detalle_url, headers=headers)
                        if detalle_resp.status_code==200:
                            detalle=detalle_resp.json()
                            writer.writerow([
                                detalle.get("Title"),
                                detalle.get("Domain"),
                                detalle.get("BreachDate"),
                                ", ".join(detalle.get("DataClasses",[])),
                                "Sí" if detalle.get("IsVerified") else "No",
                                "Sí" if detalle.get("IsSensitive") else "No"
                            ])
                        else:
                            msj=f"No se pudo obtener detalles de la brecha {nombre}"
                            msj+=f"Código: {detalle_resp.status_code}"
                            logging.error(msj)
                    except Exception as e:
                        logging.error(f"Error al consultar detalles de la brecha: {nombre}")
                    if i<2:
                        time.sleep(10)
    except Exception as e:
        print("Error al generar el archivo CSV.")
        logging.error(f"Error al escribir reporte.csv: {e}")
        sys.exit(1)
elif response.status_code == 404: 
    print(f"La cuenta {correo} no aparece en ninguna brecha conocida.") 
elif response.status_code == 401: 
    print("Error de autenticación: revisa tu API key.") 
else: 
    print(f"Error inesperado. Código de estado: {response.status_code}") 
