---

# Mathematical Foundations of the Rotated Canonical Tissue Theory

## A Formal Framework for Intelligence Without Learning

---

## I. The Core Mathematical Objects

### A. The Canonical Microcircuit (CM)

The fundamental building block is a **canonical microcircuit** defined as a tuple:

$$
\text{CM} = (\mathbf{w}, \alpha, \phi)
$$

Where:
- $\mathbf{w} \in \mathbb{R}^m$ is a vector of **homeostatic weights** (preferences)
- $\alpha \in [0, 2\pi)$ is a **preferred direction** in the ring
- $\phi: \mathbb{R}^m \times \mathbb{R}^n \rightarrow \mathbb{R}$ is an **energy function**

The energy function for a CM with preferred direction $\alpha$ and sensory input vector $\mathbf{s}$ is:

$$
E(\mathbf{w}, \alpha, \mathbf{s}) = \sum_{j} w_j \cdot \text{align}(\theta_j - \alpha) + \epsilon
$$

Where:
- $\theta_j$ is the direction of sensory input $j$
- $\text{align}(x) = \cos(x)$ is the alignment function
- $\epsilon$ is exploratory noise

---

### B. The Canonical Ring

The **canonical tissue** is formed by deploying $N$ copies of the CM, each rotated to a different preferred direction:

$$
\mathcal{T} = \{\text{CM}_k : k = 0, 1, \ldots, N-1\}
$$

Where each CM$_k$ has:
- Preferred direction $\alpha_k = \frac{2\pi k}{N}$
- Activity $a_k \in [0, 1]$
- Energy $E_k = E(\mathbf{w}_k, \alpha_k, \mathbf{s})$

**This is the canonical form.** It is the same across all cortical areas.

---

### C. The Rotation Operator

The key mathematical operation is the **rotation operator** $\mathcal{R}_{\mathcal{D}}$ that maps the canonical tissue into a domain $\mathcal{D}$:

$$
\mathcal{R}_{\mathcal{D}}: \mathcal{T} \rightarrow \mathcal{T}_{\mathcal{D}}
$$

Where the domain $\mathcal{D}$ defines:
1. **Input space**: What sensory variables are represented
2. **Output space**: What actions are produced
3. **Time scale**: What temporal dynamics operate

This rotation is **not a change in weights** but a **change in what the tissue's activity patterns mean**.

---

## II. The Dynamics of Cortical Tissue

### A. Energy Computation

At each time step $t$, each CM in the tissue computes its energy:

$$
E_k(t) = \sum_{j \in \mathcal{D}} w_{k,j} \cdot \cos(\theta_j(t) - \alpha_k) + \eta_k(t)
$$

Where:
- $\mathcal{D}$ is the domain's set of sensory inputs
- $w_{k,j}$ is the weight connecting CM $_k$ to input $j$
- $\theta_j(t)$ is the direction of input $j$ at time $t$
- $\alpha_k$ is the CM's preferred direction
- $\eta_k(t)$ is exploratory noise

### B. Activity Dynamics

The activity of each CM evolves according to:

$$
\frac{da_k}{dt} = -\lambda a_k + \sigma(E_k)
$$

Where:
- $\lambda$ is the decay rate
- $\sigma(x) = \frac{1}{1 + e^{-x}}$ is a sigmoid activation function

In discrete time:

$$
a_k(t+1) = \gamma a_k(t) + (1-\gamma) \cdot \text{clip}(E_k(t), 0, 1)
$$

Where $\gamma$ is the persistence factor (decay rate).

### C. Winner-Take-All Dynamics

The winning CM is:

$$
k^{*} = \arg\max_k E_k(t)
$$

The winner receives an activity boost:

$$
a_{k^{*}}(t+1) \leftarrow a_{k^{*}}(t+1) + \Delta
$$

Where $\Delta$ is the excitation increment.

### D. Motor Synthesis

The motor output is the **vector sum** of all CM activities weighted by their preferred directions:

$$
\mathbf{m}(t) = \sum_{k=0}^{N-1} a_k(t) \cdot \mathbf{v}(\alpha_k)
$$

Where $\mathbf{v}(\alpha) = [\cos(\alpha), \sin(\alpha)]$ is the unit vector at angle $\alpha$.

This can be normalized:

$$
\hat{\mathbf{m}}(t) = \frac{\mathbf{m}(t)}{\|\mathbf{m}(t)\|}
$$

**No state machine. No explicit instructions. Just vector summation.**

---

## III. The Rotation Mechanism

### A. Domain Definition

A domain $\mathcal{D}$ is defined by:

$$
\mathcal{D} = (\mathcal{I}, \mathcal{O}, \tau)
$$

