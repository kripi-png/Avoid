import pygame, sys, pygame_gui
from pygame import *
from CONSTANTS import *
from Highscores import Highscores
from datetime import datetime
from Utils import *
from Enemy import Enemy
from Player import Player
from Side import Side
from pypresence import Presence

RPC = Presence(DISCORD_CLIENT_ID,pipe=0) # Initialize the client class
RPC.connect() # Start the handshake loop
HIGHSCORES = Highscores('highscores.json')

class SceneManager(object):
    def __init__(this):
        this.start(MainMenu())
    def start(this, scene):
        this.scene = scene
        this.scene.manager = this

class Scene(object):
    def __init__(this): pass
    def render(this): raise NotImplementedError
    def update(this): raise NotImplementedError
    def handleEvents(this): raise NotImplementedError

class MainMenu(Scene):
    def __init__(this):
        super(MainMenu, this).__init__()
        this.clock = pygame.time.Clock()
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT))

        this.startButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH / 2 - 100, -200 + HEIGHT / 2 - 50), (200, 100)),
            text='New Game',
            manager=this.uiManager
        )

        this.text = HIGHSCORES.generateList()
        this.highscoreList = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((WIDTH / 2 - 400, HEIGHT / 2 - 50), (800, 400)),
            html_text=this.text,
            manager=this.uiManager
        )

        RPC.update(details="In Main Menu")

    def render(this, DISPLAY):
        DISPLAY.fill(BGCOLOR)
        this.uiManager.draw_ui(DISPLAY)

    def update(this):
        timeDelta = this.clock.tick(30) / 1000
        this.uiManager.update(timeDelta)

    def handleEvents(this, events):
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit()

            if event.type == pygame.USEREVENT:
             if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                 if event.ui_element == this.startButton:
                     this.manager.start(GameScene())

            this.uiManager.process_events(event)

