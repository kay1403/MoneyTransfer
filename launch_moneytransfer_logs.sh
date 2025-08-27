SESSION="moneytransfer"
DJANGO_PATH="/Users/mba-koumba/Documents/MoneyTransfer"
FRONTEND_PATH="$DJANGO_PATH/money-transfer-frontend"
LOGS_PATH="$DJANGO_PATH/logs"

mkdir -p $LOGS_PATH

tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
    tmux new-session -d -s $SESSION
    tmux send-keys -t $SESSION "cd $DJANGO_PATH && source venv/bin/activate && gunicorn MoneyTransfer.wsgi:application --bind 127.0.0.1:8000 > $LOGS_PATH/gunicorn.log 2>&1" C-m
    tmux split-window -h -t $SESSION
    tmux send-keys -t $SESSION "cd $DJANGO_PATH && source venv/bin/activate && daphne -b 0.0.0.0 -p 8001 MoneyTransfer.asgi:application > $LOGS_PATH/daphne.log 2>&1" C-m
    tmux split-window -v -t $SESSION:0.0
    tmux send-keys -t $SESSION "cd $FRONTEND_PATH && npm install && npm run dev > $LOGS_PATH/react.log 2>&1" C-m
    tmux select-layout -t $SESSION tiled
fi

tmux attach -t $SESSION
