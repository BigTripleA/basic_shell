echo "# Shellinus - Custom Shell Script

Shellinus is a simple custom shell script that allows users to execute various commands with user-friendly options.

## Usage

1. Run the script in a terminal:

   \`\`\`bash
   ./shellinus.sh
   \`\`\`

2. Enter commands with optional arguments and options.

   \`\`\`bash
   shellinus> list -detailed
   shellinus> edit filename.txt
   shellinus> cd /path/to/directory
   shellinus> print -uppercase \"Hello, World!\"
   shellinus> calculate 5 + 3
   shellinus> create new_file.txt
   shellinus> show existing_file.txt
   \`\`\`

3. To exit the shell, type:

   \`\`\`bash
   shellinus> exit
   \`\`\`

## Commands and Options

- **list**: List files in the current directory.

  - \`-detailed\`: Show detailed information (equivalent to \`ls -l\`).

- **edit**: Open a text file for editing using the Nano text editor.

- **cd**: Change the current directory.

- **print**: Print a message to the console.

  - \`-uppercase\`: Print the message in uppercase.

- **calculate**: Perform basic arithmetic calculations.

- **create**: Create a new empty file.

- **show**: Display the content of an existing file.

- **Other Commands**: Shellinus supports other standard commands. If a command is not explicitly handled, it will be executed as-is.

## Additional Notes

- Commands are case-sensitive.
- Options can be combined with the command, e.g., \`list -detailed\`.
- Use double quotes for arguments with spaces, e.g., \`print \"Hello, World!\"\`.

## Error Handling

- If an entered command is not found, an error message will be displayed.

Feel free to customize and extend this script according to your needs." > README.md
