# Rotated Canonical Tissues: Practical Guide for Researchers

**Oscar Chang, Ph.D.**

---

## What This Is

The Rotated Canonical Tissues framework demonstrates that **intelligent behavior can emerge from dynamics, not just learning**. A single, fixed-weight neural architecture—when "rotated" into different sensory-motor domains—produces complex, sequential behaviors without any weight modification.

**The core mechanism**: A ring of canonical microcircuits (CMs) with fixed weights creates an activity bump that rotates in response to sensory inputs. This rotation generates **time-decay information**—a continuous trajectory that encodes behavioral history—enabling emergent sequences without explicit programming.

---

## Why It Matters

| Problem in AI | How This Framework Helps |
|---------------|--------------------------|
| Energy costs | No training phase |
| Catastrophic forgetting | Just awake inherited cortical areas |
| Sample inefficiency | No data needed |
| Black-box opacity | Dynamics are tractable |
| Biological implausibility | Matches cortical architecture |

---

## What This Is Not

- A replacement for all learning
- A complete theory of the brain
- A solved AGI system
- A production-ready robot controller
- A claim that learning is useless

---

## The Core Model

### The Canonical Tissue

A **canonical tissue** is a ring of N microcircuits:

$$\mathcal{T} = \{CM_k : k = 0, \ldots, N-1\}$$

Each CM has:
- A preferred direction: $\alpha_k = 2\pi k/N$
- Fixed weights: $\mathbf{w}_k$ (never modified)
- Activity: $a_k \in [0,1]$

### The Energy Function

For domain $\mathcal{D}$:

$$E_k^{(\mathcal{D})}(t) = \sum_{j \in \mathcal{I}_{\mathcal{D}}} w_{k,j} \cdot \cos(\theta_j(t) - \alpha_k) + \eta_k(t)$$

This is **cosine tuning**—the same mechanism used by place cells, head-direction cells, and motor cortex neurons.

### The Rotation Dynamics

Activity evolves via:

$$a_k(t+1) = (1-\alpha_{\mathcal{D}}) \cdot a_k(t) + \alpha_{\mathcal{D}} \cdot \sigma_{\tau_{\mathcal{D}}}(\mathbf{E}(t))_k$$

**This creates time-decay information**:
- Previous activity persists but fades
- The trajectory encodes behavioral history
- Sequences emerge from the dynamics

### Motor Synthesis

$$\mathbf{m}_{\mathcal{D}}(t) = \sum_{k=0}^{N-1} a_k^{(\mathcal{D})}(t) \cdot \mathbf{v}_k, \quad \mathbf{v}_k = \begin{bmatrix} \cos(\alpha_k) \\ \sin(\alpha_k) \end{bmatrix}$$

This is the **Georgopoulos population vector**—the standard readout from motor cortex.

---

## How Rotation Creates Behavior

### The Visual Cortex Analogy

**Visual cortex**:
- Orientation columns arranged retinotopically
- A moving edge creates a rotating pattern of activation
- Rotation encodes motion direction
- Time-decay creates apparent motion perception

**This framework**:
- CMs arranged on a ring
- Moving sensory inputs create rotating activation
- Rotation encodes behavioral direction
- Time-decay creates behavioral sequences

**The same computational principle underlies both visual perception and behavioral control.**

### The Emergent Sequence

Consider the construction behavior. The agent performs a 5-step sequence that was **never explicitly programmed**:

1. Move toward material (when $L \approx 0$)
2. Pick up material (when $L$ increases)
3. Move toward nest (when $L \approx 1$)
4. Deposit material (when $L$ decreases)
5. Repeat until nest complete

**How it emerges**: The load variable $L$ evolves continuously based on the agent's position:

$$\frac{dL}{dt} = K_p \cdot G_{\text{pick}} \cdot (1 - L) - K_d \cdot G_{\text{drop}} \cdot L$$

As $L$ changes, the energy landscape changes, and the activity bump **rotates** from pointing toward material to pointing toward nest. This rotation creates the sequence.

---

## Key Theoretical Results

### No-Learning Theorem

**Theorem**: For all times $t$ and domains $\mathcal{D}$:

$$\frac{d\mathbf{w}^{(\mathcal{D})}}{dt} = \mathbf{0}$$

