import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import winsound
from matplotlib.patches import Ellipse
import sys
import time

# ============================================================
# CONSTANTES Y PARÁMETROS GLOBALES
# ============================================================

N = 25
ANGULOS = np.linspace(0, 2*np.pi, N, endpoint=False)
TIME_WARP = 1.0
DECAY_MODE = True

# Umbrales para N+2
IMPULSO_MINIMO = 0.15
EDAD_DESPIERTE = 0.6

# ============================================================
# ESTADO DEL MUNDO (VALORES INICIALES) - AJUSTADOS
# ============================================================

pos = np.array([0.0, 0.0])
theta = 0.0

# === AJUSTE: Menos hambre al inicio ===
hunger = 0.3  # <--- ANTES: 0.7
safety = 0.0  
danger = 0.0
border_stress = 0.0  

# ============================================================
# ENTIDADES DINÁMICAS
# ============================================================

food_pos = np.array([0.65, 0.45])
food_theta = 0.0
food_radius = 0.65

home_pos = np.array([-0.55, -0.35])
home_theta = np.pi
home_radius = 0.60

pred_pos = np.array([0.0, -0.7])
pred_theta = 0.0
pred_radius = 0.8

# ============================================================
# NIDO (N+2) - CONSTRUCCIÓN
# ============================================================

nido_pos = np.array([-0.70, 0.70])
nido_tamaño = 0.30
nido_celdas = 3
tam_celda = nido_tamaño / nido_celdas

materiales_recolectados = 0
materiales_maximos = 9
nido_completado = False

material_pos = np.array([0.0, 0.0])
material_activo = False
material_lock = False

tiene_brizna = False

# N+2: INSTINTO PROFUNDO (como la edad)
edad = 0.0
instinto_construccion = 0.0
build_despierto = False

# === AJUSTE: Impulso y urgencia más altos ===
impulso_construir = 0.8  # <--- ANTES: 0.6
tasa_impulso_base = 0.015
urgencia_constructiva = 1.2  # <--- ANTES: 0.8

# Control de generación de materiales
materiales_generados = 0
# === AJUSTE: Más materiales disponibles ===
max_materiales_generados = 30  # <--- ANTES: 15
tiempo_sin_material = 0.0

construccion_activa = False
tiempo_sin_construir = 0.0

# ============================================================
# CONTROL
# ============================================================

food_lock = False
home_lock = False

# ============================================================
# BIOLOGICAL BRAIN: TRES ÁREAS CORTICALES
# ============================================================

# ÁREA 1: Corteza Motivacional (MOT)
activity_mot = np.zeros(N)
cms_mot = []
for k in range(N):
    cms_mot.append({
        "angle": ANGULOS[k],
        "food_weight": np.random.uniform(1.2, 1.6),
        "home_weight": np.random.uniform(1.3, 1.7),
        "pred_weight": np.random.uniform(1.2, 1.7),
        "explore": np.random.uniform(0, 0.06)
    })

# ÁREA 2: Corteza de Navegación Basal (NAV)
activity_nav = np.zeros(N)
cms_nav = []
for k in range(N):
    cms_nav.append({
        "angle": ANGULOS[k],
        "border_weight": np.random.uniform(0.8, 1.2),
        "explore": np.random.uniform(0, 0.05)
    })

# ============================================================
# ÁREA 3: CORTEZA CONSTRUCTIVA N+2 (MEJORADA)
# ============================================================

activity_n2 = np.zeros(N)
estela_n2 = np.zeros(N)
estela_material = 0.0
estela_nido = 0.0

cms_n2 = []
for k in range(N):
    cms_n2.append({
        "angle": ANGULOS[k],
        "material_weight": np.random.uniform(1.2, 1.6),
        "nido_weight": np.random.uniform(1.3, 1.7),
        "carga_weight": np.random.uniform(1.0, 1.4),
        "descarga_weight": np.random.uniform(1.1, 1.5),
        "explore": np.random.uniform(0, 0.04)
    })

# ============================================================
# MAPA VISUAL CORTICAL (21x21)
# ============================================================

brain = np.zeros((21, 21))

# ÁREA 1: MOT - ARRIBA IZQUIERDA (filas 3-7, columnas 3-7)
core_mot = [(r, c) for r in range(3, 8) for c in range(3, 8)]

# ÁREA 2: NAV - ARRIBA DERECHA (filas 3-7, columnas 13-17)
core_nav = [(r, c) for r in range(3, 8) for c in range(13, 18)]

