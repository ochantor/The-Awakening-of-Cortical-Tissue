# Why Cortical Deployment?
### Biological constraints, how a simulation models them, and why the same structure is also an optimization problem

*A three-act case study for software and AI students, built around a small artificial-life simulation (a creature that forages, avoids a predator, and builds a nest).*

---

## Prologue: the problem biology had to solve before we did

Before looking at the code, it's worth stating the real problem. It isn't a programming problem — it's an **engineering problem under extreme constraints**, and biology solved it billions of years before Python existed.

The problem: how do you build a control system (a brain) for an organism, when the "install file" (the genome) has to fit in a space absurdly small compared to the final system — and still has to be *adjustable* generation after generation, without being rebuilt from scratch each time?

---

## Act I — Why N: the genomic bottleneck, and why low dimensionality is a feature, not a bug

**The biological constraint:**

A human genome carries on the order of ~700 MB–1 GB of information (Zador, 2019, *"A critique of pure learning and what artificial neural networks can learn from animal brains,"* Nature Communications). The brain that genome has to specify has on the order of 10¹⁴ synapses. There is no way for the genome to tell each synapse individually "connect here, with this weight." The ratio of available information to required information is brutally unfavorable. This is the **genomic bottleneck**.

**The solution evolution found:**

Don't wire every connection. Instead: specify a **compact generative rule** — "build this repeatable unit, and repeat it" — and let the unit, through repetition, generate a structure far larger than the genome could ever describe explicitly. It's compression with algorithmic decompression, like a fractal: few instructions, a lot of resulting structure.

**How the program models this:**

This is level **N**: the "mold" before it gets deployed. In the code it isn't a heavyweight class — it's deliberately information-poor:

```python
cms_mot.append({
    "angle": ANGLES[k],
    "food_weight": np.random.uniform(1.2, 1.6),
    "home_weight": np.random.uniform(1.3, 1.7),
    "pred_weight": np.random.uniform(1.2, 1.7),
    "explore": np.random.uniform(0, 0.06)
})
```

A single dictionary (one CM, "canonical microcircuit") holds ~4 numbers. That's literally the "genome" of that unit: a handful of parameters, no instructions yet about what to actually do with the world. What evolution solves with algorithmic compression, the program solves with a template plus a `for` loop generating `N` copies. It's the same *engineering strategy* facing a scarcity-of-information problem — it isn't a coincidence that both reach for "one small unit, repeated"; it's arguably the only workable answer when specifying every element individually is unaffordable.

**A second, subtler resource that low dimensionality gives you for free: fast adjustability.**

A low-dimensional "genome" per CM doesn't just solve *storage* — it solves *evolvability*. In quantitative genetics, the breeder's equation ($R = h^2 S$) shows that how fast a trait responds to selection depends on how simple and additive the genotype→phenotype map is. Fewer interdependent dimensions to move at once means selection can push a trait in a useful direction faster — sometimes within a handful of generations, not eons. Documented cases exist: Darwin's finch beak size shifting measurably after a single drought (Grant & Grant), or centuries — not eons — of dog domestication producing enormous phenotypic variation from relatively few large-effect loci.

There's a dedicated theoretical framework for this: **facilitated variation** (Kirschner & Gerhart, 2005) — the idea that the developmental core is complex and conserved, but is *weakly coupled* to a handful of regulatory parameters (thresholds, rates, expression ranges) that mutation can touch without risking the rest of the system. A CM with 4 numbers (`food_weight`, `home_weight`, `pred_weight`, `explore`) is exactly the kind of object this theory predicts as an "evolvable unit" — not a free architecture to reinvent, but a few low-risk dials.

**How this opens a door worth walking through:**

The `np.random.uniform(1.2, 1.6)` ranges aren't "arbitrary numbers" in the flat sense — they're exactly the kind of low-dimensional parameter that evolvability theory predicts as the right target for tuning, in biology and in software alike. That's a genuinely good design property, and it has a practical consequence: **a low-dimensional, weakly-coupled search space is precisely the terrain where population-based optimization shines.** That's the next section.

---

## Interlude — Prime terrain for a genetic algorithm (Holland–Goldberg)

If each CM's ranges are low-dimensional and relatively independent of one another, this system isn't just "bio-inspired by analogy" — it's a well-formed instance of the exact problem type classical genetic algorithms (Holland, 1975; Goldberg, 1989) were designed for. Worth stating precisely, not just poetically:

