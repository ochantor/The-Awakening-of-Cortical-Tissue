#  Program by Oscar Chang.    
#  Ph.D,  AI researcher
import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
try:
    import winsound
except ImportError:
    winsound = None  # no Windows: Beep() calls are already inside try/except
from matplotlib.patches import Ellipse
import sys
import time

# ============================================================
# CONSTANTS AND GLOBAL PARAMETERS
# ============================================================

N = 25
ANGLES = np.linspace(0, 2*np.pi, N, endpoint=False)
TIME_WARP = 1.0
DECAY_MODE = True

# Thresholds for N+2
MINIMUM_IMPULSE = 0.15
AWAKENING_AGE = 0.6

# ============================================================
# WORLD STATE (INITIAL VALUES) - ADJUSTED
# ============================================================

pos = np.array([0.0, 0.0])
theta = 0.0

# === ADJUSTMENT: Less hunger at start ===
hunger = 0.3  # <--- BEFORE: 0.7
safety = 0.0  
danger = 0.0
border_stress = 0.0  

# ============================================================
# DYNAMIC ENTITIES
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
# NEST (N+2) - CONSTRUCTION
# ============================================================

nest_pos = np.array([-0.70, 0.70])
nest_size = 0.30
nest_cells = 3
cell_size = nest_size / nest_cells

materials_collected = 0
max_materials = 9
nest_completed = False

material_pos = np.array([0.0, 0.0])
material_active = False
material_lock = False

has_twig = False

# N+2: DEEP INSTINCT (like age)
age = 0.0
construction_instinct = 0.0
build_awake = False

# === ADJUSTMENT: Higher impulse and urgency ===
construction_impulse = 0.8  # <--- BEFORE: 0.6
base_impulse_rate = 0.015
constructive_urgency = 1.2  # <--- BEFORE: 0.8

# Material generation control
materials_generated = 0
# === ADJUSTMENT: More materials available ===
max_materials_generated = 30  # <--- BEFORE: 15
time_without_material = 0.0

construction_active = False
time_since_building = 0.0

# ============================================================
# CONTROL
# ============================================================

food_lock = False
home_lock = False

# ============================================================
# BIOLOGICAL BRAIN: THREE CORTICAL AREAS
# ============================================================

# AREA 1: Motivational Cortex (MOT)
activity_mot = np.zeros(N)
cms_mot = []
for k in range(N):
    cms_mot.append({
        "angle": ANGLES[k],
        "food_weight": np.random.uniform(1.2, 1.6),
        "home_weight": np.random.uniform(1.3, 1.7),
        "pred_weight": np.random.uniform(1.2, 1.7),
        "explore": np.random.uniform(0, 0.06)
    })

# AREA 2: Basal Navigation Cortex (NAV)
activity_nav = np.zeros(N)
cms_nav = []
for k in range(N):
    cms_nav.append({
        "angle": ANGLES[k],
        "border_weight": np.random.uniform(0.8, 1.2),
        "explore": np.random.uniform(0, 0.05)
    })

# ============================================================
# AREA 3: CONSTRUCTIVE CORTEX N+2 (IMPROVED)
# ============================================================

activity_n2 = np.zeros(N)
wake_n2 = np.zeros(N)
wake_material = 0.0
wake_nest = 0.0

cms_n2 = []
for k in range(N):
    cms_n2.append({
        "angle": ANGLES[k],
        "material_weight": np.random.uniform(1.2, 1.6),
        "nest_weight": np.random.uniform(1.3, 1.7),
        "load_weight": np.random.uniform(1.0, 1.4),
        "unload_weight": np.random.uniform(1.1, 1.5),
        "explore": np.random.uniform(0, 0.04)
    })

# ============================================================
# CORTICAL VISUAL MAP (21x21)
# ============================================================

brain = np.zeros((21, 21))

# AREA 1: MOT - UPPER LEFT (rows 3-7, columns 3-7)
core_mot = [(r, c) for r in range(3, 8) for c in range(3, 8)]

# AREA 2: NAV - UPPER RIGHT (rows 3-7, columns 13-17)
core_nav = [(r, c) for r in range(3, 8) for c in range(13, 18)]

