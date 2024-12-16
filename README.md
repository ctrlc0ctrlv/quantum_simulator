# Quantum Simulator project

## Features

* QuantumOperation class
* RandomGenerator class
* QuantumStateVector class
* Bash scripts for 1-line usage:
  * Code formatter
  * Code linter
  * Tests runner
  * Code tests coverage checker

## Testing

* Run `./ci/run_test.sh` to run project pytest testing

## Contribution advices

* Run `./ci/code_formatter.sh` before commits for code formatter
* Run `./ci/code_linter.sh` and follow linter advices to keep good codestyle
* Run `./ci/code_coverage.sh` to check code tests coverage. After this check `./htmlcov/index.html` for detailed info

## TODO

* [x] Added testing script to `.ci`
* [x] Added RandomGenerator class
* [x] Add QuantumCircuit class
* [x] Add QuantumStateVector class
* [x] Add code coverage script to ci
* [ ] Add QuantumAlgorithm class
* [ ] Add QuantumSimulator class
* [ ] Add Grover algorithm
* [ ] Add QAOA algorithm
* [ ] Add Qiskit simulator support
* [ ] Add Qulacs simulator support
