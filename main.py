import pygame
import sys
import json
import os
from utils.helpers import resource_path
from screens.start_screen import start_screen
from screens.name_input import name_input
from screens.avatar_select import avatar_select
from screens.info_screen import info_screen
from screens.game_screen import game_screen
from utils.audio_manager import AudioManager

# Constantes de pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
ORIGINAL_SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)


# Instancia global del AudioManager
audio_manager = None


def main():
    global audio_manager

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode(ORIGINAL_SCREEN_SIZE)
    pygame.display.set_caption("PixScape")

    is_fullscreen = False

    # Inicializar y cargar audio - AHORA USA resource_path para los sonidos
    audio_manager = AudioManager()
    # Música de fondo
    audio_manager.load_music(resource_path("assets/audio/8-bit-retro-game-music-233964.mp3")) # MODIFICADO
    # Efectos de sonido
    audio_manager.load_sound("item_pickup", resource_path("assets/audio/magic-3-278824.mp3")) # MODIFICADO
    audio_manager.load_sound("victory", resource_path("assets/audio/victory.mp3")) # MODIFICADO
    audio_manager.load_sound("game_over_sfx", resource_path("assets/audio/impact-transition-impact-dramatic-boom-346103.mp3")) # MODIFICADO
    audio_manager.load_sound("box_open", resource_path("assets/audio/open-box.mp3")) # MODIFICADO
    audio_manager.load_sound("box_empty", resource_path("assets/audio/empty.mp3")) # MODIFICADO
    audio_manager.load_sound("button_click", resource_path("assets/audio/click.mp3")) # MODIFICADO
    # Iniciar música de fondo (hilo musical)
    audio_manager.play_music()

    while True:
        # Flujo de pantallas:
        # start_screen → name_input → info_screen → avatar_select → game_screen
        
        start_screen(screen, audio_manager)
        player_name = name_input(screen, audio_manager)
        
        
        selected_avatar = avatar_select(screen, player_name, audio_manager)
        
        continue_game = info_screen(screen, audio_manager)
        if not continue_game:
            # Si el usuario presiona escape en info_screen, volver al inicio
            continue
        # No detenemos la música para que se mantenga durante todo el juego
        final_time = game_screen(screen, selected_avatar, player_name)

        # if final_time is not None:
        #    ranking_data = load_ranking()
        #    ranking_data.append({"name": player_name, "time_taken": final_time})
        #    save_ranking(ranking_data)

        # Si por algún motivo la música se detuvo, la reanudamos
        if not pygame.mixer.music.get_busy():
            audio_manager.play_music()

        # Esperar input para reiniciar o salir
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        is_fullscreen = not is_fullscreen
                        if is_fullscreen:
                            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(ORIGINAL_SCREEN_SIZE)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        waiting_for_input = False
                        break
            pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()