class GameScene(Scene):
    def __init__(this):
        super(GameScene, this).__init__()
        WIDTH, HEIGHT = pygame.display.get_window_size()
        this.clock = pygame.time.Clock()
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT))
        # loading buncha stuff
        print("Loading Images")
        this.bossImage = loadImage("eyeBoss")
        this.playerImage = loadImage("player")
        print("Loading Sounds"); print("\n")
        this.hitSound = loadSound("hitSound.ogg")
        this.bulletWave = loadSound("bulletWave.ogg")

        this.sprites = pygame.sprite.Group()
        this.bulletList = pygame.sprite.Group()
        this.playerBullets = pygame.sprite.Group()
        # damage, attackSpeed, img
        this.player = Player(15, 0.2, this.playerImage, this.playerBullets)
        # hp, img, [], player, sound
        this.enemy = Enemy(500, this.bossImage, this.bulletList, this.player, this.bulletWave)
        this.sprites.add(this.enemy)
        this.sprites.add(this.player)

        # HP Bar
        this.enemyHP = pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((10,10),(100,50)),
            sprite_to_monitor=this.enemy,
            manager=this.uiManager
        )

        this.sides = pygame.sprite.Group()
        this.sides.add(Side(0,0,2,HEIGHT))       # right
        this.sides.add(Side(WIDTH-2,0,2,HEIGHT)) # left
        this.sides.add(Side(0,HEIGHT-2,WIDTH,2)) # bottom
        this.sides.add(Side(0,0,WIDTH,2))        # top

        this.invul = False
        this.score = 0
        this.rpcTimeLimit = 0

    def render(this, DISPLAY):
        DISPLAY.fill(BGCOLOR)
        this.sprites.draw(DISPLAY)
        this.bulletList.draw(DISPLAY)
        this.playerBullets.draw(DISPLAY)
        this.uiManager.draw_ui(DISPLAY)

    def gameOver(this, winner):
        this.enemy.kill() # stop enemy events
        this.player.kill() # stop player events
        pygame.time.delay(1000)
        this.manager.start(GameOver(this.score, winner))

    def update(this):
        timeDelta = this.clock.tick(60) / 1000

        this.sprites.update()
        this.bulletList.update(timeDelta)
        this.playerBullets.update(timeDelta)

        # if enemy bullet hits the player
        if pygame.sprite.spritecollide(this.player, this.bulletList, True) and not this.invul:
            this.hitSound.play()
            this.gameOver(False)

        # if player bullet hits the enemy
        if pygame.sprite.spritecollide(this.enemy, this.playerBullets, True):
            this.hitSound.play()
            this.enemy.damage()
            if this.enemy.current_health <= 0:
                this.gameOver(True)

        # if the enemy hits a wall
        if this.enemy.rect.x <= MARGIN or this.enemy.rect.x >= WIDTH - MARGIN - this.enemy.image.get_size()[0]:
            this.enemy.forceDir()

        # if enemy bullet hits a wall (walls are invisible sprites / pygame.Surfaces)
        # if player bullet hits a wall (walls are invisible sprites / pygame.Surfaces)
        pygame.sprite.groupcollide(this.sides, this.bulletList, False, True)
        pygame.sprite.groupcollide(this.sides, this.playerBullets, False, True)

        this.score += 1

        # IDEA: maybe create some RichPresence class later with update function or something
        if pygame.time.get_ticks() >= this.rpcTimeLimit + 1000:
            RPC.update(details="In Game", state=f"Score: {this.score}")
            this.rpcTimeLimit = pygame.time.get_ticks()


        this.uiManager.update(timeDelta)

    def handleEvents(this, events):
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit()
                if event.key == K_F6: this.invul = not this.invul # toggle invulnerability state
            if event.type == pygame.USEREVENT+1: # changeDirEvent
                this.enemy.changeDir()
            if event.type == pygame.USEREVENT+2: # enemy attackEvent
                this.enemy.attack()
            if event.type == pygame.USEREVENT+3: # enemy specialAttackEvent
                this.enemy.specialAttack()
            if event.type == pygame.USEREVENT+4: # player attackEvent
                this.player.attack()

class GameOver(Scene):
    def __init__(this, score, winner):
        super(GameOver, this).__init__()
        this.score = score
        this.winner = winner
        this.clock = pygame.time.Clock()
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT))

        if this.winner:
            HIGHSCORES.addScore({"score": score, "date": datetime.strftime(datetime.now(), '%d.%m.%Y-%H:%M')})

        this.startButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH / 2 - 100, -200 + HEIGHT / 2 - 50), (200, 50)),
            text='Try Again',
            manager=this.uiManager
        )

        this.text = HIGHSCORES.generateList()
        this.highscoreList = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((WIDTH / 2 - 400, HEIGHT / 2 - 50), (800, 400)),
            html_text=this.text,
            manager=this.uiManager
        )


        highscore = '-'
        if len(HIGHSCORES.data) > 0:
            highscore = HIGHSCORES.data[0]['score']

        RPC.update(details=f"Game Over - {this.score} points", state=f"Highscore: {highscore}")


    def handleEvents(this, events):
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == this.startButton:
                        pygame.time.delay(1000)
                        this.manager.start(GameScene())

            this.uiManager.process_events(event)


    def render(this, DISPLAY):
        DISPLAY.fill(BGCOLOR)
        this.uiManager.draw_ui(DISPLAY)

        # display score
        font = pygame.font.SysFont(None, 24)
        if this.winner:
            scoreText = font.render(f"You won! You got {this.score} points", True, 0x000000)
        else:
            scoreText = font.render(f"You lost! You got {this.score} points", True, 0x000000)
        DISPLAY.blit(scoreText, ((WIDTH - scoreText.get_size()[0]) / 2, 100))

    def update(this):
        timeDelta = this.clock.tick(30) / 1000
        this.uiManager.update(timeDelta)