# AREA 3: N+2 - LOWER CENTER (rows 12-16, columns 8-12)
core_n2 = [(r, c) for r in range(12, 17) for c in range(8, 13)]

# ============================================================
# FIGURE
# ============================================================

print("🔄 Creating figure...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_facecolor("black")
ax1.set_title("WORLD - N+2 CONSTRUCTION", color='white', fontsize=10)

# Zones
home_zone = plt.Circle((home_pos[0], home_pos[1]), 0.25, color='blue', alpha=0.15, fill=True)
ax1.add_patch(home_zone)

home_safety_zone = plt.Circle((home_pos[0], home_pos[1]), 0.30, color='blue', alpha=0.05, fill=True)
ax1.add_patch(home_safety_zone)

boundary = plt.Rectangle((-0.95, -0.95), 1.9, 1.9, edgecolor='red', linestyle='--', fill=False, alpha=0.3)
ax1.add_patch(boundary)

# Dynamic elements
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
# PANEL 2: CORTICAL BRAIN
# ============================================================

img = ax2.imshow(brain, vmin=0, vmax=1, cmap='inferno')

# Dividing lines
ax2.axvline(7.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axvline(12.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axhline(7.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)
ax2.axhline(11.5, color='white', linestyle=':', alpha=0.2, linewidth=0.5)

# Area labels
ax2.text(5, 19, 'MOT', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkred', alpha=0.7))
ax2.text(10, 19, 'N+2', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.7))
ax2.text(15, 19, 'NAV', color='white', fontsize=10, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.7))

# Label inside N+2 area
ax2.text(10, 14, 'CONSTRUCTION', color='white', fontsize=7, ha='center',
         bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.4))

ax2.set_title("CORTICAL BRAIN", color='white', fontsize=10)

# Information text
info_text = ax2.text(0.02, 0.98, "",
                     transform=ax2.transAxes,
                     color='white', fontsize=8,
                     verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

# ============================================================
# NEST CONSTRUCTION - CORRECTED WITH 9 INDIVIDUAL CELLS
# ============================================================

start_x = nest_pos[0] - nest_size / 2
start_y = nest_pos[1] - nest_size / 2

# Nest grid
ax1.plot([start_x, start_x + nest_size], [start_y, start_y],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([start_x, start_x + nest_size], [start_y + nest_size, start_y + nest_size],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([start_x, start_x], [start_y, start_y + nest_size],
        color='yellow', linewidth=2, alpha=0.8)
ax1.plot([start_x + nest_size, start_x + nest_size], [start_y, start_y + nest_size],
        color='yellow', linewidth=2, alpha=0.8)

for i in range(1, nest_cells):
    x = start_x + i * cell_size
    ax1.plot([x, x], [start_y, start_y + nest_size],
            color='yellow', linewidth=1, alpha=0.5)
    y = start_y + i * cell_size
    ax1.plot([start_x, start_x + nest_size], [y, y],
            color='yellow', linewidth=1, alpha=0.5)

# ============================================================
# CREATION OF 9 INDIVIDUAL CELLS FOR THE NEST
# ============================================================

cells = []
for row in range(3):
    for col in range(3):
        x = start_x + col * cell_size
        y = start_y + row * cell_size
        cell = plt.Rectangle((x, y), cell_size, cell_size,
                              facecolor='yellow', alpha=0.0, edgecolor='none')
        ax1.add_patch(cell)
        cells.append(cell)

# ============================================================
# AUXILIARY FUNCTIONS
# ============================================================

def update_nest():
    """Updates the nest using 9 individual cells.
    Filling order: row 0 (0,1,2), row 1 (3,4,5), row 2 (6,7,8)
    """
    global cells, materials_collected, max_materials, nest_completed

    cells_filled = min(materials_collected, max_materials)

    # Turn off all cells
    for cell in cells:
        cell.set_alpha(0.0)

    # Turn on filled cells (from 0 to cells_filled-1)
    for i in range(cells_filled):
        cells[i].set_alpha(0.6)

    if cells_filled >= max_materials:
        nest_completed = True

def generate_material():
    global material_pos, material_active
    global materials_generated, time_without_material

    if materials_generated >= max_materials_generated or nest_completed:
        material_active = False
        return

    if material_active:
        return

    center_x = 0.75
    center_y = -0.75
    radius = 0.20

    # === ADJUSTMENT: More attempts to find position ===
    for _ in range(200):  # <--- BEFORE: 100
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, radius)
        x = center_x + distance * np.cos(angle)
        y = center_y + distance * np.sin(angle)
        new_pos = np.array([x, y])

        dist_nest = np.linalg.norm(new_pos - nest_pos)
        dist_home = np.linalg.norm(new_pos - home_pos)
        # === ADJUSTMENT: Smaller exclusion radius ===
        if dist_nest > 0.20 and dist_home > 0.20:  # <--- BEFORE: 0.25
            material_pos = new_pos
            material_active = True
            materials_generated += 1
            print(f"🔶 Material generated at ({material_pos[0]:.2f}, {material_pos[1]:.2f})")
            return

    material_active = False

def update_age(dt):
    global age, build_awake, construction_instinct
    # Maturation 66x faster for testing
    age += 0.01 * dt

    if age > AWAKENING_AGE and not build_awake:
        build_awake = True
        print(f"🔥 CONSTRUCTION INSTINCT AWAKENS! Age: {age:.3f}")

    if build_awake:
        construction_instinct = min(1.0, (age - AWAKENING_AGE) * 3.0)

    return age, construction_instinct, build_awake

def reset_system():
    global pos, theta, hunger, safety, danger, border_stress
    global activity_mot, activity_nav, activity_n2, brain
    global food_pos, food_theta, home_pos, home_theta, pred_pos, pred_theta
    global food_lock, home_lock
    global materials_collected, material_active, material_lock
    global nest_completed, has_twig
    global construction_impulse, materials_generated, time_without_material
    global construction_active, time_since_building, constructive_urgency
    global age, construction_instinct, build_awake
    global wake_n2, wake_material, wake_nest
    global cells

    try:
        winsound.Beep(180, 600)
    except:
        pass

    print("🔄 SYSTEM RESET")

    pos = np.array([0.0, 0.0])
    theta = 0.0
    hunger = 0.3  # <--- BEFORE: 0.7
    safety = 0.0
    danger = 0.0
    border_stress = 0.0

    activity_mot = np.zeros(N)
    activity_nav = np.zeros(N)
    activity_n2 = np.zeros(N)
    wake_n2 = np.zeros(N)
    wake_material = 0.0
    wake_nest = 0.0
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
    materials_collected = 0
    material_active = False
    nest_completed = False
    has_twig = False
    construction_impulse = 0.8  # <--- BEFORE: 0.6
    materials_generated = 0
    time_without_material = 0.0
    construction_active = False
    time_since_building = 0.0
    constructive_urgency = 1.2  # <--- BEFORE: 0.8
    age = 0.0
    construction_instinct = 0.0
    build_awake = False

    update_nest()

# ============================================================
# N+2 UPDATE FUNCTION
# ============================================================

def calculate_n2_motor():
    global activity_n2, wake_n2, wake_material, wake_nest
    global age, construction_instinct, build_awake

    vec_material = material_pos - pos if material_active else np.array([0.0, 0.0])
    vec_nest = nest_pos - pos

    angle_material = np.arctan2(vec_material[1], vec_material[0]) if np.linalg.norm(vec_material) > 0 else 0.0
    angle_nest = np.arctan2(vec_nest[1], vec_nest[0]) if np.linalg.norm(vec_nest) > 0 else 0.0

    # NOTE: construction_instinct is no longer disguised as an "angle" (age*2*pi does
    # not represent any real direction). It is used as what it is: a scalar
    # that amplifies how much the impulse to build weighs against other things,
    # just like effective_hunger amplifies the food drive in MOT.
    #
    # has_twig and material_active remain binary sensor readings
    # (biologically reasonable: "are my jaws holding something?", "is there
    # material in sight right now?"). What changed is that they no longer branch
    # into different energy formulas -- they enter as 0/1 coefficients within
    # A SINGLE expression, like any other sensory term.
    load_bin = 1.0 if has_twig else 0.0
    material_available = 1.0 if material_active else 0.0

    energies = np.zeros(N)

    for i, cm in enumerate(cms_n2):
        material_align = np.cos(angle_material - cm["angle"]) if material_active else 0.0
        nest_align = np.cos(angle_nest - cm["angle"])

        energies[i] = (
            (1 - load_bin) * material_available * cm["material_weight"] * material_align * (0.8 + 0.5 * construction_instinct)
            + load_bin * cm["nest_weight"] * nest_align * (0.7 + 0.5 * construction_instinct)
            + load_bin * cm["material_weight"] * material_align * 0.1
            + (1 - load_bin) * material_available * cm["nest_weight"] * nest_align * 0.1
            + (1 - load_bin) * (1 - material_available) * cm["explore"] * np.random.uniform(0.5, 1.5) * (0.3 + construction_instinct)
            + cm["explore"] * np.random.uniform(-1, 1)
        )

    winner_n2 = np.argmax(energies)

    # N+2 WAKE (exponential decay)
    wake_n2 *= 0.90
    wake_n2[winner_n2] += 1.0

    if has_twig:
        wake_nest += 1.0
    else:
        if material_active:
            wake_material += 1.0

    # N+2 activity - strong injection for visibility
    activity_n2 *= (0.95 ** TIME_WARP)
    activity_n2[winner_n2] += 2.0 + 1.0 * construction_impulse

    if winner_n2 >= 0:
        for i in range(max(0, winner_n2-3), min(N, winner_n2+4)):
            if i != winner_n2:
                diff = abs(i - winner_n2)
                activity_n2[i] += (1.5 + 0.5 * construction_impulse) * (1.0 - diff/4.0)

    activity_n2 = np.clip(activity_n2, 0, 2.0)

    motor = np.zeros(2)
    for i in range(N):
        vec = np.array([np.cos(ANGLES[i]), np.sin(ANGLES[i])])
        motor += activity_n2[i] * vec

    if wake_material > 0 and material_active:
        motor += 0.1 * (material_pos - pos) / (1.0 + np.linalg.norm(material_pos - pos))
    if wake_nest > 0:
        motor += 0.1 * (nest_pos - pos) / (1.0 + np.linalg.norm(nest_pos - pos))

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
    global materials_collected, material_active, material_pos, material_lock
    global nest_completed, has_twig
    global construction_impulse, materials_generated, time_without_material
    global construction_active, time_since_building, constructive_urgency
    global age, construction_instinct, build_awake

    # ========================================================
    # 1. CRITICAL DISTANCES
    # ========================================================
    dist_food = np.linalg.norm(pos - food_pos)
    dist_home = np.linalg.norm(pos - home_pos)
    dist_pred = np.linalg.norm(pos - pred_pos)
    dist_nest = np.linalg.norm(pos - nest_pos)
    dist_material = np.linalg.norm(pos - material_pos) if material_active else 999.0

    # ========================================================
    # 2. HOMEOSTASIS - ADJUSTED
    # ========================================================
    # === ADJUSTMENT: Hunger grows slower ===
    hunger += 0.0015 * TIME_WARP  # <--- BEFORE: 0.0028

    if dist_home < 0.25:
        safety = 0.0
    else:
        safety += 0.0020 * TIME_WARP

    hunger = np.clip(hunger, 0, 1)
    safety = np.clip(safety, 0, 1)
    # === ADJUSTMENT: Danger grows slower ===
    danger += 0.003 * TIME_WARP  # <--- BEFORE: 0.006
    danger = np.clip(danger, 0, 1)

    # ========================================================
    # HOMEOSTATIC GATING - continuous version (no if/elif branches)
    # ========================================================
    # Previously this was a tree of 4 cases (dist_home</>=0.25, hunger>/<0.40,
    # safety>/<0.80, etc.), each with its own formula -- exactly the
    # same problem we already fixed in N+2. Here it is replaced by
    # smooth gates (sigmoids) that do the same thing continuously:
    # at the same threshold values, the result is practically identical,
    # but there is no longer a discrete branch selecting the formula.
    def _gate(x, steepness=30.0):
        return 1.0 / (1.0 + np.exp(-steepness * x))

    gate_at_home = _gate(0.25 - dist_home)          # ~1 if dist_home << 0.25
    gate_low_hunger = _gate(0.40 - hunger)          # ~1 if hunger << 0.40
    gate_high_safety = _gate(safety - 0.80)         # ~1 if safety >> 0.80
    gate_urgency = _gate(hunger - 0.50) * _gate(0.40 - safety)  # ~1 if hungry and unsafe

    # Case "away from home": the three old formulas, mixed by gates
    attenuation = np.clip((1.0 - safety) / 0.20, 0, 1)
    eh_attenuated = hunger * attenuation
    sn_attenuated = safety * 1.8
    eh_urgent = hunger * 1.5
    sn_urgent = safety * 0.3
    eh_flat = hunger
    sn_flat = safety

    weight_attenuated = gate_high_safety
    weight_urgent = gate_urgency * (1.0 - weight_attenuated)
    weight_flat = np.clip(1.0 - weight_attenuated - weight_urgent, 0, 1)

    effective_hunger_away = weight_attenuated * eh_attenuated + weight_urgent * eh_urgent + weight_flat * eh_flat
    current_safety_need_away = weight_attenuated * sn_attenuated + weight_urgent * sn_urgent + weight_flat * sn_flat

    # Final blend: at_home_active (at home, still hungry) / at_home_rest / away
    at_home_active = gate_at_home * (1.0 - gate_low_hunger)
    rest_intensity = gate_at_home * gate_low_hunger   # replaces boolean in_cave_repose
    away = 1.0 - gate_at_home

    effective_hunger = at_home_active * hunger + away * effective_hunger_away
    current_safety_need = rest_intensity * 1.0 + away * current_safety_need_away

    # in_cave_repose is preserved as an informative reading (for on-screen
    # text), but it no longer governs any formula by itself.
    in_cave_repose = rest_intensity > 0.5

    # ========================================================
    # 3. AGE AND INSTINCT
    # ========================================================
    age, construction_instinct, build_awake = update_age(TIME_WARP)

    # ========================================================
    # 4. CONSTRUCTIVE URGENCY
    # ========================================================
    if not nest_completed:
        constructive_urgency += 0.005 * TIME_WARP

        if material_active and not has_twig:
            constructive_urgency += 0.015 * TIME_WARP

        if has_twig:
            constructive_urgency += 0.02 * TIME_WARP

        if materials_collected > 0:
            progress = materials_collected / max_materials
            constructive_urgency += 0.005 * progress * TIME_WARP

        time_since_building += TIME_WARP
        if time_since_building > 60:
            constructive_urgency += 0.01 * TIME_WARP

        # No artificial floor: if the nest progresses and there is no accumulated urgency,
        # this can truly decrease instead of being forced to stay at 0.5.
        constructive_urgency = np.clip(constructive_urgency, 0, 1.5)

    # ========================================================
    # 5. BORDER STRESS
    # ========================================================
    dist_to_wall_x = 1.0 - abs(pos[0])
    dist_to_wall_y = 1.0 - abs(pos[1])
    closest_wall_dist = min(dist_to_wall_x, dist_to_wall_y)
    if closest_wall_dist < 0.25:
        border_stress = np.clip((0.25 - closest_wall_dist) / 0.25, 0, 1) ** 2
    else:
        border_stress = 0.0

    # ========================================================
    # 6. ENTITY MOVEMENT
    # ========================================================
    food_theta += 0.015 * TIME_WARP
    food_pos = np.array([food_radius * np.cos(food_theta), 0.55 * np.sin(1.7 * food_theta)])

    home_theta -= 0.010 * TIME_WARP
    home_pos = np.array([home_radius * np.cos(home_theta), 0.45 * np.sin(1.3 * home_theta)])
    home_zone.set_center((home_pos[0], home_pos[1]))
    home_safety_zone.set_center((home_pos[0], home_pos[1]))

    # ========================================================
    # 7. PREDATOR MOVEMENT
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
    # 8. COLLISIONS / REWARDS
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
    # 9. CONSTRUCTION IMPULSE
    # ========================================================
    if nest_completed:
        construction_impulse *= 0.95
    else:
        construction_impulse += base_impulse_rate * TIME_WARP
        construction_impulse += constructive_urgency * 0.02 * TIME_WARP

        if material_active and not has_twig:
            construction_impulse += 0.01 * TIME_WARP

        if has_twig:
            construction_impulse += 0.02 * TIME_WARP

        if materials_collected > 0:
            progress = materials_collected / max_materials
            construction_impulse += 0.005 * progress * TIME_WARP

        if time_since_building > 50:
            construction_impulse += 0.01 * TIME_WARP

        # No artificial floor of 0.4: it is left to truly decay when
        # there are no signals sustaining it (no active material, no twig,
        # no recent progress).

    construction_impulse = np.clip(construction_impulse, 0, 1)

    # ========================================================
    # 10. MATERIAL COLLECTION
    # ========================================================
    if (dist_material < 0.12 and material_active and not material_lock
        and not has_twig and not nest_completed):
        has_twig = True
        material_active = False
        material_lock = True
        try:
            winsound.Beep(800, 100)
        except:
            pass
        construction_active = True
        time_since_building = 0.0

    if has_twig and dist_nest < 0.25 and not nest_completed:
        materials_collected += 1
        has_twig = False
        try:
            winsound.Beep(600, 150)
        except:
            pass
        update_nest()
        construction_active = True
        time_since_building = 0.0
        # Truly decreases after depositing, instead of being forced into [0.6, 1]
        construction_impulse = np.clip(construction_impulse - 0.05, 0.0, 1.0)

    if dist_material > 0.15 and material_lock:
        material_lock = False

    # ========================================================
    # 11. GENERATE NEW MATERIAL
    # ========================================================
    if materials_collected >= max_materials:
        nest_completed = True
        material_active = False
    else:
        if not material_active and not material_lock:
            if materials_generated < max_materials_generated:
                generate_material()
            else:
                time_without_material += TIME_WARP
                if time_without_material > 150:
                    materials_generated = 0
                    time_without_material = 0.0
                    generate_material()

    # ========================================================
    # 12. SENSORY DIRECTIONS
    # ========================================================
    vec_food = food_pos - pos
    vec_home = home_pos - pos
    vec_pred = pred_pos - pos
    angle_food = np.arctan2(vec_food[1], vec_food[0])
    angle_home = np.arctan2(vec_home[1], vec_home[0])
    angle_pred = np.arctan2(vec_pred[1], vec_pred[0])

    force_west = 1.0 / (1.0 + (pos[0] - (-0.95)))
    force_east = 1.0 / (1.0 + (0.95 - pos[0]))
    force_south = 1.0 / (1.0 + (pos[1] - (-0.95)))
    force_north = 1.0 / (1.0 + (0.95 - pos[1]))
    vec_border_continuous = np.array([
        (force_east - force_west),
        (force_north - force_south)
    ])
    angle_border = np.arctan2(vec_border_continuous[1], vec_border_continuous[0])

    # ========================================================
    # 13. AREA 1 COMPETITION: MOTIVATIONAL
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
    # 14. AREA 2 COMPETITION: NAVIGATION
    # ========================================================
    energies_nav = np.zeros(N)
    for i, cm in enumerate(cms_nav):
        border_align = np.cos(angle_border - cm["angle"])
        E_nav = -border_stress * cm["border_weight"] * border_align + cm["explore"] * np.random.uniform(-1, 1)
        energies_nav[i] = E_nav + 0.05 * np.random.randn()
    winner_nav = np.argmax(energies_nav)

    # ========================================================
    # 15. AREA 3 COMPETITION: CONSTRUCTIVE N+2
    # ========================================================
    motor_n2 = np.zeros(2)
    winner_n2 = -1

    if build_awake and construction_impulse > MINIMUM_IMPULSE:
        motor_n2, winner_n2 = calculate_n2_motor()

    # ========================================================
    # 16. AREA 1 AND 2 DECAY
    # ========================================================
    if DECAY_MODE:
        activity_mot *= (0.92 ** TIME_WARP)
        activity_mot[winner_mot] += 1.0

        # Previously this was "if in_cave_repose: ... else: ...". Now it is mixed
        # continuously with rest_intensity (0 to 1), without a discrete branch.
        nav_decay_rate = 0.70 + 0.20 * (1.0 - rest_intensity)
        activity_nav *= (nav_decay_rate ** TIME_WARP)
        activity_nav[winner_nav] += (1.0 - rest_intensity) * 1.0
        if np.random.uniform(0, 1) < 0.40 * rest_intensity:
            num_flashes = np.random.choice([1, 2])
            lucky_indices = np.random.choice(N, size=num_flashes, replace=False)
            flash_brightness = (0.65 + 0.25 * np.sin(frame * 0.2)) * rest_intensity
            activity_nav[lucky_indices] += flash_brightness
    else:
        activity_mot[:] = 0.0
        activity_mot[winner_mot] = 1.0
        activity_nav[:] = 0.0
        activity_nav[winner_nav] = 1.0

    activity_mot = np.clip(activity_mot, 0, 1)
    activity_nav = np.clip(activity_nav, 0, 1)

    # ========================================================
    # 17. MOTOR SYNTHESIS
    # ========================================================
    motor_mot = np.zeros(2)
    motor_nav = np.zeros(2)

    for i in range(N):
        vec = np.array([np.cos(ANGLES[i]), np.sin(ANGLES[i])])
        motor_mot += activity_mot[i] * vec
        motor_nav += activity_nav[i] * vec

    if np.linalg.norm(motor_mot) > 0:
        motor_mot /= np.linalg.norm(motor_mot)
    if np.linalg.norm(motor_nav) > 0:
        motor_nav /= np.linalg.norm(motor_nav)

    # ========================================================
    # 18. AREA INTEGRATION - ADJUSTED
    # ========================================================
    if build_awake and construction_impulse > MINIMUM_IMPULSE:
        # === ADJUSTMENT: N+2 has more weight ===
        weight_n2 = construction_impulse * 0.7  # <--- BEFORE: 0.5

        hunger_factor = 1.0 - (hunger * 0.5)
        weight_n2 *= hunger_factor

        if dist_pred < 0.4:
            danger_factor = dist_pred / 0.4
            weight_n2 *= danger_factor

        if has_twig:
            weight_n2 = min(1.0, weight_n2 * 1.3)

        # === ADJUSTMENT: Higher limit ===
        weight_n2 = np.clip(weight_n2, 0, 0.7)  # <--- BEFORE: 0.5
        primary_motor = (1.0 - weight_n2) * motor_mot + weight_n2 * motor_n2
    else:
        primary_motor = motor_mot

    if border_stress > 0.15:
        motor = (1.0 - border_stress) * primary_motor + border_stress * motor_nav
    else:
        motor = primary_motor

    if np.linalg.norm(motor) > 0:
        motor /= np.linalg.norm(motor)

    # ========================================================
    # 19. FINAL MOVEMENT - ADJUSTED
    # ========================================================
    mag = np.linalg.norm(motor)
    if mag > 0:
        theta = np.arctan2(motor[1], motor[0])
        # === ADJUSTMENT: Creature is faster ===
        speed = (0.04 + 0.04 * np.clip(mag, 0, 1)) * TIME_WARP * (1.0 - rest_intensity)
        pos += speed * motor

    pos = np.clip(pos, -0.95, 0.95)

    # ========================================================
    # 20. CORTICAL VISUAL MAP
    # ========================================================
    brain *= 0.82

    # MOT (rows 3-7, columns 3-7)
    for i, a in enumerate(activity_mot):
        if i < len(core_mot):
            r, c = core_mot[i]
            brain[r, c] = a

    # NAV (rows 3-7, columns 13-17)
    for i, a in enumerate(activity_nav):
        if i < len(core_nav):
            r, c = core_nav[i]
            brain[r, c] = a

    # N+2 (rows 12-16, columns 8-12)
    for i, a in enumerate(activity_n2):
        if i < len(core_n2):
            r, c = core_n2[i]
            brain[r, c] = a * 5.0

    brain = np.clip(brain, 0, 1)

    # ========================================================
    # 21. GRAPHICAL INTERFACE
    # ========================================================
    dot.set_data([pos[0]], [pos[1]])
    head = pos + 0.12 * np.array([np.cos(theta), np.sin(theta)])
    line.set_data([pos[0], head[0]], [pos[1], head[1]])

    food_dot.set_data([food_pos[0]], [food_pos[1]])
    home_dot.set_data([home_pos[0]], [home_pos[1]])
    pred_dot.set_data([pred_pos[0]], [pred_pos[1]])

    if material_active:
        material_patch.center = (material_pos[0], material_pos[1])
        material_patch.set_visible(True)
    else:
        material_patch.set_visible(False)

    img.set_data(brain)

    # ========================================================
    # 22. INFORMATION TEXT
    # ========================================================
    intensity_n2 = np.mean(activity_n2)
    if np.linalg.norm(motor_n2) > 0:
        angle_n2 = np.arctan2(motor_n2[1], motor_n2[0]) * 180 / np.pi
        direction_n2 = f"{angle_n2:.0f}°"
    else:
        direction_n2 = "---"

    nest_status = "🏠 COMPLETED 🎉" if nest_completed else f"🔨 {materials_collected}/{max_materials}"
    twig_status = "🧱 Yes" if has_twig else "❌ No"
    build_status = "🔥 ACTIVE" if build_awake else "💤 ASLEEP"

    info_text.set_text(
        f"🍖 HUNGER: {hunger:.2f}  🛡️ SAFETY: {safety:.2f}\n"
        f"⚡ IMPULSE: {construction_impulse:.2f}  🔥 URGENCY: {constructive_urgency:.2f}\n"
        f"🧱 TWIG: {twig_status}  🎯 N+2: {intensity_n2:.2f}\n"
        f"📐 DIRECTION: {direction_n2}  {nest_status}\n"
        f"🧬 AGE: {age:.2f}  {build_status}"
    )

    return dot, line, img, food_dot, home_dot, pred_dot, material_patch, info_text

# ============================================================
# EXECUTION
# ============================================================

print("=" * 60)
print("🐝 CREATURE DEEPY BEE N+2")
print("=" * 60)
print("🔬 Cortical areas:")
print("   - MOT: Motivational (needs) - UPPER LEFT")
print("   - NAV: Navigation (borders) - UPPER RIGHT")
print("   - N+2: Constructive (collect/deposit) - LOWER CENTER")
print("")
print("🔧 Changes retained from previous revision (no wall, no memory")
print("   of blocking -- they were removed to avoid introducing new elements")
print("   before validating the rest):")
print("   - Removed the trick of 'age as angle' (age*2*pi did not represent")
print("     any real direction); construction_instinct is now an honest")
print("     scalar that amplifies weights, not false geometry.")
print("   - Removed artificial floors from construction_impulse and")
print("     constructive_urgency: they can now truly decrease.")
print("")
print("⏳ Starting simulation...")
print("   (Close the window to terminate)")
print("=" * 60)
print("")

try:
    ani = FuncAnimation(fig, update, interval=60, cache_frame_data=False)
    plt.tight_layout()
    plt.show(block=True)

except KeyboardInterrupt:
    print("\n⏹️ Simulation interrupted by user.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    print("\n" + "=" * 60)
    print("✨ END OF SIMULATION")
    print("=" * 60)
    if nest_completed:
        print("🏠 The creature built its nest!")
        print(f"   Materials collected: {materials_collected}")
        print(f"   Age: {age:.3f}")
    else:
        print(f"🏠 Progress: {materials_collected}/{max_materials}")
        print(f"   Age: {age:.3f}")
    print("=" * 60)
    sys.exit(0)
