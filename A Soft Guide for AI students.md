
# Why Is This Cortical-like Deployment Code So Special?

*A tour through the engineering ideas hidden inside a few hundred lines of Python that explore an architecture inspired by how biological systems reuse and deploy neural motifs.*

---

## 1. The First Question

When software and AI students first open this program, they usually have the same reaction.

Nothing looks familiar.

There is no planner. No behavior tree. No reinforcement learning. No search algorithm. No symbolic world model. No state machine deciding what the creature should do next.

In fact, many of the ingredients that modern AI textbooks consider indispensable are simply missing.

Instead, the program contains something almost embarrassingly small: three functional populations with twenty-five nearly identical computational modules (cortical microcircuits CMs) each, arranged in three separate rings. Each CM stores only a handful of numerical parameters. Every simulation step they all wake up, compute an activation, compete with one another, and then quietly decay before repeating the entire process a fraction of a second later.

At first glance this seems like an unnecessarily complicated way to decide whether a creature should walk north or south.

* Why not just write an `if` statement?
* Why not train a neural network?
* Why not store a map?

Those are reasonable questions. They are exactly the questions this essay is meant to answer.

By the time you reach the end, I hope you will look at this code and realize that almost every wise design decision follows from a single engineering constraint: **inherited information is expensive**. Once that constraint is accepted, many familiar AI architectures become surprisingly difficult to justify, while a population of continuously competing canonical modules begins to look almost inevitable, just as it does in nature.

This essay is therefore not a tutorial on Python. It is a tour through the engineering ideas hidden inside a few hundred lines of code that take inspiration from how biological brains deploy their circuitry.

---

## 2. The Strange Thing About the Genome

Let's start with something the code doesn't show you directly, but which explains almost everything it does.

The creature has a genome. That genome is small. It has to be small, because it has to fit inside a single cell. That cell divides and grows into the creature, and somewhere along the way, the genome has to specify how to build the creature's brain.

But here's the problem: the genome is tiny compared to the brain it has to build.

A human genome contains about 750 megabytes of information. The human brain contains about one hundred trillion synaptic connections. There is no way to specify each connection individually. The arithmetic simply fails.

> The genome contains far less explicit information than the complete connectivity pattern of the adult brain.

Evolution faced this problem billions of years ago. It couldn't build a brain by describing it. It had to build a brain by describing something much smaller that, when deployed many times, grows into a brain.

This is the central constraint that shapes the entire program.

Think of it this way: if you had to build the city of Montreal, but all you had was a USB stick that holds 200 megabytes, you couldn't describe the city. You'd have to describe the machinery that grows the city. A set of rules for construction that, when executed, produce the city through controlled repetition.

That's what this code does. It doesn't describe the creature's behavior directly. It describes a small unit — the canonical microcircuit — and then deploys it across three functional populations, each with twenty-five copies. The behavior emerges from the interaction of all those copies.

This is the genomic bottleneck, and every brain that has ever existed had to be born from a workaround, not a blueprint. The workaround: don't specify every connection. Specify a compact, repeatable rule — build this one small unit, and repeat it — and let repetition generate a structure far larger than the instructions describing it. Compression, with algorithmic decompression. A fractal construction, not a floor plan.

---

## 3. Three Populations, Twenty-Five Copies Each? That Can't Be Right

Most programmers spend years trying to eliminate duplicated code. So why does this program intentionally create three separate functional populations, each with twenty-five nearly identical computational units?

At first this looks like poor software engineering. In reality, it is the central idea of the entire architecture.

Each unit within a population is almost identical. What distinguishes one from another is not its algorithm but its parameters.

* In the **motor population**, one unit slightly prefers food, another prefers home, another reacts more strongly to predators.
* In the **navigation population**, units respond to borders and explore.
* In the **construction population**, units respond to materials and the nest.

Individually these differences are insignificant. Collectively they create populations capable of representing many competing behavioral tendencies without requiring seventy-five different algorithms.

Software engineers already use this idea every day. A class is written once and instantiated many times. A web server may create thousands of identical worker threads. A graphics processor executes the same instruction across thousands of cores. Complexity emerges from many copies of a simple mechanism rather than from one enormously complicated mechanism.

The cortical microcircuit plays a similar role in this program. It is not interesting because it is complicated. It is interesting because it is reusable.

Look at the definition for one unit:

```text
one CM ("canonical microcircuit") =
    food_weight ~ small random number
    home_weight ~ small random number
    pred_weight ~ small random number
    explore     ~ small random number

```