**Interpretation**: Weights never change. All behavior emerges from dynamics, not from weight modification.

### Emergence Theorem

**Theorem**: The construction behavior emerges from the dynamics without explicit instructions.

**Proof sketch**: The load $L$ evolves continuously, causing the energy landscape to shift. The activity bump rotates from material to nest and back, creating the 5-step sequence. No code tells the agent what to do at each step.

### Additive Scaling Theorem

**Theorem**: Complexity scales additively:

$$C(K) = C_0 + \sum_{k=1}^K C_{\mathcal{D}_k}$$

**Interpretation**: Each new domain adds complexity linearly, not combinatorially. This is fundamentally different from traditional approaches where $C(K) = O(2^K)$.

### Stability Theorem

**Theorem**: The system is asymptotically stable if $\alpha_{\mathcal{D}} > 0$ for all domains.

**Interpretation**: The softmax update is a contraction mapping, ensuring convergence to stable fixed points.

---

## Implementation Overview

### The Core Algorithm

```python
def softmax_update(activity, energy, alpha, tau):
    # Softmax competition (winner-take-most)
    e = energy - max(energy)
    target = exp(e / tau)
    target = target / sum(target)
    
    # Time-decay (memory of previous state)
    return (1 - alpha) * activity + alpha * target
```

### Domain Specification

Each domain requires:
1. **An energy function**: Maps sensory inputs to CM energies
2. **A set of weights**: Fixed, not modified
3. **A relaxation rate ($\alpha$)** : Controls time-decay
4. **A temperature ($\tau$)** : Controls competition sharpness

### Continuous State Variables

The framework replaces discrete boolean flags with continuous variables:

| Discrete Approach | Continuous Approach |
|-------------------|---------------------|
| `has_stick = True/False` | Load $L \in [0,1]$ |
| `build_awake = True/False` | Instinct $I(t) \in [0,1]$ |
| `if hungry:` | Hunger $h \in [0,1]$ with continuous gating |

### Domain Integration

Domains compete continuously through weighted blending:

$$\mathbf{m}(t) = \sum_{\mathcal{D}} w_{\mathcal{D}}(t) \cdot \mathbf{m}_{\mathcal{D}}(t)$$

Where $w_{\mathcal{D}}(t)$ are continuous weights (e.g., based on instinct, load, border stress).

---

## Research Directions

### 1. Evolution of Weights

**Question**: Can evolution discover functional weights?

**Approach**: Use genetic algorithms to evolve weights for multiple domains.

**Expected outcome**: Weights that support robust behavior across domains.

### 2. Hierarchical Tissues

**Question**: Can multiple tissues be organized hierarchically?

**Approach**: Combine tissues in a hierarchical structure, with higher-level tissues modulating lower-level ones.

**Expected outcome**: More complex behaviors, abstraction, planning.

### 3. Physical Robot Implementation

**Question**: Does the framework work in the real world?

**Approach**: Implement on a physical robot platform.

**Expected outcome**: Validation of the framework in noisy, complex environments.

### 4. More Domains

**Question**: Does additive scaling hold with more domains?

**Approach**: Test with 10+ behavioral domains.

**Expected outcome**: Complexity scaling additively, not combinatorially.

### 5. Hybrid Systems

**Question**: Can learning and dynamics work together?

**Approach**: Combine fixed dynamics with learnable parameters.

**Expected outcome**: Systems that are robust and adaptable.

---

## Experimental Protocol

### Metrics to Measure

| Metric | What It Shows |
|--------|---------------|
| Task success rate | Behavioral competence |
| Emergence detection | Did sequence appear without instructions? |
| Scaling | Additive vs combinatorial growth |
| Robustness | Dynamical stability |
| Transfer | Generalization across environments |

### Experimental Design

1. **Initialize** the system with random weights
2. **Run** the agent in the environment
3. **Measure** task success, emergence, and robustness
4. **Compare** across:
   - Number of domains
   - Different weight initializations
   - Different environments
   - With/without learning

### Reproducibility

- Use a fixed random seed for reproducibility
- Demonstrate that the framework works across a range of initial weights
- The system's robustness to initial conditions is a strength, not a weakness