1. **Low-order gene encoding.** Each CM contributes a handful of bounded scalars. All CMs across `cms_mot`, `cms_nav`, `cms_n2` (plus global thresholds like `AWAKENING_AGE` or `MINIMUM_IMPULSE`) can be concatenated into a single real-valued chromosome. Textbook case for a real-coded GA.

2. **The building-block hypothesis (Goldberg).** Holland's schema theory predicts good convergence when there are low-order sub-blocks with relatively isolated fitness contributions and **low epistasis** between them — i.e., recombining two individuals doesn't destroy what each block contributed on its own. Each CM is, almost by construction, a building block: its own weight tuple determines its own energy contribution, while the rest of the machinery (competition + decay + vector summation) is agnostic to the specific values. Crossing one individual's `pred_weight` with another's `food_weight` doesn't break anything else — exactly the property building-block theory requires for crossover to make sense.

3. **Fitness that's well-defined and cheap to evaluate.** The program already provides a natural fitness function for free: survival time before the wolf forces a `reset_system()`, or speed of nest completion (`materials_collected / max_materials` as a function of elapsed time).

**The experiment that would turn this analogy into actual evidence:**

Instead of hand-tuning `1.2 → 1.6` while watching the screen, one could run a real GA: a population of vectors (all weights across the three cortical areas plus global thresholds), fitness = survival + nest progress, selection + crossover by building block (per CM) + small Gaussian mutation, run for generations with no human in the loop. If it converges, within a few generations, to ranges similar to what the author hand-tuned — that would be genuine evidence those values aren't arbitrary, but close to a real optimum for the problem. If it converges elsewhere, or fails to converge due to poorly scaled fitness, that's informative too: it would reveal which human design biases entered the manual tuning that "blind" search wouldn't necessarily have found as fast. (With the obligatory *No Free Lunch* caveat, Wolpert & Macready: no optimizer is universally superior — but this problem's structure specifically — low order, low epistasis, cheap fitness — is precisely where classical GAs tend to shine.)

**Where the hardcoded ranges in the file actually came from — three routes, no moral hierarchy among them:**

Worth distinguishing carefully between three distinct search processes, because all three are legitimate and each leaves a different signature:

- **Natural selection:** filters by a single, non-negotiable external criterion — did it survive and reproduce? — over a real population, across real generations.
- **Tuning by eye:** a human runs the program, watches the outcome on screen, and nudges a number because "it looks better." Fast, directed, but biased by one person's aesthetic intuition.
- **LLM-assisted tuning:** when ranges were adjusted via prompts, that isn't the same as "guessing with no grounding." A language model suggests values through *pattern completion* over a huge corpus of existing code and computational-neuroscience / agent-simulation literature — i.e., it cheaply and quickly distills a statistical regularity of what ranges have worked in similar systems others already built and documented. It's closer to breeding with a manual of best practices inherited from generations of prior breeders than to raw natural selection or one programmer's bare eye.

None of the three is dishonest. But only one of them is natural selection, and it matters not to credit evolution with a result that actually came from one of the other two — especially since each leaves a distinct signature that, as engineers, you should be able to recognize in front of a given number.

---

## Act II — Why N+1: rotated repetition + a constant energy budget

**The biological resource (twofold):**

First, **rotated cortical columns** (Mountcastle, 1957; strikingly visible in V1, primary visual cortex): the same microcircuitry repeats spatially, but each copy is "tuned" to a different value of a continuous variable — in V1, the orientation angle of a visual edge (0°–180°); in this program, movement angle (0°–360°). It's the same compression trick from Act I, now applied not to "one unit" but to "a continuum of directions covered by rotated copies of that unit."

Second, **the brain is never off** (Raichle and the default mode network): even at rest, the brain spends a large share of the body's energy budget on *intrinsic* activity, not activity evoked by a task. The brain isn't a program waiting on an `input()` call — it runs continuously, competing with itself, even when "nothing is happening."

**How the program models this:**

`N+1` is the moment the mold stops being a mold and becomes **operational tissue**: 25 deployed copies, each looking at a different angle:

```python
ANGLES = np.linspace(0, 2*np.pi, N, endpoint=False)
```

