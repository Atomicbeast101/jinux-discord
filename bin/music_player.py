from datetime import datetime, timedelta
from random import shuffle as shuffle_
from bin import yt_title
from bin.song import Song
import re


# Check if value is an int
def is_int_value(_value):
    try:
        int(_value)
        return True
    except ValueError:
        return False


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


def get_youtube_id(_url):
    regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.'
                       r'(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
    match = regex.match(_url)
    if match:
        return match.group('id')
    return None


def current_song(_song_ends, _duration, _title):
    diff = _duration - (_song_ends - datetime.now()).seconds
    diff_min, diff_sec = divmod(diff, 60)
    dur_min, dur_sec = divmod(_duration, 60)
    return '''**Now Playing:** 
```markdown
[{}:{:02}/{}:{:02}]: {}
```'''.format(diff_min, diff_sec, dur_min, dur_sec, _title)


def playlist_name_valid(_name):
    if re.match('^[\w\d_-]*$', _name):
        return True
    return False


def name_exists(_db_ex, _name):
    for row in _db_ex.execute('SELECT name FROM playlist WHERE name=?;', (_name, )):
        return True
    return False


def song_exists(_db_ex, _youtube_id):
    for row in _db_ex.execute('SELECT name FROM song WHERE youtube_id=?;', (_youtube_id, )):
        return True
    return False


def song_exists_in_playlist(_db_ex, _name, _youtube_id):
    for row in _db_ex.execute('SELECT * FROM playlist_song WHERE name=? AND youtube_id=?;', (_name, _youtube_id)):
        return True
    return False


def has_permission(_db_ex, _name, _channel, _author):
    owner = ''
    for row in _db_ex.execute('SELECT owner FROM playlist WHERE name=?;', (_name, )):
        owner = row[0]
    if owner == _author.id:
        return True
    elif _channel.permissions_for(_author).administrator:
        return True
    return False


async def create_player_with_queue(_player, _song_queue, _queue_spot, _assignment):
    if _player is not None:
        _player.stop()

    _current_song = _song_queue[_queue_spot]
    _player = await _assignment.create_ytdl_player(_current_song.get_youtube_url())
    _current_song_duration = _player.duration
    _song_enddatetime = datetime.now() + timedelta(seconds=_player.duration)
    _player.start()
    _playing = True
    return _current_song, _player, _current_song_duration, _song_enddatetime, _playing


async def create_player_with_yt(_player, _assignment, _current_song, _song_queue):
    if _player is not None:
        _player.stop()

    _song_queue.append(_current_song)
    _player = await _assignment.create_ytdl_player(_current_song.get_youtube_url())
    _current_song_duration = _player.duration
    _song_enddatetime = datetime.now() + timedelta(seconds=_player.duration)
    _player.start()
    _playing = True
    return _player, _current_song_duration, _song_enddatetime, _playing, _song_queue


# -play, -play <song>
async def play(_dclient, _channel, _mention, _cmdchar, _msg, _assignment, _playing, _player, _current_song,
               _current_song_duration, _song_enddatetime, _queue_spot, _song_queue):
    _msg = _msg.split(' ')
    if len(_msg) == 1:  # -play
        if _player is None:
            if len(_song_queue) > 0:
                _current_song, _player, _current_song_duration, _song_enddatetime, _playing = \
                    await create_player_with_queue(_player, _song_queue, _queue_spot, _assignment)
                await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration,
                                                                   _player.title))
            else:
                await _dclient.send_message(_channel, ':warning: {} There are no queued songs to play!'
                                            .format(_mention))
        else:
            if _player.is_playing():
                await _dclient.send_message(_channel, ':warning: {} There is already a song playing right now!'
                                            .format(_mention))
            else:
                _player.resume()
                await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration, _player.title))
    elif len(_msg) == 2:  # -play <youtube_url>
        youtube_id = get_youtube_id(_msg[1])
        if youtube_id is None:
            await _dclient.send_message(_channel, ':warning: {} `{}` Is not a valid YouTube URL!'
                                        .format(_mention, _msg[1].lower()))
        else:
            _current_song = Song()
            if _current_song.set(youtube_id):
                _player, _current_song_duration, _song_enddatetime, _playing, _song_queue = \
                    await create_player_with_yt(_player, _assignment, _current_song, _song_queue)
                await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration,
                                                                   _player.title))
            else:
                await _dclient.send_message(_channel, ':warning: {} Invalid YouTube URL! Please put in the '
                                                      'correct one.'.format(_mention))
    else:
        await _dclient.send_message(_channel, usage_msg('play <youtube_url>', _mention, _cmdchar))
    return _playing, _player, _current_song, _current_song_duration, _song_enddatetime, _queue_spot, _song_queue


