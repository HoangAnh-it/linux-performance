#!/bin/bash

source .env

sendMailToMe() {
    MAIL=$1
    PASS=$2
    CPU=$3
    RAM=$4

    MAIL_SUBJECT="Performance of linux"
    MAIL_BODY="Warning! Your linux OS is overloading. CPU: $CPU%, RAM: $RAM%"

    curl -s --url 'smtps://smtp.gmail.com:465' --ssl-reqd \
    --mail-from $MAIL \
    --mail-rcpt $MAIL \
    --user $MAIL:$PASS \
    -T <(echo -e "From: $MAIL\nTo: $MAIL\nSubject: $MAIL_SUBJECT\n\n$MAIL_BODY")
    echo ">>> Sent mail" 
}

log() {
    DATE=`date +'%Y-%m-%d %H:%M:%S'`
    content="$DATE CPU: $2%, RAM: $3%"
    echo $content
    echo $content >> $1
}

main() {
    percentUsageCPU=$(printf "%.2f" `top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}'`)
    percentUsageRAM=$(printf "%.2f" `free | grep Mem | awk '{print ($3/$2) * 100}'`)
    echo "Log path: $LOG_PATH"
    echo "Interval checkingL: $INTERVAL_CHECKING"
    echo "Limited: $LIMITED_USAGE"

    while true
    do
        if ([[ "$percentUsageCPU" > "$LIMITED_USAGE" ]] || [[ "$percentUsageCPU" == "$LIMITED_USAGE" ]]  || [[ "$percentUsageRAM" > "$LIMITED_USAGE" ]] || [[ "$percentUsageRAM" == "$LIMITED_USAGE" ]] )
        then
            if [[ -n "$MAIL" ]] && [[ -n "$MAIL_PASSWORD" ]] ;then
                sendMailToMe $MAIL $MAIL_PASSWORD $percentUsageCPU $percentUsageRAM
            fi
        fi

        log $LOG_PATH $percentUsageCPU $percentUsageRAM
        sleep $INTERVAL_CHECKING
    done
}

main