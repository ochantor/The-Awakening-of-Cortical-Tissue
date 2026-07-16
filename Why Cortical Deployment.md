
# Why Cortical Deployment?
# The Mold That Grew a Mind

*Why canonical microcircuits matter — a story for students, built around a small artificial-life simulation creature or agent called Pip*

---

## Prologue: a problem older than programming

Before we meet Pip, our agent creature running in Python, it's worth naming the real problem, because it isn't a programming problem. It's an engineering problem under severe constraints, and biology solved it billions of years before Python or Pip existed.

The problem: how do you build a control system — a brain — for a creature, when the "install file" (the genome) has to fit in a space absurdly small compared to the finished system, and still has to be adjustable across generations without being rebuilt from scratch every time?

This is the true story of Pip, a small artificial creature that forages for food, avoids a wolf, and builds a nest — and all of this being possible with a four numbers wide canonical structure, where "canonical" means a basic unit repeated over and over during brain deployment.

---

## Act I — The mold: why so little information has to do so much

Pip didn't have a brain built *for* anything, the way a laptop has a program built for a task. Pip had something stranger: a single, tiny mold, and from that mold an entire creature's will to live had to emerge.

A human genome carries somewhere on the order of a gigabyte of information. The brain it has to specify has on the order of 10¹⁴ synapses. There is no way for the genome to say, to each synapse individually, "connect here, at this strength." The ratio of available instructions to required instructions is catastrophically unfavorable. This is the genomic bottleneck, and every brain that has ever existed had to be born from a workaround, not a blueprint.

The workaround: don't specify every connection. Specify a compact, repeatable rule — *build this one small unit, and repeat it* — and let repetition generate a structure far larger than the instructions describing it. Compression, with algorithmic decompression. A fractal, not a floor plan.

Here is Pip's version of that rule, in full:

```
one CM ("canonical microcircuit") =
    food_weight   ~ small random number
    home_weight   ~ small random number
    pred_weight   ~ small random number
    explore       ~ small random number
```

That's it. Four numbers. No instructions yet about what to actually *do* with the world — just a handful of dials. That single dictionary is, quite literally, the "genome" of one unit. What evolution solves with algorithmic compression, the program solves with a template and a loop that stamps out twenty-five copies. It isn't a coincidence that both reach for "one small unit, repeated" — when specifying every element by hand is unaffordable, it may be the only workable answer left.

There's a second gift hiding inside this low-dimensionality, one that's easy to miss: it doesn't just solve storage, it solves *evolvability*. A genome with a few independent dials is a genome that selection can push in a useful direction quickly — sometimes in a handful of generations, not eons. Darwin's finches shifted beak size measurably after a single drought. Dogs went from wolves to Chihuahuas in centuries, not epochs, because relatively few large-effect knobs were doing the steering. A four-number CM is exactly the kind of object that theory — facilitated variation, in the technical literature — predicts as a good "evolvable unit": not a free architecture to reinvent from nothing, but a few low-risk dials that can be nudged without risking everything else.

And once you notice that, something else follows: a search space this low-dimensional and this loosely coupled is *exactly* the terrain where population-based optimization — a genetic algorithm — does its best work. Each CM's weight tuple determines its own contribution and nothing else; crossing one individual's `pred_weight` with another's `food_weight` doesn't break anything downstream. That's the textbook building-block property that makes crossover meaningful instead of destructive. If you ran a real GA on this problem — a population of weight-vectors, fitness scored by survival time and nest-building speed, selection and crossover per-CM, small mutations, no human in the loop — and it converged toward the same ranges a person had hand-tuned by eye, that would be genuine evidence those numbers are close to a real optimum, not an arbitrary aesthetic choice. If it converged somewhere else, that would be informative too: it would show you exactly which human bias got baked into the "by eye" version.

Worth being honest about where the actual numbers in front of you came from, because it shapes what Pip is a proof *of*.

The weights you're about to see were not discovered by natural selection. They were not tuned by a human watching Pip move and adjusting sliders. They were produced by prompting a language model — an AI that has read a vast corpus of papers, manuals, and code about foraging agents, neural competition, and canonical microcircuits — and asking it: *"Given this architecture, what ranges for these four weights would produce coherent behavior?"*

This is not cheating. It's closer to inheriting a manual of best practices than to either evolution or one programmer's bare intuition. The LLM has no skin in the game — it doesn't care if Pip survives — but it does have *pattern recognition*: it knows what numbers have tended to work in similar architectures it has read about.

Could you have gotten there by hand? Probably, with enough trial and error. Could an evolutionary algorithm have found them? Almost certainly, given enough generations. But neither of those is what happened here. What happened is *distilled collective knowledge*, rendered into four floats by a model that was trained to complete patterns.

That is a *fourth* route to a working number — distinct from evolution, intuition, and optimization. And it matters, as an engineer, that you can tell which one produced a given set of weights in front of you, because each route carries different assumptions, different failure modes, and different implications for what you've actually built.

