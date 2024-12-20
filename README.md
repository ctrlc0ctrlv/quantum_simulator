# Quantum Simulator project

## Features

* QuantumOperation class
* RandomGenerator class
* QuantumStateVector class
* CustomQuantumEmulator class
* QiskitQuantumEmulator class
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
* [x] Added QuantumCircuit class
* [x] Added QuantumStateVector class
* [x] Added code coverage script to ci
* [x] Added AbstractQuantumEmulator class
* [x] Added CustomQuantumEmulator class
* [x] Added QiskitQuantumEmulator class
* [ ] Add QuantumEmulator circuit tests
* [ ] Add QulacsQuantumEmulator class
* [ ] Add QuantumEmulators benchmark (compare emulator results on random circuits)
* [ ] Add QuantumAlgorithm class
* [ ] Add Grover algorithm
* [ ] Add QAOA algorithm