---

## Frequently Asked Questions

### Q: Is this just control theory?

**A**: No. Control theory has explicit feedback loops and targets. This framework has:
- No explicit targets (no goal specified)
- No explicit sequence (sequence emerges)
- No explicit switching (competition creates blending)

### Q: Where does the intelligence come from?

**A**: From the **dynamics**, not from stored knowledge or learned representations:
- The ring structure creates a spatial map
- Rotation creates temporal dynamics
- Time-decay creates memory
- Competition creates prioritization
- Integration creates blending

### Q: How is this different from reinforcement learning?

**A**: RL requires:
- A reward function (explicit goal)
- Trial and error (learning)
- Policy updates (weight changes)

This framework requires:
- No reward function
- No trial and error
- No weight changes

### Q: Can this scale to human-level intelligence?

**A**: The framework proposes **additive scaling**:
- $C(K) = C_0 + \sum_{k=1}^K C_{\mathcal{D}_k}$
- New domains add complexity linearly, not combinatorially

The path to human-level intelligence:
1. More domains (10+)
2. Hierarchical tissues
3. Evolution of weights
4. Physical embodiment

### Q: What about adaptation?

**A**: Adaptation occurs through:
1. **Parameter tuning** (low-dimensional)
2. **Structural evolution** (new tissues)
3. **Homeostatic modulation** (continuous)

**Not through**:
1. Weight modification
2. Experience-based learning
3. Gradient descent

---

## Communication Strategy

### Papers to Write

| Paper | Focus | Audience |
|-------|-------|----------|
| Core Framework | Mathematical proof and demonstration | AI theorists, neuroscientists |
| Implementation Guide | Code and best practices | Engineers, practitioners |
| Biological Plausibility | Cortical mapping | Neuroscientists |
| Robotics | Physical implementation | Robotics researchers |
| Evolutionary Specification | Weight discovery | Evolutionary computing |

### Conferences to Target

| Conference | Relevance | Notes |
|------------|-----------|-------|
| NeurIPS | AI theory | Needs rigorous experimentation |
| ICLR | Deep learning alternative | Challenge the paradigm |
| Neuroscience | Biological plausibility | Show cortical mapping |
| Robotics | Physical implementation | Real-world validation |
| ALife | Emergent behavior | Natural audience |

### Key Papers to Cite

1. **Mountcastle (1978)** - Canonical microcircuit hypothesis
2. **Georgopoulos (1986)** - Population vector coding
3. **Amari (1977)** - Neural field dynamics
4. **Hopfield (1982)** - Attractor networks
5. **Friston (2010)** - Free energy principle
6. **Tani (2016)** - Neural dynamics
7. **Chang (2025)** - AGI Dynamics

---

## What I Need From the Research Community

1. **Validation**: Run the code. See if it works. Report results.
2. **Critique**: Find the weaknesses. Push the theory.
3. **Extension**: Add new domains. Test scaling.
4. **Application**: Implement on robots. Test in the real world.
5. **Theory**: Formalize the rotation. Prove the scaling.

---

## The Open Questions

| Question | How to Answer |
|----------|---------------|
| Can evolution specify weights? | Genetic algorithm experiments |
| Can 10+ domains coexist? | Scale up the code |
| Does this work on a robot? | Physical implementation |
| Is this how the brain works? | Neuroscientific experiments |
| Can this scale to AGI? | Theoretical + empirical work |

---

## Final Words

### The Big Picture

**We are not trying to build a better learning machine.**

We are trying to show that **learning is not necessary for intelligence**.

This is a fundamental challenge to:
- The dominant paradigm in AI
- The assumption that intelligence requires experience
- The belief that learning is the core of intelligence

### The Challenge

**If intelligence can arise from dynamics, then**:
1. We need not build learning machines
2. We need not worry about training data
3. We need not face catastrophic forgetting
4. We need not accept black-box opacity

**This changes everything.**

### The Invitation

**Come see for yourself**:
1. Run the code
2. Watch the behavior
3. Analyze the dynamics
4. Extend the framework
5. Join the revolution

---

**The mind is not in the brain. The mind is the brain rotated in space-time.**

---

*Oscar Chang, Ph.D.*

*2026*