So when you run Pip and watch it forage, flee, and build a nest, you are watching a simulation whose *numbers* were borrowed from the statistical memory of the field, whose *architecture* was borrowed from biology, and whose *behavior* emerges from neither — but from the interaction of the two, running live. That is not less interesting. It is, in fact, exactly the kind of hybrid system we will build more and more of going forward.

---

## Act II — Deployment: a mold becomes tissue, and the lights never go out

**The mold becomes operational.** Twenty-five copies of the CM get stamped out, each one tuned to face a different direction — a full circle, 0° to 360°. This mirrors something real: rotated cortical columns in the visual cortex repeat the same microcircuitry across space, each copy tuned to a different orientation of a line in your visual field. Same compression trick as Act I, now spread across a continuum instead of collapsed into one unit.

Picture the layout: twenty-five small units (CMs) arranged in a ring, each one a full copy of the same four-number mold, each one facing a slightly different compass heading. None of them are special. None of them know, in advance, which direction will matter. They're just *there*, waiting, and creating different tendencies or "personalities" among the 25 participants.

And here is the part that matters most: they are never *not* running.

```
activity *= 0.92         # every copy loses a little strength, every frame
activity[winner] += 1.0  # and one copy always wins, every frame
```

This never pauses. There's no `if something_interesting_happening:` gate. The competition runs whether Pip is one step from a wolf or standing in an empty field doing nothing in particular — which mirrors something genuinely true about real brains: even at rest, a large share of the body's energy budget goes to intrinsic activity that isn't a response to anything in particular. The brain is not a function waiting on an `input()` call. It runs continuously, competing with itself, whether or not the world is currently offering it something to react to.

Picture it as a small race that never finishes: twenty-five bars, each shrinking a little every tick, until something in the world — the smell of food, the shape of a predator — gives one of them a shove. That bar jumps ahead of the rest. It wins this tick. Pip moves toward it. Then decay starts again, and the race continues, forever, with no finish line and no off switch.

This is why Pip can look, from the outside, like it's *deciding*. It isn't consulting a rulebook. It's letting twenty-five small opinions decay and compete, endlessly, and whichever opinion the world happens to reward hardest in a given instant is the one that moves Pip's legs.

*Where the analogy has a limit, worth sitting with:* rotation across a visual angle works because angle really is a continuous, circular quantity in the world. Movement direction is the same kind of thing. But would this still make sense for a variable that isn't naturally circular — "hunger level," say, or "temperature"? Does it even mean anything to arrange copies of a unit "around a circle" for a quantity that has no wraparound? That's a genuine limit of this kind of population coding, not a flaw specific to Pip — and it's worth asking yourself the next time "put N copies on a circle" looks like the obvious move.

---

## Act III — Growing up: new tissue, not a rewritten mind

Pip is not born able to build a nest. That capability doesn't exist on day one, and for good reason: nest-building needs motor skill and physiological readiness that simply aren't there yet, and running the circuitry for it before Pip can use it well would just waste energy on machinery Pip can't yet operate. Real brains do something similar — myelination, the process that lets neural circuits fire efficiently, continues well into adulthood, arriving late and gradually rather than all at once.

So when the moment comes, biology doesn't reach for the tempting shortcut of modifying the tissue that already works. It grows something new instead, alongside it:

```
if age > AWAKENING_AGE and not build_awake:
    build_awake = True
```

A third population of CMs — structurally identical to the first two, but with its own vocabulary of weights — has been sitting in memory since birth, present but silent, without permission to act. When it wakes, it doesn't overwrite anything. It blends in, with a share of the vote that grows slowly:

```
primary_motor = (1 - weight_n2) * old_motor + weight_n2 * new_motor
```

The old motor tissue is never touched. Not one of its numbers changes. The new tissue simply starts contributing a small, growing fraction of the final decision.

There's a concrete, well-documented reason this matters, and it isn't just aesthetic. Artificial neural networks have a famous failure mode called catastrophic forgetting: train a network on one task, keep training the same weights on a second task, and the second task's corrections silently overwrite what the network learned for the first. It's close to the *default* behavior of a shared set of weights trained sequentially on different things — the same risk you run when you edit a shared base class to add a feature and quietly break something that depended on the old behavior. One family of fixes in machine learning tries to protect the old weights while still touching them — allow the edit, but penalize breaking what mattered before. The other family — the one Pip's design actually mirrors — freezes the old network completely and adds a new column beside it, with connections that let the new column read the old one's output without ever being able to overwrite it. Zero risk of forgetting, because there's nothing shared left to overwrite.

**And here's the piece that's easy to miss the first time through this story.**

Describing the new tissue as "new, but silent" undersells what actually makes this efficient. If the new zone had to *learn* nest-building the moment it woke up — starting from nothing, adjusting its own synapses live, through trial and error against the real world — that would be the expensive path. Learning by modifying synapses costs real time and real energy: every adjustment needs repeated activity, error signals, metabolic upkeep for growing or pruning connections, and a great many failed attempts before anything useful emerges. That's a slow, costly road, and biology avoids walking it any more than it has to.

