import pygame, pygame_gui, sys
from datetime import datetime
from pygame.locals import *
from pypresence import Presence
from .Highscores import Highscores
from .CONSTANTS import *
from .Utils import *
from .EventManager import EventManager
from .AssetLoader import AssetLoader
ASSETLOADER = AssetLoader()

from .components.Player import Player
from .components.Enemy import Enemy
from .components.Side import Side
from .components.PickUp import FireRatePickUp
# from .components.Bullet import Bullet

HIGHSCORES = Highscores('data/highscores.json')
RPC = Presence(DISCORD_CLIENT_ID,pipe=0) # Initialize the client class
RPC.connect() # Start the handshake loop

class Button(pygame_gui.elements.UIButton):
    """Creates a button using pygame_gui library"""
    def __init__(
                self,
                text,
                manager,
                object_id=None,
                loc=(WIDTH / 2 - 100, -200 + HEIGHT / 2 - 50),
                size=(200, 100)):
        super(Button, self).__init__(
            text=text,
            manager=manager,
            object_id=object_id,
            relative_rect=pygame.Rect(loc,size))


class SceneManager(object):
    """
    Basic scene manager for changing between scenes without creating
    a function for each scene and then calling them inside each other
    """
    def __init__(this):
        this.levels = readLevelsFile()["levels"]
        this.start(MainMenu())

    def start(this, scene):
        this.scene = scene
        this.scene.manager = this
        RPC.update(details=this.scene.description)


class _Scene(object):
    """
    Base object for scenes. This should only be used as a parent class for Scenes and no
    direct _Scene object should ever be created.
    """
    def __init__(this):
        this.clock = pygame.time.Clock()
        this.description = None
    def render(this): raise NotImplementedError
    def update(this): raise NotImplementedError
    def handleEvents(this): raise NotImplementedError

class MainMenu(_Scene):
    """Main menu screen"""
    def __init__(this):
        super(MainMenu, this).__init__()
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
        this.description = "In Menu" # for RPC

        this.startButton = Button('Select Level', this.uiManager)

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
                     ASSETLOADER.menuClickSound.play()
                     pygame.time.delay(100)
                     this.manager.start(LevelSelect(this.manager.levels))

            this.uiManager.process_events(event)

class LevelSelect(_Scene):
    """Level Select screen"""
    def __init__(this, levels):
        super(LevelSelect, this).__init__()
        this.description = "Selecting level" # for RPC
        this.clock = pygame.time.Clock()
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
        this.levels = levels

        buttonX, buttonY = WIDTH / 2 - 520, -200 + HEIGHT / 2 - 50
        buttonW, buttonH = 200, 100
        x,y = 0,0

        for level in this.levels:
            Button(this.levels[level]["name"], this.uiManager, object_id=level, loc=(buttonX, buttonY), size=(buttonW, buttonH))
            x += 1
            buttonX += 10 + buttonW
            if x >= 5:
                buttonY += 10 + buttonH
                x = 0
                buttonX = WIDTH / 2 - 520

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
                 ASSETLOADER.menuClickSound.play()
                 pygame.time.delay(100)
                 this.manager.start(GameScene(this.levels[event.ui_element.__dict__["object_ids"][0]]))

            this.uiManager.process_events(event)

