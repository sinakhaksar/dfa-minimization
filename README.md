# DFA Minimization

This project contains a program that minimizes a given Deterministic Finite Automaton (DFA). The DFA is read from a file named `file.txt` and processed to produce a minimized version of the DFA, which is then visualized.

## Requirements

- Python 3.x
- matplotlib
- networkx

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sinakhaksar/dfa-minimization.git
    cd dfa-minimization
    ```

2. Create and activate a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## File Format

The input file `file.txt` should have the following format:
```
0->(1,2) 
1->(0,2)
1->(1,4)
2->(1,4)
2->(0,1)
3->(0,2)
3->(1,4)
4->(0,4)
4->(1,4)
0   
4   
0,1 
```

### Explanation:

- **Transitions**:
  - Each line of the format `state->(alphabet, destination state)` specifies a transition in the DFA:
    - `state`: The current state.
    - `alphabet`: The alphabet symbol that triggers the transition.
    - `destination state`: The state to transition to.

- **Special Lines**:
  - The last three lines specify:
    - **Start State**: The state where the DFA begins processing.
    - **Final State(s)**: The state(s) where the DFA can successfully terminate.
    - **Alphabet**: The set of symbols the DFA recognizes, separated by commas.

Example:
```
0->(1,2) # State 0 transitions to state 1 on input '2'
1->(0,2) # State 1 transitions to state 0 on input '2'
1->(1,4) # State 1 transitions to state 1 on input '4'
2->(1,4) # State 2 transitions to state 1 on input '4'
2->(0,1) # State 2 transitions to state 0 on input '1'
3->(0,2) # State 3 transitions to state 0 on input '2'
3->(1,4) # State 3 transitions to state 1 on input '4'
4->(0,4) # State 4 transitions to state 0 on input '4'
4->(1,4) # State 4 transitions to state 1 on input '4'
0 # Start state is 0
4 # Final state is 4
0,1 # Alphabet consists of symbols '0' and '1'

```

## Usage

1. Ensure your `file.txt` is in the correct format and placed in the project directory.

2. Run the program:

    ```bash
    python dfa_minimization.py
    ```

3. The program will read the DFA from `file.txt`, minimize it, and display the original and minimized DFA.

## Code Summary

- **`open_file(fileName)`**: Reads the DFA from a file and converts it into a matrix.
- **`make_adjacency_matrix(matrix, alpha)`**: Converts the matrix into an adjacency matrix.
- **`draw_dfa(matrix, start, finals)`**: Draws the DFA using `networkx` and `matplotlib`.
- **`alpha_check(adjacency_matrix, alpha)`**: Ensures all nodes use all alphabet symbols.
- **`remove_unreachable_nodes(matrix, alpha, start)`**: Removes nodes that cannot be reached from the start state.
- **`finals_non_finals(matrix, finals)`**: Classifies states into final and non-final states.
- **`get_transition_class(state, matrix, equivalence_classes, alpha)`**: Gets the transition class for a state.
- **`refine_equivalence_classes(matrix, finals, alpha)`**: Minimizes the DFA by refining equivalence classes.
- **`write_transactions(equivalence_classes, matrix)`**: Writes the transitions for the minimized DFA.
- **`visualize_dfa_transactions(equivalence_classes, transactions)`**: Visualizes the minimized DFA.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT [LICENSE](LICENSE).

## Contact

For any inquiries, please reach out to me at sinakhaksar3@gmail.com .