# ÁREA 3: N+2 - CENTRO ABAJO (filas 12-16, columnas 8-12)
core_n2 = [(r, c) for r in range(12, 17) for c in range(8, 13)]

# ============================================================
# FIGURA
# ============================================================

print("🔄 Creando figura...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_facecolor("black")
ax1.set_title("MUNDO - CONSTRUCCIÓN N+2", color='white', fontsize=10)

# Zonas
home_zone = plt.Circle((home_pos[0], home_pos[1]), 0.25, color='blue', alpha=0.15, fill=True)
ax1.add_patch(home_zone)

home_safety_zone = plt.Circle((home_pos[0], home_pos[1]), 0.30, color='blue', alpha=0.05, fill=True)
ax1.add_patch(home_safety_zone)

boundary = plt.Rectangle((-0.95, -0.95), 1.9, 1.9, edgecolor='red', linestyle='--', fill=False, alpha=0.3)
ax1.add_patch(boundary)

# Elementos dinámicos
dot, = ax1.plot([0], [0], 'wo', markersize=7)
food_dot, = ax1.plot(food_pos[0], food_pos[1], 'r*', markersize=14)
home_dot, = ax1.plot(home_pos[0], home_pos[1], 'bo', markersize=12)
pred_dot, = ax1.plot(pred_pos[0], pred_pos[1], 'go', markersize=14)

material_patch = Ellipse((0, 0), width=0.08, height=0.05,
                         facecolor='yellow', edgecolor='yellow', alpha=0.9)
ax1.add_patch(material_patch)
material_patch.set_visible(False)

line, = ax1.plot([0, 0], [0, 0], 'w-', linewidth=2)

# ============================================================
# PANEL 2: CORTEZA CEREBRAL
# ============================================================

img = ax2.imshow(brain, vmin=0, vmax=1, cmap='inferno')

# Líneas divisorias
ax2.axvline(7.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axvline(12.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axhline(7.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axhline(11.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)

# Etiquetas de áreas
ax2.text(5, 19, 'MOT', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkred', alpha=0.7))
ax2.text(10, 19, 'N+2', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.7))
ax2.text(15, 19, 'NAV', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.7))

# Etiqueta dentro del área N+2
ax2.text(10, 14, 'CONSTRUCCIÓN', color='white', fontsize=7, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.4))

ax2.set_title("CORTEZA CEREBRAL", color='white', fontsize=10)

# Texto de información
info_text = ax2.text(0.02, 0.98, "",
                     transform=ax2.transAxes,
                     color='white', fontsize=8,
                     verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

# ============================================================
# CONSTRUCCIÓN DEL NIDO - CORREGIDO CON 9 CELDAS INDIVIDUALES
# ============================================================

inicio_x = nido_pos[0] - nido_tamaño / 2
inicio_y = nido_pos[1] - nido_tamaño / 2

# Cuadrícula del nido
ax1.plot([inicio_x, inicio_x + nido_tamaño], [inicio_y, inicio_y],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([inicio_x, inicio_x + nido_tamaño], [inicio_y + nido_tamaño, inicio_y + nido_tamaño],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([inicio_x, inicio_x], [inicio_y, inicio_y + nido_tamaño],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([inicio_x + nido_tamaño, inicio_x + nido_tamaño], [inicio_y, inicio_y + nido_tamaño],
        color='yellow', linewidth=2, alpha=0.8)

for i in range(1, nido_celdas):
    x = inicio_x + i * tam_celda
    ax1.plot([x, x], [inicio_y, inicio_y + nido_tamaño],
            color='yellow', linewidth=1, alpha=0.5)
    y = inicio_y + i * tam_celda
    ax1.plot([inicio_x, inicio_x + nido_tamaño], [y, y],
            color='yellow', linewidth=1, alpha=0.5)

# ============================================================
# CREACIÓN DE 9 CELDAS INDIVIDUALES PARA EL NIDO
# ============================================================

celdas = []
for fila in range(3):
    for col in range(3):
        x = inicio_x + col * tam_celda
        y = inicio_y + fila * tam_celda
        celda = plt.Rectangle((x, y), tam_celda, tam_celda,
                              facecolor='yellow', alpha=0.0, edgecolor='none')
        ax1.add_patch(celda)
        celdas.append(celda)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def actualizar_nido():
    """Actualiza el nido usando 9 celdas individuales.
    El llenado sigue el orden: fila 0 (0,1,2), fila 1 (3,4,5), fila 2 (6,7,8)
    """
    global celdas, materiales_recolectados, materiales_maximos, nido_completado

    celdas_llenas = min(materiales_recolectados, materiales_maximos)

    # Apagar todas las celdas
    for celda in celdas:
        celda.set_alpha(0.0)

    # Encender las celdas llenas (de 0 a celdas_llenas-1)
    for i in range(celdas_llenas):
        celdas[i].set_alpha(0.6)

    if celdas_llenas >= materiales_maximos:
        nido_completado = True

def generar_material():
    global material_pos, material_activo
    global materiales_generados, tiempo_sin_material

    if materiales_generados >= max_materiales_generados or nido_completado:
        material_activo = False
        return

    if material_activo:
        return

    centro_x = 0.75
    centro_y = -0.75
    radio = 0.20

    # === AJUSTE: Más intentos para encontrar posición ===
    for _ in range(200):  # <--- ANTES: 100
        angulo = np.random.uniform(0, 2 * np.pi)
        distancia = np.random.uniform(0, radio)
        x = centro_x + distancia * np.cos(angulo)
        y = centro_y + distancia * np.sin(angulo)
        nueva_pos = np.array([x, y])

        dist_nido = np.linalg.norm(nueva_pos - nido_pos)
        dist_home = np.linalg.norm(nueva_pos - home_pos)
        # === AJUSTE: Radio de exclusión más pequeño ===
        if dist_nido > 0.20 and dist_home > 0.20:  # <--- ANTES: 0.25
            material_pos = nueva_pos
            material_activo = True
            materiales_generados += 1
            print(f"🔶 Material generado en ({material_pos[0]:.2f}, {material_pos[1]:.2f})")
            return

    material_activo = False

def actualizar_edad(dt):
    global edad, build_despierto, instinto_construccion
    # Maduración 66x más rápida para pruebas
    edad += 0.01 * dt

    if edad > EDAD_DESPIERTE and not build_despierto:
        build_despierto = True
        print(f"🔥 ¡INSTINTO DE CONSTRUCCIÓN DESPIERTA! Edad: {edad:.3f}")

    if build_despierto:
        instinto_construccion = min(1.0, (edad - EDAD_DESPIERTE) * 3.0)

    return edad, instinto_construccion, build_despierto

def reset_system():
    global pos, theta, hunger, safety, danger, border_stress
    global activity_mot, activity_nav, activity_n2, brain
    global food_pos, food_theta, home_pos, home_theta, pred_pos, pred_theta
    global food_lock, home_lock
    global materiales_recolectados, material_activo, material_lock
    global nido_completado, tiene_brizna
    global impulso_construir, materiales_generados, tiempo_sin_material
    global construccion_activa, tiempo_sin_construir, urgencia_constructiva
    global edad, instinto_construccion, build_despierto
    global estela_n2, estela_material, estela_nido
    global celdas

    try:
        winsound.Beep(180, 600)
    except:
        pass

    print("🔄 SISTEMA REINICIADO")

    pos = np.array([0.0, 0.0])
    theta = 0.0
    hunger = 0.3  # <--- ANTES: 0.7
    safety = 0.0
    danger = 0.0
    border_stress = 0.0

    activity_mot = np.zeros(N)
    activity_nav = np.zeros(N)
    activity_n2 = np.zeros(N)
    estela_n2 = np.zeros(N)
    estela_material = 0.0
    estela_nido = 0.0
    brain = np.zeros((21, 21))

    food_theta = np.random.uniform(0, 2*np.pi)
    home_theta = np.random.uniform(0, 2*np.pi)
    pred_theta = np.random.uniform(0, 2*np.pi)

    food_pos = np.array([food_radius * np.cos(food_theta), 0.55 * np.sin(1.7 * food_theta)])
    home_pos = np.array([home_radius * np.cos(home_theta), 0.45 * np.sin(1.3 * home_theta)])
    pred_pos = np.array([pred_radius * np.sin(pred_theta), pred_radius * np.cos(pred_theta)])

    food_lock = False
    home_lock = False
    material_lock = False
    materiales_recolectados = 0
    material_activo = False
    nido_completado = False
    tiene_brizna = False
    impulso_construir = 0.8  # <--- ANTES: 0.6
    materiales_generados = 0
    tiempo_sin_material = 0.0
    construccion_activa = False
    tiempo_sin_construir = 0.0
    urgencia_constructiva = 1.2  # <--- ANTES: 0.8
    edad = 0.0
    instinto_construccion = 0.0
    build_despierto = False

    actualizar_nido()

# ============================================================
# FUNCIÓN DE ACTUALIZACIÓN DE N+2
# ============================================================

def calcular_motor_n2():
    global activity_n2, estela_n2, estela_material, estela_nido
    global edad, instinto_construccion, build_despierto

    vec_material = material_pos - pos if material_activo else np.array([0.0, 0.0])
    vec_nido = nido_pos - pos

    angle_material = np.arctan2(vec_material[1], vec_material[0]) if np.linalg.norm(vec_material) > 0 else 0.0
    angle_nido = np.arctan2(vec_nido[1], vec_nido[0]) if np.linalg.norm(vec_nido) > 0 else 0.0

    angle_edad = edad * 2 * np.pi
    angle_instinto = instinto_construccion * 2 * np.pi
    angle_buche = 0.0 if not tiene_brizna else np.pi

    energias = np.zeros(N)

    for i, cm in enumerate(cms_n2):
        material_align = np.cos(angle_material - cm["angle"]) if material_activo else 0.0
        nido_align = np.cos(angle_nido - cm["angle"])
        edad_align = np.cos(angle_edad - cm["angle"])
        instinto_align = np.cos(angle_instinto - cm["angle"])
        buche_align = np.cos(angle_buche - cm["angle"])

        if tiene_brizna:
            energias[i] = (
                cm["nido_weight"] * nido_align * 0.7 +
                cm["descarga_weight"] * buche_align * 0.5 +
                cm["material_weight"] * material_align * 0.1 +
                instinto_construccion * 1.5 * instinto_align +
                cm["explore"] * np.random.uniform(-1, 1)
            )
        else:
            if material_activo:
                energias[i] = (
                    cm["material_weight"] * material_align * 0.8 +
                    cm["carga_weight"] * (1.0 - buche_align) * 0.5 +
                    cm["nido_weight"] * nido_align * 0.1 +
                    instinto_construccion * 1.5 * instinto_align +
                    cm["explore"] * np.random.uniform(-1, 1)
                )
            else:
                energias[i] = (
                    cm["explore"] * np.random.uniform(0.5, 1.5) +
                    instinto_construccion * 1.0 * instinto_align
                )

        if build_despierto:
            energias[i] *= (1.0 + instinto_construccion * 0.5)

    winner_n2 = np.argmax(energias)

    # ESTELA DE N+2 (decaimiento exponencial)
    estela_n2 *= 0.90
    estela_n2[winner_n2] += 1.0

    if tiene_brizna:
        estela_nido += 1.0
    else:
        if material_activo:
            estela_material += 1.0

    # Actividad de N+2 - inyección fuerte para visibilidad
    activity_n2 *= (0.95 ** TIME_WARP)
    activity_n2[winner_n2] += 2.0 + 1.0 * impulso_construir

    if winner_n2 >= 0:
        for i in range(max(0, winner_n2-3), min(N, winner_n2+4)):
            if i != winner_n2:
                diff = abs(i - winner_n2)
                activity_n2[i] += (1.5 + 0.5 * impulso_construir) * (1.0 - diff/4.0)

    activity_n2 = np.clip(activity_n2, 0, 2.0)

    motor = np.zeros(2)
    for i in range(N):
        vec = np.array([np.cos(ANGULOS[i]), np.sin(ANGULOS[i])])
        motor += activity_n2[i] * vec

    if estela_material > 0 and material_activo:
        motor += 0.1 * (material_pos - pos) / (1.0 + np.linalg.norm(material_pos - pos))
    if estela_nido > 0:
        motor += 0.1 * (nido_pos - pos) / (1.0 + np.linalg.norm(nido_pos - pos))

    if np.linalg.norm(motor) > 0:
        motor /= np.linalg.norm(motor)

    return motor, winner_n2

# ============================================================
# UPDATE LOOP
# ============================================================

def update(frame):
    global pos, theta
    global hunger, safety, danger, border_stress
    global activity_mot, activity_nav, activity_n2, brain
    global food_pos, home_pos, pred_pos
    global food_theta, home_theta, pred_theta
    global food_lock, home_lock
    global materiales_recolectados, material_activo, material_pos, material_lock
    global nido_completado, tiene_brizna
    global impulso_construir, materiales_generados, tiempo_sin_material
    global construccion_activa, tiempo_sin_construir, urgencia_constructiva
    global edad, instinto_construccion, build_despierto

    # ========================================================
    # 1. DISTANCIAS CRÍTICAS
    # ========================================================
    dist_food = np.linalg.norm(pos - food_pos)
    dist_home = np.linalg.norm(pos - home_pos)
    dist_pred = np.linalg.norm(pos - pred_pos)
    dist_nido = np.linalg.norm(pos - nido_pos)
    dist_material = np.linalg.norm(pos - material_pos) if material_activo else 999.0

    # ========================================================
    # 2. HOMEOSTASIS - AJUSTADA
    # ========================================================
    # === AJUSTE: El hambre crece más lento ===
    hunger += 0.0015 * TIME_WARP  # <--- ANTES: 0.0028

    if dist_home < 0.25:
        safety = 0.0
    else:
        safety += 0.0020 * TIME_WARP

    hunger = np.clip(hunger, 0, 1)
    safety = np.clip(safety, 0, 1)
    # === AJUSTE: El peligro crece más lento ===
    danger += 0.003 * TIME_WARP  # <--- ANTES: 0.006
    danger = np.clip(danger, 0, 1)

    in_cave_repose = False
    if dist_home < 0.25:
        if hunger > 0.40:
            in_cave_repose = False
            effective_hunger = hunger
            current_safety_need = 0.0
        else:
            in_cave_repose = True
            effective_hunger = 0.0
            current_safety_need = 1.0
    else:
        if safety > 0.80:
            attenuation = (1.0 - safety) / 0.20
            effective_hunger = hunger * np.clip(attenuation, 0, 1)
            current_safety_need = safety * 1.8
        elif hunger > 0.50 and safety < 0.40:
            effective_hunger = hunger * 1.5
            current_safety_need = safety * 0.3
        else:
            effective_hunger = hunger
            current_safety_need = safety

    # ========================================================
    # 3. EDAD E INSTINTO
    # ========================================================
    edad, instinto_construccion, build_despierto = actualizar_edad(TIME_WARP)

    # ========================================================
    # 4. URGENCIA CONSTRUCTIVA
    # ========================================================
    if not nido_completado:
        urgencia_constructiva += 0.005 * TIME_WARP

        if material_activo and not tiene_brizna:
            urgencia_constructiva += 0.015 * TIME_WARP

        if tiene_brizna:
            urgencia_constructiva += 0.02 * TIME_WARP

        if materiales_recolectados > 0:
            progreso = materiales_recolectados / materiales_maximos
            urgencia_constructiva += 0.005 * progreso * TIME_WARP

        tiempo_sin_construir += TIME_WARP
        if tiempo_sin_construir > 60:
            urgencia_constructiva += 0.01 * TIME_WARP

        urgencia_constructiva = max(urgencia_constructiva, 0.5)
        urgencia_constructiva = np.clip(urgencia_constructiva, 0, 1.5)

    # ========================================================
    # 5. ESTRÉS DE BORDES
    # ========================================================
    dist_to_wall_x = 1.0 - abs(pos[0])
    dist_to_wall_y = 1.0 - abs(pos[1])
    closest_wall_dist = min(dist_to_wall_x, dist_to_wall_y)
    if closest_wall_dist < 0.25:
        border_stress = np.clip((0.25 - closest_wall_dist) / 0.25, 0, 1) ** 2
    else:
        border_stress = 0.0

    # ========================================================
    # 6. MOVIMIENTO DE ENTIDADES
    # ========================================================
    food_theta += 0.015 * TIME_WARP
    food_pos = np.array([food_radius * np.cos(food_theta), 0.55 * np.sin(1.7 * food_theta)])

    home_theta -= 0.010 * TIME_WARP
    home_pos = np.array([home_radius * np.cos(home_theta), 0.45 * np.sin(1.3 * home_theta)])
    home_zone.set_center((home_pos[0], home_pos[1]))
    home_safety_zone.set_center((home_pos[0], home_pos[1]))

    # ========================================================
    # 7. MOVIMIENTO DEPREDADOR
    # ========================================================
    pred_speed = 0.023 * TIME_WARP
    if dist_home < 0.30:
        pred_theta += np.random.uniform(-0.8, 0.8)
    else:
        to_prey = pos - pred_pos
        pred_theta = np.arctan2(to_prey[1], to_prey[0])
    pred_pos += pred_speed * np.array([np.cos(pred_theta), np.sin(pred_theta)])
    pred_pos = np.clip(pred_pos, -1.2, 1.2)

    # ========================================================
    # 8. COLISIONES / RECOMPENSAS
    # ========================================================
    if dist_food < 0.10 and not food_lock:
        hunger = 0.0
        try:
            winsound.Beep(1200, 120)
        except:
            pass
        food_lock = True

    if dist_home < 0.10 and not home_lock:
        try:
            winsound.Beep(500, 180)
        except:
            pass
        home_lock = True

    if dist_pred < 0.12:
        if dist_home < 0.30:
            danger = 0.0
        else:
            reset_system()
            return dot, line, img, food_dot, home_dot, pred_dot, material_patch, info_text

    if dist_food > 0.18:
        food_lock = False
    if dist_home > 0.18:
        home_lock = False

    # ========================================================
    # 9. IMPULSO CONSTRUCTIVO
    # ========================================================
    if nido_completado:
        impulso_construir *= 0.95
    else:
        impulso_construir += tasa_impulso_base * TIME_WARP
        impulso_construir += urgencia_constructiva * 0.02 * TIME_WARP

        if material_activo and not tiene_brizna:
            impulso_construir += 0.01 * TIME_WARP

        if tiene_brizna:
            impulso_construir += 0.02 * TIME_WARP

        if materiales_recolectados > 0:
            progreso = materiales_recolectados / materiales_maximos
            impulso_construir += 0.005 * progreso * TIME_WARP

        if tiempo_sin_construir > 50:
            impulso_construir += 0.01 * TIME_WARP

        impulso_construir = max(impulso_construir, 0.4)

    impulso_construir = np.clip(impulso_construir, 0, 1)

    # ========================================================
    # 10. RECOLECCIÓN DE MATERIALES
    # ========================================================
    if (dist_material < 0.12 and material_activo and not material_lock
        and not tiene_brizna and not nido_completado):
        tiene_brizna = True
        material_activo = False
        material_lock = True
        try:
            winsound.Beep(800, 100)
        except:
            pass
        construccion_activa = True
        tiempo_sin_construir = 0.0

    if tiene_brizna and dist_nido < 0.25 and not nido_completado:
        materiales_recolectados += 1
        tiene_brizna = False
        try:
            winsound.Beep(600, 150)
        except:
            pass
        actualizar_nido()
        construccion_activa = True
        tiempo_sin_construir = 0.0
        # === AJUSTE: Casi no baja el impulso ===
        impulso_construir = np.clip(impulso_construir - 0.005, 0.6, 1)  # <--- ANTES: 0.02, 0.4

    if dist_material > 0.15 and material_lock:
        material_lock = False

    # ========================================================
    # 11. GENERAR NUEVO MATERIAL
    # ========================================================
    if materiales_recolectados >= materiales_maximos:
        nido_completado = True
        material_activo = False
    else:
        if not material_activo and not material_lock:
            if materiales_generados < max_materiales_generados:
                generar_material()
            else:
                tiempo_sin_material += TIME_WARP
                if tiempo_sin_material > 150:
                    materiales_generados = 0
                    tiempo_sin_material = 0.0
                    generar_material()

    # ========================================================
    # 12. DIRECCIONES SENSORIALES
    # ========================================================
    vec_food = food_pos - pos
    vec_home = home_pos - pos
    vec_pred = pred_pos - pos
    angle_food = np.arctan2(vec_food[1], vec_food[0])
    angle_home = np.arctan2(vec_home[1], vec_home[0])
    angle_pred = np.arctan2(vec_pred[1], vec_pred[0])

    fuerza_oeste = 1.0 / (1.0 + (pos[0] - (-0.95)))
    fuerza_este = 1.0 / (1.0 + (0.95 - pos[0]))
    fuerza_sur = 1.0 / (1.0 + (pos[1] - (-0.95)))
    fuerza_norte = 1.0 / (1.0 + (0.95 - pos[1]))
    vec_border_continuo = np.array([
        (fuerza_este - fuerza_oeste),
        (fuerza_norte - fuerza_sur)
    ])
    angle_border = np.arctan2(vec_border_continuo[1], vec_border_continuo[0])

    # ========================================================
    # 13. COMPETENCIA ÁREA 1: MOTIVACIONAL
    # ========================================================
    current_danger_factor = 0.0 if dist_home < 0.25 else danger

    energies_mot = np.zeros(N)
    for i, cm in enumerate(cms_mot):
        food_align = np.cos(angle_food - cm["angle"])
        home_align = np.cos(angle_home - cm["angle"])
        pred_align = np.cos(angle_pred - cm["angle"])
        E_mot = (
            effective_hunger * cm["food_weight"] * food_align +
            current_safety_need * cm["home_weight"] * home_align -
            current_danger_factor * cm["pred_weight"] * pred_align +
            cm["explore"] * np.random.uniform(-1, 1)
        )
        energies_mot[i] = E_mot + 0.06 * np.random.randn()
    winner_mot = np.argmax(energies_mot)

    # ========================================================
    # 14. COMPETENCIA ÁREA 2: NAVEGACIÓN
    # ========================================================
    energies_nav = np.zeros(N)
    for i, cm in enumerate(cms_nav):
        border_align = np.cos(angle_border - cm["angle"])
        E_nav = -border_stress * cm["border_weight"] * border_align + cm["explore"] * np.random.uniform(-1, 1)
        energies_nav[i] = E_nav + 0.05 * np.random.randn()
    winner_nav = np.argmax(energies_nav)

    # ========================================================
    # 15. COMPETENCIA ÁREA 3: CONSTRUCTIVA N+2
    # ========================================================
    motor_n2 = np.zeros(2)
    winner_n2 = -1

    if build_despierto and impulso_construir > IMPULSO_MINIMO:
        motor_n2, winner_n2 = calcular_motor_n2()

    # ========================================================
    # 16. DECAY DE ÁREAS 1 Y 2
    # ========================================================
    if DECAY_MODE:
        activity_mot *= (0.92 ** TIME_WARP)
        activity_mot[winner_mot] += 1.0

        if in_cave_repose:
            activity_nav *= (0.70 ** TIME_WARP)
            if np.random.uniform(0, 1) < 0.40:
                num_destellos = np.random.choice([1, 2])
                indices_suertudos = np.random.choice(N, size=num_destellos, replace=False)
                brillo_destello = 0.65 + 0.25 * np.sin(frame * 0.2)
                activity_nav[indices_suertudos] += brillo_destello
        else:
            activity_nav *= (0.90 ** TIME_WARP)
            activity_nav[winner_nav] += 1.0
    else:
        activity_mot[:] = 0.0
        activity_mot[winner_mot] = 1.0
        activity_nav[:] = 0.0
        activity_nav[winner_nav] = 1.0

    activity_mot = np.clip(activity_mot, 0, 1)
    activity_nav = np.clip(activity_nav, 0, 1)

    # ========================================================
    # 17. SÍNTESIS MOTORA
    # ========================================================
    motor_mot = np.zeros(2)
    motor_nav = np.zeros(2)

    for i in range(N):
        vec = np.array([np.cos(ANGULOS[i]), np.sin(ANGULOS[i])])
        motor_mot += activity_mot[i] * vec
        motor_nav += activity_nav[i] * vec

    if np.linalg.norm(motor_mot) > 0:
        motor_mot /= np.linalg.norm(motor_mot)
    if np.linalg.norm(motor_nav) > 0:
        motor_nav /= np.linalg.norm(motor_nav)

    # ========================================================
    # 18. INTEGRACIÓN DE ÁREAS - AJUSTADA
    # ========================================================
    if build_despierto and impulso_construir > IMPULSO_MINIMO:
        # === AJUSTE: N+2 tiene más peso ===
        peso_n2 = impulso_construir * 0.7  # <--- ANTES: 0.5

        factor_hambre = 1.0 - (hunger * 0.5)
        peso_n2 *= factor_hambre

        if dist_pred < 0.4:
            factor_peligro = dist_pred / 0.4
            peso_n2 *= factor_peligro

        if tiene_brizna:
            peso_n2 = min(1.0, peso_n2 * 1.3)

        # === AJUSTE: Límite más alto ===
        peso_n2 = np.clip(peso_n2, 0, 0.7)  # <--- ANTES: 0.5
        motor_primario = (1.0 - peso_n2) * motor_mot + peso_n2 * motor_n2
    else:
        motor_primario = motor_mot

    if border_stress > 0.15:
        motor = (1.0 - border_stress) * motor_primario + border_stress * motor_nav
    else:
        motor = motor_primario

    if np.linalg.norm(motor) > 0:
        motor /= np.linalg.norm(motor)

    # ========================================================
    # 19. MOVIMIENTO FINAL - AJUSTADO
    # ========================================================
    mag = np.linalg.norm(motor)
    if mag > 0:
        theta = np.arctan2(motor[1], motor[0])
        # === AJUSTE: Criatura más rápida ===
        speed = (0.04 + 0.04 * np.clip(mag, 0, 1)) * TIME_WARP  # <--- ANTES: 0.03
        if not in_cave_repose:
            pos += speed * motor

    pos = np.clip(pos, -0.95, 0.95)

    # ========================================================
    # 20. MAPA VISUAL CORTICAL
    # ========================================================
    brain *= 0.82

    # MOT (filas 3-7, columnas 3-7)
    for i, a in enumerate(activity_mot):
        if i < len(core_mot):
            r, c = core_mot[i]
            brain[r, c] = a

    # NAV (filas 3-7, columnas 13-17)
    for i, a in enumerate(activity_nav):
        if i < len(core_nav):
            r, c = core_nav[i]
            brain[r, c] = a

    # N+2 (filas 12-16, columnas 8-12)
    for i, a in enumerate(activity_n2):
        if i < len(core_n2):
            r, c = core_n2[i]
            brain[r, c] = a * 5.0

    brain = np.clip(brain, 0, 1)

    # ========================================================
    # 21. INTERFAZ GRÁFICA
    # ========================================================
    dot.set_data([pos[0]], [pos[1]])
    head = pos + 0.12 * np.array([np.cos(theta), np.sin(theta)])
    line.set_data([pos[0], head[0]], [pos[1], head[1]])

    food_dot.set_data([food_pos[0]], [food_pos[1]])
    home_dot.set_data([home_pos[0]], [home_pos[1]])
    pred_dot.set_data([pred_pos[0]], [pred_pos[1]])

    if material_activo:
        material_patch.center = (material_pos[0], material_pos[1])
        material_patch.set_visible(True)
    else:
        material_patch.set_visible(False)

    img.set_data(brain)

    # ========================================================
    # 22. TEXTO DE INFORMACIÓN
    # ========================================================
    intensidad_n2 = np.mean(activity_n2)
    if np.linalg.norm(motor_n2) > 0:
        angulo_n2 = np.arctan2(motor_n2[1], motor_n2[0]) * 180 / np.pi
        direccion_n2 = f"{angulo_n2:.0f}°"
    else:
        direccion_n2 = "---"

    estado_nido = "🏠 COMPLETADO 🎉" if nido_completado else f"🔨 {materiales_recolectados}/{materiales_maximos}"
    brizna_status = "🧱 Sí" if tiene_brizna else "❌ No"
    build_status = "🔥 ACTIVO" if build_despierto else "💤 DORMIDO"

    info_text.set_text(
        f"🍖 HAMBRE: {hunger:.2f}  🛡️ SEGURIDAD: {safety:.2f}\n"
        f"⚡ IMPULSO: {impulso_construir:.2f}  🔥 URGENCIA: {urgencia_constructiva:.2f}\n"
        f"🧱 BRIZNA: {brizna_status}  🎯 N+2: {intensidad_n2:.2f}\n"
        f"📐 DIRECCIÓN: {direccion_n2}  {estado_nido}\n"
        f"🧬 EDAD: {edad:.2f}  {build_status}"
    )

    return dot, line, img, food_dot, home_dot, pred_dot, material_patch, info_text

# ============================================================
# EJECUCIÓN
# ============================================================

print("=" * 60)
print("🐝 CREATURE DEEPY BEE N+2 - VERSIÓN DEFINITIVA")
print("=" * 60)
print("🔬 Áreas corticales:")
print("   - MOT: Motivacional (necesidades) - ARRIBA IZQUIERDA")
print("   - NAV: Navegación (espacio) - ARRIBA DERECHA")
print("   - N+2: Constructiva (MÚLTIPLES PESOS) - CENTRO ABAJO")
print("")
print("🎯 La criatura construirá un nido de 3x3")
print("📦 Materiales necesarios: 9 briznas")
print("")
print("✅ MEJORAS PARA COMPLETAR EL NIDO:")
print("   - Hambre inicial reducida (0.7 → 0.3)")
print("   - Hambre crece más lento (0.0028 → 0.0015)")
print("   - Peligro crece más lento (0.006 → 0.003)")
print("   - Impulso constructivo inicial más alto (0.6 → 0.8)")
print("   - Urgencia constructiva más alta (0.8 → 1.2)")
print("   - Más materiales disponibles (15 → 30)")
print("   - N+2 tiene más peso (0.5 → 0.7)")
print("   - Criatura más rápida (0.03 → 0.04)")
print("   - El impulso apenas baja al depositar")
print("")
print("⏳ Iniciando simulación...")
print("   (Cierra la ventana para terminar)")
print("=" * 60)
print("")

try:
    ani = FuncAnimation(fig, update, interval=60, cache_frame_data=False)
    plt.tight_layout()
    plt.show(block=True)

except KeyboardInterrupt:
    print("\n⏹️ Simulación interrumpida por el usuario.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("\n" + "=" * 60)
    print("✨ FIN DE LA SIMULACIÓN")
    print("=" * 60)
    if nido_completado:
        print("🏠 ¡La criatura construyó su nido!")
        print(f"   Materiales recolectados: {materiales_recolectados}")
        print(f"   Edad: {edad:.3f}")
    else:
        print(f"🏠 Progreso: {materiales_recolectados}/{materiales_maximos}")
        print(f"   Edad: {edad:.3f}")
    print("=" * 60)
    sys.exit(0)