Four numbers. That's the entire description of one unit. The program then stamps out twenty-five copies for the motor population, each one slightly different because of the random initialization. Then it does the same for the navigation population with different parameters. Then again for the construction population.

The same mold produces seventy-five individuals, each with its own personality, organized into three functional populations. This is not a bug. It is the whole point.

> **A note on terminology:** Throughout this essay, we use terms like "genome," "evolution," and "cortical" as *analogies* to biology. The code does not implement a real genome (there is no inheritance across generations), nor real evolution (the parameters are randomly initialized, not selected), nor real cortical columns (there are no lateral connections or hierarchical structure). These analogies help us think about the architecture, but they are not literal simulations. The code is *inspired by* biology, not *replicating* it.

This can be interpreted as a form of canonical deployment: a repeated developmental motif that generates diverse functional circuits. The genome doesn't describe every neuron. It describes a small circuit that gets deployed many times across different populations, each copy slightly adjusted to its location and function. A few pages of genetic code produce a brain of immense complexity not because the code contains more information but because the same information is used over and over again.

---

## 4. The First Surprise: Nothing Ever Sleeps

One of the easiest mistakes to make when reading this program is to assume that each microcircuit is activated only when it is needed. That is how most software is written. A function is called, performs its task, returns a result, and remains inactive until the next call.

This program does not behave that way.

Every microcircuit in every functional population runs continuously. Even those that are losing the competition continue to compute their activation. They are not disabled; they are merely less influential than the current winner. At every simulation step, seventy-five competing hypotheses about the creature's next movement coexist across three populations. The winners change as the sensory inputs change, but the competition itself never stops.

This design may seem wasteful from the perspective of conventional programming, yet it mirrors one of the most robust observations in systems neuroscience. Even during sleep, the cerebral cortex remains metabolically active. Brains do not alternate between computation and inactivity. They compute continuously, while the dominant patterns of activity change from moment to moment.

The Python program adopts the same philosophy. Computation is continuous; selection is dynamic.

This distinction is subtle, but it changes the entire architecture. Instead of asking which module should run next, the program allows every module to run and asks only which one currently deserves to influence behavior.

Look at the execution logic:

```python
activity *= 0.92         # every copy loses a little strength, every frame
activity[winner] += 1.0  # and one copy always wins, every frame

```

This never pauses. There is no gate. The competition runs whether the creature is one step from a predator or standing in an empty field doing nothing in particular.

This is why the creature can look, from the outside, like it is making decisions. It isn't consulting a rulebook. It is letting seventy-five small opinions decay and compete endlessly across three populations, and whichever opinions the world happens to reward hardest in a given instant are the ones that move the creature's legs.

In neuroscience, this mirrors the brain's **default mode network** — even at rest, a large share of the body's energy budget goes to intrinsic activity that isn't a response to anything in particular. The brain is not a function waiting on an input call. It runs continuously, competing with itself, whether or not the world is currently offering it something to react to.

---

## 5. The Competition That Never Finishes

Let's look more closely at how this competition actually works.

Each of the twenty-five copies in each population has an activity level. At every frame, that activity decays slightly. Then, the copies that best match the current sensory input receive a boost.

The boost is not binary. It's proportional to how well the copy's tuning matches the direction of whatever is being sensed.

* In the **motor population**, food, home, and predators each push activity in slightly different directions.
* In the **navigation population**, borders push activity away from walls.
* In the **construction population**, materials and the nest push activity toward building.

The result is a race that never finishes. Seventy-five runners across three tracks, each slowing down a little every step, and every step some of them get a push from the environment. The ones that get pushed hardest win their population this frame. Then decay starts again, and the races continue.

This is implemented through a mechanism called **softmax relaxation**:

```python
def relajar_softmax(actividad, energias, alpha, temperatura):
    e = energias - np.max(energias)
    pesos = np.exp(e / temperatura)
    objetivo = pesos / np.sum(pesos)
    return (1.0 - alpha) * actividad + alpha * objetivo

```

This function takes the current activity levels and the new sensory energies, and moves the activity smoothly toward the distribution that best matches the current world state. No single copy is ever declared the winner. The activity is always a distribution across the population.

This is **population coding**. The direction the creature moves is not determined by any single copy. It is the vector average of all active copies across all populations, weighted by their current activity. The creature moves in the direction that emerges from the collective competition across all three functional populations.

In biology, this is how cortical columns work. Rotated cortical columns in the visual cortex repeat the same microcircuitry across space, each copy tuned to a different orientation of a line in your visual field. Same compression trick, now spread across a continuum instead of collapsed into one unit.

---

## 6. Growing Up: The Third Population