# -playing
async def playing(_dclient, _channel, _mention, _player, _song_enddatetime):
    if _player is not None:
        if _player.is_playing():
            await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration, _player.title))
        else:
            await _dclient.send_message(_channel, ':warning: {} There\'s no song playing right now!'.format(_mention))
    else:
        await _dclient.send_message(_channel, ':warning: {} There\'s no song playing right now!'.format(_mention))


# -pause
async def pause(_dclient, _channel, _mention, _assignment, _player, _song_enddatetime):
    if _player.is_playing():
        _player.pause()
        await _dclient.send_message(_channel, ':pause_button: Paused song!')
    else:
        await _dclient.send_message(_channel, ':warning: {} Music player is already paused!'.format(_mention))
    return _player


# -stop
async def stop(_dclient, _channel, _mention, _playing, _player):
    if _playing:
        _playing = False
        _player.stop()
        _player = None
        await _dclient.send_message(_channel, ':octagonal_sign: Stopped the song!')
    else:
        await _dclient.send_message(_channel, ':warning: {} There\'s no music playing/paused right now!'
                                    .format(_mention))
    return _playing, _player


# -shuffle
async def shuffle(_dclient, _channel, _mention, _song_queue, _queue_spot):
    if len(_song_queue) > 2:
        curr_song = _song_queue[_queue_spot]
        del _song_queue[_queue_spot]
        shuffle_(_song_queue)
        _song_queue.insert(0, curr_song)
        _queue_spot = 0
        await _dclient.send_message(_channel, '{} Active playlist has been shuffled!'.format(_mention))
    else:
        await _dclient.send_message(_channel, ':warning: {} Can\'t shuffle the queued list that isn\'t greater than 2!'
                                    .format(_mention))
    return _song_queue, _queue_spot


# -queue <song>
async def queue(_dclient, _channel, _mention, _cmdchar, _msg, _song_queue):
    _msg = _msg.split(' ')
    if len(_msg) == 2:
        youtube_id = get_youtube_id(_msg[1])
        if youtube_id is None:
            await _dclient.send_message(_channel, ':warning: {} `{}` Is not a valid YouTube URL!'
                                        .format(_mention, _msg[1]))
        else:
            song = Song()
            if song.set(youtube_id):
                _song_queue.append(song)
                await _dclient.send_message(_channel, '''**Next song in queue:**
```markdown
{}
```'''.format(song.name))
            else:
                await _dclient.send_message(_channel, ':warning: {} Invalid YouTube URL! Please put in the '
                                                      'correct one.'.format(_mention))
    else:
        await _dclient.send_message(_channel, usage_msg('queue <youtube_url>', _mention, _cmdchar))
    return _song_queue


# -clear
async def clear(_dclient, _channel, _mention, _player, _song_queue, _queue_spot):
    if _player is None:
        _song_queue = list()
        await _dclient.send_message(_channel, '{} Active playlist/queued list has been cleared!'.format(_mention))
    else:
        curr_song = _song_queue[_queue_spot]
        _song_queue = list()
        _song_queue.append(curr_song)
        _queue_spot = 0
        await _dclient.send_message(_channel, '{} Active playlist/queued list has been cleared except for the current '
                                              'song!'.format(_mention))
    return _song_queue, _queue_spot


