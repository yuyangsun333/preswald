#!/bin/bash

## Function to format time duration
format_time() {
    local seconds=$1
    printf "%02d:%02d:%02d" $((seconds/3600)) $((seconds%3600/60)) $((seconds%60))
}

# Function to print section headers
print_header() {
    echo "========================================="
    echo "$1"
    echo "========================================="
}

# Optional: Enable colors (comment out if not desired)
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m" # No Color

for dir in examples/*/; do
	print_header "Processing directory: $dir"

	start_time=$(date +%s)
    cp autotest/deployments/structured/.env.structured "$dir"
	end_time=$(date +%s)
	echo -e "${GREEN}[ OK ]${NC} Copied .env file [Time: $(format_time $((end_time - start_time)))]"

	cd "$dir" || { echo -e "${RED}[FAIL]${NC} Failed to enter directory: $dir"; continue; }

	# First deployment
	echo -e "\nRunning initial deployment..."
	start_time=$(date +%s)
    output=$(preswald deploy --target structured)
    end_time=$(date +%s)
    deploy_time=$((end_time - start_time))

    APP_URL=""
    
    if echo "$output" | grep -q "Deployment completed successfully"; then
		echo -e "${GREEN}[ OK ]${NC} Deployment successful! [Time: $(format_time $deploy_time)]"
        APP_URL=$(echo "$output" | grep -o 'https://[^"]*')
		echo "   App URL: $APP_URL"

		start_time=$(date +%s)
        curl_output=$(curl -f "$APP_URL" 2>/dev/null)
        end_time=$(date +%s)
        echo -e "${GREEN}[ OK ]${NC} Verified app accessibility [Time: $(format_time $((end_time - start_time)))]"
        echo "   Response preview:"
        echo "$curl_output" | sed 's/^/     /'
    else
		echo -e "${RED}[FAIL]${NC} Deployment failed [Time: $(format_time $deploy_time)]"
        echo "   Output: $output"
    fi

	# Revision deployment
    echo -e "\nRevising deployment..."
    start_time=$(date +%s)
    output=$(preswald deploy --target structured)
    end_time=$(date +%s)
    revise_time=$((end_time - start_time))

    if echo "$output" | grep -q "Deployment completed successfully"; then
		echo -e "${GREEN}[ OK ]${NC} Revision successful! [Time: $(format_time $revise_time)]"
        APP_URL=$(echo "$output" | grep -o 'https://[^"]*')
        echo "   App URL: $APP_URL"

        start_time=$(date +%s)
        curl_output=$(curl -f "$APP_URL" 2>/dev/null)
        end_time=$(date +%s)
        echo -e "${GREEN}[ OK ]${NC} Verified app accessibility [Time: $(format_time $((end_time - start_time)))]"
        echo "   Response preview:"
        echo "$curl_output" | sed 's/^/     /'
    else
		echo -e "${RED}[FAIL]${NC} Revision failed [Time: $(format_time $revise_time)]"
        echo "   Output: $output"
    fi

	# Stop deployment
    echo -e "\nStopping deployment..."
    start_time=$(date +%s)
    output=$(preswald stop --target structured)
    end_time=$(date +%s)
    stop_time=$((end_time - start_time))

    if echo "$output" | grep -q "Deployment stopped successfully"; then
        echo -e "${GREEN}[ OK ]${NC} Stop successful! [Time: $(format_time $stop_time)]"

        start_time=$(date +%s)
        if curl -f "$APP_URL" 2>/dev/null; then
            end_time=$(date +%s)
            echo -e "${RED}[FAIL]${NC} Error: App still accessible [Check time: $(format_time $((end_time - start_time)))]"
            exit 1
        else
            end_time=$(date +%s)
            echo -e "${GREEN}[ OK ]${NC} Confirmed app is down [Check time: $(format_time $((end_time - start_time)))]"
        fi
    else
        echo -e "${RED}[FAIL]${NC} Stop failed [Time: $(format_time $stop_time)]"
        echo "   Output: $output"
    fi

    # Cleanup
    start_time=$(date +%s)
    rm ".env.structured"
    end_time=$(date +%s)
    echo -e "\n${GREEN}[ OK ]${NC} Cleaned up .env file [Time: $(format_time $((end_time - start_time)))]"

    cd - > /dev/null
    echo -e "\n"
done