Here is another strange thing about the code.

The creature in its early moments is not able to build a nest. That capability doesn't show on day one. And when the time comes, the program doesn't modify the existing circuits to add the new capability. It activates a third functional population, with full inherited nest build capacities, that has been sitting silent since birth.

```python
if age > AWAKENING_AGE and not build_awake:
    build_awake = True

```

The third population — the construction population, labeled `N+2` in the code — has been present but silent, without permission to act. When it wakes, it doesn't overwrite anything. It blends in, with a share of the vote that grows slowly over time.

```python
primary_motor = (1 - weight_n2) * old_motor + weight_n2 * new_motor

```

The old motor and navigation populations are never touched. Not one of their numbers changes. The new population simply starts contributing a small, growing fraction of the final decision.

This matters for a reason that every AI researcher should recognize. Artificial neural networks have a famous failure mode called **catastrophic forgetting**. Train a network on one task, keep training the same weights on a second task, and the second task's corrections silently overwrite what the network learned for the first.

The standard fix is to protect the old weights while still touching them. The other fix — the one this program uses — is to freeze the old networks completely and add a new population beside them. Zero risk of forgetting, because there's nothing shared left to overwrite.

There's a deeper reason this matters too. If the new population had to learn nest-building the moment it woke up, that would be expensive. Learning takes time and energy. The far cheaper move is for the new population to wake up already shaped — not an empty room waiting to be furnished, but a pre-built module wheeled into place and plugged into wiring that's already there.

The competence was paid for somewhere else. The creature just switches it on.

In biology, this mirrors **myelination** — the process that lets neural circuits fire efficiently continues well into adulthood, arriving late and gradually rather than all at once. New capabilities appear not by rewriting existing circuits but by adding new circuits alongside them. It also mirrors the idea of critical periods, though with an important simplification: in this code, the gate is purely age-based, whereas in biology critical periods often require both age and appropriate sensory experience during the window.

---

## 7. Everything Is Continuous

One more strange thing about the code: it avoids boolean flags wherever possible.

Most programs use `if` statements to decide between behaviors. This program uses continuous gates.

Consider the creature's load. In the original version, it had a boolean flag `tiene_brizna` ("has twig") that was either `True` or `False`. In this version, that has been replaced by a continuous variable `L` that ranges from 0 to 1.

```python
L = np.clip(L + dt * (flujo_entrada - flujo_salida), 0, 1)

```

The creature is not either "carrying" or "not carrying." It is gradually filling and emptying, like a cup being filled with water and poured out. This allows the behavior to be smooth rather than binary.

The same principle applies to the maturation trigger. Instead of a boolean flag that flips when the creature reaches a certain age, the program uses a sigmoid:

```python
instinto_construccion = _compuerta(edad - EDAD_DESPIERTE, filo=RHO_MADURACION)

```

The creature doesn't suddenly wake up to the possibility of nest-building. It gradually becomes more aware of it, over time, as the sigmoid moves from 0 to 1.

Even the decision of whether to approach the nest or the material is continuous:

```python
g_pickup = _compuerta(PICKUP_RADIUS - dist_material, filo=STEEPNESS_GATE) if material_activo else 0.0
g_drop = _compuerta(NIDO_RADIUS - dist_nido, filo=STEEPNESS_GATE) if not nido_completado else 0.0

```

These are soft gates. They don't suddenly activate when the creature is within a certain distance. They gradually increase as the creature gets closer.

This is not just an aesthetic choice. It prevents the creature from lurching between behaviors. It allows smooth transitions, smooth responses, and smooth decisions. In biological terms, it replaces hard switches with continuous, gradual gates — exactly what evolution favors when abrupt changes would be costly or dangerous.

---

## 8. The Final Surprise: There Is No Explicit Memory

By this point, many readers have searched the code looking for a map. Or a list of visited locations. Or perhaps a planner.

You won't find one. That absence is deliberate.

The creature does not survive because it remembers the world with an explicit map. It survives because its continuously competing populations across three functional populations react appropriately to the present.

> **A clarification:** This does not mean the creature has no memory at all. The activity levels carry information from previous frames because they decay slowly. This is **implicit memory** — trace information that influences current decisions without being stored as an explicit map or list. It's the difference between remembering where you are and remembering where you've been. The creature does the former; it does not do the latter.

This is probably the most surprising property of the entire program.

Modern AI often accumulates knowledge by adding more memory: more parameters, more layers, more training data. This architecture attempts something different. It asks how far carefully organized competition can go before explicit memory becomes necessary.

Whether that answer ultimately extends to biological intelligence remains an open scientific question. For this small creature, however, the experiment is surprisingly successful.

