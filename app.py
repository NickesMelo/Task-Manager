from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Estrutura de dados para armazenar quadros, listas e cartões
boards = []

@app.route('/')
def index():
    now = datetime.now()
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M')
    current_datetime = now.strftime('%d/%m/%Y %H:%M')
    return render_template('index.html', boards=boards, current_date=current_date, current_time=current_time, current_datetime=current_datetime)

@app.route('/create_board', methods=['POST'])
def create_board():
    board_name = request.form.get('board_name')
    if board_name:
        boards.append({
            'name': board_name,
            'lists': []
        })
    return redirect(url_for('index'))

@app.route('/delete_board/<int:board_index>', methods=['POST'])
def delete_board(board_index):
    global boards
    boards = [board for i, board in enumerate(boards) if i != board_index]
    return redirect(url_for('index'))

@app.route('/create_list/<int:board_index>', methods=['POST'])
def create_list(board_index):
    board = boards[board_index]
    list_name = request.form.get('list_name')
    if list_name:
        board['lists'].append({
            'name': list_name,
            'cards': []
        })
    return redirect(url_for('index'))

@app.route('/create_card/<int:board_index>/<int:list_index>', methods=['POST'])
def create_card(board_index, list_index):
    board = boards[board_index]
    task_name = request.form.get('task_name')
    task_priority = request.form.get('task_priority')
    task_date = request.form.get('task_date')
    task_time = request.form.get('task_time')
    task_deadline = request.form.get('task_deadline')
    if task_name:
        board['lists'][list_index]['cards'].append({
            'name': task_name,
            'priority': task_priority,
            'date': task_date,
            'time': task_time,
            'deadline': task_deadline,
            'completed': False
        })
    return redirect(url_for('index'))

@app.route('/toggle_card/<int:board_index>/<int:list_index>/<int:card_index>', methods=['POST'])
def toggle_card(board_index, list_index, card_index):
    card = boards[board_index]['lists'][list_index]['cards'][card_index]
    card['completed'] = not card['completed']
    return redirect(url_for('index'))

@app.route('/delete_card/<int:board_index>/<int:list_index>/<int:card_index>', methods=['POST'])
def delete_card(board_index, list_index, card_index):
    board = boards[board_index]
    board['lists'][list_index]['cards'].pop(card_index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