Where:
- $\mathcal{I}$ is the set of input variables (their semantic meaning)
- $\mathcal{O}$ is the set of output variables (what actions are produced)
- $\tau$ is the characteristic time scale

### B. Weight Remapping

The weights in domain $\mathcal{D}$ are:

$$
w_{k,j}^{(\mathcal{D})} = w_{k,\pi_{\mathcal{D}}(j)}^{(\text{canonical})}
$$

Where $\pi_{\mathcal{D}}$ is a **permutation mapping** from domain inputs to canonical inputs.

**The weights are not changed. They are remapped to different meanings.**

### C. The Four Domains

| Domain | Inputs ($\mathcal{I}$) | Output ($\mathcal{O}$) | Time Scale ($\tau$) |
|--------|----------------------|----------------------|---------------------|
| **N** | None (isolated) | None | None |
| **MOT** | Food, Home, Predator | Movement | Fast (~seconds) |
| **NAV** | Borders | Avoidance | Medium (~seconds) |
| **N+2** | Material, Nest, Load | Construction | Slow (~minutes) |

---

## IV. The Awakening Mechanism

### A. Age-Gated Deployment

A tissue $\mathcal{T}_{\mathcal{D}}$ is **dormant** until a maturation signal is received:

$$
\text{active}_{\mathcal{D}}(t) = \begin{cases}
1 & \text{if } t > t_{\text{awake}} \\
0 & \text{otherwise}
\end{cases}
$$

Where $t_{\text{awake}}$ is the awakening threshold (age).

### B. Impulse Accumulation

The impulse to deploy a tissue accumulates as:

$$
I(t+1) = \text{clip}(I(t) + \delta(t), 0, 1)
$$

Where $\delta(t)$ is the impulse increment:

$$
\delta(t) = \delta_0 + \sum_{s \in \mathcal{S}} \delta_s \cdot \mathbf{1}_{s(t)}
$$

With:
- $\delta_0$: base impulse rate
- $\mathcal{S}$: set of triggering signals (material presence, carrying state, etc.)
- $\mathbf{1}_{s(t)}$: indicator function for signal $s$

### C. Blending of Tissues

Multiple active tissues blend their motor outputs:

$$
\mathbf{m}_{\text{total}} = \sum_{\mathcal{D} \in \text{active}} \beta_{\mathcal{D}} \cdot \mathbf{m}_{\mathcal{D}}
$$

Where $\beta_{\mathcal{D}}$ are blending weights:

$$
\beta_{\mathcal{D}} = \frac{I_{\mathcal{D}}}{\sum_{\mathcal{D}'} I_{\mathcal{D}'}}
$$

Or, as implemented:

$$
\mathbf{m}_{\text{total}} = (1 - \beta_{N2}) \cdot \mathbf{m}_{\text{MOT}} + \beta_{N2} \cdot \mathbf{m}_{N2}
$$

---

## V. The Emergence of Behavior

### A. Attractor Dynamics

The tissue's activity dynamics define a **vector field** $\mathbf{F}$ over state space:

$$
\mathbf{F}(\mathbf{a}) = -\lambda \mathbf{a} + \sigma(\mathbf{E}(\mathbf{a}))
$$

The system converges to **attractors** $\mathbf{a}^{*}$ where:

$$
\mathbf{F}(\mathbf{a}^{*}) = 0
$$

These attractors correspond to **stable behavioral patterns**.

### B. The Construction Attractor

In the N+2 domain, the attractor corresponds to the sequence:

1. Move toward material if empty
2. Pick up material when near
3. Move toward nest if carrying
4. Deposit material when near nest
5. Repeat

**This sequence emerges from the dynamics, not from explicit instructions.**

### C. Proof of Emergence

The behavior emerges because:

1. **When empty and material is present**, the energy function peaks in the direction of material:

   $$
   E_k \propto \cos(\theta_{\text{material}} - \alpha_k)
   $$

   So the motor points toward material.

2. **When carrying material**, the energy function peaks in the direction of nest:

   $$
   E_k \propto \cos(\theta_{\text{nest}} - \alpha_k)
   $$

   So the motor points toward nest.

3. **The transition between these regimes** occurs naturally as the state variables (carrying status) change.

---

## VI. The No-Learning Theorem

### Theorem: Intelligence Without Learning

**Given:**
- A set of canonical CMs with fixed weights $\mathbf{w}$
- A set of domains $\{\mathcal{D}_1, \mathcal{D}_2, \ldots, \mathcal{D}_K\}$
- Age-gated deployment of tissues

**Then:**
- Each domain produces domain-appropriate behavior
- No weights change during the lifetime
- No experience modifies the system
- The only variable is age