The creature forages for food. It flees from the wolf. It builds a nest. It does all of this without a map, without a planner, without a decision tree, and without a state machine. What it has instead is three functional populations, each with twenty-five copies of a four-number mold, arranged in rings, competing continuously, with the third population waking up when the time is right.

---

## 9. What This System Cannot Do

Before concluding, it is important to be clear about the limitations of this architecture.

* **This system does not learn in the current ambient:** The weights are fixed from the start (inherited). The creature never updates its parameters based on experience. Behavior is pre-specified dynamics responding to different holographics inputs. This is deployment, not training.
* **This system has no long-term planning, unless new cortical areas are awaken:** Without a map or sequence memory, the creature cannot plan routes, anticipate future states, or reason about consequences beyond the immediate present. In principle, as proven with N+2, new cortical areas can extend long term planning.
* **This system mat not not survive to novel environments:** If the creature is placed in a world with different food types, different predators, or different nest-building requirements, it will fail. Its capabilities are fixed at deployment. But its CMs structure may rapidly adapt.
* **This system has no hierarchical behavior:** All decisions are immediate motor responses to holographic variables. There is no higher-level control that orchestrates sub-goals or sequences of actions. The creature cannot say "first find material, then approach the nest, then build" as a plan; these behaviors emerge from the dynamics but are not explicitly structured.
* **This system has no lateral connectivity or recurrence:** The three cortical areas are independent except for their blended output. There is no communication between areas, no top-down modulation, and no recurrent loops within areas. This makes the system simpler, resilient and more survival prone, but also perhaps less powerful than a truly recurrent or hierarchical architecture.

These are design choices. The architecture trades generality for simplicity, stability, and interpretability. It is a proof of concept for developmental deployment, not a general solution to all AI problems, so far.

---

## 10. So Why Write Code Like This?

The answer to the original question — *"Why on Earth would anyone write code like this?"* — is now clear.

Because specifying behavior directly doesn't scale.

If you tried to write an `if` statement for every situation the creature might encounter now or in future, you would never finish. If you tried to train a neural network on every possible scenario, you would never have enough data nor enough power to modify sinapses. If you tried to build a map of the world, the creature would be helpless in any environment it hadn't memorized.

This architecture takes a different approach. It builds a small, repeatable unit and deploys it many times across multiple functional populations. The unit is simple. The deployment is systematic. The behavior emerges from the interaction and energy burn.

This is the same approach that biology discovered billions of years ago and use today to build biological brains, under the severe constraint of the genomic bottleneck. It is the same approach that software engineers use when they write a class and instantiate it many times. It is the same approach that hardware engineers use when they configure an FPGA with replicated logic blocks.

Deployment — not description — is how you build things that are too large to describe.

Evolution discovered this. Biology embodies this. This code demonstrates this.

Now it's your turn to use it.

---

## References and Further Reading

This work draws inspiration from:

### Biological Foundations

* **Zador, A. M. (2019).** *A critique of pure learning and what artificial neural networks can learn from animal brains.* Nature Communications, 10(1), 1-7. — The genomic bottleneck hypothesis.
* **Mountcastle, V. B. (1997).** *The columnar organization of the neocortex.* Brain, 120(4), 701-722. — Cortical columns as repeated motifs.
* **Raichle, M. E. (2015).** *The brain's default mode network.* Annual Review of Neuroscience, 38, 433-447. — Continuous intrinsic activity.
* **Kirschner, M. W., & Gerhart, J. C. (1998).** *Evolvability.* Proceedings of the National Academy of Sciences, 95(15), 8420-8427. — Facilitated variation and developmental deployment.

### Engineering and AI

* **Holland, J. H. (1975).** *Adaptation in Natural and Artificial Systems.* — Genetic algorithms.
* **Goldberg, D. E. (1989).** *Genetic Algorithms in Search, Optimization and Machine Learning.* — Practical GA implementation.
* **Rusu, A. A., et al. (2016).** *Progressive neural networks.* arXiv preprint arXiv:1606.04671. — Adding new networks without forgetting.
* **Kirkpatrick, J., et al. (2017).** *Overcoming catastrophic forgetting in neural networks.* Proceedings of the National Academy of Sciences, 114(13), 3521-3526. — Elastic weight consolidation.
* **Chang, A. (2026).** *vAGI-2026 Reikiavick. Evolving Cooperative Neural Agents.* — The specific codebase this essay explores.

---

*A tour through the engineering ideas hidden inside a few hundred lines of Python that take inspiration from biological brain deployment.*
