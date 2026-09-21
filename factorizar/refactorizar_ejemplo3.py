# Sistema de telemetría y alertas industriales
g_alerts = []

class SensorManager:
    # Malas prácticas: argumentos por defecto mutables
    def __init__(self, cfg={"temp_limit": 80, "press_limit": 100, "log_path": "alerts.log"}):
        self.cfg = cfg

    # Monolito con lógica de negocio, I/O, notificaciones y retorno inconsistente
    def process_readings(self, readings, notify=True, storage=[]):
        global g_alerts
        
        for r in readings:
            # Pirámide de condicionales y verificación no idiomática de tipos
            if type(r) == dict:
                if 'type' in r.keys():
                    if r['type'] == 'temp':
                        if 'val' in r.keys():
                            v = r['val']
                            if v > self.cfg['temp_limit']:
                                msg = "CRITICAL: High Temp " + str(v) + " in " + str(r.get('loc', 'unknown'))
                                g_alerts.append(msg)
                                storage.append(msg)
                                if notify == True:
                                    print("SENDING EMAIL TO admin@factory.com: " + msg)
                                try:
                                    f = open(self.cfg['log_path'], "a")
                                    f.write(msg + "\n")
                                    f.close()
                                except Exception:
                                    pass
                            elif v > self.cfg['temp_limit'] - 10:
                                print("WARNING: Temp high " + str(v))
                            else:
                                print("Temp OK: " + str(v))
                    elif r['type'] == 'press':
                        if 'val' in r.keys():
                            v = r['val']
                            if v > self.cfg['press_limit']:
                                msg = "CRITICAL: High Pressure " + str(v) + " in " + str(r.get('loc', 'unknown'))
                                g_alerts.append(msg)
                                storage.append(msg)
                                if notify == True:
                                    print("SENDING SMS TO +123456789: " + msg)
                                try:
                                    f = open(self.cfg['log_path'], "a")
                                    f.write(msg + "\n")
                                    f.close()
                                except Exception:
                                    pass
                            else:
                                print("Pressure OK: " + str(v))
                    else:
                        print("Unknown sensor type")
                else:
                    return False
            else:
                return -1
        
        return len(storage)

# Ejecución de prueba
sm = SensorManager()
data = [
    {'type': 'temp', 'val': 95, 'loc': 'Zone-A'},
    {'type': 'press', 'val': 110, 'loc': 'Zone-B'},
    {'type': 'temp', 'val': 75, 'loc': 'Zone-A'}
]

sm.process_readings(data)
