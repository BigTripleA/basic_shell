#!/bin/bash

while true; do
    # Display the shell prompt in red
    echo -ne "\e[31mshellinus>\e[0m "

    # Read user input and options in yellow and grey
    read -p $'\e[33m' -e command_with_options

    # Check if the user wants to exit
    if [ "$command_with_options" == "exit" ]; then
        echo "Exiting shell. Goodbye!"
        break
    fi

    # Extract command and options
    command=$(echo "$command_with_options" | awk '{print $1}')
    options=""
    arguments=""

    # Check for options and arguments
    if [[ "$command_with_options" == *-* ]]; then
        options=$(echo "$command_with_options" | grep -o '\s-[^ ]*' | xargs)
        arguments=$(echo "$command_with_options" | sed "s/$command $options//")
    else
        arguments=$(echo "$command_with_options" | sed "s/$command\s*//")
    fi

    # Map user-friendly commands to system commands
    case "$options" in
        "-detailed")
            options="-l"
            ;;
        "-hidden")
            options="-a"
            ;;
        "-uppercase")
            options="-u"
            ;;
        *)
            ;;
    esac

    case "$command" in
        "list") 
            system_command="ls $options"
            ;;
        "edit")
            nano "$arguments"
            ;;
        "cd")
            cd $arguments && pwd
            continue
            ;;
        "print")
            system_command="echo $options $arguments"
            ;;
        "calculate")
            echo $arguments
            system_command="echo $arguments | bc"
            ;;
        "create")
            # Create a file with the specified name
            touch "$arguments"
            system_command="ls -l $arguments"
            ;;
        "show")
            system_command="cat $arguments"
            ;;
        *)
            if ! command -v "$command" &> /dev/null; then
                echo "Error: Command not found - $command"
                continue
            else
                system_command="$command_with_options"
            fi
            ;;
    esac

    # Execute the command and display the output in green
    output=$(eval "$system_command")
    
    # Print formatted output
    echo -e "\e[34mOutput:\n\e[32m$output\e[0m"
done