# -skip
async def skip(_dclient, _channel, _mention, _assignment, _player, _song_queue, _queue_spot, _current_song_duration,
               _song_enddatetime):
    if len(_song_queue) > 1:
        if _player.is_playing():
            _queue_spot += 1
            if _queue_spot >= len(_song_queue):
                _queue_spot = 0
            song = _song_queue[_queue_spot]
            _player.stop()
            _player = await _assignment.create_ytdl_player(song.get_youtube_url())
            _current_song_duration = _player.duration
            _song_enddatetime = datetime.now() + timedelta(seconds=_player.duration)
            _player.start()
            await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration,
                                                               _player.title))
        else:
            await _dclient.send_message(_channel, ':warning: {} There\'s no music playing/paused right now!'
                                        .format(_mention))
    else:
        await _dclient.send_message(_channel, ':warning: {} Can\'t skip a song when there\'s only one song in the '
                                              'active playlist!'.format(_mention))
    return _player, _song_queue, _queue_spot, _current_song_duration, _song_enddatetime


# -playlist create <name>, -playlist remove <name>,
# -playlist edit <name> add <song>, -playlist edit <name> remove <id>,
# -playlist empty <name>, -playlist list <name>, -playlist
async def playlist(_dclient, _channel, _mention, _cmdchar, _msg, _author, _assignment, _playing, _player, _song_queue,
                   _queue_spot, _current_song_duration, _song_enddatetime, _db, _db_ex, _mus_playlistnamecharlimit):
    _msg = _msg.split(' ')
    if len(_msg) == 1:
        if len(_song_queue) > 0:
            response = '''**Active Playlist:**
```css
'''
            count = 0
            for song in _song_queue:
                if count == _queue_spot:
                    response += '''> {:5} {}
'''.format('[' + str(count + 1) + ']:', song.name)
                else:
                    response += '''  {:5} {}
'''.format('[' + str(count + 1) + ']:', song.name)
                count += 1
            response += '''```'''
            await _dclient.send_message(_channel, response)
        else:
            await _dclient.send_message(_channel, ':warning: {} There are no songs in the active playlist/song queue!'
                                        .format(_mention))
    else:
        if _msg[1].lower() == 'create':
            if len(_msg) == 3:
                name = _msg[2].lower()
                if len(name) > 50:
                    await _dclient.send_message(_channel, ':warning: {} Name `{}` must be `50` characters or less!'
                                                .format(_mention, name))
                else:
                    if len(name) > _mus_playlistnamecharlimit:
                        await _dclient.send_message(_channel, ':warning: {} Name `{}` must be `{}` characters or less!'
                                                    .format(_mention, name, _mus_playlistnamecharlimit))
                    else:
                        if name_exists(_db_ex, name):
                            await _dclient.send_message(_channel, ':warning: {} Playlist `{}` already exists!'
                                                        .format(_mention, name))
                        else:
                            if playlist_name_valid(name):
                                _db_ex.execute('INSERT INTO playlist VALUES (?, ?);', (name, _author.id))
                                _db.commit()
                                await _dclient.send_message(_channel, '{} Playlist `{}` has been made!'
                                                            .format(_mention, name))
                            else:
                                await _dclient.send_message(_channel, ':warning: {} Playlist names can only contain '
                                                                      'any `numbers`, `letters`, and `_` & `-`. '
                                                            .format(_mention))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist create <name>', _mention, _cmdchar))
        elif _msg[1].lower() == 'remove':
            if len(_msg) == 3:
                name = _msg[2].lower()
                if name_exists(_db_ex, name):
                    _db_ex.execute('DELETE FROM playlist_song WHERE name=?;', (name, ))
                    _db_ex.execute('DELETE FROM playlist WHERE name=? AND owner=?', (name, _author.id))
                    _db.commit()
                    await _dclient.send_message(_channel, '{} Playlist `{}` has been removed!'.format(_mention, name))
                else:
                    await _dclient.send_message(_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                .format(_mention, name))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist remove <name>', _mention, _cmdchar))
        elif _msg[1].lower() == 'edit':
            if len(_msg) == 5:
                name = _msg[2].lower()
                if name_exists(_db_ex, name):
                    if has_permission(_db_ex, name, _channel, _author):
                        if _msg[3].lower() == 'add':
                            youtube_id = get_youtube_id(_msg[4])
                            if youtube_id is None:
                                await _dclient.send_message(_channel, ':warning: {} `{}` Is not a valid YouTube URL!'
                                                            .format(_mention, _msg[1].lower()))
                            else:
                                curr_song = Song()
                                if curr_song.set(youtube_id):
                                    if not song_exists(_db_ex, youtube_id):
                                        _db_ex.execute('INSERT INTO song VALUES (?, ?);', (youtube_id, curr_song.name))
                                        _db.commit()
                                    if song_exists_in_playlist(_db_ex, name, youtube_id):
                                        await _dclient.send_message(_channel, ':warning: {} Song `{}` is already in '
                                                                              'the `{}` playlist!'
                                                                    .format(_mention, curr_song.name, name))
                                    else:
                                        _db_ex.execute('INSERT INTO playlist_song VALUES (?, ?);', (name, youtube_id))
                                        _db.commit()
                                        await _dclient.send_message(_channel,
                                                                    '{} Song `{}` has been added to `{}` playlist!'
                                                                    .format(_mention, curr_song.name, name))
                                else:
                                    await _dclient.send_message(_channel, ':warning: {} Invalid YouTube URL! Please '
                                                                          'put in the correct one.'.format(_mention))
                        elif _msg[3].lower() == 'remove':
                            youtube_id = _msg[4]
                            if song_exists_in_playlist(_db_ex, name, youtube_id):
                                _db_ex.execute('DELETE FROM playlist_song WHERE name=? AND youtube_id=?;',
                                               (name, youtube_id))
                                _db.commit()
                                valid, title = yt_title.get_yt_title(youtube_id)
                                await _dclient.send_message(_channel, '{} Song `{}` has been removed from `{}` '
                                                                      'playlist!'
                                                            .format(_mention, title, name))
                            else:
                                await _dclient.send_message(_channel, ':warning: {} This song doesn\'t exist in the '
                                                                      '`{}` playlist!'.format(_mention, name))
                        else:
                            await _dclient.send_message(_channel, usage_msg('playlist edit <name> <add|remove> '
                                                                            '<youtube_url|id#>', _mention, _cmdchar))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} You do not own this `{}` playlist!'
                                                    .format(_mention, name))
                else:
                    await _dclient.send_message(_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                .format(_mention, name))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist edit <name> <add|remove> <youtube_url|id#>',
                                                                _mention, _cmdchar))
        elif _msg[1].lower() == 'empty':
            if len(_msg) == 3:
                name = _msg[2].lower()
                if name_exists(_db_ex, name):
                    if has_permission(_db_ex, name, _channel, _author):
                        _db_ex.execute('DELETE FROM playlist_song WHERE name=?;', (name, ))
                        _db.commit()
                        await _dclient.send_message(_channel, '{} Playlist `{}` has been emptied!'.format(_mention,
                                                                                                          name))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} You do not own this `{}` playlist!'
                                                    .format(_mention, name))
                else:
                    await _dclient.send_message(_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                .format(_mention, name))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist empty <name>', _mention, _cmdchar))
        elif _msg[1].lower() == 'load':
            if len(_msg) == 3:
                name = _msg[2].lower()
                if name_exists(_db_ex, name):
                    song_list = {}
                    for row in _db_ex.execute('SELECT song.youtube_id, song.name FROM song JOIN playlist_song ON '
                                              'song.youtube_id=playlist_song.youtube_id AND playlist_song.name=?;',
                                              (name, )):
                        song_list[row[0]] = row[1]
                    _song_queue = []
                    for key, value in song_list.items():
                        _song = Song()
                        _song.full_set(key, value)
                        _song_queue.append(_song)
                    _queue_spot = 0
                    if _player is not None:
                        _player.stop()
                    curr_song = _song_queue[_queue_spot]
                    _player = await _assignment.create_ytdl_player(curr_song.get_youtube_url())
                    _current_song_duration = _player.duration
                    _song_enddatetime = datetime.now() + timedelta(seconds=_player.duration)
                    _player.start()
                    _playing = True
                    await _dclient.send_message(_channel, '{} Playlist `{}` has been loaded!'.format(_mention, name))
                    await _dclient.send_message(_channel, current_song(_song_enddatetime, _player.duration,
                                                                       _player.title))
                else:
                    await _dclient.send_message(_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                .format(_mention, name))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist load <name>', _mention, _cmdchar))
        elif _msg[1].lower() == 'list':
            if len(_msg) == 3:
                name = _msg[2].lower()
                if name_exists(_db_ex, name):
                    song_list = {}
                    not_empty = False
                    for row in _db_ex.execute('SELECT song.youtube_id, song.name FROM song JOIN playlist_song ON '
                                              'song.youtube_id=playlist_song.youtube_id AND playlist_song.name=?;',
                                              (name, )):
                        not_empty = True
                        song_list[row[0]] = row[1]
                    if not_empty:
                        response = '''**Playlist `{}`:**
```css
'''.format(name)
                        for key, value in song_list.items():
                            response += '''{:13} {}
'''.format('[' + key + ']:', value)
                        response += '''```'''
                        await _dclient.send_message(_channel, response)
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Playlist `{}` is empty!'
                                                    .format(_mention, name))
                else:
                    await _dclient.send_message(_channel, ':warning: {} Playlist `{}` doesn\'t exist!'
                                                .format(_mention, name))
            else:
                await _dclient.send_message(_channel, usage_msg('playlist list <name>', _mention, _cmdchar))
        elif _msg[1].lower() == 'all':
            playlist_names = list()
            for row in _db_ex.execute('SELECT name FROM playlist;'):
                playlist_names.append(row[0])
            if len(playlist_names) > 0:
                await _dclient.send_message(_channel, '''**List of Playlists:**
```{}```'''.format(', '.join(playlist_names)))
            else:
                await _dclient.send_message(_channel, ':warning: {} There\'s no playlist created!'.format(_mention))
        else:
            await _dclient.send_message(_channel, usage_msg('playlist <create|remove|edit|empty|list|all>', _mention,
                                                            _cmdchar))
    return _playing, _player, _song_queue, _queue_spot, _current_song_duration, _song_enddatetime


# -volume, -volume <#> (between 1 and 200)
async def volume(_dclient, _channel, _mention, _cmdchar, _msg, _player):
    _msg = _msg.split(' ')
    if len(_msg) == 2:
        if is_int_value(_msg[1]):
            value = int(_msg[1])
            if 0 <= value <= 200:
                _player.volume = value / 100.0
                await _dclient.send_message(_channel, '{} Volume has been set to `{}%`!'.format(_mention, value))
            else:
                await _dclient.send_message(_channel, ':warning: {} `{}` value must be between `0` and `200`.'
                                            .format(_mention, value))
        else:
            await _dclient.send_message(_channel, ':warning: {} Invalid input! It must be a numeric value.'
                                        .format(_mention))
    else:
        await _dclient.send_message(_channel, usage_msg('volume <#>', _mention, _cmdchar))
    return _player
