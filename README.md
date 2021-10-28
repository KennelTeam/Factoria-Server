Любое сообщение - это json, в котором есть поля.
В любом сообщении есть поле message_type


Сообщения, которые отправляют клиенты:
1. connect_to_room: room_id - int, nickname - string
2. create_room: nickname - string
3. leave_room
4. answer: answer - int (делитель, который выбрал пользователь)
5. start_game

Сообщения, которые отправляет сервер:
1. response: status - bool (какой-то результат вашего последнего запроса)
2. question: variants - list[int] (три варианта ответа), number - int 
(число, которое сейчас надо отобразить)
3. room_created: room_id - int (-1, если не удалось)
4. connected_player: nickname - string
5. disconnected_player: nickname - string
6. start_game: dividers_count - int
7. mistake_info: mistaken_player - string (никнейм)
8. answer_info: answered_player - string (никнейм)
9. finished: results - {string (nickname) -> 
{mistakes - int, progress - int, time - float}}
10. room_closed