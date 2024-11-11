from Syntax_Analyzer import Parser
from LA import Lexer


if __name__ == "__main__":
    input_files = ["test_case1.txt", "test_case2.txt", "test_case3.txt"]
    output_file = "output.txt"

    # Clear the output file before starting
    with open(output_file, 'w') as f:
        f.write("Lexical and Syntax Analysis Output:\n")
        f.write("=" * 40 + "\n")

    # Process each input file
    for i, input_file in enumerate(input_files):
        try:
            with open(input_file, 'r') as file:
                source_code = file.read()  # Read the entire content of the file

            # Check if the source_code is not empty before processing
            if source_code.strip():
                lexer = Lexer(source_code)  # Initialize Lexer with the source code
                lexer.tokenize()  # Generate tokens from the source code
                parser = Parser(lexer.tokens)
                rules = parser.parse()  # Get parsing rules from the parser
                lexer.write_tokens_to_file(output_file, i + 1, rules)  # Pass rules to write_tokens_to_file
            
            else:
                # If the file is empty, write an appropriate message to the output file
                with open(output_file, 'a') as f:
                    f.write(f"\n{'-'*40}\n")
                    f.write(f"{'Test Case ' + str(i + 1):^40}\n")
                    f.write(f"{'-'*40}\n")
                    f.write("Empty source code. No tokens to display.\n")
                    f.write(f"{'-'*40}\n\n")

        except FileNotFoundError:
            # Handle the case where the input file does not exist
            with open(output_file, 'a') as f:
                f.write(f"\n{'-'*40}\n")
                f.write(f"{'Test Case ' + str(i + 1):^40}\n")
                f.write(f"{'-'*40}\n")
                f.write(f"Error: File '{input_file}' not found.\n")
                f.write(f"{'-'*40}\n\n")

    print(f"Lexical and Syntax analysis complete. Output written to {output_file}.")