And the "decay + compete" cycle runs every frame, no exceptions, whether or not there's an interesting stimulus:

```python
activity_mot *= (0.92 ** TIME_WARP)   # always decays
activity_mot[winner_mot] += 1.0        # and always competes
```

This models Raichle's point reasonably well: activity isn't "zero until food arrives," it's continuous, and food only *biases who wins the competition*, not *whether there is a competition*. That's a solid design choice, and not a trivial one — a lot of naive simulations only turn the brain on when "something happens."

**Where it's worth looking more closely:**

Rotation in V1 covers a *continuous variable with real geometric structure* (edge angle really is an angle in visual space). In `MOT`, each CM's preferred angle likewise corresponds to a real movement angle — the analogy holds up cleanly there. As an exercise: would this still hold for variables that *aren't* naturally angular (e.g., "hunger level" or "temperature")? Does it even make sense to "rotate" a CM over a non-cyclic variable? That's a real limitation of circular population coding, not of this program specifically — and it's a good question to ask yourselves the next time "put N copies on a circle" looks like the obvious design move.

---

## Act III — Why N+2: maturation and the marginal cost of adding a new behavior

**The biological constraint and resource, at once:**

The constraint: not every behavior an organism has is available at birth — for good reason. Building a nest, for instance, requires motor capabilities and physiological maturity that simply don't exist on day one. Deploying the *entire* behavioral repertoire from the start would also waste metabolic energy on circuits the organism can't use well yet (think of the human brain's progressive myelination, which continues well into adulthood).

The resource: instead of reconfiguring existing tissue (costly and risky — modifying something that already works so it also does something new), **add new, separate tissue that switches on once development allows it**. Safer (you don't break what already worked) and cheaper to specify genetically (a "maturation trigger" is a simple threshold, not a full reprogramming).

**How the program models this:**

A third population of CMs, structurally identical to the previous two but with its own weight vocabulary, starts at `activity_n2 = np.zeros(N)` — present in memory from the start, but **without permission to act**:

```python
if age > AWAKENING_AGE and not build_awake:
    build_awake = True
```

And integration with the old tissue never overwrites anything — it blends, with a weight that grows gradually:

```python
primary_motor = (1.0 - weight_n2) * motor_mot + weight_n2 * motor_n2
```

This models "don't reconfigure the old, add something new alongside it and let it carry more weight over time" reasonably well — which, incidentally, is a perfectly recognizable software engineering principle: **composition, not override-via-inheritance.** If you've ever avoided modifying a working base class and instead composed a new module alongside it behind a *feature flag* — congratulations, you've reinvented, in your own domain, the same strategy cortical maturation uses in the brain.

**The problem this strategy avoids — and why it should sound familiar:**

There's a concrete reason, not just an aesthetic one, not to reconfigure the old MOT tissue when N+2 arrives. Artificial neural networks have a well-documented failure mode called **catastrophic forgetting**: train a network on task A, then keep training *those same weights* on task B, and B's gradients overwrite and destroy what the network learned for A. It's not a rare bug — it's close to the default behavior of any network trained sequentially on different tasks without special care. It's fundamentally the same risk you run when you modify a shared base class to add a new feature: without good tests, it's easy to silently break old behavior that depended on that class.

There are two families of solutions in ML, and both have an exact mirror in this code:

- **Elastic Weight Consolidation (EWC)** and variants: you do touch the old weights, but you heavily penalize changing the ones that mattered for the previous task. The equivalent of "you may modify the base class, but a guard stops you if you break the old contract."
- **Progressive Neural Networks** (Rusu et al., 2016): the solution this program actually mirrors. Instead of touching the old network, you *freeze* it entirely and add a new column of neurons alongside it, with lateral connections that let it read (not write) the previous column's knowledge. The old network stays intact, guaranteed, because it's literally never touched.

Look at the code again through that lens:

```python
motor_mot = ...   # computed exactly as before, N+2 never touches it
motor_n2 = ...    # new tissue, new weights, zero interference with MOT
primary_motor = (1.0 - weight_n2) * motor_mot + weight_n2 * motor_n2
```

`cms_mot` is never modified when `cms_n2` deploys. That's exactly the Progressive Networks pattern: zero risk of catastrophic forgetting, because there are no shared weights to overwrite — only a blend at the output. The evolutionary rationale is the same engineering rationale: modifying a structure that already works to make room for a new capability is the fastest way to break the old capability without noticing. Adding new tissue alongside is more expensive in "space" (more columns, more parameters) but radically safer. That's the exact trade-off evolution appears to have taken — and the one Rusu et al. took decades of continual-learning research later, whether or not they knew they were rediscovering cortical arealization.

Worth noting the irony: this program is sometimes framed as "proof that intelligence doesn't need learning" — and its most defensible design decision (new tissue, not reconfiguration) is precisely the solution the **continual learning** field developed *to make learning survive itself*. It isn't that learning is absent from the story — it's that by learning nothing at all, the program sidesteps entirely the problem (catastrophic forgetting) that architecture was built to solve. That doesn't invalidate the design, but it does change the reading: not "look, this is how you get intelligence without learning," but "look, this is how you structure a system so that, if it ever did learn, it wouldn't destroy itself in the process."

**Where the model simplifies — and why it matters for you:**

`build_awake` is a boolean that flips from `False` to `True` in a single frame once `age` crosses `0.6`. It's a **discrete switch**, not gradual maturation. Real biological maturation (myelination, synaptic pruning, prefrontal cortex development) is a continuous process taking years, with no single "now" instant. The program *simplifies* that to an `if` — perfectly fine for a didactic simulation, but notice it's exactly the kind of discrete branch the rest of the file went out of its way to eliminate elsewhere (see the comments about replacing `if/elif` with continuous sigmoid gates, `_gate()`). It's an interesting design inconsistency to spot: the author applied "make it continuous" to homeostasis, but not to the maturation trigger. As an exercise, try rewriting `build_awake` as a continuous gate (`construction_instinct` is already gradual — the problem is that *permission to compete at all* is still binary) and see whether the resulting behavior feels more or less biologically convincing.

---

## Epilogue: the engineering lesson, not just the biology one

What this program really teaches — beyond whether it "proves" anything about consciousness or evolution (it doesn't) — is a lesson in **bio-inspired software architecture**:

1. When facing "too much structure, too little information available to specify it," consider generative compression (mold + repetition) instead of exhaustive specification — and if you can, keep that compression *low-dimensional*: it not only fits better, it's also easier to optimize, whether by a GA or any other population-based search.
2. A system can look "always active and deciding" without an explicit state machine — continuous competition + decay is a legitimate alternative to `if/elif` for producing behavior that reads as deliberate.
3. Adding a new capability to a system that already works is safer via composition-with-a-gate than via modifying the existing core — and that exact decision has a name in ML: it's what avoids catastrophic forgetting, the same way Progressive Neural Networks do.
4. If your parameter space has low-order, low-epistasis building blocks (like this program's CMs), don't leave those numbers to eyeballing alone — they have cheap-to-evaluate fitness and a structure a classical genetic algorithm can exploit better than human intuition. Try both, and compare.
5. And, most importantly for your training as engineers: **when your own code does something that "feels" deep, ask honestly what process produced each number — natural selection, a human's eye, or a model trained on someone else's corpus — and don't mistake one for another.** None of the three is dishonest. But only one of them is evolution, and that distinction determines what you can honestly claim the program demonstrates.

---

### References

- Zador, A. (2019). *A critique of pure learning and what artificial neural networks can learn from animal brains.* Nature Communications.
- Mountcastle, V.B. (1957). *Modality and topographic properties of single neurons of cat's somatic sensory cortex.*
- Raichle, M.E. (2001–2015 body of work on the default mode network and the brain's intrinsic activity).
- Kirschner, M. & Gerhart, J. (2005). *The Plausibility of Life: Resolving Darwin's Dilemma.* (Facilitated variation.)
- Grant, P.R. & Grant, B.R. — long-term field studies of Darwin's finches (beak-size response to selection).
- Holland, J.H. (1975). *Adaptation in Natural and Artificial Systems.*
- Goldberg, D.E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning.*
- Wolpert, D.H. & Macready, W.G. (1997). *No Free Lunch Theorems for Optimization.*
- Rusu, A.A. et al. (2016). *Progressive Neural Networks.* DeepMind.
- Kirkpatrick, J. et al. (2017). *Overcoming catastrophic forgetting in neural networks* (Elastic Weight Consolidation). PNAS.
