from pygame import*

#Створимо батьківський клас для усіх спрайтів у грі
class GameSprite(sprite.Sprite):
    # sprite.Sprite - це клас з pygame який використовують для створення спрайтів
    #Конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()#викликаємо конструктор батьківського класу
        #Завантаження та зміну розміру зображення
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed#Швидкість спрайту
        self.rect = self.image.get_rect()#Отримання прямокутника, обведеного навколо зображення
        self.rect.x = player_x#Початкова позиція по осі x
        self.rect.y = player_y#Початкова позиція по осі y

    #Метод для відображення спрайту на екрані
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
        # .blit використовується для копіювання зображення на вказану поврхню
#Створимо дочірній клас для спрайту-гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        # key.get_pressed повертає список, де кожен елемент
        #вказує чи була натиснута відповідна клавіша
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_DOWN] and self.rect.y < win_h - 80:
            self.rect.y += self.speed

#Клас(д) для спрайта ворога (переміщається сам)
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_w - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self,color_1, color_2, color_3, wall_x, wall_y, wall_w, wall_h):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_w
        self.height = wall_h
        self.image = Surface((self.width, self.height))# Створює об'єкт Suface заданої ширини та висоти
        self.image.fill((color_1, color_2, color_3))# Заповнити об'єкт кольором(RGB)
        #Кожен спрайт повинен зберігати властивість кусе - прямокутник
        self.rect = self.image.get_rect()# Визначає прямокутну область,яку займає спрайт
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))# Розміщуємо зображення стіни






#Розмір вікна гри
win_w = 700
win_h = 500

#Створення вікна гри
window = display.set_mode((win_w, win_h))
display.set_caption("Лабіринт")#Заголовок вікна
#Завантаження та змінили розмір фону
background = transform.scale(image.load("background.jpg"), (win_w, win_h))

#Створити об'єкт гравця, монстр та скарбу
player = Player("hero.png", 5, win_h - 80, 4)
monster = Enemy("cyborg.png", win_w - 80, 280, 2)
final = GameSprite("treasure.png", win_w - 120, win_h - 80, 0)

#стіни
w1 = Wall(99, 135, 130,100,20,310,10)
w2 = Wall(99, 135, 130,100,100,10,350)
w3 = Wall(99, 135, 130,200,30,10,300)
w4 = Wall(99, 135, 130,300,100,10,350)
w5 = Wall(99, 135, 130,400,30,10,300)
w6 = Wall(99, 135, 130,100,450,410,10)
w7 = Wall(99, 135, 130,500,350,10,100)
w8 = Wall(99, 135, 130,500,170,10,100)
w9 = Wall(99, 135, 130,400,160,110,10)

game = True
finish = False
clock = time.Clock()
FPS = 60

#Написи
# font.init() - ініціалізуємо модуль Pygame для роботи
# з шрифтом
font.init()
# Створити об'єкт шрифту
font = font.Font(None, 70)
#None - стандартний шрифт, 70 - розмір
# font.render() - генерувати зображення нашого тексту
# True - згалудження тексту
win = font.render("YOU WIIN!!!", True,(255,215,0))
lose = font.render("YOU LOSE!!!", True,(180,0,0))


#Інізіалізація музичного модуля та відтвору муз файу
mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
# mixer.Sound - створимо музичний об'єкт
kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

#Визначимо змінну для відслідковування часу
time = 0

while game:
    for e in event.get():
        #event.get() повертає список подій, які сталися
        #в нашій грі з моменту її виклику
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0,0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()
        w7.draw_wall()
        w8.draw_wall()
        w9.draw_wall()

    # ситуація програш
    # sprite.collide_rect() - функція бібл. Pygame яка визначає
    # чи взаэмодыють прямокутники спрайтыв у грі
    if sprite.collide_rect(player, w1) or sprite.collide_rect(player,monster) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6) or sprite.collide_rect(player, w7) or sprite.collide_rect(player, w8):

        finish = True
        window.blit(lose,(200,200))
        kick.play()

        # Відслідковується час, який пройшов після програшу
        time += clock.tick(FPS)

        # Після декількох секунд гра починається знову
        if time == 1000:
            finish = False
            player.rect.x = 5
            player.rect.y = win_h - 80
            time = 0

    # Ситуація перемога
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win,(200,200))
        money.player()


    display.update()
    clock.tick(FPS)