The far cheaper move is for the new zone to wake up *already shaped*. Not an empty room waiting to be furnished, but a pre-built module wheeled into place and plugged into wiring that's already there. The competence was paid for somewhere else — by evolutionary history, by a training process that happened before this creature was ever born — and Pip doesn't relearn it from zero. Pip just switches it on, and it starts voting immediately.

Picture the contrast directly: a blank zone, awakened, spends a long stretch of clumsy, low-competence behavior while it slowly adjusts its own synapses through trial and error, one small correction at a time, at real metabolic cost. A pre-trained zone, awakened at the exact same trigger, arrives with its weights already shaped by something outside this particular creature's own lived experience — and it starts contributing a competent signal the moment the switch flips. Same trigger. Same wiring pattern for how it joins the vote. Radically different cost, because one path pays for its competence live and the other one doesn't.

This is the deeper reason "add new tissue, don't rewrite the old" is more than just *safe* — it's *cheap*, in exactly the currency biology is stingiest about. Evolution doesn't retrain a species' brain from scratch every time a new trick is needed. It recruits. It repurposes what's already been shaped elsewhere. It switches things on. Live, synapse-by-synapse learning is the fallback — the expensive route taken only when there's no shortcut left to take.

*Worth noticing, as an exercise:* the maturation trigger itself is a single boolean flip — false to true, the instant age crosses a threshold — while the rest of the system goes out of its way to replace hard switches with continuous, gradual gates. That's a real inconsistency, and a good one to sit with: what would it look like to make *permission to wake up* itself a gradual thing, rather than the one hard edge left in an otherwise smooth design?

---

## Epilogue: what Pip actually proves

Not that Pip is conscious. Not that evolution has been "solved." What Pip demonstrates is narrower, and more useful to carry with you:

**No explicit state machine.** There's no `if hungry: seek_food(); elif predator_near: flee()` anywhere in this creature. Behavior emerges from continuous competition among small biased units — the "state" is distributed across a population, not stored in a register.

**No explicit memory.** No lookup table of known food locations, no map of the world. Navigation emerges from activity patterns interacting via simple vector addition. The world isn't remembered — it's continuously sampled and responded to.

**No explicit behavior scripts.** No `move_to_food()`, no `escape_predator()`, no planner sequencing actions. What we recognize as foraging, fleeing, and nest-building are emergent consequences of biased competition, constant decay, and a sensory stream that tips the balance one way or another.

What Pip has *instead*: a compact generative rule, repeated; a handful of low-dimensional biases per copy; a competition that never stops; a maturation schedule that adds capability without ever touching what already worked; and, when the budget allows for it, new capability that arrives pre-shaped rather than learned live at full cost.

From that minimal, information-poor substrate, Pip generates behavior that looks, unmistakably, like deliberate, goal-directed action — without a central executive, without a memory system, without a library of scripts, and without paying full price, in time and energy, for every trick it ever needs. That is the lesson worth carrying into every system you build after this one: sometimes the most robust, most efficient behavior isn't the one you carefully specify. It's the one you let emerge from a small part, repeated, competing forever — and the one you're willing to switch on instead of relearning from nothing.

---

*A story built around a small artificial-life simulation, for students of software and AI — following the biological ideas of Zador (genomic bottleneck), Mountcastle (cortical columns), Raichle (the default mode network), Kirschner & Gerhart (facilitated variation), Holland and Goldberg (genetic algorithms), Chang (Evolving Cooperative Neural Agents) and Rusu et al. (Progressive Neural Networks) alongside the catastrophic-forgetting literature (Kirkpatrick et al., Elastic Weight Consolidation).*

---

## References

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
- Chang, O. (2010). *Evolving Cooperative Neural Agents for Controlling a Vision Guided Mobile Robot.* 10.1109/UKRICIS.2010.5898127. (Early effort of the author to reach the current advances.)
- Douglas, P.K. (2025). *Computing with Canonical Microcircuits.* arXiv:2508.06501.
- Iqbal, A., et al. (2025). *Biologically grounded neocortex computational primitives implemented on neuromorphic hardware improve vision transformer performance.* PNAS, 122(41), e2504164122.
- Devia, C., et al. (2024). *Exploring biological challenges in building a thinking machine.* Cognitive Systems Research, 87, 101260.
- Yamauchi, T., et al. (2025). *A computational model of canonical cortical microcircuits for dynamic Bayesian inference and control as inference.* Neural Networks.
- Max, K., et al. (2025). *'Backpropagation and the brain' realized in cortical error neuron microcircuits.* bioRxiv.
- Li, Y., et al. (2025). *Neural column-inspired spiking neural networks for episodic memory.* In Towards Neuromorphic Machine Intelligence (pp. 117-147).
- Bateni, A. (2024). *Hybrid Spiking Neural Network -- Transformer Video Classification Model.* arXiv:2412.00237.
- Olson, B., et al. (2020). *Self-organization of canonical microcircuits.* (Related work on STDP and self-organization.)
- Golkar, S., et al. (2020). *Two-compartment learning and local supervision in cortical microcircuits.* (Related work on local learning.)
- Yang, G., et al. (2022). *Biologically plausible learning in spiking networks.* (Related work on feedback alignment.)

---