class GameScene(_Scene):
    """
    main game logic
    """
    def __init__(this, levelData):
        super(GameScene, this).__init__()
        this.levelData = levelData
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
        this.eventManager = EventManager()

        # create invisible borders which are used for destroying bullets
        this.sides = pygame.sprite.Group()
        this.sides.add(Side(0,0,2,HEIGHT))       # right
        this.sides.add(Side(WIDTH-2,0,2,HEIGHT)) # left
        this.sides.add(Side(0,HEIGHT-2,WIDTH,2)) # bottom
        this.sides.add(Side(0,0,WIDTH,2))        # top

        this.sprites = pygame.sprite.Group() # a group for both player and enemy sprite(s)
        this.enemiesGroup = pygame.sprite.Group() # a group for enemies only
        this.bulletList = pygame.sprite.Group()
        this.playerBullets = pygame.sprite.Group()
        this.pickUpList = pygame.sprite.Group()
        # damage, fireRate, img
        this.player = Player(15, 4, this)
        this.sprites.add(this.player)

        this.enemies = []
        for enemy in this.levelData["enemies"]:
            # hp, unique ID, [], player, sound
            enemy = Enemy(enemy["hp"], enemy["attacks"], 'enemy'+str(len(this.enemies)), this.bulletList, this, ASSETLOADER.soundAttackWaveEnemy)
            this.enemies.append(enemy)
            this.sprites.add(enemy)
            this.enemiesGroup.add(enemy)

        # HP Bar
        this.enemyHPBar = pygame_gui.elements.UIScreenSpaceHealthBar(
            relative_rect=pygame.Rect((20,20),(200,30)),
            sprite_to_monitor=this.enemies[0],
            manager=this.uiManager
        )
        this.invul = False
        this.startTime = pygame.time.get_ticks()
        this.time = None

        if levelData["name"] != "Legacy":
            this.eventManager.addEvent("spawnPickUp", this.spawnPickUp, 4000)

    def render(this, DISPLAY):
        DISPLAY.fill(BGCOLOR)
        this.sprites.draw(DISPLAY)
        this.bulletList.draw(DISPLAY)
        this.playerBullets.draw(DISPLAY)
        this.uiManager.draw_ui(DISPLAY)

    def gameOver(this, winner):
        this.player.kill() # stop player events
        this.eventManager.removeEvent("spawnPickUp")
        this.sprites.empty()
        this.bulletList.empty()
        this.playerBullets.empty()
        this.manager.start(GameOver(this.time, winner, GameScene(this.levelData), legacy=this.score if this.levelData["name"] == "Legacy" else None))

    def spawnPickUp(this):
        pickup = FireRatePickUp()
        this.pickUpList.add(pickup)
        this.sprites.add(pickup)

    def update(this):
        timeDelta = this.clock.tick(60) / 1000

        if pygame.time.get_ticks() - this.startTime >= 2500:
            this.eventManager.checkEvents(pygame.time.get_ticks())

        this.sprites.update()
        this.bulletList.update(timeDelta)
        this.playerBullets.update(timeDelta)

        # if enemy bullet hits the player
        if pygame.sprite.spritecollide(this.player, this.bulletList, True) and not this.invul:
            ASSETLOADER.hitSound.play()
            this.gameOver(False)
        # if player touches an enemy
        if pygame.sprite.spritecollide(this.player, this.enemiesGroup, False) and not this.invul:
            this.gameOver(False)
        # if player collects a pickup
        collidingBoxes = pygame.sprite.spritecollide(this.player, this.pickUpList, True)
        if collidingBoxes:
            for box in collidingBoxes:
                box.pickUp(this.player)

        # if player bullet hits the enemy
        colliders = pygame.sprite.groupcollide(this.enemiesGroup, this.playerBullets, False, True) # group1, group2, kill1, kill2
        if colliders:
            for enemy in colliders:
                this.enemyHPBar.sprite_to_monitor = enemy
                ASSETLOADER.hitSound.play()
                enemy.damage()
                if enemy.current_health <= 0:
                    this.enemiesGroup.remove(enemy)
                    this.sprites.remove(enemy)
                    this.enemies.remove(enemy)
                    enemy.kill()
                    enemy.dead = True

                if all([x.dead for x in this.enemies]):
                    this.enemyHPBar.kill()
                    this.gameOver(True) # winner=True

        # if the enemy hits a wall
        for enemy in this.enemies:
            if enemy.rect.x <= MARGIN or enemy.rect.x >= WIDTH - MARGIN - enemy.image.get_size()[0]:
                enemy.forceDir()

        # if enemy bullet hits a wall (walls are invisible sprites / pygame.Surfaces)
        # if player bullet hits a wall (walls are invisible sprites / pygame.Surfaces)
        pygame.sprite.groupcollide(this.sides, this.bulletList, False, True)
        pygame.sprite.groupcollide(this.sides, this.playerBullets, False, True)

        this.uiManager.update(timeDelta)
        this.time = pygame.time.get_ticks() - this.startTime

        if this.levelData["name"] == 'Legacy':
            if not hasattr(this, 'score'): this.score = 0
            this.score += 1

    def handleEvents(this, events):
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit()
                if event.key == K_F6: this.invul = not this.invul # toggle invulnerability state
                if event.key == K_r: this.manager.start(GameScene(this.levelData)) # toggle invulnerability state

class GameOver(_Scene):
    """
    game over screen
    """
    def __init__(this, time, winner, currentLevel, legacy=None):
        super(GameOver, this).__init__()
        this.time = time
        this.winner = winner
        this.description = "In Menu" # for RPC
        this.currentLevel = currentLevel
        this.legacy = legacy
        this.uiManager = pygame_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')

        HIGHSCORES.load(currentLevel.levelData["name"])
        if this.winner:
            data = {"time": legacy if legacy else this.time, "date": datetime.strftime(datetime.now(), '%d.%m.%Y-%H:%M')}
            HIGHSCORES.addScore(data, currentLevel.levelData["name"])

        this.startButton = Button("Try Again", this.uiManager, loc=(WIDTH / 2 - 100, -200 + HEIGHT / 2 - 50), size=(200,50))
        this.backToLevelListButton = Button("Level Menu", this.uiManager, loc=(WIDTH / 2 - 100, -140 + HEIGHT / 2 - 50), size=(200,50))

        this.text = HIGHSCORES.generateList(legacy=legacy)
        this.highscoreList = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((WIDTH / 2 - 400, HEIGHT / 2 - 50), (800, 400)),
            html_text=this.text,
            manager=this.uiManager
        )

        # RPC.update(details=f"Game Over - {this.time} points", state=f"Highscore: {highscore}")

    def handleEvents(this, events):
        for event in events:
            if event.type == pygame.QUIT: sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == this.startButton:
                        ASSETLOADER.menuClickSound.play()
                        pygame.time.delay(100)
                        this.manager.start(this.currentLevel)
                    if event.ui_element == this.backToLevelListButton:
                        ASSETLOADER.menuClickSound.play()
                        pygame.time.delay(100)
                        this.manager.start(LevelSelect(this.manager.levels))

            this.uiManager.process_events(event)

    def render(this, DISPLAY):
        DISPLAY.fill(BGCOLOR)
        this.uiManager.draw_ui(DISPLAY)
        # display score
        if this.legacy:
            text = f"You won! You got {this.legacy} points!" if this.winner else f"You lost! You got {this.legacy} points."
        else: text = f"You won! Your time: {formatTime(this.time)}" if this.winner else f"You lost!"
        font = pygame.font.Font(None, 24)
        scoreText = font.render(text, True, 0x000000)
        DISPLAY.blit(scoreText, ((WIDTH - scoreText.get_size()[0]) / 2, 100))

    def update(this):
        timeDelta = this.clock.tick(30) / 1000
        this.uiManager.update(timeDelta)
