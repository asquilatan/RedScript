# Architectural Validation Checklist: RedScript Compiler

**Purpose**: Validate architectural integrity and physics compliance of the compiler design
**Created**: 2025-12-06
**Feature**: [Link to spec.md](../spec.md)

## Voxel-DAG Parser Integrity

- [ ] Are the mapping rules from temporal syntax (e.g., `wait(20)`) to discrete tick events explicitly defined? [Clarity, Spec §FR-005]
- [ ] Is the AST structure capable of representing parallel execution branches? [Completeness, Data Model]
- [ ] Are syntax validation rules defined for invalid kinematic commands? [Coverage, Edge Case]
- [ ] Is the "Time as Semantics" principle enforced in the parser's intermediate representation? [Constitution]

## Spatial Solver & Physics Compliance

- [ ] Are Quasi-Connectivity (QC) check algorithms explicitly defined for pistons and droppers? [Physics-First, Spec §FR-010]
- [ ] Is the Block Update Detection (BUD) range specified for all relevant components? [Clarity, Physics-First]
- [ ] Are sub-tick update order constraints defined for simultaneous piston events? [Completeness, Spec §FR-005]
- [ ] Does the solver include checks for piston push limits (12 blocks)? [Coverage, Vanilla Purity]
- [ ] Are "Kinematic Safety" checks defined to prevent self-destruction (e.g., pushing extended pistons)? [Constitution, Spec §FR-006]

## Auto-Router & Signal Integrity

- [ ] Is the collision logic defined to strictly prevent adjacency of uninsulated signal lines? [Spatial Isolation, Spec §FR-004]
- [ ] Are signal strength decay calculations (15-block limit) included in the pathfinding cost function? [Completeness, Spec §FR-003]
- [ ] Is the behavior defined for when a path cannot be resolved (e.g., "Routing Failed" error)? [Edge Case]
- [ ] Are vertical transmission mechanisms (glass towers, slabs) explicitly supported in the routing graph? [Coverage]
- [ ] Is the placement of support blocks for redstone dust enforced by the solver? [Physics-First]

## Visualization & Verification

- [ ] Does the visualization layer render the *exact* internal voxel state used by the solver? [Fidelity, Spec §FR-007]
- [ ] Are controls defined for inspecting internal wiring layers (e.g., layer peeling, x-ray)? [Usability, Spec §FR-008]
- [ ] Is the visual feedback for routing errors or timing violations specified? [Clarity]
- [ ] Does the viewer support the scale of expected user builds (e.g., >10k blocks)? [Performance, Spec §SC-004]

## Serializer & Output Validity

- [ ] Are the generated `.litematic` files validated against the official format specification? [Interoperability, Spec §FR-009]
- [ ] Is metadata (author, description, regions) correctly mapped to the output file? [Completeness]
- [ ] Are block states (e.g., `facing=north`, `powered=true`) validated before serialization? [Correctness]
- [ ] Is the output guaranteed to be free of illegal blocks (e.g., command blocks)? [Vanilla Purity]

## Notes

- This checklist serves as a gate for the Architecture Review phase.
- Items marked "Physics-First" require deep validation against Minecraft Wiki mechanics.