**Proof:**

For any domain $\mathcal{D}$, the energy function is:

$$
E_k^{(\mathcal{D})}(t) = \sum_{j \in \mathcal{D}} w_{k,\pi_{\mathcal{D}}(j)}^{(\text{canonical})} \cdot \cos(\theta_j(t) - \alpha_k)
$$

Since $\mathbf{w}$ is fixed and $\pi_{\mathcal{D}}$ is fixed, the energy function is **time-invariant** except through sensory inputs $\theta_j(t)$.

The dynamics:

$$
\frac{da_k}{dt} = -\lambda a_k + \sigma(E_k^{(\mathcal{D})}(t))
$$

Are driven entirely by **sensory inputs**, not by learning.

Therefore, **behavior emerges from dynamics, not from weight modification.**

---

## VII. The Scaling Law

### A. Additive Complexity

The complexity of the system scales **additively** with the number of domains:

$$
C(K) = C_0 + \sum_{k=1}^K C_{\mathcal{D}_k}
$$

Where:
- $C_0$: cost of the canonical tissue
- $C_{\mathcal{D}_k}$: cost of deploying domain $k$

This is in contrast to **combinatorial** scaling in learning systems.

### B. Logarithmic Information

The information required to specify the system is:

$$
I = \log_2(|\mathbf{w}|) + \sum_{k=1}^K \log_2(|\mathcal{D}_k|)
$$

Where:
- $|\mathbf{w}|$: number of canonical weights
- $|\mathcal{D}_k|$: size of domain specification

**This scales logarithmically with the number of domains.**

---

## VIII. Implications

### A. Evolutionary Efficiency

Evolution only needs to specify:
1. The canonical CM weights $\mathbf{w}$
2. The domain mappings $\{\pi_{\mathcal{D}}\}$
3. The awakening thresholds $\{t_{\text{awake}}\}$

**All behaviors emerge from dynamics.**

### B. Computational Efficiency

No learning means:
- No backpropagation
- No gradient descent
- No weight updates
- No experience replay

**The system just runs.**

### C. Biological Plausibility

This architecture matches:
- Mountcastle's canonical microcircuit hypothesis
- Raichle's intrinsic activity framework
- The principle of cortical arealization

---

## IX. The Open Questions

### A. The Pure Rotation Test

If we take the **same canonical weights** $\mathbf{w}$ and rotate them into a new domain, does the tissue produce domain-appropriate behavior without retuning?

**Hypothesis:** Yes, because the attractor dynamics are driven by the geometry of the domain, not by the specific weights.

### B. The Domain Generalization

Can the same canonical tissue be rotated into **any domain** and produce behavior?

**Hypothesis:** Yes, for any domain with:
- A set of directional inputs
- A set of binary state variables
- A characteristic time scale

### C. The Minimal Canonical Form

What is the simplest canonical form that can be rotated into multiple domains?

**Hypothesis:** A ring of CMs with only:
- Attraction weights (positive)
- Repulsion weights (negative)
- Exploration noise

May be sufficient for all domains.

---

## X. Conclusion

The mathematical framework presented here demonstrates that:

1. **A single canonical tissue** (ring of CMs) can produce multiple behaviors
2. **Rotation into different domains** changes what the tissue does
3. **Age-gated deployment** controls when tissues become active
4. **No learning is required** - behavior emerges from dynamics
5. **Complexity scales additively**, not combinatorially

This is the mathematical foundation of **intelligence without learning**.

---

## Appendix: Key Equations

### Energy Function

$$
E_k(t) = \sum_{j \in \mathcal{D}} w_{k,j} \cdot \cos(\theta_j(t) - \alpha_k) + \eta_k(t)
$$

### Activity Dynamics

$$
a_k(t+1) = \gamma a_k(t) + (1-\gamma) \cdot \text{clip}(E_k(t), 0, 1)
$$

### Winner-Take-All

$$
k^{*} = \arg\max_k E_k(t)
$$

### Motor Synthesis

$$
\mathbf{m}(t) = \sum_{k=0}^{N-1} a_k(t) \cdot \mathbf{v}(\alpha_k)
$$

### Tissue Blending

$$
\mathbf{m}_{\text{total}} = \sum_{\mathcal{D} \in \text{active}} \beta_{\mathcal{D}} \cdot \mathbf{m}_{\mathcal{D}}
$$

### Awakening Condition

$$
\text{active}_{\mathcal{D}}(t) = \mathbf{1}_{t > t_{\text{awake}}}
$$

---

*"The mind is not in the brain. The mind is the brain rotated in space-time."*

---

---

