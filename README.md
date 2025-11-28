# Chronograf Specification  
**The Temporal Standard for Autonomous Systems**

Chronograf defines a formal, machine-readable temporal substrate designed to unify how autonomous systems, cognitive agents, and simulation engines perceive, represent, and exchange time.

This repository contains the authoritative **Chronograf Specification**, including:

- The canonical `.rcg` files (time kernel, channels, topology)
- The build system that produces the Chronograf Manifest
- The validator ensuring correctness and reproducibility
- The normative documentation for Time Atoms, Uncertainty Models, and Temporal Barcodes

Chronograf is part of the broader **OpenRGD** initiative.

---

## Vision

Chronograf is designed as a **temporal lingua franca**: an interoperable layer that any agent, robot, model, or runtime can adopt independently of its hardware, vendor, or cognitive architecture.

The core principles guiding its design are:

### **1. Structural Elegance**
Everything in Chronograf follows a strict formalism, expressed through `.rcg` (Robot ChronoGraph) files. These files are intentionally minimal, unambiguous, and versioned with semantic intent.

### **2. Temporal Neutrality**
Chronograf does not assume one source of truth. Whether a system runs on UTC, TAI, GPS, monotonic clocks, or simulated time, Chronograf provides a uniform representation based on Time Atoms and defined uncertainty bounds.

### **3. Parametric Uncertainty**
Time in real systems is never exact. Chronograf makes uncertainty first-class: measurable, comparable, and attached to every Time Atom. This enables reliable reasoning even in distributed, asynchronous, or accelerated environments.

### **4. Polymorf Licensing Philosophy**
Chronograf’s specification is openly available, stable, and vendor-neutral.  
Implementations may vary, evolve, and differentiate — including commercial or hardware-coupled engines — while still conforming to the standard.

> *Distributed wealth is sustained when the core language is open,  
but implementations are free to differentiate.*

---

## Repository Structure

```
spec/
  chronograf/
    layers/
    manifest/
    tools/
docs/
  white-paper.md
  glossary.md
  rfc/
LICENSE_SPEC
README.md
```

---

## .rcg Layers

### **time_kernel.rcg**  
Defines Time Atom structure, uncertainty model, epoch references, and Temporal Barcode schema.

### **time_channels.rcg**  
Defines all temporal channels with IDs, priorities, and semantic bindings.

### **time_topology.rcg**  
Defines loop frequencies, upstream/downstream dependencies, and scheduler hints.

### **chronograf_manifest.rcg**  
Frozen, integrity-checked snapshot optimized for runtime environments.

---

## Tools

### Build

```bash
python spec/chronograf/tools/build_chronograf.py all
```

### Validate

```bash
python spec/chronograf/tools/validate_chronograf.py
```

---

## Governance

Chronograf follows a transparent RFC process (see `/docs/rfc`).  
The specification is designed to be stable and backwards-aware.

---

## License

Released under **LICENSE_SPEC** following the polymorf philosophy.

---

## Contributing

PRs welcome for RFCs, extensions, clarifications, and vocabulary improvements.
