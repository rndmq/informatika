import curses
import time
import random

def get_input(stdscr, y, x, prompt, color_pair):
    stdscr.addstr(y, x, prompt, curses.color_pair(color_pair) | curses.A_BOLD)
    stdscr.refresh()
    curses.echo(); curses.curs_set(1) 
    user_input = stdscr.getstr(y, x + len(prompt), 15).decode('utf-8')
    curses.noecho(); curses.curs_set(0) 
    return user_input

def start_menu(stdscr):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    border_line = "=" * (max_x - 2)
    
    while True:
        stdscr.erase()
        stdscr.addstr(1, 1, border_line, curses.color_pair(4))
        stdscr.addstr(2, (max_x // 2) - 15, " TERMINAL MONSTER SHOOTER ", curses.color_pair(3) | curses.A_REVERSE)
        stdscr.addstr(3, 1, border_line, curses.color_pair(4))
        stdscr.addstr(5, 2, "--- Masukkan Data Karakter ---", curses.color_pair(4))
        
        try:
            name = get_input(stdscr, 7, 2, "[?] Nama Karakter     : ", 1)
            fp = int(get_input(stdscr, 8, 2, "[?] Firepower (ex:50) : ", 1))
            rof = int(get_input(stdscr, 9, 2, "[?] Rate of Fire      : ", 1))
            acc = int(get_input(stdscr, 10, 2, "[?] Accuracy (1-100)  : ", 1))
            eva = int(get_input(stdscr, 11, 2, "[?] Evasion (1-100)   : ", 1))
            break 
        except ValueError:
            stdscr.addstr(13, 2, "[!] ERROR: Input stat harus berupa ANGKA!", curses.color_pair(2) | curses.A_BLINK)
            stdscr.getch()

    stdscr.erase()
    stdscr.addstr(1, 1, border_line, curses.color_pair(4))
    stdscr.addstr(2, (max_x // 2) - 10, " STATISTIK LU ", curses.color_pair(1) | curses.A_REVERSE)
    stdscr.addstr(5, 2, f"Nama: {name} | Base HP: 100", curses.color_pair(1))
    stdscr.addstr(7, 2, "SKILL BATTLE:", curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(8, 2, "[1] Fireball (Dmg x2.5) | [2] Magic Missile (Cepat) | [3] Laser (Tembus)", curses.color_pair(4))
    stdscr.addstr(11, 2, ">>> TEKAN [SPASI] UNTUK MULAI GAME <<<", curses.color_pair(2) | curses.A_BLINK)
    
    while True:
        if stdscr.getch() == ord(' '): break

    return {"name": name, "firepower": fp, "rof": rof, "accuracy": acc, "evasion": eva, "hp": 100, "max_hp": 100}

def draw_safe(pad, y, x, text, attr=0):
    try: pad.addstr(int(y), int(x), text, attr)
    except curses.error: pass

AOE_PATTERN = [
    "   ■■■■■■■■   ",
    " ■□□□□□□□□□□■ ",
    "■□□□□□□□□□□□□■",
    "■□□□□□□□□□□□□■",
    "■□□□□□□□□□□□□■",
    "■□□□□□□□□□□□□■",
    "■□□□□□□□□□□□□■",
    "■□□□□□□□□□□□□■",
    " ■□□□□□□□□□□■ ",
    "  ■□□□□□□□□■  ",
    "   ■■■■■■■■   "
]

def game_loop(stdscr, stats):
    stdscr.nodelay(1); stdscr.timeout(50); stdscr.clearok(False)
    max_y, max_x = stdscr.getmaxyx()
    pad = curses.newpad(max_y, max_x)
    
    player_y, player_x = max_y // 2, 5
    bullets, monsters, traces = [], [], []
    score = 0
    stage = 1
    playing = True
    base_cooldown = max(0.1, 1.0 - (stats['rof'] / 150))
    last_shoot_time = 0
    player_stun_timer = 0 

    boss = {
        'hp': stats['max_hp'] * 100, 'max_hp': stats['max_hp'] * 100, 
        'shield': 300, 'def': 30,
        'y': max_y // 2, 'x': max_x - 10,
        'active': False, 'state': 'idle', 'cast_timer': 0, 'current_skill': 0,
        'cd': {1: 0, 2: 0, 3: 0, 4: 0}, 'cd_max': {1: 2, 2: 7, 3: 15, 4: 45},
        'staff_char': '|', 'staff_anim_timer': 0, 'skill_data': {},
        'skills_cast_count': 0,
        'move_timer': 0, 'parry_text_timer': 0
    }

    while playing:
        pad.erase()
        current_time = time.time()
        
        if score >= 2 and stage == 1:
            stage = 2
            boss['active'] = True
            monsters.clear(); bullets.clear()
            for k in boss['cd']: boss['cd'][k] = current_time + 2 

        ui_mode = "BOSS FIGHT!" if stage == 2 else "MOB CLEARING"
        ui_text = f" Stage: {ui_mode} | Kills: {score} | HP: {stats['hp']} | Player: {stats['name']} "
        draw_safe(pad, 0, 1, ui_text, curses.color_pair(3) | curses.A_BOLD)
        pad.hline(1, 0, '-', max_x)

        key = stdscr.getch()
        old_py, old_px = player_y, player_x
        
        if key == ord('q'): playing = False
        
        if current_time < player_stun_timer:
            draw_safe(pad, player_y - 1, player_x - 2, "*STUN*", curses.color_pair(3) | curses.A_BLINK)
        else:
            if key == curses.KEY_UP and player_y > 2: player_y -= 1
            elif key == curses.KEY_DOWN and player_y < max_y - 2: player_y += 1
            elif stage == 2 and key == curses.KEY_LEFT and player_x > 1: player_x -= 1
            elif stage == 2 and key == curses.KEY_RIGHT and player_x < max_x - 20: player_x += 1

            if current_time - last_shoot_time > base_cooldown:
                if key == ord('1'):
                    bullets.append({'y': player_y, 'x': player_x + 3, 'char': 'O', 'col': 2, 'speed': 1, 'dmg': stats['firepower'] * 2.5, 'type': 1})
                    last_shoot_time = current_time + 0.3
                elif key == ord('2'):
                    bullets.append({'y': player_y, 'x': player_x + 3, 'char': '*', 'col': 4, 'speed': 2, 'dmg': stats['firepower'] * 1.0, 'type': 2})
                    last_shoot_time = current_time
                elif key == ord('3'):
                    bullets.append({'y': player_y, 'x': player_x + 3, 'char': '≡', 'col': 5, 'speed': 4, 'dmg': stats['firepower'] * 1.5, 'type': 3})
                    last_shoot_time = current_time + 0.5

        if player_y != old_py or player_x != old_px:
            traces.append([old_py, old_px, "≈", 4, 1])

        for t in traces[:]:
            t[4] -= 1
            if t[4] <= 0: traces.remove(t)
            else: draw_safe(pad, t[0], t[1], t[2], curses.color_pair(t[3]))

        for b in bullets[:]:
            traces.append([b['y'], b['x'], '~' if b['type']==1 else ('+' if b['type']==2 else '='), b['col'], 1])
            b['x'] += b['speed']
            
            if b['x'] >= max_x - 2 or b['x'] <= 1: 
                bullets.remove(b)
                continue
                
            draw_safe(pad, b['y'], b['x'], b['char'], curses.color_pair(b['col']) | curses.A_BOLD)
            
            if b.get('is_reflected'):
                if abs(b['y'] - player_y) <= 1 and abs(b['x'] - player_x) <= max(1, abs(b['speed'])):
                    stats['hp'] -= 30
                    if b in bullets: bullets.remove(b)
                continue

            if stage == 2 and boss['active']:
                if abs(b['y'] - boss['y']) <= 1 and boss['x'] - 4 <= b['x'] <= boss['x'] + 1:
                    if random.randint(1, 100) <= 40:
                        boss['state'] = 'idle' 
                        b['speed'] = -b['speed'] 
                        b['is_reflected'] = True
                        b['col'] = 5 
                        
                        boss['parry_text_timer'] = current_time + 1.0
                        boss['staff_anim_timer'] = current_time + 0.3
                        boss['staff_char'] = '/'
                    else:
                        if random.randint(1, 100) <= stats['accuracy']: 
                            actual_dmg = max(1, int(b['dmg']) - boss['def'])
                            
                            if boss['shield'] > 0:
                                if boss['shield'] >= actual_dmg:
                                    boss['shield'] -= actual_dmg
                                    actual_dmg = 0
                                else:
                                    actual_dmg -= boss['shield']
                                    boss['shield'] = 0
                            
                            boss['hp'] -= actual_dmg
                        
                        if b['type'] != 3 and b in bullets: bullets.remove(b)


        if stage == 1:
            if random.randint(1, 100) < 8: monsters.append([random.randint(3, max_y - 2), max_x - 4, 150, 150])
            for m in monsters[:]:
                traces.append([m[0], m[1] + 3, ".", 2, 1])
                m[1] -= 1
                if m[1] <= player_x + 1 and m[0] == player_y:
                    if random.randint(1, 100) > stats['evasion']: stats['hp'] -= 20
                    if m in monsters: monsters.remove(m)
                    if stats['hp'] <= 0: playing = False
                    continue
                for b in bullets[:]:
                    if b.get('is_reflected'): continue
                    if b['y'] == m[0] and abs(b['x'] - m[1]) <= max(1, b['speed']):
                        if b['type'] != 3 and b in bullets: bullets.remove(b)
                        if random.randint(1, 100) <= stats['accuracy']:
                            m[2] -= b['dmg']
                            if m[2] <= 0:
                                if m in monsters: monsters.remove(m)
                                score += 1
                                break
                if m in monsters:
                    if m[1] > 1:
                        draw_safe(pad, m[0], m[1], "[M]", curses.color_pair(2) | curses.A_BOLD)
                        hp_ratio = max(0, m[2]) / m[3]
                        draw_safe(pad, m[0]-1, m[1]-1, "[" + "#"*int(hp_ratio * 5) + "-"*(5 - int(hp_ratio * 5)) + "]", curses.color_pair(1 if hp_ratio > 0.4 else 2))
                    else: monsters.remove(m)

        elif stage == 2 and boss['active']:
            

            if current_time > boss['move_timer'] and boss['state'] == 'idle':

                if boss['x'] > player_x + 6: boss['x'] -= 1
                elif boss['x'] < player_x - 6: boss['x'] += 1
                
                if boss['y'] > player_y + 1: boss['y'] -= 1
                elif boss['y'] < player_y - 1: boss['y'] += 1
                
                boss['move_timer'] = current_time + 1.2
            

            if abs(player_x - boss['x']) <= 4 and abs(player_y - boss['y']) <= 2:
                if current_time > player_stun_timer:
                    stats['hp'] -= 40 
                    player_stun_timer = current_time + 3.0
                    boss['staff_anim_timer'] = current_time + 0.3
                    boss['staff_char'] = '\\' # Animasi gebug
                    
                    if player_x < boss['x']: player_x = 2
                    else: player_x = max_x - 6
                    
                    traces.append([player_y, player_x, "BONK!", 2, 3])

            if boss['state'] == 'idle':
                ready_skills = [k for k, v in boss['cd'].items() if current_time >= v]
                if 4 in ready_skills and boss['skills_cast_count'] < 2: ready_skills.remove(4)

                if ready_skills:
                    chosen_skill = max(ready_skills)
                    boss['state'] = 'casting'
                    boss['current_skill'] = chosen_skill
                    boss['cast_timer'] = current_time
                    boss['staff_anim_timer'] = current_time + 0.5 
                    
                    if chosen_skill == 1: boss['skill_data'] = {'x': player_x, 'y': player_y, 'start': current_time}
                    elif chosen_skill == 2: boss['skill_data'] = {'x': player_x, 'y': player_y, 'start': current_time, 'dmg': stats['max_hp'] // 6}
                    elif chosen_skill == 3:
                        dx = player_x - boss['x']
                        dy = player_y - boss['y']
                        boss['skill_data'] = {'dx': dx, 'dy': dy, 'start': current_time, 'dur': 1.5}
                        if dy < -2: boss['staff_char'] = '\\'
                        elif dy > 2: boss['staff_char'] = '/'
                        else: boss['staff_char'] = '-'
                    elif chosen_skill == 4: boss['skill_data'] = {'wave': 0, 'start': current_time, 'phase': 0, 'pillars': []}

            if boss['state'] == 'casting':
                sk = boss['current_skill']
                sd = boss['skill_data']
                time_elapsed = current_time - sd['start']
                
                if sk == 1:
                    if time_elapsed < 0.5: draw_safe(pad, sd['y'] - 3, sd['x'], "|", curses.color_pair(3))
                    elif time_elapsed < 1.0: draw_safe(pad, sd['y'] - 1, sd['x'], "|", curses.color_pair(3))
                    elif time_elapsed < 1.2: draw_safe(pad, sd['y'], sd['x'], "●", curses.color_pair(2) | curses.A_BOLD)
                    elif time_elapsed < 1.5:
                        draw_safe(pad, sd['y'], sd['x']-1, "*#*", curses.color_pair(2) | curses.A_BOLD)
                        if not sd.get('hit') and player_x == sd['x'] and player_y == sd['y']:
                            stats['hp'] -= stats['max_hp'] // 8; sd['hit'] = True
                    else:
                        boss['state'] = 'idle'
                        boss['cd'][1] = current_time + boss['cd_max'][1]
                        boss['skills_cast_count'] += 1

                elif sk == 2:
                    if time_elapsed < 1.0:
                        fall_y = int(sd['y'] - 5 + (time_elapsed * 5))
                        draw_safe(pad, fall_y, sd['x'], "■", curses.color_pair(5))
                    elif time_elapsed < 2.5:
                        sy = sd['y'] - len(AOE_PATTERN)//2
                        sx = sd['x'] - len(AOE_PATTERN[0])//2
                        for r, row in enumerate(AOE_PATTERN):
                            for c, char in enumerate(row):
                                if char != ' ':
                                    col = 2 if char == '■' else 4
                                    draw_safe(pad, sy + r, sx + c, char, curses.color_pair(col) | curses.A_BOLD)
                        
                        if not sd.get('hit'):
                            if sy <= player_y < sy + len(AOE_PATTERN) and sx <= player_x < sx + len(AOE_PATTERN[0]):
                                hit_char = AOE_PATTERN[player_y - sy][player_x - sx]
                                if hit_char == '□': stats['hp'] -= sd['dmg']
                                elif hit_char == '■': stats['hp'] -= sd['dmg'] // 2
                            sd['hit'] = True
                    else:
                        boss['state'] = 'idle'
                        boss['cd'][2] = current_time + boss['cd_max'][2]
                        boss['skills_cast_count'] += 1

                elif sk == 3:
                    if time_elapsed < sd['dur']:
                        steps = max(abs(sd['dx']), abs(sd['dy']))
                        steps = max(1, steps)
                        x_inc = sd['dx'] / steps
                        y_inc = sd['dy'] / steps
                        
                        laser_y = boss['y']
                        laser_x = boss['x'] - 2
                        
                        for i in range(1, int(max_x * 1.5)): 
                            lx = int(laser_x + (x_inc * i))
                            ly = int(laser_y + (y_inc * i))
                            if lx < 0 or lx >= max_x or ly < 0 or ly >= max_y: break
                            
                            char = "°" if i == 1 else ("•" if i == 2 else "●")
                            draw_safe(pad, ly, lx, char, curses.color_pair(5) | curses.A_BOLD)
                            
                            interval = int(time_elapsed * 3)
                            if sd.get(f'hit_{interval}') is None and player_x == lx and player_y == ly:
                                stats['hp'] -= stats['max_hp'] // 4
                                sd[f'hit_{interval}'] = True
                    else:
                        boss['state'] = 'idle'
                        boss['staff_char'] = '|' 
                        boss['cd'][3] = current_time + boss['cd_max'][3]
                        boss['skills_cast_count'] += 1

                elif sk == 4:
                    if sd['phase'] == 0:
                        sd['pillars'] = []
                        for _ in range(50):
                            px = random.randint(2, max_x - 5)
                            py = random.randint(2, max_y - 3)
                            sd['pillars'].append((px, py))
                        sd['phase'] = 1; sd['start'] = current_time
                    
                    elif sd['phase'] == 1:
                        for px, py in sd['pillars']: draw_safe(pad, py, px, "!", curses.color_pair(3) | curses.A_BLINK)
                        if time_elapsed > 1.0: sd['phase'] = 2; sd['start'] = current_time
                    
                    elif sd['phase'] == 2:
                        for px, py in sd['pillars']: 
                            draw_safe(pad, py, px, "X", curses.color_pair(2) | curses.A_BOLD)
                            if player_x == px and player_y == py: stats['hp'] = 0 
                        if time_elapsed > 0.5:
                            sd['wave'] += 1
                            if sd['wave'] < 3: sd['phase'] = 0
                            else: 
                                sd['phase'] = 3
                                sd['start'] = current_time
                    
                    elif sd['phase'] == 3 or sd['phase'] == 5:
                        sd['x'] = random.randint(15, max_x - 15)
                        sd['y'] = random.randint(6, max_y - 6)
                        sd['phase'] += 1
                        sd['start'] = current_time
                        sd['hit'] = False
                    
                    elif sd['phase'] == 4 or sd['phase'] == 6:
                        if time_elapsed < 1.0:
                            fall_y = int(sd['y'] - 5 + (time_elapsed * 5))
                            draw_safe(pad, fall_y, sd['x'], "■", curses.color_pair(2))
                        elif time_elapsed < 2.5:
                            sy = sd['y'] - len(AOE_PATTERN)//2
                            sx = sd['x'] - len(AOE_PATTERN[0])//2
                            for r, row in enumerate(AOE_PATTERN):
                                for c, char in enumerate(row):
                                    if char != ' ': draw_safe(pad, sy + r, sx + c, char, curses.color_pair(2) | curses.A_BOLD)
                            if not sd.get('hit'):
                                if sy <= player_y < sy + len(AOE_PATTERN) and sx <= player_x < sx + len(AOE_PATTERN[0]):
                                    hit_char = AOE_PATTERN[player_y - sy][player_x - sx]
                                    if hit_char != ' ': stats['hp'] = 0 
                                sd['hit'] = True
                        else:
                            if sd['phase'] == 4:
                                sd['phase'] = 5 
                                sd['start'] = current_time
                            else:
                                boss['state'] = 'idle'
                                boss['cd'][4] = current_time + boss['cd_max'][4]
                                boss['skills_cast_count'] += 1

            by, bx = boss['y'], boss['x']
            draw_safe(pad, by, bx, "K", curses.color_pair(1) | curses.A_BOLD)            
            if current_time < boss['parry_text_timer']:
                p_col = 6 if int(current_time * 10) % 2 == 0 else 4 
                draw_safe(pad, by - 1, bx - 2, "PARRY!", curses.color_pair(p_col) | curses.A_BOLD)
            
            if current_time < boss['staff_anim_timer']:
                if boss['current_skill'] == 3:
                    draw_safe(pad, by, bx-2, boss['staff_char']*2, curses.color_pair(5))
                else:
                    draw_safe(pad, by, bx-1, "-", curses.color_pair(4))
                    draw_safe(pad, by, bx-2, boss['staff_char'], curses.color_pair(4))
                    if boss['staff_char'] == '|':
                        draw_safe(pad, by-1, bx-3, "   * ", curses.color_pair(2))
                        draw_safe(pad, by,   bx-3, " *○* ", curses.color_pair(2) | curses.A_BOLD)
                        draw_safe(pad, by+1, bx-3, "   * ", curses.color_pair(2))
            else:
                draw_safe(pad, by, bx-1, "-", curses.color_pair(4))
                draw_safe(pad, by, bx-2, boss['staff_char'], curses.color_pair(4))

            hp_ratio = max(0, boss['hp']) / boss['max_hp']
            b_len = 20
            f_len = int(hp_ratio * b_len)
            hp_str = f"BOSS: [" + "#"*f_len + "-"*(b_len - f_len) + f"] {boss['hp']}/{boss['max_hp']} | SHIELD: {boss['shield']}"
            draw_safe(pad, 1, (max_x - len(hp_str)) // 2, hp_str, curses.color_pair(2 if boss['shield'] <= 0 else 4) | curses.A_BOLD)

            if boss['hp'] <= 0:
                score += 9999
                playing = False

        if stats['hp'] <= 0: playing = False
        draw_safe(pad, player_y, player_x, "=>", curses.color_pair(1) | curses.A_BOLD)

        try: pad.refresh(0, 0, 0, 0, max_y - 1, max_x - 1)
        except curses.error: pass

    stdscr.nodelay(0); stdscr.clear()
    msg = " YOU DEFEATED THE KING! " if (stage == 2 and boss.get('hp', 1) <= 0) else f" GAME OVER! Kills: {score} "
    stdscr.addstr(max_y//2, (max_x - len(msg))//2, msg, curses.color_pair(1 if stage == 2 and boss.get('hp', 1) <= 0 else 2) | curses.A_BOLD)
    stdscr.addstr((max_y//2) + 2, (max_x - 25)//2, "Tekan apa saja buat keluar...", curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

    player_stats = start_menu(stdscr)
    game_loop(stdscr, player_stats)

if __name__ == "__main__":
    curses.wrapper(main)