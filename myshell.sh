#!/bin/bash

shell_history_file=".shell_history.txt"
command_history_file="command_history.txt"

clear
echo -e "Welcome to Shellinus! An interactive and easy-to-use shell for linux!\n"

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

    # Save history
    echo "$command_with_options" >> "$shell_history_file"

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
            cd "$arguments" && pwd
            continue
            ;;
        "print")
            system_command="echo $options $arguments"
            ;;
        "calculate")
            echo "$arguments"
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
        "open-memory")
            system_command="python3 Memory_Manager.py"
            ;;
        "check-network")
            system_command="python3 Network_Manager.py"
            ;;
        "date-time")
            system_command="date"
            ;;
        "disk-usage")
            system_command="df -h"
            ;;
        "free-memory")
            system_command="free -h"
            ;;
        "system-info")
            system_command="uname -a"
            ;;
        "save-history")
            current_datetime=$(date "+%Y-%m-%d %H:%M:%S")
            echo "Command history at $current_datetime:" >> "$command_history_file"
            cat "$shell_history_file" >> "$command_history_file"
            rm "$shell_history_file"
            echo "Shell history saved to $command_history_file."
            continue
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
