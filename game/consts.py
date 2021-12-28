FPS = 60
WINDOW_SIZE = (1500, 800)
PLAYAREA_WIDTH = 1200
MESSAGE_AREA_WIDTH = WINDOW_SIZE[0] - PLAYAREA_WIDTH

MS_YAW_VELOCITY = 6
MS_SPEED = 170
MS_ACCEL = 300
MS_FRICTION = 50
MS_SCALE = (75, 75)
MS_MAX_HP = 100
MS_BOOST_DURATION = 5000
MS_BOOST_RATE = 3

ES_YAW_VELOCITY = 0.5
ES_SPEED = 100
ES_ACCEL = 100
ES_FRICTION = 70
ES_SCALE = (75, 75)
ES_DAMAGE = 1

SS_SCALE = (50, 50)
SS_YAW_VELOCITY = 2
SS_HEAL_VALUE = 25

S_PER_FRAME = 1 / FPS

GAP = 50
VIEW_RANGE = 1.5
SHOOT_RANGE = 0.4

ICON_SIZE = (48, 48)
HP_BAR_HEIGHT = 30

JATBOT_LINK = 'https://unjatbot.tenessinum.repl.co/'

WELCOME_TEXT = '''
Вы были отправлены Империей в дальний космос,
где на Вас напал вражеский флот.
Ваша задача - продержаться как можно дольше. 
Вам в помощь был дан спутник Федора, он способен активировать
способности по Вашей команде.
Управление кораблем происходит с помощью клавиш:
W - движение вперед
A - поворот влево
D - поворот вправо
SPACE - стрельба
SHIFT - вызов спутника (нажимаете, появляется микрофон, говорите).

После прочтения данного сообщения нажмите SPACE.
'''